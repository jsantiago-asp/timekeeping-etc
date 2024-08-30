import time
import json
from datetime import datetime, date, timedelta
import tkinter as tk
from tkinter import messagebox, scrolledtext

# Load and save data functions
def load_data():
    try:
        with open('pomodoro_data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"daily_count": {}, "total_count": 0, "logs": []}

def save_data(data):
    with open('pomodoro_data.json', 'w') as f:
        json.dump(data, f, indent=4)

def format_log_entry(log_entry):
    dt = datetime.fromisoformat(log_entry["datetime"])
    start_time = dt.strftime("%H:%M:%S")
    end_time = (dt + timedelta(minutes=25)).strftime("%H:%M:%S")
    task = log_entry.get("task", "No task provided")
    notes = log_entry.get("notes", "No notes provided")
    return f"Date: {dt.date()}\nTask: {task}\nStart Time: {start_time}\nEnd Time: {end_time}\nNotes: {notes}\n"

# Main application class
class PomodoroApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.data = load_data()
        self.current_date = str(date.today())
        if self.current_date not in self.data["daily_count"]:
            self.data["daily_count"][self.current_date] = 0

        self.title("Pomodoro Timer")
        self.geometry("500x600")
        
        self.countdown_active = False
        self.countdown_start_time = None
        self.task = ""
        self.log_index = len(self.data["logs"]) - 1

        # GUI components
        self.create_widgets()
        self.update_log_display()

    def create_widgets(self):
        self.title_label = tk.Label(self, text="Pomodoro Timer", font=("Helvetica", 20))
        self.title_label.pack(pady=10)

        self.task_label = tk.Label(self, text="What do you plan to do?", font=("Helvetica", 12))
        self.task_label.pack()
        self.task_entry = tk.Entry(self, font=("Helvetica", 12))
        self.task_entry.pack(pady=5)

        self.timer_label = tk.Label(self, text="25:00", font=("Helvetica", 48))
        self.timer_label.pack(pady=20)

        self.start_button = tk.Button(self, text="Start", font=("Helvetica", 12), command=self.start_timer)
        self.start_button.pack(side="left", padx=10, pady=10)

        self.stop_button = tk.Button(self, text="Stop", font=("Helvetica", 12), command=self.stop_timer, state="disabled")
        self.stop_button.pack(side="left", padx=10, pady=10)

        self.reset_button = tk.Button(self, text="Reset", font=("Helvetica", 12), command=self.reset_timer)
        self.reset_button.pack(side="left", padx=10, pady=10)

        self.daily_label = tk.Label(self, text=f"Daily Pomodoros: {self.data['daily_count'][self.current_date]}", font=("Helvetica", 12))
        self.daily_label.pack(pady=10)

        self.alltime_label = tk.Label(self, text=f"All-time Pomodoros: {self.data['total_count']}", font=("Helvetica", 12))
        self.alltime_label.pack(pady=10)

        self.notes_label = tk.Label(self, text="Notes:", font=("Helvetica", 12))
        self.notes_label.pack(pady=5)

        self.notes_text = scrolledtext.ScrolledText(self, width=60, height=10, font=("Helvetica", 12))
        self.notes_text.pack(pady=10)

        self.logs_label = tk.Label(self, text="Previous Pomodoros:", font=("Helvetica", 12))
        self.logs_label.pack(pady=5)

        self.logs_display = tk.Label(self, text="", font=("Helvetica", 12), bg="white", justify="left")
        self.logs_display.pack(pady=10)

        self.prev_button = tk.Button(self, text="Previous", font=("Helvetica", 12), command=self.prev_log)
        self.prev_button.pack(side="left", padx=10, pady=10)

        self.next_button = tk.Button(self, text="Next", font=("Helvetica", 12), command=self.next_log)
        self.next_button.pack(side="left", padx=10, pady=10)

    def start_timer(self):
        task = self.task_entry.get()
        if not task:
            messagebox.showwarning("Input Error", "Please enter a task!")
            return
        messagebox.showinfo("Starting Task", f"Starting task: {task}")
        self.countdown_active = True
        self.countdown_start_time = time.time()
        self.task_entry.config(state="disabled")
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.task = task
        self.update_timer()

    def stop_timer(self):
        messagebox.showinfo("Stopping Task", f"Stopping task: {self.task}")
        self.countdown_active = False
        self.task_entry.config(state="normal")
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")

    def reset_timer(self):
        messagebox.showinfo("Reset Timer", "Resetting timer")
        self.countdown_active = False
        self.timer_label.config(text="25:00")
        self.task_entry.config(state="normal")
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")

    def update_timer(self):
        if self.countdown_active:
            elapsed_time = time.time() - self.countdown_start_time
            remaining_time = max(0, 25 * 60 - elapsed_time)
            mins, secs = divmod(remaining_time, 60)
            timeformat = '{:02d}:{:02d}'.format(int(mins), int(secs))
            self.timer_label.config(text=timeformat)
            if remaining_time <= 0:
                self.complete_pomodoro()
            else:
                self.after(1000, self.update_timer)

    def complete_pomodoro(self):
        self.countdown_active = False
        notes = self.notes_text.get("1.0", "end-1c")
        self.data["daily_count"][self.current_date] += 1
        self.data["total_count"] += 1
        log_entry = {
            "task": self.task,
            "datetime": datetime.now().isoformat(),
            "notes": notes
        }
        self.data["logs"].append(log_entry)
        save_data(self.data)
        self.daily_label.config(text=f"Daily Pomodoros: {self.data['daily_count'][self.current_date]}")
        self.alltime_label.config(text=f"All-time Pomodoros: {self.data['total_count']}")
        self.task_entry.delete(0, tk.END)
        self.task_entry.config(state="normal")
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.notes_text.delete("1.0", tk.END)
        self.log_index = len(self.data["logs"]) - 1
        self.update_log_display()
        messagebox.showinfo("Pomodoro Completed", f"Pomodoro completed! Task: {self.task}")

    def update_log_display(self):
        if self.data["logs"]:
            log_entry = self.data["logs"][self.log_index]
            self.logs_display.config(text=format_log_entry(log_entry))
        else:
            self.logs_display.config(text="No Pomodoros logged yet.")

    def prev_log(self):
        if self.log_index > 0:
            self.log_index -= 1
            self.update_log_display()

    def next_log(self):
        if self.log_index < len(self.data["logs"]) - 1:
            self.log_index += 1
            self.update_log_display()

# Run the application
if __name__ == "__main__":
    app = PomodoroApp()
    app.mainloop()
