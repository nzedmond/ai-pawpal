from dataclasses import dataclass, field
from typing import List


@dataclass
class Owner:
    name: str
    available_minutes: int
    preferences: str = ""

    def get_constraints(self) -> dict:
        """Return a dict of scheduling constraints for this owner."""
        pass


@dataclass
class Pet:
    name: str
    species: str
    age: int
    owner: Owner

    def get_required_tasks(self) -> List["Task"]:
        """Return a list of tasks that are always required for this pet's species."""
        pass


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str          # "low", "medium", or "high"
    category: str          # e.g. "walk", "feeding", "meds", "grooming", "enrichment"
    completed: bool = False

    def is_high_priority(self) -> bool:
        """Return True if this task is high priority."""
        pass


@dataclass
class Schedule:
    date: str
    owner: Owner
    pet: Pet
    scheduled_tasks: List[Task] = field(default_factory=list)
    total_duration: int = 0

    def add_task(self, task: Task) -> None:
        """Add a task to the schedule and update total_duration."""
        pass

    def remove_task(self, task: Task) -> None:
        """Remove a task from the schedule and update total_duration."""
        pass

    def get_total_duration(self) -> int:
        """Return the sum of duration_minutes for all scheduled tasks."""
        pass

    def display(self) -> str:
        """Return a formatted string representation of the schedule."""
        pass


class Scheduler:
    def __init__(self, owner: Owner, pet: Pet, available_tasks: List[Task]):
        self.owner = owner
        self.pet = pet
        self.available_tasks = available_tasks

    def generate_plan(self) -> Schedule:
        """Build and return a Schedule based on owner constraints and task priorities."""
        pass

    def explain_plan(self, schedule: Schedule) -> str:
        """Return a human-readable explanation of why each task was chosen and ordered."""
        pass
