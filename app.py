import datetime
import streamlit as st
from pawpal_system import Task, Pet, Owner

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

PRIORITY_MAP = {"high": 1, "medium": 2, "low": 3}
PRIORITY_LABEL = {1: "high", 2: "medium", 3: "low"}

# --- Session state init ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")

owner = st.session_state.owner

# --- Owner ---
st.subheader("Owner")
col_name, col_time = st.columns(2)
with col_name:
    owner_name = st.text_input("Owner name", value=owner.name)
    if owner_name != owner.name:
        owner.name = owner_name
with col_time:
    time_budget = st.number_input(
        "Available time (minutes)", min_value=10, max_value=480, value=owner.scheduler.time
    )
    if int(time_budget) != owner.scheduler.time:
        owner.scheduler.time = int(time_budget)

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
    st.table([{"Name": p.name, "Species": p.species, "Age": p.age} for p in owner.pets])
else:
    st.info("No pets yet. Add one above.")

# --- Add a Task ---
st.divider()
st.subheader("Add a Task")

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
        due_datetime = datetime.datetime.combine(datetime.date.today(), due_time)
        task = Task(
            name=task_title,
            pet=target_pet,
            duration=int(duration),
            priority=PRIORITY_MAP[priority_label],
            due_date=due_datetime,
        )
        target_pet.add_task(task)
        st.success(f"Task '{task_title}' added to {task_pet_name}.")

# --- View Tasks ---
st.divider()
st.subheader("View Tasks")

all_tasks = owner.scheduler.get_tasks()

if not all_tasks:
    st.info("No tasks yet. Add one above.")
else:
    col_sort, col_filter = st.columns(2)
    with col_sort:
        sort_by = st.selectbox("Sort by", ["Due time", "Priority"])
    with col_filter:
        pet_options = ["All"] + [p.name for p in owner.pets]
        pet_filter = st.selectbox("Filter by pet", pet_options)

    if sort_by == "Due time":
        tasks_to_show = owner.scheduler.sort_by_time()
    else:
        tasks_to_show = owner.scheduler.sort_by_priority()

    if pet_filter != "All":
        tasks_to_show = owner.scheduler.filter_by_pet(pet_filter)
        # re-sort the filtered result
        if sort_by == "Priority":
            tasks_to_show = sorted(tasks_to_show, key=lambda t: t.priority)
        else:
            tasks_to_show = sorted(tasks_to_show, key=lambda t: t.due_date)

    # Conflict warnings
    conflicts = owner.scheduler.detect_conflicts()
    for warning in conflicts:
        st.warning(warning)

    st.table(
        [
            {
                "Pet": t.pet.name,
                "Task": t.name,
                "Due": t.due_date.strftime("%H:%M"),
                "Duration (min)": t.duration,
                "Priority": PRIORITY_LABEL.get(t.priority, str(t.priority)),
                "Done": "Yes" if t.completed else "No",
            }
            for t in tasks_to_show
        ]
    )

# --- Generate Schedule ---
st.divider()
st.subheader("Build Schedule")

if st.button("Generate schedule"):
    plan = owner.generate_schedule()
    if plan:
        total_min = sum(t.duration for t in plan)
        st.success(
            f"Schedule generated! {len(plan)} task(s) — {total_min} of {owner.scheduler.time} minutes used."
        )
        st.table(
            [
                {
                    "Due time": t.due_date.strftime("%H:%M"),
                    "Task": t.name,
                    "Pet": t.pet.name,
                    "Duration (min)": t.duration,
                    "Priority": PRIORITY_LABEL.get(t.priority, str(t.priority)),
                }
                for t in plan
            ]
        )
    else:
        st.warning("No tasks fit within the available time budget.")
