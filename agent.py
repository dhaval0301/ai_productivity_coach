import json
from typing import Dict, Any, Optional
from openai import OpenAI

# one client for all calls
client = OpenAI()

# default model used when none is provided
DEFAULT_MODEL = "gpt-4o-mini"

SYSTEM_PROMPT = """You are a supportive yet practical productivity coach.
You help users set realistic goals, chunk work, fight procrastination, and reflect at night.
Keep messages concise, positive, and specific. When asked to generate plans or summaries,
return structured JSON when appropriate.
"""

PLAN_JSON_INSTRUCTIONS = """Return a JSON object with this shape:
{
  "goals": [{"id": "G1", "text": "...", "why": "..."}],
  "tasks": [
    {"id": "T1", "goal_id": "G1", "text": "concrete step", "estimate_min": 25, "priority": "high"}
  ],
  "schedule_blocks": [
    {"label": "Deep Work", "duration_min": 50, "task_ids": ["T1","T2"]}
  ],
  "notes": "short tips"
}
Ensure time estimates are reasonable and tasks are small enough to complete within 25-50 minute focus blocks.
"""

NUDGE_JSON_INSTRUCTIONS = """Return a JSON object:
{
  "nudge": "one-sentence encouragement",
  "micro_step": "small next step the user can do in <= 2 minutes",
  "reframe": "brief cognitive reframe to reduce procrastination"
}"""

REFLECT_JSON_INSTRUCTIONS = """Return a JSON object:
{
  "summary": "2-3 sentence summary of the day",
  "wins": ["...","..."],
  "lessons": ["..."],
  "tomorrow_top_one": "the most important thing to do first"
}"""

def _chat_json(
    user_prompt: str,
    model: Optional[str] = None,
    temperature: float = 0.4,
) -> Dict[str, Any]:
    """
    Call the model and force a JSON object output.
    """
    model = model or DEFAULT_MODEL
    resp = client.chat.completions.create(
        model=model,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=temperature,
    )
    text = resp.choices[0].message.content or "{}"
    try:
        return json.loads(text)
    except Exception:
        # fallback: wrap raw text
        return {"raw": text}

def plan_day(
    freeform_goals: str,
    model: Optional[str] = None,
    temperature: float = 0.4,
) -> Dict[str, Any]:
    prompt = f"""User's goals or tasks (freeform):


```
{freeform_goals}
```
Create a pragmatic plan for today with small tasks and 25-50 minute focus blocks.
{PLAN_JSON_INSTRUCTIONS}"""
    return _chat_json(prompt, model=model, temperature=temperature)

def nudge(
    context: str,
    model: Optional[str] = None,
    temperature: float = 0.2,
) -> Dict[str, Any]:
    prompt = f"""The user feels a bit stuck. Context:
{context}

Provide 1 short encouragement, a tiny next step, and a brief reframe.
{NUDGE_JSON_INSTRUCTIONS}"""
    return _chat_json(prompt, model=model, temperature=temperature)

def reflect(
    day_notes: str,
    model: Optional[str] = None,
    temperature: float = 0.4,
) -> Dict[str, Any]:
    prompt = f"""Summarize the user's day and suggest one priority for tomorrow.
Notes:
{day_notes}
{REFLECT_JSON_INSTRUCTIONS}"""
    return _chat_json(prompt, model=model, temperature=temperature)
