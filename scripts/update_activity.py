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
from profile_theme import ASSETS, NAVY, MUTED, BLUE, CYAN, text, rect, frame, svg, write_assets, city_scene

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


def calendar_grid(weeks, x, y, step, mobile=False):
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
                                   COLORS[day["level"]], 1, "none") + "</g>")
    for offset, month in labels:
        body.append(text(x + offset, y - 13, month, 15 if mobile else 12, MUTED, True))
    for row, label in [(1, "Mon"), (3, "Wed"), (5, "Fri")]:
        body.append(text(x - 40, y + row * step + 10, label, 13 if mobile else 11, MUTED, True))
    return "\n".join(body)


def render_activity(data, mobile=False):
    w, h = (480, 504) if mobile else (840, 296)
    total = data["total"]
    active = sum(day["count"] > 0 for day in data["days"])
    busiest = max(day["count"] for day in data["days"])
    body = [frame(w, h), city_scene(w, h, .38),
            text(24, 46, f"{total:,}", 36, weight=700),
            text(24, 70, "contributions in the last year", 15 if mobile else 14, MUTED),
            text(270 if mobile else 554, 43, active, 28, CYAN, True),
            text(270 if mobile else 554, 66, "Active days", 14, MUTED),
            text(374 if mobile else 710, 43, busiest, 28, BLUE, True),
            text(374 if mobile else 710, 66, "Busiest day", 14, MUTED)]
    weeks = weeks_from_days(data["days"])
    if mobile:
        # Opaque sky behind the data keeps windows from competing with day cells.
        body += [rect(16, 102, w - 32, 304, NAVY, 0, "none"),
                 calendar_grid(weeks[:27], 64, 134, 14, True),
                 calendar_grid(weeks[27:], 64, 298, 14, True)]
    else:
        body += [rect(16, 94, w - 32, 130, NAVY, 0, "none"), calendar_grid(weeks, 64, 122, 14)]
    period = f'{data["days"][0]["date"]} to {data["days"][-1]["date"]}'
    body += [text(24, 436 if mobile else 252, period, 15 if mobile else 12, MUTED, True),
             text(24, 460 if mobile else 276, f'Updated {data["updated"]} UTC · GitHub data', 14 if mobile else 11, MUTED, True)]
    legend_x, legend_y = (292, 477) if mobile else (682, 263)
    body.append(text(legend_x - 42, legend_y + 10, "Less", 13 if mobile else 11, MUTED, True))
    for index, color in enumerate(COLORS):
        body.append(rect(legend_x + index * 18, legend_y, 10, 10, color, 1, "none"))
    body.append(text(legend_x + 94, legend_y + 10, "More", 13 if mobile else 11, MUTED, True))
    description = (f"{total} contributions in the last year, {active} active days, and {busiest} contributions on the busiest day. "
                   f"{period}. Updated {data['updated']} UTC. Generated from GitHub contribution data; not the native profile interface.")
    return svg(w, h, f"GitHub Activity — {data['username']}", "\n".join(body), description)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--username", default="TsmHabib03")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--github-cli", action="store_true")
    mode.add_argument("--render-snapshot", action="store_true",
                      help="Redraw the saved snapshot offline, preserving its reporting and update dates.")
    args = parser.parse_args()
    if args.render_snapshot:
        data = json.loads((ASSETS / "activity-data.json").read_text(encoding="utf-8"))
        if any(type(day["level"]) is not int or not 0 <= day["level"] < len(LEVELS) for day in data["days"]):
            raise ValueError("Invalid contribution level in saved snapshot.")
        # Apply the same integrity checks, relative to the recorded update date.
        calendar = {"totalContributions": data["total"], "weeks": [{"contributionDays": [
            {"date": day["date"], "contributionCount": day["count"], "contributionLevel": LEVELS[day["level"]]}
            for day in data["days"]]}]}
        normalize_calendar(calendar, date.fromisoformat(data["updated"]))
        write_assets({"github-activity.svg": render_activity(data), "github-activity-mobile.svg": render_activity(data, True)})
        print(f"Redrew the verified snapshot dated {data['updated']}; no data or dates changed.")
        return
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
