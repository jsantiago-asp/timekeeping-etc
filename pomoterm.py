import time
import json
from datetime import datetime, date

def load_data():
    try:
        with open('pomodoro_data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"daily_count": {}, "total_count": 0, "logs": []}

def save_data(data):
    with open('pomodoro_data.json', 'w') as f:
        json.dump(data, f, indent=4)

def countdown(minutes):
    total_seconds = minutes * 60
    progress_length = 50  # Length of the progress bar
    interval = total_seconds / progress_length

    for i in range(progress_length):
        print('*' * (i + 1) + '-' * (progress_length - i - 1), end='\r')
        time.sleep(interval)

    print('*' * progress_length)  # Ensure full bar is shown when complete
    print("Time's up!")

def main():
    data = load_data()

    task = input("What do you plan to do? ")

    print("Starting 25 minute Pomodoro timer...")
    countdown(25)

    current_date = str(date.today())
    if current_date not in data["daily_count"]:
        data["daily_count"][current_date] = 0
    data["daily_count"][current_date] += 1
    data["total_count"] += 1

    log_entry = {
        "task": task,
        "datetime": datetime.now().isoformat()
    }
    data["logs"].append(log_entry)

    save_data(data)

    print(f"Pomodoro completed! Total for today: {data['daily_count'][current_date]}, Total all time: {data['total_count']}")

if __name__ == "__main__":
    main()