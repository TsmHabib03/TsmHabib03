"""Refresh contribution SVGs from GitHub's official GraphQL API.
Use GITHUB_TOKEN in Actions, or --github-cli locally.
Failed requests or invalid data leave the last successful artwork untouched.
"""
import argparse
from datetime import date, datetime, timedelta, timezone
import json
import os
import subprocess
from urllib.request import Request, urlopen
from profile_theme import ASSETS, MUTED, BLUE, CYAN, PURPLE, text, rect, frame, svg, write_assets

QUERY = """query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount contributionLevel } }
      }
    }
  }
}"""
LEVELS = ["NONE", "FIRST_QUARTILE", "SECOND_QUARTILE", "THIRD_QUARTILE", "FOURTH_QUARTILE"]
COLORS = ["#303B5D", "#3D59A1", "#565F89", "#7AA2F7", "#7DCFFF"]


def fetch_calendar(username, github_cli=False):
    payload = json.dumps({"query": QUERY, "variables": {"login": username}})
    if github_cli:
        response = subprocess.run(["gh", "api", "graphql", "--input", "-"], input=payload,
                                  capture_output=True, text=True, check=True, timeout=60)
        data = json.loads(response.stdout)
    else:
        token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
        if not token:
            raise RuntimeError("Set GITHUB_TOKEN, or run with --github-cli using existing CLI authentication.")
        request = Request("https://api.github.com/graphql", data=payload.encode("utf-8"), headers={
            "Authorization": f"Bearer {token}", "User-Agent": "TsmHabib03-profile-activity", "Content-Type": "application/json",
        })
        with urlopen(request, timeout=45) as response:
            data = json.load(response)
    if data.get("errors") or not data.get("data", {}).get("user"):
        raise ValueError("GitHub did not return a valid user contribution calendar.")
    return data["data"]["user"]["contributionsCollection"]["contributionCalendar"]


def normalize_calendar(calendar, today=None):
    today = today or datetime.now(timezone.utc).date()
    days = []
    for week in calendar["weeks"]:
        for day in week["contributionDays"]:
            count = day["contributionCount"]
            if type(count) is not int or count < 0:
                raise ValueError("Invalid contribution count.")
            day_date = date.fromisoformat(day["date"])
            days.append({"date": day_date.isoformat(), "count": count, "level": LEVELS.index(day["contributionLevel"])})
    days.sort(key=lambda d: d["date"])
    if not 365 <= len(days) <= 367:
        raise ValueError("Expected a complete rolling-year calendar.")
    dates = [date.fromisoformat(d["date"]) for d in days]
    if any(b - a != timedelta(days=1) for a, b in zip(dates, dates[1:])):
        raise ValueError("Calendar contains duplicate or missing dates.")
    if abs((dates[-1] - today).days) > 1:
        raise ValueError("GitHub returned a stale calendar.")
    total = calendar["totalContributions"]
    if type(total) is not int or total < 0 or total != sum(day["count"] for day in days):
        raise ValueError("Reported total does not match the daily contribution counts.")
    return {"total": total, "days": days}


def weeks_from_days(days):
    weeks = {}
    for day in days:
        day_date = date.fromisoformat(day["date"])
        weekday = (day_date.weekday() + 1) % 7
        sunday = day_date - timedelta(days=weekday)
        weeks.setdefault(sunday, [None] * 7)[weekday] = day
    return list(weeks.values())


def calendar_grid(weeks, x, y, step):
    body = []
    previous_month, labels = None, []
    for column, week in enumerate(weeks):
        first = next(day for day in week if day)
        month = date.fromisoformat(first["date"]).strftime("%b")
        if month != previous_month:
            label = (column * step, month)
            if labels and label[0] - labels[-1][0] < 34:
                # Prefer the new full month over a short partial month at the edge.
                labels[-1] = label
            else:
                labels.append(label)
        previous_month = month
        for row, day in enumerate(week):
            if day is not None:
                body.append(f'<g><title>{day["date"]}: {day["count"]} contributions</title>'
                            + rect(x + column * step, y + row * step, step - 4, step - 4,
                                   COLORS[day["level"]], 3, "none") + "</g>")
    for offset, month in labels:
        body.append(text(x + offset, y - 13, month, 12, MUTED, True))
    for row, label in [(1, "Mon"), (3, "Wed"), (5, "Fri")]:
        body.append(text(x - 40, y + row * step + 12, label, 11, MUTED, True))
    return "\n".join(body)


def render_activity(data, mobile=False):
    w, h = (640, 628) if mobile else (1200, 386)
    total = data["total"]
    active = sum(day["count"] > 0 for day in data["days"])
    busiest = max(day["count"] for day in data["days"])
    body = [frame(w, h), text(32, 35, "Contribution activity", 18, PURPLE, True),
            text(32, 99, f"{total:,}", 52, weight=700),
            text(32, 129, "contributions in the last year", 17, MUTED),
            text(350 if mobile else 722, 94, active, 32, CYAN, True),
            text(350 if mobile else 722, 122, "ACTIVE DAYS", 13, MUTED, True),
            text(490 if mobile else 961, 94, busiest, 32, BLUE, True),
            text(490 if mobile else 961, 122, "BUSIEST DAY", 13, MUTED, True)]
    weeks = weeks_from_days(data["days"])
    if mobile:
        body += [calendar_grid(weeks[:27], 88, 191, 18), calendar_grid(weeks[27:], 88, 389, 18)]
    else:
        body.append(calendar_grid(weeks, 78, 182, 20))
    period = f'{data["days"][0]["date"]} to {data["days"][-1]["date"]}'
    body += [text(32, 555 if mobile else 349, period, 13, MUTED, True),
             text(32, 580 if mobile else 372, f'Updated {data["updated"]} UTC · GitHub data', 12, MUTED, True)]
    legend_x, legend_y = (378, 595) if mobile else (970, 346)
    body.append(text(legend_x - 38, legend_y + 12, "Less", 11, MUTED, True))
    for index, color in enumerate(COLORS):
        body.append(rect(legend_x + index * 20, legend_y, 14, 14, color, 3, "none"))
    body.append(text(legend_x + 106, legend_y + 12, "More", 11, MUTED, True))
    description = (f"{total} contributions in the last year, {active} active days, and {busiest} contributions on the busiest day. "
                   f"{period}. Updated {data['updated']} UTC. Generated from GitHub contribution data; not the native profile interface.")
    return svg(w, h, f"GitHub Activity — {data['username']}", "\n".join(body), description)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--username", default="TsmHabib03")
    parser.add_argument("--github-cli", action="store_true")
    args = parser.parse_args()
    data = normalize_calendar(fetch_calendar(args.username, args.github_cli))
    data.update(username=args.username, updated=datetime.now(timezone.utc).date().isoformat(),
                source="https://docs.github.com/en/graphql/reference/objects#contributioncalendar")
    outputs = {"github-activity.svg": render_activity(data), "github-activity-mobile.svg": render_activity(data, True)}
    write_assets(outputs)
    snapshot = ASSETS / "activity-data.json"
    temporary = snapshot.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    temporary.replace(snapshot)
    print(f"Updated {args.username}: {data['total']} verified contributions across {len(data['days'])} days.")


if __name__ == "__main__":
    main()
