import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_live_usd_high_impact_events():
    url = "https://www.forexfactory.com/calendar"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    events = []
    current_date = None

    for row in soup.select("tr.calendar__row"):
        impact = row.select_one("td.calendar__impact")
        if not impact or "high" not in impact.get("class", []):
            continue

        currency = row.select_one("td.calendar__currency")
        if not currency or currency.text.strip() != "USD":
            continue

        # Update current date if this row has it
        date_td = row.select_one("td.calendar__date")
        if date_td and date_td.text.strip():
            raw_date = date_td.text.strip()
            try:
                current_date = datetime.strptime(raw_date + " " + str(datetime.today().year), "%b %d %Y").strftime("%Y-%m-%d")
            except:
                pass

        if not current_date:
            continue

        time = row.select_one("td.calendar__time")
        event = row.select_one("td.calendar__event")
        forecast = row.select_one("td.calendar__forecast")

        events.append({
            "date": current_date,
            "time": time.text.strip(),
            "event": event.text.strip(),
            "impact": "High",
            "forecast": forecast.text.strip() or "N/A"
        })

    return events

def load_local_data():
    with open("data/usd-high-impact.json") as f:
        return json.load(f)

def save_updated_data(data):
    with open("data/usd-high-impact.json", "w") as f:
        json.dump(data, f, indent=2)

def compare_and_flag(local, live):
    live_set = {(e['date'], e['time'], e['event']) for e in live}
    updated = []

    for event in local:
        key = (event['date'], event['time'], event['event'])
        if key not in live_set:
            event['status'] = 'canceled'
        else:
            event['status'] = 'confirmed'
        updated.append(event)

    return updated

if __name__ == "__main__":
    print("🔎 Checking for canceled or changed events...")
    local_data = load_local_data()
    live_data = get_live_usd_high_impact_events()
    updated_data = compare_and_flag(local_data, live_data)
    save_updated_data(updated_data)
    print("✅ Done. Statuses updated.")
