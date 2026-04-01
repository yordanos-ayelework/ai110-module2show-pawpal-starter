from pawpal_system import Owner, Pet, Task

owner = Owner(name="Yordanos", time=120)

snake = Pet(name="Xavier", species="Snake", age=2)
cat = Pet(name="Venus", species="Cat", age=4)
dog = Pet(name="Leo", species="Dog", age=5)

owner.add_pet(snake)
owner.add_pet(cat)
owner.add_pet(dog)

task1 = Task(name="Feeding", pet=snake, duration=15, priority=2, due_time="09:00")
snake.add_task(task1)

task2 = Task(name="Vet Appointment", pet=cat, duration=60, priority=1, due_time="10:00")
task3 = Task(name="Grooming", pet=cat, duration=20, priority=3, due_time="14:00")
cat.add_task(task2)
cat.add_task(task3)

task4 = Task(name="Morning Walk", pet=dog, duration=30, priority=1, due_time="07:00")
dog.add_task(task4)

print("\n====== Today's Schedule ======")
sorted_tasks = owner.scheduler.sort_by_time()
owner.generate_schedule()