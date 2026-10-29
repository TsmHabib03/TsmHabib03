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
from profile_theme import ASSETS, NAVY, BORDER, WHITE, MUTED, BLUE, CYAN, text, rect, frame, svg, write_assets

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
COLORS = ["#292E42", "#3D527C", "#577BC0", "#7AA2F7", "#7DCFFF"]


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
    # GitHub pads the beginning of the rolling year to a calendar week.
    # A valid response can therefore contain up to 372 consecutive dates.
    if not 365 <= len(days) <= 372:
        raise ValueError("Expected a complete rolling-year calendar.")
    dates = [date.fromisoformat(d["date"]) for d in days]
    if any(b - a != timedelta(days=1) for a, b in zip(dates, dates[1:])):
        raise ValueError("Calendar contains duplicate or missing dates.")
    if abs((dates[-1] - today).days) > 1:
        raise ValueError("GitHub returned a stale calendar.")
    try:
        year_start = dates[-1].replace(year=dates[-1].year - 1)
    except ValueError:  # Feb 29 has no counterpart in a non-leap year.
        year_start = dates[-1].replace(year=dates[-1].year - 1, day=28)
    padded_start = year_start - timedelta(days=(year_start.weekday() + 1) % 7)
    if not padded_start <= dates[0] <= year_start + timedelta(days=1):
        raise ValueError("Expected a complete rolling-year calendar with week padding.")
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
                                   COLORS[day["level"]], 0, "none") + "</g>")
    for offset, month in labels:
        body.append(text(x + offset, y - 13, month, 15 if mobile else 12, MUTED, True))
    for row, label in [(1, "Mon"), (3, "Wed"), (5, "Fri")]:
        body.append(text(x - 40, y + row * step + 10, label, 13 if mobile else 11, MUTED, True))
    return "\n".join(body)


def render_activity(data, mobile=False):
    w, h = (480, 470) if mobile else (840, 282)
    total = data["total"]
    active = sum(day["count"] > 0 for day in data["days"])
    busiest = max(day["count"] for day in data["days"])
    body = [frame(w, h)]
    positions = (24, 196, 354) if mobile else (24, 310, 596)
    for x, value, label, color in zip(
            positions, (total, active, busiest),
            ("Contributions", "Active days", "Busiest day"), (WHITE, CYAN, BLUE)):
        body += [text(x, 48, f"{value:,}", 32, color, True, weight=600),
                 text(x, 76, label, 17 if mobile else 16, MUTED)]
    body.append(f'<path d="M24 96H{w-24}" stroke="{BORDER}"/>')
    weeks = weeks_from_days(data["days"])
    if mobile:
        body += [calendar_grid(weeks[:27], 58, 134, 14, True),
                 calendar_grid(weeks[27:], 58, 292, 14, True)]
    else:
        body.append(calendar_grid(weeks, 64, 130, 14))
    period = f'{data["days"][0]["date"]} to {data["days"][-1]["date"]}'
    body += [text(24, 409 if mobile else 247, period, 17 if mobile else 14, MUTED),
             text(24, 438 if mobile else 270,
                  f'Updated {data["updated"]} UTC', 17 if mobile else 13, MUTED)]
    legend_x, legend_y = (326, 428) if mobile else (692, 253)
    # Use the same five discrete colors as the data cells.
    body.append(text(legend_x - 42, legend_y + 12, "Less", 14 if mobile else 12, MUTED))
    for index, color in enumerate(COLORS):
        body.append(rect(legend_x + index * 17, legend_y, 12, 12, color, 0, "none"))
    body.append(text(legend_x + 90, legend_y + 12, "More", 14 if mobile else 12, MUTED))
    description = (f"{total} contributions, {active} active days, and {busiest} contributions on the busiest day. "
                   f"{period}. Updated {data['updated']} UTC. "
                   "Dated snapshot from GitHub contribution data, including calendar week padding.")
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
