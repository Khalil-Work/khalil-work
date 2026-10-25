"""Build daily profile SVGs from attributed public sources; standard library only."""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timedelta, timezone
import hashlib
import html
import json
import os
from pathlib import Path
import random
import textwrap
import time
import urllib.request

OWNER = "Khalil-Work"
LOCAL = timezone(timedelta(hours=8))
RAW = f"https://raw.githubusercontent.com/{OWNER}/khalil-work/output/daily/state.json"
PALETTES = {
    "dark": dict(bg="#0d1117", text="#f0f3fa", muted="#a6afc3", accent="#bd9bff", line="#30363d", bar="#252034"),
    "light": dict(bg="#ffffff", text="#202034", muted="#586174", accent="#7544b5", line="#d8dee8", bar="#eee7f7"),
}


def get_json(url, token=None):
    headers = {"User-Agent": "Khalil-Work-daily-profile/1.0", "Accept": "application/json"}
    token = token or (os.environ.get("GH_TOKEN") if url.startswith("https://api.github.com/") else None)
    if token:
        headers["Authorization"] = "Bearer " + token
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=25) as response:
                raw = response.read(2_000_001)
            if len(raw) > 2_000_000:
                raise ValueError("Response exceeded the size limit")
            return json.loads(raw)
        except Exception:
            if attempt == 2:
                raise
            time.sleep(2)


def plain(value, limit=500):
    if not isinstance(value, str):
        raise ValueError("Expected source text")
    value = " ".join(html.unescape(value).split())
    if not value or len(value) > limit:
        raise ValueError("Source text is empty or too long")
    return value


def quote_from(data, day):
    q = plain(data[0]["q"])
    a = plain(data[0]["a"], 100)
    if a.lower() == "zenquotes.io" or len(q.split()) > 25:
        raise ValueError("Daily quote is unsuitable for the compact card")
    return {"text": q, "author": a, "date": day, "source": "https://zenquotes.io/"}


def trivia_from(data, day):
    if data.get("response_code") != 0:
        raise ValueError("Trivia provider returned no question")
    item = data["results"][0]
    question = plain(item["question"], 280)
    answer = plain(item["correct_answer"], 100)
    options = [answer] + [plain(s, 100) for s in item["incorrect_answers"]]
    if len(options) != 4 or len(set(options)) != 4:
        raise ValueError("Expected four different answer choices")
    random.Random(day + question).shuffle(options)
    return {"question": question, "answer": answer, "options": options,
            "date": day, "source": "https://opentdb.com/", "license": "CC BY-SA 4.0"}


def push_timing(events, now):
    counts = Counter(dict.fromkeys(["Morning", "Afternoon", "Evening", "Night"], 0))
    seen = set()
    dates = []
    for event in events:
        if event.get("id") in seen or event.get("type") != "PushEvent":
            continue
        if event.get("actor", {}).get("login", "").lower() != OWNER.lower():
            continue
        stamp = datetime.fromisoformat(event["created_at"].replace("Z", "+00:00"))
        if not now - timedelta(days=30) <= stamp <= now:
            continue
        seen.add(event["id"])
        hour = stamp.astimezone(LOCAL).hour
        label = "Morning" if 6 <= hour < 12 else "Afternoon" if 12 <= hour < 18 else "Evening" if 18 <= hour < 24 else "Night"
        counts[label] += 1
        dates.append(stamp.date().isoformat())
    return {"counts": dict(counts), "total": sum(counts.values()), "timezone": "UTC+8",
            "sample": "Up to 300 recent public events, within 30 days",
            "earliest_push": min(dates) if dates else None, "updated": now.isoformat()}


def fetch_state(now, old, fetch=get_json):
    day = now.astimezone(LOCAL).date().isoformat()
    state = dict(old)
    warnings = []
    for key, url, parse in [
        ("quote", "https://zenquotes.io/api/today", quote_from),
        ("trivia", "https://opentdb.com/api.php?amount=1&category=9&type=multiple", trivia_from),
    ]:
        if old.get(key, {}).get("date") == day:
            continue
        try:
            data = fetch(url)
            try:
                state[key] = parse(data, day)
            except ValueError:
                if key != "quote":
                    raise
                # Keep inspiration concise; choose another attributed quote when
                # today's provider selection is too long for a readable card.
                choices = []
                for item in fetch("https://zenquotes.io/api/quotes"):
                    try:
                        choices.append(quote_from([item], day))
                    except ValueError:
                        pass
                if not choices:
                    raise ValueError("No compact attributed quote available")
                state[key] = choices[int(hashlib.sha256(day.encode()).hexdigest(), 16) % len(choices)]
        except Exception as error:
            warnings.append(f"{key}: retained last successful content ({type(error).__name__})")
            if key not in state:
                raise RuntimeError(f"No initial {key} is available") from error
    try:
        events = []
        for page in range(1, 4):
            batch = fetch(f"https://api.github.com/users/{OWNER}/events/public?per_page=100&page={page}")
            events.extend(batch)
            if len(batch) < 100:
                break
        state["timing"] = push_timing(events, now)
    except Exception as error:
        warnings.append(f"timing: retained last successful sample ({type(error).__name__})")
        if "timing" not in state:
            raise RuntimeError("No timing data is available") from error
    state["generated_at"] = now.isoformat()
    state["warnings"] = warnings
    return state


def text(x, y, value, size=24, color="text", p=None, weight=400):
    return f'<text x="{x}" y="{y}" fill="{p[color]}" font-size="{size}" font-weight="{weight}">{html.escape(str(value))}</text>'


def lines(value, width=34):
    return textwrap.wrap(value, width=width, break_long_words=True, break_on_hyphens=False)


def svg(title, height, body, p, description):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="520" height="{height}" viewBox="0 0 520 {height}" role="img" aria-labelledby="title desc">
<title id="title">{html.escape(title)}</title><desc id="desc">{html.escape(description)}</desc>
<rect x=".5" y=".5" width="519" height="{height-1}" rx="14" fill="{p['bg']}" stroke="{p['line']}"/>
<g font-family="Arial,Helvetica,sans-serif">{body}</g></svg>'''


def render_quote(q, p):
    body = text(26, 38, "A MOMENT TO REFLECT", 18, "accent", p, 700)
    body += text(494, 38, q["date"], 16, "muted", p).replace('<text x="494"', '<text text-anchor="end" x="494"')
    y = 82
    for line in lines("“" + q["text"] + "”", 33):
        body += text(26, y, line, 26, p=p)
        y += 34
    for author_line in lines("— " + q["author"], 40):
        body += text(26, y + 12, author_line, 20, "accent", p)
        y += 26
    body += text(26, y + 20, "Daily inspiration · ZenQuotes API", 17, "muted", p)
    return svg("Daily inspiration", y + 44, body, p, q["text"] + " — " + q["author"])


def render_trivia(q, p, answer=False):
    body = text(26, 38, "THE DAILY CURIOSITY" if not answer else "TODAY’S ANSWER", 18, "accent", p, 700)
    body += text(494, 38, q["date"], 16, "muted", p).replace('<text x="494"', '<text text-anchor="end" x="494"')
    y = 80
    for line in lines(q["answer"] if answer else q["question"], 34):
        body += text(26, y, line, 26, p=p)
        y += 32
    if not answer:
        y += 9
        for i, option in enumerate(q["options"]):
            for j, line in enumerate(lines(option, 32)):
                body += text(30, y, ("ABCD"[i] + ". " if j == 0 else "    ") + line, 22, "muted", p)
                y += 30
            y += 6
    body += text(26, y + 24, "Open Trivia DB · CC BY-SA 4.0", 17, "muted", p)
    return svg("Daily trivia answer" if answer else "Daily general-knowledge trivia", y + 46, body, p, q["answer"] if answer else q["question"] + " Choices: " + "; ".join(q["options"]))


def render_timing(sample, p):
    body = text(26, 38, "WHEN I PUSH", 18, "accent", p, 700)
    sample_day = datetime.fromisoformat(sample["updated"]).astimezone(LOCAL).date().isoformat()
    body += text(494, 38, sample_day, 16, "muted", p).replace('<text x="494"', '<text text-anchor="end" x="494"')
    body += text(26, 72, "Recent public push events · UTC+8", 22, p=p)
    y = 119
    for label, n in sample["counts"].items():
        percent = n / sample["total"] * 100 if sample["total"] else 0
        body += text(26, y, label, 22, p=p)
        body += f'<rect x="170" y="{y-18}" width="190" height="22" rx="6" fill="{p["bar"]}"/>'
        if n:
            body += f'<rect x="170" y="{y-18}" width="{1.9*percent:.1f}" height="22" rx="6" fill="{p["accent"]}"/>'
        body += text(380, y, f"{n} · {percent:.0f}%", 21, "muted", p)
        y += 44
    body += text(26, y + 8, f'{sample["total"]} public pushes · up to 30 days', 17, "muted", p)
    body += text(26, y + 34, "Push timing, not working hours or commit totals.", 16, "muted", p)
    return svg("Recent public push timing", y + 56, body, p, json.dumps(sample["counts"]) + ". " + sample["sample"])


def write_output(state, dest):
    dest.mkdir(parents=True, exist_ok=True)
    for theme, p in PALETTES.items():
        for name, value in [("quote", render_quote(state["quote"], p)), ("trivia", render_trivia(state["trivia"], p)),
                            ("answer", render_trivia(state["trivia"], p, True)), ("timing", render_timing(state["timing"], p))]:
            (dest / f"{name}-{theme}.svg").write_text(value, encoding="utf-8")
    (dest / "state.json").write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
    q, t, s = state["quote"], state["trivia"], state["timing"]
    readable = f'''# Daily inspiration & curiosity

## Daily inspiration · {q['date']}

> {q['text']}

— **{q['author']}**

Inspirational quotes provided by [ZenQuotes API](https://zenquotes.io/).

## General-knowledge trivia · {t['date']}

{t['question']}

'''
    readable += "\n".join(f"- **{'ABCD'[i]}.** {opt}" for i, opt in enumerate(t["options"]))
    readable += f'''\n\n<details><summary>Reveal the answer</summary>\n\n**{t['answer']}**\n\n</details>

Question and answers from [Open Trivia DB](https://opentdb.com/), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Presentation adapted for this profile; the trivia cards and text retain that license.

## Recent public push timing

Timezone **UTC+8**. {s['sample']}. These are public **push events**, not commit counts or working hours. Private activity and other event types are excluded; GitHub may return less than 30 days. No historical author dates are used.

| Time | Public pushes |
| --- | ---: |
'''
    readable += "\n".join(f"| {label} | {n} |" for label, n in s["counts"].items())
    readable += f"\n\nTiming sample last refreshed: {s['updated']}.\n\nLast refresh attempt: {state['generated_at']}. If a provider is unavailable, its previous content and original date remain visible.\n"
    if state["warnings"]:
        readable += "\nRefresh warnings: " + "; ".join(state["warnings"]) + ".\n"
    (dest / "README.md").write_text(readable, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("dist/daily"))
    args = parser.parse_args()
    try:
        old = get_json(RAW)
    except Exception:
        old = {}
    now = datetime.now(timezone.utc)
    state = fetch_state(now, old)
    write_output(state, args.output)
    print(json.dumps({"date": now.date().isoformat(), "pushes": state["timing"]["total"], "warnings": state["warnings"]}))


if __name__ == "__main__":
    main()
