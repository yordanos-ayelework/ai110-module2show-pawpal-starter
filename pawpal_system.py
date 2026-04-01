from dataclasses import dataclass
from typing import List


@dataclass
class Pet:
    name: str
    species: str
    age: int


@dataclass
class Task:
    name: str
    duration: int  # in minutes
    priority: int


class Scheduler:
    def __init__(self, tasks: List[Task], time: int):
        self.tasks = tasks
        self.time = time  # available time in minutes

    def generate_plan(self):
        pass

    def sort(self):
        pass


class Owner:
    def __init__(self, name: str):
        self.name = name
        self.schedule: List[Task] = []

    def edit_pet(self, pet: Pet):
        pass

    def edit_task(self, task: Task):
        pass

    def generate_schedule(self):
        pass
