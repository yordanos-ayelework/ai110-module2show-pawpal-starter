import datetime
import streamlit as st
from pawpal_system import Task, Pet, Owner

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

# --- Session state init ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")

owner = st.session_state.owner

# --- Owner ---
st.subheader("Owner")
owner_name = st.text_input("Owner name", value=owner.name)
if owner_name != owner.name:
    owner.name = owner_name

# --- Add a Pet ---
st.divider()
st.subheader("Add a Pet")

col1, col2, col3 = st.columns(3)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.text_input("Species", value="dog")
with col3:
    age = st.number_input("Age (years)", min_value=0, max_value=30, value=2)

if st.button("Add Pet"):
    pet = Pet(name=pet_name, species=species, age=int(age))
    owner.add_pet(pet)
    st.success(f"{pet_name} added to {owner.name}'s pets!")

if owner.pets:
    st.write("Current pets:")
    st.table([{"name": p.name, "species": p.species, "age": p.age} for p in owner.pets])
else:
    st.info("No pets yet. Add one above.")

# --- Add a Task ---
st.divider()
st.subheader("Add a Task")

PRIORITY_MAP = {"high": 1, "medium": 2, "low": 3}

if not owner.pets:
    st.warning("Add a pet first before scheduling tasks.")
else:
    col1, col2 = st.columns(2)
    with col1:
        task_pet_name = st.selectbox("For which pet?", [p.name for p in owner.pets])
    with col2:
        task_title = st.text_input("Task title", value="Morning walk")

    col3, col4, col5 = st.columns(3)
    with col3:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col4:
        priority_label = st.selectbox("Priority", ["high", "medium", "low"])
    with col5:
        due_time = st.time_input("Due time", value=datetime.time(8, 0))

    if st.button("Add Task"):
        target_pet = next(p for p in owner.pets if p.name == task_pet_name)
        task = Task(
            name=task_title,
            pet=target_pet,
            duration=int(duration),
            priority=PRIORITY_MAP[priority_label],
            due_time=due_time.strftime("%H:%M"),
        )
        target_pet.add_task(task)
        st.success(f"Task '{task_title}' added to {task_pet_name}.")

    all_tasks = owner.scheduler.get_tasks()
    if all_tasks:
        st.write("Current tasks:")
        st.table(
            [
                {
                    "pet": t.pet.name,
                    "task": t.name,
                    "due": t.due_time,
                    "duration (min)": t.duration,
                    "priority": t.priority,
                    "done": t.completed,
                }
                for t in all_tasks
            ]
        )
    else:
        st.info("No tasks yet. Add one above.")

# --- Generate Schedule ---
st.divider()
st.subheader("Build Schedule")

if st.button("Generate schedule"):
    plan = owner.generate_schedule()
    if plan:
        st.success("Schedule generated!")
        st.table(
            [
                {
                    "due time": t.due_time,
                    "task": t.name,
                    "pet": t.pet.name,
                    "duration (min)": t.duration,
                }
                for t in plan
            ]
        )
    else:
        st.warning("No tasks fit within the available time budget.")
