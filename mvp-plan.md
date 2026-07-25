# AI SDE Coach - MVP Development Plan

## Project Goal

Build an AI-powered study coach that generates a personalized daily study plan based on the **TakeUForward SDE Sheet**, the current day of the week, upcoming LeetCode contests, and the user's learning progress.

The MVP should deliver the study plan automatically every morning via **Telegram** using **GitHub Actions** and the **OpenAI API**.

---

# MVP Objectives

The MVP should be able to:

* Generate a personalized study plan every day.
* Adapt the workload based on the day of the week.
* Prioritize concepts during weekdays.
* Prioritize problem solving during weekends.
* Reduce workload on LeetCode contest days.
* Track learning progress.
* Deliver the plan through Telegram.
* Run automatically without requiring a dedicated server.

---

# Non-Goals (MVP)

The following features are intentionally **out of scope** for the first version:

* Android application
* Web dashboard
* User authentication
* Multiple users
* LeetCode account integration
* Automatic progress detection
* Database
* Analytics
* AI chat interface
* Flashcards
* Revision scheduling algorithms

These will be added in future iterations.

---

# High-Level Architecture

```text
                    GitHub Repository
                           │
                           │
                  GitHub Actions (Cron)
                           │
                           ▼
                     planner.py
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
     progress.json     tuf_sheet.json   config.json
                           │
                           ▼
                  Prompt Builder
                           │
                           ▼
                   OpenAI Responses API
                           │
                           ▼
                   Daily Study Plan
                           │
                           ▼
                    Telegram Bot API
                           │
                           ▼
                      Telegram User
```

---

# Technology Stack

| Component       | Technology                   |
| --------------- | ---------------------------- |
| Language        | Python 3.12                  |
| Scheduler       | GitHub Actions               |
| LLM             | OpenAI Responses API         |
| Notification    | Telegram Bot                 |
| Storage         | JSON                         |
| Version Control | GitHub                       |
| Package Manager | pip                          |
| Configuration   | Environment Variables + JSON |

---

# Repository Structure

```text
sde-ai-coach/

├── planner/
│   ├── planner.py
│   ├── prompt_builder.py
│   ├── scheduler.py
│   ├── llm.py
│   ├── roadmap.py
│   └── models.py
│
├── telegram/
│   └── telegram_bot.py
│
├── data/
│   ├── progress.json
│   ├── tuf_sheet.json
│   └── config.json
│
├── .github/
│   └── workflows/
│       └── daily.yml
│
├── requirements.txt
├── .env.example
├── README.md
└── LICENSE
```

---

# Milestone 1 – Project Setup

## Deliverables

* Create GitHub repository
* Configure Python environment
* Configure `.gitignore`
* Add OpenAI SDK
* Add Telegram SDK
* Configure environment variables

### Definition of Done

* Project runs locally.
* API keys load correctly.
* Repository structure is in place.

---

# Milestone 2 – TakeUForward Roadmap

Convert the TakeUForward SDE Sheet into structured JSON.

Example:

```json
{
  "topic": "Arrays",
  "difficulty": "Easy",
  "problems": [
    "Two Sum",
    "Best Time to Buy and Sell Stock"
  ]
}
```

### Deliverables

* `tuf_sheet.json`
* Ordered topics
* Ordered problems

### Definition of Done

The planner can determine:

* current topic
* next topic
* remaining topics

---

# Milestone 3 – Progress Tracking

Maintain user progress in a local JSON file.

Example:

```json
{
  "current_topic": "Arrays",
  "completed_topics": [],
  "completed_problems": [],
  "revision_queue": [],
  "current_system_design": "Caching",
  "last_study_date": null
}
```

### Definition of Done

Planner can:

* read progress
* update progress
* resume after interruption

---

# Milestone 4 – Scheduling Rules

Implement deterministic scheduling logic before invoking the LLM.

## Weekdays

* Focus on concepts
* 3–5 coding problems
* One system design topic
* Revision

## Saturday

If Biweekly Contest:

* Contest
* Upsolve
* Maximum two additional problems

Otherwise:

* Medium workload
* More problem solving

## Sunday

If Weekly Contest:

* Contest
* Upsolve
* Revision only

Otherwise:

* Heavy problem solving

### Definition of Done

The planner correctly identifies the workload profile based on the day.

---

# Milestone 5 – Prompt Builder

Generate a structured prompt containing:

* Current date
* Day of week
* Contest information
* Current topic
* Completed topics
* Revision queue
* Current system design topic
* Daily scheduling rules

Expected LLM Output:

```json
{
  "summary": "...",
  "tasks": [],
  "revision": [],
  "motivation": "..."
}
```

### Definition of Done

Prompt is deterministic and reusable.

---

# Milestone 6 – OpenAI Integration

Use the OpenAI Responses API to generate the daily study plan.

Responsibilities:

* Build prompt
* Send request
* Parse response
* Validate output
* Handle API failures gracefully

### Definition of Done

Running the planner locally produces a valid study plan.

---

# Milestone 7 – Telegram Integration

Create a Telegram Bot.

Daily message format:

```text
📅 Monday

Today's Focus
-------------
Binary Trees

Tasks
-----
• Study DFS
• Solve 4 problems
• Revise Sliding Window

System Design
-------------
Caching

Estimated Time
--------------
3 hours

Good luck!
```

### Definition of Done

Planner sends the generated study plan to Telegram.

---

# Milestone 8 – GitHub Actions

Configure a scheduled workflow.

Daily Flow:

1. Trigger workflow.
2. Load progress.
3. Generate prompt.
4. Call OpenAI.
5. Send Telegram message.
6. Log execution status.

### Definition of Done

The workflow executes automatically on schedule.

---

# Configuration

## Environment Variables

```text
OPENAI_API_KEY=
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
```

---

# Success Criteria

The MVP is considered complete when:

* A GitHub Action runs automatically every morning.
* The planner generates a day-specific study plan.
* The plan reflects weekday/weekend scheduling rules.
* Contest days receive reduced workloads.
* The study plan is delivered successfully via Telegram.
* The planner uses stored progress to continue from previous work.

---

# Future Enhancements (Post-MVP)

## Phase 2

* SQLite instead of JSON
* Automatic revision scheduler
* Progress analytics
* Weekly summary reports

## Phase 3

* LeetCode integration
* Automatic solved-problem detection
* Difficulty-based adaptive planning

## Phase 4

* Android application
* Flutter UI
* Push notifications
* Offline support

## Phase 5

* AI interview simulator
* System design mentor
* Behavioural interview coach
* Resume reviewer
* Company-specific interview preparation

---

# Development Principles

* Keep business logic deterministic; use the LLM for planning and explanation, not for state management.
* Store all progress locally in version-controlled data files (or a future database), never inside prompts.
* Design modules to be replaceable (e.g., Telegram can later be swapped for an Android app without changing the planner).
* Prefer simple, testable components over premature optimisation.
* Build each milestone with a clear "Definition of Done" before moving to the next.

---

# MVP Checklist

* [ ] Initialise repository
* [ ] Configure Python project
* [ ] Add OpenAI integration
* [ ] Add Telegram bot integration
* [ ] Create `tuf_sheet.json`
* [ ] Create `progress.json`
* [ ] Implement scheduling rules
* [ ] Build prompt generator
* [ ] Generate daily study plan
* [ ] Send plan to Telegram
* [ ] Configure GitHub Actions
* [ ] Verify end-to-end daily execution
* [ ] Document setup and usage
