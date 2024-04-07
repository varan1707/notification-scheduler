import tkinter as tk
from tkinter import messagebox, ttk
from plyer import notification
import schedule
import threading
import time

class NotificationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Notification App")

        self.label_message = tk.Label(root, text="Enter notification message:")
        self.label_message.pack()

        self.entry_message = tk.Entry(root)
        self.entry_message.pack()

        self.label_time = tk.Label(root, text="Set notification time (HH:MM):")
        self.label_time.pack()

        self.entry_time = tk.Entry(root)
        self.entry_time.pack()

        self.schedule_button = tk.Button(root, text="Schedule Notification", command=self.schedule_notification)
        self.schedule_button.pack()

    def schedule_notification(self):
        message = self.entry_message.get()
        time_str = self.entry_time.get()

        if not message:
            messagebox.showwarning("Warning", "Please enter a message!")
            return

        if not time_str:
            messagebox.showwarning("Warning", "Please enter a time!")
            return

        try:
            hour, minute = map(int, time_str.split(':'))
        except ValueError:
            messagebox.showwarning("Warning", "Invalid time format! Please use HH:MM.")
            return

        if not (0 <= hour < 24) or not (0 <= minute < 60):
            messagebox.showwarning("Warning", "Invalid time! Please enter a valid time.")
            return

        schedule.every().day.at(f"{hour:02d}:{minute:02d}").do(lambda: self.send_notification(message))
        messagebox.showinfo("Success", "Notification scheduled!")
        self.close_window()

    def send_notification(self, message):
        notification.notify(
            title="Notification",
            message=message,
            timeout=10
        )

    def close_window(self):
        self.root.destroy()

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    root = tk.Tk()
    app = NotificationApp(root)
    threading.Thread(target=run_schedule).start()
    root.mainloop()
