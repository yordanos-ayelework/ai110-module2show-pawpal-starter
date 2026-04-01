from datetime import datetime
from pawpal_system import Owner, Pet, Task

owner = Owner(name="Yordanos", time=120)

snake = Pet(name="Xavier", species="Snake", age=2)
cat = Pet(name="Venus", species="Cat", age=4)
dog = Pet(name="Leo", species="Dog", age=5)

owner.add_pet(snake)
owner.add_pet(cat)
owner.add_pet(dog)

task1 = Task(name="Feeding", pet=snake, duration=15, priority=2, due_date=datetime(2026, 4, 1, 9, 0))
snake.add_task(task1)

task2 = Task(name="Vet Appointment", pet=cat, duration=60, priority=1, due_date=datetime(2026, 4, 1, 10, 0))
task3 = Task(name="Grooming", pet=cat, duration=20, priority=3, due_date=datetime(2026, 4, 1, 14, 0))
cat.add_task(task2)
cat.add_task(task3)

task4 = Task(name="Morning Walk", pet=dog, duration=30, priority=1, due_date=datetime(2026, 4, 1, 7, 0))
task5 = Task(name="Evening Walk", pet=dog, duration=30, priority=2, due_date=datetime(2026, 4, 1, 18, 0))
task6 = Task(name="Nail Trim", pet=dog, duration=10, priority=3, due_date=datetime(2026, 4, 1, 11, 0))
dog.add_task(task6)   # added out of order (11:00 before 07:00)
dog.add_task(task4)
dog.add_task(task5)

print("\n====== Sorted by Time ======")
for t in owner.scheduler.sort_by_time():
    print(f"  {t.due_date.strftime('%Y-%m-%d %H:%M')} | {t.name} ({t.pet.name})")

print("\n====== Sorted by Priority ======")
for t in owner.scheduler.sort_by_priority():
    print(f"  Priority {t.priority} | {t.name} ({t.pet.name})")

task2.mark_complete()

print("\n====== Filter: Leo's Tasks ======")
for t in owner.scheduler.filter_by_pet("Leo"):
    status = "Done" if t.completed else "Pending"
    print(f"  [{status}] {t.name} | Due: {t.due_date.strftime('%Y-%m-%d %H:%M')}")

task7 = Task(name="Brushing", pet=cat, duration=10, priority=2, due_date=datetime(2026, 4, 1, 9, 0))
cat.add_task(task7)  # conflict

print("\n====== Conflict Detection ======")
conflicts = owner.scheduler.detect_conflicts()
if conflicts:
    for warning in conflicts:
        print(f"  {warning}")
else:
    print("  No conflicts found.")

print("\n====== Today's Schedule ======")
owner.generate_schedule()