import time
import json
from datetime import datetime, date
import PySimpleGUI as sg

def load_data():
    try:
        with open('pomodoro_data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"daily_count": {}, "total_count": 0, "logs": []}

def save_data(data):
    with open('pomodoro_data.json', 'w') as f:
        json.dump(data, f, indent=4)

def main():
    data = load_data()
    current_date = str(date.today())

    if current_date not in data["daily_count"]:
        data["daily_count"][current_date] = 0

    sg.theme('Reddit')

    layout = [
        [sg.Text('Pomodoro Timer', size=(30, 1), justification='center', font='Helvetica 20')],
        [sg.Text('What do you plan to do?', font='Helvetica 12'), sg.InputText(key='-TASK-', font='Helvetica 12')],
        [sg.Text('25:00', size=(8, 1), font='Helvetica 48', justification='center', key='-TIMER-')],
        [sg.Button('Start', button_color=('white', 'red'), font='Helvetica 12')],
        [sg.Text('Daily Pomodoros:', size=(20, 1), font='Helvetica 12'), sg.Text(data["daily_count"][current_date], size=(5, 1), font='Helvetica 12', key='-DAILY-')],
        [sg.Text('All-time Pomodoros:', size=(20, 1), font='Helvetica 12'), sg.Text(data["total_count"], size=(5, 1), font='Helvetica 12', key='-ALLTIME-')],
        [sg.Output(size=(60, 10), font='Helvetica 12')]
    ]

    window = sg.Window('Pomodoro Timer', layout, element_justification='c')

    countdown_active = False
    countdown_start_time = None
    task = ""

    while True:
        event, values = window.read(timeout=100)
        if event == sg.WIN_CLOSED:
            break
        if event == 'Start' and not countdown_active:
            task = values['-TASK-']
            if not task:
                print("Please enter a task!")
                continue
            print(f"Starting task: {task}")
            countdown_active = True
            countdown_start_time = time.time()
            window['-TASK-'].update(disabled=True)
            window['Start'].update(disabled=True)
        if countdown_active:
            elapsed_time = time.time() - countdown_start_time
            remaining_time = max(0, 25 * 60 - elapsed_time)
            mins, secs = divmod(remaining_time, 60)
            timeformat = '{:02d}:{:02d}'.format(int(mins), int(secs))
            window['-TIMER-'].update(timeformat)
            if remaining_time <= 0:
                countdown_active = False
                data["daily_count"][current_date] += 1
                data["total_count"] += 1
                log_entry = {
                    "task": task,
                    "datetime": datetime.now().isoformat()
                }
                data["logs"].append(log_entry)
                save_data(data)
                window['-DAILY-'].update(data["daily_count"][current_date])
                window['-ALLTIME-'].update(data["total_count"])
                window['-TASK-'].update('', disabled=False)
                window['Start'].update(disabled=False)
                print(f"Pomodoro completed! Task: {task}")

    window.close()

if __name__ == "__main__":
    main()
