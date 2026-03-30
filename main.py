from datetime import date

from pawpal_system import Owner, Pet, Priority, Scheduler, Task


def main():
    # ------------------------------------------------------------------ #
    # 1. Create Owner                                                      #
    # ------------------------------------------------------------------ #
    jordan = Owner(
        name="Jordan",
        available_minutes=90,
        preferred_start_time="08:00",
        preferred_categories=["walk", "feeding"],
    )

    # ------------------------------------------------------------------ #
    # 2. Create Pets                                                       #
    # ------------------------------------------------------------------ #
    mochi = Pet(name="Mochi", species="dog", age=3)
    luna = Pet(name="Luna", species="cat", age=5)

    # ------------------------------------------------------------------ #
    # 3. Add Tasks                                                         #
    # ------------------------------------------------------------------ #

    # Tasks for Mochi (dog)
    mochi.add_task(Task(
        title="Evening Walk",
        duration_minutes=40,
        priority=Priority.HIGH,
        category="walk",
        frequency="daily",
    ))
    mochi.add_task(Task(
        title="Flea Medicine",
        duration_minutes=5,
        priority=Priority.MEDIUM,
        category="meds",
        frequency="weekly",
    ))
    mochi.add_task(Task(
        title="Brush Coat",
        duration_minutes=15,
        priority=Priority.LOW,
        category="grooming",
        frequency="weekly",
    ))

    # Tasks for Luna (cat)
    luna.add_task(Task(
        title="Enrichment Toy Session",
        duration_minutes=20,
        priority=Priority.MEDIUM,
        category="enrichment",
        frequency="daily",
    ))

    jordan.add_pet(mochi)
    jordan.add_pet(luna)

    # ------------------------------------------------------------------ #
    # 4. Generate and print Today's Schedule                               #
    # ------------------------------------------------------------------ #
    today = date.today().isoformat()
    scheduler = Scheduler(owner=jordan)
    schedule = scheduler.generate_plan(date=today)

    print("\n" + "=" * 44)
    print("         PAWPAL+ — TODAY'S SCHEDULE")
    print("=" * 44)
    print(schedule.display())
    print()
    print(scheduler.explain_plan(schedule))
    print("=" * 44 + "\n")


if __name__ == "__main__":
    main()
