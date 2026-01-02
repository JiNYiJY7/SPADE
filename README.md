# Smart Academic Planning Intelligent Agent (SPADE-inspired)

This project implements a **Smart Academic Planning Intelligent Agent** using a **Python-based, SPADE-inspired framework**, developed as part of the Intelligent Agents coursework (Phase 2).

The focus of this implementation is on **framework initialization, code structure, and agent skeleton design**, rather than advanced intelligence or real-time deployment.

---

## 📌 Project Objective

The objective of this project is to design and implement the **skeleton of an intelligent academic planning agent** that:

- Follows the architecture proposed in Phase 2
- Uses a Python-based agent framework conceptually inspired by SPADE
- Demonstrates clear agent behaviours and shared memory
- Runs without errors as a foundation for further development

---

## 🧠 Agent Architecture Overview

The system is designed as a **single intelligent agent** composed of multiple behaviours that interact through a **shared agent memory**.

### Key Components
- **Agent Memory**
  - Central storage for tasks, free time slots, generated plans, and logs
- **Task Management Behaviour**
  - Handles task input, availability setup, and progress updates
- **Priority Evaluation Behaviour**
  - Ranks tasks based on deadline urgency, importance, and remaining workload
- **Schedule Planning Behaviour**
  - Generates a study plan by allocating tasks into available time slots
- **Rescheduling Behaviour**
  - Rebuilds the plan when task progress or constraints change
- **Reminder Management Behaviour**
  - Generates reminders with frequency based on deadline proximity

This structure strictly reflects the **behaviour modelling and flow diagram proposed in Phase 2**.

---

## 🏗️ Project Structure

```text
SPADE/
│
├── study_planner/
│ ├── __init__.py
│ ├── main.py  #Agent entry point
│ ├── models.py  #Data models
│ ├── memory.py  #Shared agent memory
│ │
│ ├── behaviours/
│ │ ├── task_management.py
│ │ ├── priority_evaluation.py
│ │ ├── schedule_planning.py
│ │ ├── rescheduling.py
│ │ └── reminder_management.py
│ │
│ └── utils/
│ ├── scoring.py
│ ├── scheduler.py
│ └── time_utils.py
│
├── tests/
│ ├── conftest.py
│ ├── test_priority.py
│ └── test_scheduler.py
│
├── requirements.txt
└── README.md

```

---

## ⚙️ Framework Choice

This project adopts a **SPADE-inspired agent framework** implemented in Python.

- Real XMPP deployment is **not required**
- Agent communication and behaviours are **simulated locally**
- The focus is on **architecture correctness**, not infrastructure overhead

This approach is consistent with the Phase 2 requirement that **simulation is acceptable** while preserving agent design principles.

---

## ▶️ How to Run the Agent
### 1. Install dependencies

```bash
pip install -r requirements.txt

```

##Run the agent (default demo input)
```bash
python -m study_planner.main

```

###Run unit tests
```bash
pytest -q

```

