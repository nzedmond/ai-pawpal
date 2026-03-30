classDiagram
    class Owner {
        +String name
        +int available_minutes
        +String preferences
        +get_constraints()
    }

    class Pet {
        +String name
        +String species
        +int age
        +Owner owner
        +get_required_tasks()
    }

    class Task {
        +String title
        +int duration_minutes
        +String priority
        +String category
        +bool completed
        +is_high_priority()
    }

    class Schedule {
        +String date
        +Owner owner
        +Pet pet
        +List scheduled_tasks
        +int total_duration
        +add_task()
        +remove_task()
        +get_total_duration()
        +display()
    }

    class Scheduler {
        +Owner owner
        +Pet pet
        +List available_tasks
        +generate_plan()
        +explain_plan()
    }

    Owner "1" --> "1..*" Pet : owns
    Pet "1" --> "0..*" Task : has
    Scheduler --> Owner : reads constraints
    Scheduler --> Pet : reads tasks
    Scheduler ..> Schedule : produces
    Schedule "1" --> "0..*" Task : contains
