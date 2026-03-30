from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


@dataclass
class Task:
    """Represents a single pet care activity."""
    title: str
    duration_minutes: int
    priority: Priority
    category: str               # "walk", "feeding", "meds", "grooming", "enrichment"
    frequency: str = "daily"    # "daily", "weekly", "once"
    completed: bool = False
    start_time: Optional[str] = None  # assigned by Scheduler, e.g. "09:00"

    def is_high_priority(self) -> bool:
        """Return True if this task's priority is HIGH."""
        return self.priority == Priority.HIGH

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def reset(self) -> None:
        """Clear completion state and assigned start time for a new day."""
        self.completed = False
        self.start_time = None


@dataclass
class Pet:
    """Stores pet details and owns its list of care tasks."""
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet's task list."""
        self.tasks.remove(task)

    def get_required_tasks(self) -> List[Task]:
        """Return species-specific tasks that must always appear in the schedule."""
        defaults = {
            "dog": [
                Task("Morning Walk", 30, Priority.HIGH, "walk"),
                Task("Feeding", 10, Priority.HIGH, "feeding"),
            ],
            "cat": [
                Task("Feeding", 10, Priority.HIGH, "feeding"),
                Task("Litter Box", 5, Priority.HIGH, "grooming"),
            ],
        }
        return defaults.get(self.species.lower(), [])


@dataclass
class Owner:
    """Manages multiple pets and provides access to all their tasks."""
    name: str
    available_minutes: int
    pets: List[Pet] = field(default_factory=list)
    preferred_start_time: str = "08:00"
    preferred_categories: List[str] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's pet list."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from this owner's pet list."""
        self.pets.remove(pet)

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks across every pet."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

    def get_constraints(self) -> dict:
        """Return a dict of scheduling constraints for this owner."""
        return {
            "available_minutes": self.available_minutes,
            "preferred_start_time": self.preferred_start_time,
            "preferred_categories": self.preferred_categories,
        }


@dataclass
class Schedule:
    """The output plan produced by the Scheduler."""
    date: str
    owner: Owner
    scheduled_tasks: List[Task] = field(default_factory=list)

    @property
    def total_duration(self) -> int:
        """Always computed — never drifts out of sync."""
        return sum(t.duration_minutes for t in self.scheduled_tasks)

    def add_task(self, task: Task) -> None:
        """Append a task to the scheduled task list."""
        self.scheduled_tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from the scheduled task list."""
        self.scheduled_tasks.remove(task)

    def display(self) -> str:
        """Return a formatted string of the full schedule with times and status."""
        lines = [f"Schedule for {self.owner.name} — {self.date}", "-" * 44]
        for i, task in enumerate(self.scheduled_tasks, 1):
            status = "✓" if task.completed else "○"
            time = task.start_time or "TBD"
            lines.append(
                f"{i}. [{status}] {time}  {task.title}"
                f" ({task.duration_minutes} min) [{task.priority.name}]"
            )
        lines.append(f"\nTotal: {self.total_duration} / {self.owner.available_minutes} min")
        return "\n".join(lines)


class Scheduler:
    """
    The brain of PawPal+.
    Retrieves tasks across all pets, merges required tasks, sorts by
    priority, fits within the owner's time budget, and assigns start times.
    """

    def __init__(self, owner: Owner):
        """Initialise the Scheduler with the owner whose pets will be planned for."""
        self.owner = owner

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _merge_tasks(self, pet: Pet) -> List[Task]:
        """
        Combine user-added tasks with species-required tasks.
        Required tasks are only added when a matching title isn't already present.
        """
        existing_titles = {t.title.lower() for t in pet.tasks}
        merged = list(pet.tasks)
        for required_task in pet.get_required_tasks():
            if required_task.title.lower() not in existing_titles:
                merged.append(required_task)
        return merged

    def _collect_all_tasks(self) -> List[Task]:
        """Collect merged tasks from every pet the owner has."""
        all_tasks = []
        for pet in self.owner.pets:
            all_tasks.extend(self._merge_tasks(pet))
        return all_tasks

    def _assign_start_times(self, tasks: List[Task]) -> None:
        """
        Assign sequential start times beginning at owner.preferred_start_time.
        Mutates each task's start_time in place.
        """
        hour, minute = map(int, self.owner.preferred_start_time.split(":"))
        current_minutes = hour * 60 + minute
        for task in tasks:
            h, m = divmod(current_minutes, 60)
            task.start_time = f"{h:02d}:{m:02d}"
            current_minutes += task.duration_minutes

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate_plan(self, date: str) -> Schedule:
        """
        Build and return a Schedule for the given date.
        Steps:
          1. Merge required + user tasks across all pets.
          2. Sort by priority descending; use duration as a tiebreaker (shorter first).
          3. Greedily select tasks that fit within owner.available_minutes.
          4. Assign sequential start times.
        """
        all_tasks = self._collect_all_tasks()

        sorted_tasks = sorted(
            all_tasks,
            key=lambda t: (-t.priority.value, t.duration_minutes),
        )

        budget = self.owner.available_minutes
        selected: List[Task] = []
        time_used = 0
        for task in sorted_tasks:
            if time_used + task.duration_minutes <= budget:
                selected.append(task)
                time_used += task.duration_minutes

        self._assign_start_times(selected)

        schedule = Schedule(date=date, owner=self.owner)
        for task in selected:
            schedule.add_task(task)
        return schedule

    def explain_plan(self, schedule: Schedule) -> str:
        """
        Return a human-readable explanation of why each task was chosen
        and any tasks that were skipped due to the time budget.
        """
        lines = [
            f"Plan explanation for {schedule.owner.name} — {schedule.date}",
            "=" * 50,
        ]

        scheduled_titles = {t.title for t in schedule.scheduled_tasks}
        all_tasks = self._collect_all_tasks()

        for task in schedule.scheduled_tasks:
            reasons = []
            if task.is_high_priority():
                reasons.append("high priority")
            if task.category in schedule.owner.preferred_categories:
                reasons.append("matches owner preference")
            if not reasons:
                reasons.append("fits within time budget")
            lines.append(
                f"• {task.title} at {task.start_time}: {', '.join(reasons)}."
            )

        skipped = [t for t in all_tasks if t.title not in scheduled_titles]
        if skipped:
            lines.append(f"\nSkipped ({len(skipped)}) — exceeded {schedule.owner.available_minutes}-min budget:")
            for task in skipped:
                lines.append(f"  - {task.title} ({task.duration_minutes} min, {task.priority.name})")

        return "\n".join(lines)
