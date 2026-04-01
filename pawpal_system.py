from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    name: str
    duration: int  # in minutes
    priority: int
    due_time: str
    completed: bool = False

    def mark_complete(self):
        pass


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def edit_task(self, task: Task):
        pass

    def list_tasks(self):
        pass


class Scheduler:
    def __init__(self, owner: "Owner", tasks: List[Task], time: int):
        self.owner = owner
        self.tasks = tasks
        self.time = time  # available time in minutes

    def get_tasks(self):
        pass

    def generate_plan(self):
        pass

    def sort(self):
        pass


class Owner:
    def __init__(self, name: str):
        self.name = name
        self.schedule: List[Task] = []
        self.pets: List[Pet] = []

    def edit_pet(self, pet: Pet):
        pass

    def edit_task(self, task: Task):
        pass

    def generate_schedule(self):
        pass
