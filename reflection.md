# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

--- Actions a user should be able to perform:
1. Add a pet
2. Add a pet care task
3. Generate a daily schedule

--- Classes:
- Owner
Attributes: name, pets, scheduler
Methods: add pet, edit pet, remove pet, generate schedule

- Pet
Attributes: name, species, age, tasks
Methods: add task, edit task, remove task, list tasks

- Task
Attributes: name, pet, duration, priority, due date, frequency, completed
Methods: mark complete

- Scheduler 
Attributes: owner, time
Methods: get tasks, generate plan, sort by time, sort by priority, filter by priority, filter by pet, detect conflicts 

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

--- Yes. I only had edit pet/task, which don't account for populating the objects. Based on AI feedback, I added add and remove methods for the objects. I also added a scheduler attribute to owner, so that the generate_schedule method could use it, and a pet attribute to task for better identification.

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

--- It considers time that the pet owner has available, due date, and priority. Available time is the most important constraint because it is what determines what tasks the pet owner can do in a day. I also wanted tasks to be considered in chronological order.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

--- The conflict detection algorithm only checks for tasks that have the same timestamp. It doesn't check if tasks overlap (with different start times). I think the tradeoff is reasonable because tasks can still be treated as reminders instead of a strict and complete schedule. 

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

--- I used Claude for brainstorming, generating code, and refactoring methods. I think the most helpful types of prompts were the ones that focused on a specific function or section of the application.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

--- Claude tried using str data type for the due date attribute. Though I'm sure that could've worked by changing the data type later in the methods, it was simpler to just use datetime.

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

--- The tests cover:
- Task completion changes the completed status
- Adding a task to a pet adds to its task list
- Sorting returns tasks in chronological order
- Completing a daily task schedules a follow-up a day later
- Two tasks at the same time trigger a conflict warning
- Two tasks at different times do not trigger a conflict warning

-- These tests are important because they check for core functions of the app, especially conflict detection and sorting.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---  4/5

--- I'd try scheduling tasks with no available time on the pet owner's end and having multiple pets with the same name belonging to different owners.

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

--- The different methods for Scheduler

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

--- The classes to make sure that edits made are reflected properly

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

--- It's easy to have Claude edit code in one file and forget to make the appropriate changes in another.