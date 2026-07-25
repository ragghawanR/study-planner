# AI SDE Coach – Study Planner

An AI-powered study coach that generates personalized daily study plans based on the **TakeUForward SDE Sheet**, the current day of the week, upcoming LeetCode contests, and learning progress. The plan is delivered automatically via Telegram using GitHub Actions and OpenAI.

## Features

- 📅 Generates personalized study plans daily
- 📊 Adapts workload based on day of the week
- 🎯 Prioritizes concepts on weekdays, problem-solving on weekends
- ⚡ Reduces workload on LeetCode contest days
- 📈 Tracks learning progress locally
- 💬 Delivers plans via Telegram
- ⚙️ Runs automatically with GitHub Actions (no server needed)

## Quick Start

### Prerequisites

- Python 3.12+
- Git
- OpenAI API key
- Telegram bot token

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/sde-ai-coach.git
   cd sde-ai-coach
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

### Usage

Run the planner locally:
```bash
python planner/planner.py
```

## Project Structure

```
sde-ai-coach/
├── planner/              # Core planning logic
│   ├── planner.py
│   ├── prompt_builder.py
│   ├── scheduler.py
│   ├── llm.py
│   ├── roadmap.py
│   └── models.py
├── telegram/             # Telegram bot integration
│   └── telegram_bot.py
├── data/                 # Data files
│   ├── progress.json
│   ├── tuf_sheet.json
│   └── config.json
├── .github/workflows/    # GitHub Actions
│   └── daily.yml
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── LICENSE
```

## Development Milestones

- [x] Milestone 1: Project Setup
- [ ] Milestone 2: TakeUForward Roadmap
- [ ] Milestone 3: Progress Tracking
- [ ] Milestone 4: Scheduling Rules
- [ ] Milestone 5: Prompt Builder
- [ ] Milestone 6: OpenAI Integration
- [ ] Milestone 7: Telegram Integration
- [ ] Milestone 8: GitHub Actions

## Configuration

See `.env.example` for required environment variables:
- `OPENAI_API_KEY` – OpenAI API key
- `TELEGRAM_BOT_TOKEN` – Telegram bot token
- `TELEGRAM_CHAT_ID` – Your Telegram chat ID

## License

MIT

## Contributing

See CONTRIBUTING.md for guidelines.
