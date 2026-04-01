import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pawpal_system import Task, Pet


def test_mark_complete_changes_status():
    pet = Pet(name="Buddy", species="Dog", age=3)
    task = Task(name="Morning Walk", pet=pet, duration=30, priority=1, due_time="08:00")
    assert task.completed == False
    task.mark_complete()
    assert task.completed == True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Whiskers", species="Cat", age=2)
    assert len(pet.tasks) == 0
    task = Task(name="Feed", pet=pet, duration=10, priority=2, due_time="07:00")
    pet.add_task(task)
    assert len(pet.tasks) == 1
