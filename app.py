from datetime import date

import streamlit as st

from pawpal_system import Owner, Pet, Priority, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# ------------------------------------------------------------------ #
# Section 1 — Owner                                                   #
# ------------------------------------------------------------------ #
st.subheader("Owner Info")

col1, col2 = st.columns(2)
with col1:
    owner_name = st.text_input("Owner name", value="Jordan")
with col2:
    available_minutes = st.number_input(
        "Time available today (minutes)", min_value=10, max_value=480, value=90
    )

preferred_start = st.text_input("Preferred start time (HH:MM)", value="08:00")

if st.button("Save owner"):
    st.session_state.owner = Owner(
        name=owner_name,
        available_minutes=int(available_minutes),
        preferred_start_time=preferred_start,
    )
    st.success(f"Owner '{owner_name}' saved.")

if "owner" not in st.session_state:
    st.info("Save owner info above to continue.")
    st.stop()

# ------------------------------------------------------------------ #
# Section 2 — Pets                                                    #
# ------------------------------------------------------------------ #
st.divider()
st.subheader("Pets")

if "pets" not in st.session_state:
    st.session_state.pets = {}          # name -> Pet

col1, col2, col3 = st.columns(3)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])
with col3:
    pet_age = st.number_input("Age (years)", min_value=0, max_value=30, value=3)

if st.button("Add pet"):
    if pet_name in st.session_state.pets:
        st.warning(f"'{pet_name}' is already added.")
    else:
        pet = Pet(name=pet_name, species=species, age=int(pet_age))
        st.session_state.pets[pet_name] = pet
        st.session_state.owner.add_pet(pet)
        st.success(f"Pet '{pet_name}' added.")

if st.session_state.pets:
    st.write("Your pets:", ", ".join(st.session_state.pets.keys()))
else:
    st.info("No pets added yet.")
    st.stop()

# ------------------------------------------------------------------ #
# Section 3 — Tasks                                                   #
# ------------------------------------------------------------------ #
st.divider()
st.subheader("Tasks")

PRIORITY_MAP = {"low": Priority.LOW, "medium": Priority.MEDIUM, "high": Priority.HIGH}

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    task_title = st.text_input("Task title", value="Evening Walk")
with col2:
    duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=30)
with col3:
    priority_str = st.selectbox("Priority", ["low", "medium", "high"], index=2)
with col4:
    category = st.selectbox("Category", ["walk", "feeding", "meds", "grooming", "enrichment"])
with col5:
    assign_to = st.selectbox("Assign to", list(st.session_state.pets.keys()))

if st.button("Add task"):
    task = Task(
        title=task_title,
        duration_minutes=int(duration),
        priority=PRIORITY_MAP[priority_str],
        category=category,
    )
    st.session_state.pets[assign_to].add_task(task)
    st.success(f"Task '{task_title}' added to {assign_to}.")

# Display all tasks grouped by pet
for pet_name, pet in st.session_state.pets.items():
    all_tasks = pet.tasks
    if all_tasks:
        st.markdown(f"**{pet_name}'s tasks**")
        st.table([
            {
                "Title": t.title,
                "Duration (min)": t.duration_minutes,
                "Priority": t.priority.name,
                "Category": t.category,
                "Done": "✓" if t.completed else "○",
            }
            for t in all_tasks
        ])

# ------------------------------------------------------------------ #
# Section 4 — Generate Schedule                                       #
# ------------------------------------------------------------------ #
st.divider()
st.subheader("Today's Schedule")

if st.button("Generate schedule"):
    scheduler = Scheduler(owner=st.session_state.owner)
    schedule = scheduler.generate_plan(date=date.today().isoformat())
    st.session_state.schedule = schedule
    st.session_state.explanation = scheduler.explain_plan(schedule)

if "schedule" in st.session_state:
    schedule = st.session_state.schedule
    st.text(schedule.display())

    with st.expander("Why was this plan chosen?"):
        st.text(st.session_state.explanation)
