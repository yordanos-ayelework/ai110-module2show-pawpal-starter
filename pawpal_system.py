from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional


@dataclass
class Task:
    name: str
    pet: "Pet"
    duration: int  # in minutes
    priority: int  # 1 = highest priority
    due_date: datetime  # e.g. datetime(2026, 4, 1, 8, 0)
    completed: bool = False
    frequency: Optional[str] = None  # "daily", "weekly", or None

    def mark_complete(self):
        """Mark this task as completed. If frequency is set, auto-schedules the next occurrence."""
        self.completed = True
        print(f"Task '{self.name}' marked as complete.")

        if self.frequency and self.due_date:
            if self.frequency == "daily":
                next_date = self.due_date + timedelta(days=1)
            elif self.frequency == "weekly":
                next_date = self.due_date + timedelta(weeks=1)
            else:
                return

            next_task = Task(
                name=self.name,
                pet=self.pet,
                duration=self.duration,
                priority=self.priority,
                due_date=next_date,
                frequency=self.frequency,
            )
            self.pet.tasks.append(next_task)
            print(f"Next '{self.name}' scheduled for {next_date.strftime('%Y-%m-%d %H:%M')} ({self.frequency}).")


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a task to this pet's task list."""
        self.tasks.append(task)
        print(f"Task '{task.name}' added to {self.name}.")

    def edit_task(self, task_name: str, **updates):
        """Update attributes of a task by name."""
        for task in self.tasks:
            if task.name == task_name:
                for attr, value in updates.items():
                    if hasattr(task, attr):
                        setattr(task, attr, value)
                print(f"Task '{task_name}' updated.")
                return
        print(f"Task '{task_name}' not found.")

    def remove_task(self, task_name: str):
        """Remove a task from this pet's task list by name."""
        for task in self.tasks:
            if task.name == task_name:
                self.tasks.remove(task)
                print(f"Task '{task_name}' removed from {self.name}.")
                return
        print(f"Task '{task_name}' not found.")

    def list_tasks(self):
        """Print all tasks for this pet with their status and details."""
        if not self.tasks:
            print(f"{self.name} has no tasks.")
            return
        print(f"Tasks for {self.name}:")
        for task in self.tasks:
            status = "Done" if task.completed else "Pending"
            print(f"  [{status}] {task.name} | Due: {task.due_date.strftime('%Y-%m-%d %H:%M')} | {task.duration} min | Priority: {task.priority}")


class Scheduler:
    def __init__(self, owner: "Owner", time: int):
        self.owner = owner
        self.time = time  # available time budget in minutes

    def get_tasks(self) -> List[Task]:
        """Return all tasks across all of the owner's pets."""
        all_tasks = []
        for pet in self.owner.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

    def sort_by_time(self) -> List[Task]:
        """Return all tasks sorted by due time."""
        tasks = self.get_tasks()
        return sorted(tasks, key=lambda t: t.due_date)

    def sort_by_priority(self) -> List[Task]:
        """Return all tasks sorted by priority (1 = highest)."""
        tasks = self.get_tasks()
        return sorted(tasks, key=lambda t: t.priority)

    def filter_by_pet(self, pet_name: str) -> List[Task]:
        """Return all tasks belonging to the named pet."""
        return [t for t in self.get_tasks() if t.pet.name == pet_name]

    def detect_conflicts(self) -> List[str]:
        """Return warning messages for any tasks that share the same due_date."""
        warnings = []
        tasks = [t for t in self.get_tasks() if not t.completed]
        seen: dict = {}  # due_date -> first task seen at that time
        for task in tasks:
            key = task.due_date
            if key in seen:
                other = seen[key]
                warnings.append(
                    f"WARNING: '{task.name}' ({task.pet.name}) conflicts with "
                    f"'{other.name}' ({other.pet.name}) at {key.strftime('%Y-%m-%d %H:%M')}"
                )
            else:
                seen[key] = task
        return warnings

    def filter_by_priority(self, max_priority: int) -> List[Task]:
        """Return incomplete tasks at or above the given priority level."""
        tasks = self.get_tasks()
        return [t for t in tasks if not t.completed and t.priority <= max_priority]

    def generate_plan(self) -> List[Task]:
        """Build and print a schedule of tasks that fit within the available time budget."""
        sorted_tasks = self.sort_by_time()
        plan = []
        time_used = 0
        for task in sorted_tasks:
            if task.completed:
                continue
            if time_used + task.duration <= self.time:
                plan.append(task)
                time_used += task.duration
        print(f"\nSchedule for {self.owner.name} ({self.time} min available):")
        if not plan:
            print("  No tasks fit in the available time.")
        for task in plan:
            print(f"  {task.due_date.strftime('%Y-%m-%d %H:%M')} | {task.name} ({task.pet.name}) | {task.duration} min")
        return plan


class Owner:
    def __init__(self, name: str, time: int = 120):
        self.name = name
        self.pets: List[Pet] = []
        self.scheduler: Scheduler = Scheduler(owner=self, time=time)

    def add_pet(self, pet: Pet):
        """Add a pet to this owner's pet list."""
        self.pets.append(pet)
        print(f"{pet.name} added to {self.name}'s pets.")

    def edit_pet(self, pet_name: str, **updates):
        """Update attributes of a pet by name."""
        for pet in self.pets:
            if pet.name == pet_name:
                for attr, value in updates.items():
                    if hasattr(pet, attr):
                        setattr(pet, attr, value)
                print(f"Pet '{pet_name}' updated.")
                return
        print(f"Pet '{pet_name}' not found.")

    def remove_pet(self, pet_name: str):
        """Remove a pet from this owner's pet list by name."""
        for pet in self.pets:
            if pet.name == pet_name:
                self.pets.remove(pet)
                print(f"{pet_name} removed from {self.name}'s pets.")
                return
        print(f"Pet '{pet_name}' not found.")

    def generate_schedule(self) -> List[Task]:
        """Delegate to the scheduler to generate the owner's daily task plan."""
        return self.scheduler.generate_plan()
