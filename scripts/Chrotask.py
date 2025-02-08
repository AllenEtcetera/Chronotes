import random
import time
import tkinter as tk
from tkinter import messagebox,ttk
import tkcalendar as tkc

def set_reminder():
    rootRemind.withdraw()
    # Convert strings to time
    time_str = f"{hour_var.get()}:{min_var.get()} {ampm_var.get()}"
    deadline_str = f"{date_entry.get()} {time_str}"
    deadline = time.mktime(time.strptime(deadline_str, "%m/%d/%Y %I:%M %p"))
    # Set up reminder
    reminder(deadline,task_entry.get())

def reminder(deadline, task):
    deadline_text = time.strftime("%B %d, %H:%M", time.localtime(deadline))
    msg = f"{task} @ {deadline_text}"
    msg_now = f"Deadline reached: {task} now if not done already."
    while True:
        time_diff = deadline - time.time()
        interval = random.uniform((time_diff/8), (time_diff/2))
        print(f"Reminder will occur on {time.strftime("%B %d, %H:%M", time.localtime(time.time()+interval))}")
        time.sleep(interval)

        show_reminder(msg,True)

        if time.time() >= deadline:
            show_reminder(msg_now,False)
            break
    rootRemind.deiconify()

def show_reminder(msg,keep_reminding):
    if keep_reminding == True:
        # If Cancel, explode quietly
        if not messagebox.askokcancel("Reminder!", msg):
            rootRemind.destroy()
    else:
        messagebox.showwarning("Do ASAP",msg)
rootRemind = tk.Tk()
rootRemind.title("Chrotask")
task_label = tk.Label(rootRemind, text="To do:")
task_entry = tk.Entry(rootRemind)

date_label = tk.Label(rootRemind, text="Due Date:")
date_entry = tkc.DateEntry(rootRemind, date_pattern="mm/dd/yyyy")

hour_var = tk.StringVar(value="01")
min_var = tk.StringVar(value="00")
ampm_var = tk.StringVar(value="AM")

hour_label = tk.Label(rootRemind, text="Due Time:")
hour_combo = ttk.Combobox(rootRemind, textvariable=hour_var, values=[f"{i:02}" for i in range(1, 13)], width=5)
min_combo = ttk.Combobox(rootRemind, textvariable=min_var, values=[f"{i*5:02}" for i in range(12)], width=5)
ampm_combo = ttk.Combobox(rootRemind, textvariable=ampm_var, values=["AM", "PM"], width=5)

remind_button = tk.Button(rootRemind, text="Set Reminder", command=set_reminder)

task_label.pack()
task_entry.pack()
date_label.pack()
date_entry.pack()
hour_label.pack()
hour_combo.pack()
min_combo.pack()
ampm_combo.pack()
remind_button.pack()

rootRemind.mainloop()