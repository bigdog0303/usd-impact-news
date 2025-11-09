import json
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def scrape_usd_high_impact():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://www.forexfactory.com/calendar")
        time.sleep(5)  # wait for JS to load

        rows = driver.find_elements(By.CSS_SELECTOR, "tr.calendar__row")
        events = []
        current_date = ""

        for row in rows:
            classes = row.get_attribute("class")
            if "calendar__row--new-day" in classes:
                try:
                    date_cell = row.find_element(By.CSS_SELECTOR, "td.calendar__date")
                    raw = date_cell.text.strip()
                    dt = datetime.strptime(raw + " " + str(datetime.today().year), "%b %d %Y")
                    current_date = dt.strftime("%Y-%m-%d")
                except Exception:
                    pass
                continue

            impact_cell = row.find_element(By.CSS_SELECTOR, "td.calendar__impact")
            if "high" not in impact_cell.get_attribute("class").lower():
                continue

            currency = row.find_element(By.CSS_SELECTOR, "td.calendar__currency").text.strip()
            if currency != "USD":
                continue

            time_cell = row.find_element(By.CSS_SELECTOR, "td.calendar__time")
            event_cell = row.find_element(By.CSS_SELECTOR, "td.calendar__event")
            forecast_cell = row.find_element(By.CSS_SELECTOR, "td.calendar__forecast")

            events.append({
                "date": current_date or datetime.today().strftime("%Y-%m-%d"),
                "time": time_cell.text.strip(),
                "event": event_cell.text.strip(),
                "impact": "High",
                "forecast": forecast_cell.text.strip() or "N/A"
            })

        with open("data/usd-high-impact.json", "w") as f:
            json.dump(events, f, indent=2)

    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_usd_high_impact()
