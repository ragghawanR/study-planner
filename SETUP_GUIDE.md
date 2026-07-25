# AI SDE Coach - Setup & Usage Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Git
- OpenAI API key
- Telegram bot token

### Installation

1. **Clone and setup:**
```bash
git clone https://github.com/yourusername/sde-ai-coach.git
cd sde-ai-coach
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Configure environment:**
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. **Test locally:**
```bash
python planner/planner.py
```

---

## 🔧 Configuration

### OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Add to `.env`: `OPENAI_API_KEY=sk-...`

### Telegram Bot
1. Create a bot via [@BotFather](https://t.me/botfather) on Telegram
2. Get your chat ID from [@userinfobot](https://t.me/userinfobot)
3. Add to `.env`:
   ```
   TELEGRAM_BOT_TOKEN=your_bot_token
   TELEGRAM_CHAT_ID=your_chat_id
   ```

### GitHub Actions (Automated Daily Execution)
1. Fork the repository
2. Go to Settings → Secrets and variables → Actions
3. Add three secrets:
   - `OPENAI_API_KEY`
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`

The workflow will trigger automatically at 9:00 AM IST (3:30 AM UTC) daily.

---

## 📚 Project Structure

```
sde-ai-coach/
├── planner/
│   ├── __init__.py
│   ├── planner.py          # Test/debug entry point
│   ├── main.py             # Production entry point (for GitHub Actions)
│   ├── models.py           # Pydantic data models
│   ├── roadmap.py          # TakeUForward roadmap manager
│   ├── progress.py         # Progress tracking
│   ├── scheduler.py        # Scheduling rules
│   ├── prompt_builder.py   # LLM prompt generation
│   └── llm.py              # OpenAI integration
│
├── telegram/
│   ├── __init__.py
│   └── telegram_bot.py     # Telegram messaging
│
├── data/
│   ├── tuf_sheet.json      # TakeUForward topics & problems
│   ├── progress.json       # User progress (auto-updated)
│   └── config.json         # Configuration
│
├── .github/workflows/
│   └── daily.yml           # GitHub Actions workflow
│
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── .gitignore
├── README.md              # Main readme
└── SETUP_GUIDE.md         # This file
```

---

## 🎯 Usage

### Local Testing
```bash
# Test the planner without API keys
python planner/planner.py

# Run the full pipeline (requires API keys)
python -m planner.main
```

### Viewing Logs
```bash
# Check execution logs
ls logs/
cat logs/planner_YYYY-MM-DD_HH-MM-SS.log
```

### Checking Progress
```bash
# View current progress
cat data/progress.json

# View study roadmap
cat data/tuf_sheet.json
```

---

## 📊 How It Works

### Daily Pipeline

1. **Environment Check** → Validates API keys
2. **Load Roadmap** → Reads TakeUForward topics
3. **Load Progress** → Reads user study progress
4. **Determine Workload** → Based on day of week
5. **Build Prompt** → Creates contextualized prompt for LLM
6. **Generate Plan** → Calls OpenAI API
7. **Format & Send** → Sends study plan via Telegram
8. **Update Progress** → Records last study date

### Scheduling Rules

| Day | Workload | Focus | Problems | System Design |
|-----|----------|-------|----------|---------------|
| Mon-Fri | Medium | Concepts | 3-5 | Yes |
| Saturday | Heavy | Problem solving | 5-7 | No |
| Sunday | Heavy | Problem solving | 5-7 | No |
| **Contest Day** | Contest | Compete/Upsolve | Varies | No |

---

## 🔄 Workflow

### Manual Trigger
To manually trigger the workflow on GitHub:
1. Go to Actions tab
2. Select "Daily Study Plan Generation"
3. Click "Run workflow"

### Automatic Execution
The workflow runs automatically every day at 9:00 AM IST.

---

## 🚨 Troubleshooting

### API Key Issues
```bash
# Test OpenAI API key
python -c "import openai; openai.api_key='your-key'; print(openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=[{'role':'user','content':'test'}]))"
```

### Telegram Bot Issues
```bash
# Test Telegram bot
curl "https://api.telegram.org/botYOUR_BOT_TOKEN/getMe"
```

### Environment Variables Not Loading
```bash
# Verify .env file exists and is in project root
ls -la .env

# Check if env vars are loaded
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('OPENAI_API_KEY'))"
```

### GitHub Actions Failures
1. Check workflow logs in GitHub Actions tab
2. Verify secrets are correctly set
3. Ensure repository is public or Actions are enabled for private repos

---

## 📈 Progress Tracking

The system tracks:
- ✓ Current topic being studied
- ✓ Completed topics
- ✓ Completed problems
- ✓ Revision queue
- ✓ Total problems solved
- ✓ Last study date
- ✓ Current system design topic

View progress anytime:
```bash
cat data/progress.json
```

---

## 🎓 Study Tips

1. **Consistency**: Study at the same time daily for best results
2. **Workload**: The planner adapts workload based on day of week
3. **Revision**: Problems are added to revision queue automatically
4. **Topics**: Progress through TakeUForward systematically
5. **System Design**: One system design topic per weekday

---

## 🔮 Future Enhancements

- [ ] SQLite database instead of JSON
- [ ] Automatic revision scheduling algorithm
- [ ] LeetCode account integration
- [ ] Progress analytics dashboard
- [ ] Weekly summary reports
- [ ] Interview preparation modes
- [ ] Mobile app

---

## 📞 Support

- Check logs in `logs/` directory
- Review README.md for project overview
- Verify environment variables are set correctly
- Ensure API keys are valid and have sufficient quota

---

## 📄 License

MIT License - see LICENSE file for details
