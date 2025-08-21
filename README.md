

# Daily Productivity Coach AI

Plan your day, focus deeply, and close the loop  in one tiny app.
**Features:** voice input → plan, real elapsed focus minutes, habit streaks, nightly reflection, weekly report (Markdown), and calendar export (.ics). Built with **Gradio + OpenAI**


## Demo

* **Hugging Face Space:** https://huggingface.co/spaces/dhaval0003/daily-productivity-coach-ai
* **Medium post:** https://medium.com/@dhruvingale1926/focus-flow-done-a-tiny-ai-coach-youll-actually-use-75ca9c88fda4


##  What it does

* **Plan**: Paste or speak goals → AI produces SMART-ish tasks + suggested focus blocks.
* **Focus**: Start/End a session → logs **actual elapsed minutes** (not just a timer value).
* **Habits**: Add habits and mark done to build streaks.
* **Reflect**: Short nightly reflection (summary, wins, lessons, tomorrow’s top one).
* **Reports**: One-click weekly report (`weekly_report.md`).
* **Calendar**: Export focus blocks to `.ics` and drop into Google/Apple/Outlook.
* **Voice**: Whisper transcription for quick “speak → plan”.





##  Tech stack

* **Frontend:** Gradio (Python)
* **AI:** OpenAI (Chat for plan/nudge/reflect, Whisper for voice)
* **Charts:** matplotlib
* **Storage:** local JSON files (auto-created)
* **Hosting:** Hugging Face Spaces (CPU)



##  Quickstart (local)

1. **Clone & install**

```bash
git clone <your-repo-url>
cd daily-productivity-coach-ai
python -m venv .venv && source .venv/bin/activate  # or use conda
pip install -r requirements.txt
```

2. **Set your key**

```bash
export OPENAI_API_KEY=sk-...
# Windows (PowerShell):  $env:OPENAI_API_KEY="sk-..."
```

3. **Run**

```bash
python app.py
```


##  Configuration

* **Model presets:** in `app.py` (`MODE_PRESETS`) → “Speed”, “Balanced”, “Insight”.
* **Files created at runtime:**
  `data/` (auto) → `tasks.json`, `sessions.json`, `habits.json`, `reflections.json`
* **Secrets:** `OPENAI_API_KEY` (required for chat + Whisper).



##  Requirements

Create `requirements.txt` (or keep the one in repo):

```
gradio>=4.0.0
openai>=1.30.0
matplotlib>=3.8.0
python-dateutil>=2.9.0
pydantic>=2.6.0
```


##  How to use

1. **Plan** tab: paste goals → **Generate Plan**.
2. **Focus** tab: pick one task → **Start** → work → **End & Save** (logs real minutes).
3. **Habits** tab: add a habit; mark done to grow the streak.
4. **Reflect** tab: quick check-in; AI drafts the summary + tomorrow’s top one.
5. **Reports** tab: **Generate Weekly Report** → download `weekly_report.md`.
6. **Calendar Export** tab: create `.ics` from latest plan and import to your calendar.
7. **Voice** tab: record a short note; it transcribes and plans.

**Sample plan text**

```
- Write blog intro (30m)
- Review PR #431 (20m)
- Prepare 3 slides for demo (45m)
- 30 min run
```


##  Project structure

```
app.py            # Gradio UI + callbacks (tabs, voice, exports)
agent.py          # OpenAI calls: plan_day, nudge, reflect (JSON I/O)
storage.py        # JSON read/write helpers (tasks/sessions/habits/reflections)
requirements.txt  # Python deps
README.md
```
