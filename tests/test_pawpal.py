import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Pet, Priority, Task


def make_task(title="Morning Walk", duration=30, priority=Priority.HIGH, category="walk"):
    """Helper to create a Task without repeating boilerplate in every test."""
    return Task(title=title, duration_minutes=duration, priority=priority, category=category)


def make_pet(name="Mochi", species="dog", age=3):
    """Helper to create a Pet without repeating boilerplate in every test."""
    return Pet(name=name, species=species, age=age)


# ------------------------------------------------------------------ #
# Test 1 — Task Completion                                            #
# ------------------------------------------------------------------ #
def test_mark_complete_changes_status():
    task = make_task()

    assert task.completed is False, "Task should start as incomplete"

    task.mark_complete()

    assert task.completed is True, "Task should be marked complete after calling mark_complete()"


# ------------------------------------------------------------------ #
# Test 2 — Task Addition                                              #
# ------------------------------------------------------------------ #
def test_add_task_increases_pet_task_count():
    pet = make_pet()

    assert len(pet.tasks) == 0, "Pet should start with no tasks"

    pet.add_task(make_task("Morning Walk", 30, Priority.HIGH, "walk"))
    pet.add_task(make_task("Feeding", 10, Priority.HIGH, "feeding"))
    pet.add_task(make_task("Brush Coat", 15, Priority.LOW, "grooming"))

    assert len(pet.tasks) == 3, "Pet should have 3 tasks after adding three"
