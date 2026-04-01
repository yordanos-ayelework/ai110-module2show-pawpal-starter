import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime
from pawpal_system import Task, Pet, Owner


def test_mark_complete_changes_status():
    pet = Pet(name="Buddy", species="Dog", age=3)
    task = Task(name="Morning Walk", pet=pet, duration=30, priority=1, due_date=datetime(2026, 4, 1, 8, 0))
    assert task.completed == False
    task.mark_complete()
    assert task.completed == True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Whiskers", species="Cat", age=2)
    assert len(pet.tasks) == 0
    task = Task(name="Feed", pet=pet, duration=10, priority=2, due_date=datetime(2026, 4, 1, 7, 0))
    pet.add_task(task)
    assert len(pet.tasks) == 1


def test_sort_by_time_returns_chronological_order():
    """Tasks should come back earliest due_date first."""
    owner = Owner(name="Alex", time=120)
    pet = Pet(name="Rex", species="Dog", age=4)
    owner.add_pet(pet)

    late_task  = Task(name="Evening Walk", pet=pet, duration=30, priority=2, due_date=datetime(2026, 4, 1, 18, 0))
    early_task = Task(name="Morning Walk", pet=pet, duration=30, priority=1, due_date=datetime(2026, 4, 1, 7, 0))
    mid_task   = Task(name="Lunch Feed",   pet=pet, duration=10, priority=1, due_date=datetime(2026, 4, 1, 12, 0))

    pet.add_task(late_task)
    pet.add_task(early_task)
    pet.add_task(mid_task)

    sorted_tasks = owner.scheduler.sort_by_time()
    due_dates = [t.due_date for t in sorted_tasks]
    assert due_dates == sorted(due_dates), "Tasks are not in chronological order"


def test_daily_recurrence_schedules_next_day():
    """Completing a daily task should add a new task due exactly one day later."""
    pet = Pet(name="Mochi", species="Cat", age=1)
    task = Task(
        name="Medication",
        pet=pet,
        duration=5,
        priority=1,
        due_date=datetime(2026, 4, 1, 9, 0),
        frequency="daily",
    )
    pet.add_task(task)

    task.mark_complete()

    assert len(pet.tasks) == 2, "A recurring daily task should create one follow-up task"
    next_task = pet.tasks[1]
    assert next_task.due_date == datetime(2026, 4, 2, 9, 0), "Next task should be due exactly one day later"
    assert next_task.completed == False, "The new task should start as incomplete"


def test_conflict_detection_flags_same_due_date():
    """Two tasks scheduled at the exact same time should trigger a conflict warning."""
    owner = Owner(name="Sam", time=120)
    pet = Pet(name="Noodle", species="Dog", age=2)
    owner.add_pet(pet)

    t1 = Task(name="Bath",  pet=pet, duration=20, priority=1, due_date=datetime(2026, 4, 1, 10, 0))
    t2 = Task(name="Groom", pet=pet, duration=15, priority=2, due_date=datetime(2026, 4, 1, 10, 0))
    pet.add_task(t1)
    pet.add_task(t2)

    warnings = owner.scheduler.detect_conflicts()
    assert len(warnings) == 1, "Expected exactly one conflict warning"
    assert "Bath" in warnings[0] or "Groom" in warnings[0], "Warning should name one of the conflicting tasks"


def test_no_conflict_when_times_differ():
    """Tasks at different times should produce no conflict warnings."""
    owner = Owner(name="Sam", time=120)
    pet = Pet(name="Noodle", species="Dog", age=2)
    owner.add_pet(pet)

    t1 = Task(name="Bath",  pet=pet, duration=20, priority=1, due_date=datetime(2026, 4, 1, 9, 0))
    t2 = Task(name="Groom", pet=pet, duration=15, priority=2, due_date=datetime(2026, 4, 1, 10, 0))
    pet.add_task(t1)
    pet.add_task(t2)

    warnings = owner.scheduler.detect_conflicts()
    assert warnings == [], "No conflict expected when tasks are at different times"
