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

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

--- The conflict detection algorithm only checks for tasks that have the same timestamp. It doesn't check if tasks overlap (with different start times). I think the tradeoff is reasonable because tasks can still be treated as reminders instead of a strict and complete schedule. 

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
