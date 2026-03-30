from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


@dataclass
class Owner:
    name: str
    available_minutes: int
    preferred_start_time: str = "08:00"   # structured instead of free-text string
    preferred_categories: List[str] = field(default_factory=list)  # e.g. ["walk", "feeding"]

    def get_constraints(self) -> dict:
        """Return a dict of scheduling constraints for this owner."""
        pass


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: Priority          # Enum instead of raw string
    category: str               # e.g. "walk", "feeding", "meds", "grooming", "enrichment"
    completed: bool = False
    start_time: Optional[str] = None   # set by Scheduler once the plan is built, e.g. "09:00"

    def is_high_priority(self) -> bool:
        """Return True if this task is high priority."""
        pass


@dataclass
class Pet:
    name: str
    species: str
    age: int
    owner: Owner
    tasks: List[Task] = field(default_factory=list)  # all tasks associated with this pet

    def get_required_tasks(self) -> List[Task]:
        """Return species-specific tasks that must always appear in the schedule."""
        pass


@dataclass
class Schedule:
    date: str
    pet: Pet                                            # owner accessible via pet.owner
    scheduled_tasks: List[Task] = field(default_factory=list)

    @property
    def owner(self) -> Owner:
        """Convenience accessor — single source of truth via pet."""
        return self.pet.owner

    @property
    def total_duration(self) -> int:
        """Computed from scheduled tasks so it never drifts out of sync."""
        return sum(t.duration_minutes for t in self.scheduled_tasks)

    def add_task(self, task: Task) -> None:
        """Add a task to the schedule."""
        pass

    def remove_task(self, task: Task) -> None:
        """Remove a task from the schedule."""
        pass

    def display(self) -> str:
        """Return a formatted string representation of the schedule."""
        pass


class Scheduler:
    def __init__(self, pet: Pet, available_tasks: List[Task]):
        self.pet = pet
        self.owner = pet.owner                  # single source of truth
        self.available_tasks = available_tasks

    def _merge_tasks(self) -> List[Task]:
        """Merge user-added tasks with pet's required tasks, avoiding duplicates."""
        pass

    def generate_plan(self) -> Schedule:
        """
        Build and return a Schedule based on owner constraints and task priorities.
        Merges required tasks from get_required_tasks() with available_tasks,
        sorts by Priority, and fits tasks within owner.available_minutes.
        """
        pass

    def explain_plan(self, schedule: Schedule) -> str:
        """Return a human-readable explanation of why each task was chosen and ordered."""
        pass
