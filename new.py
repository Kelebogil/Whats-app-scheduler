import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import pywhatkit
import datetime

# Function to schedule WhatsApp message
def schedule_msg():
    number = phone_entry.get().replace(" ", "")
    message = message_entry.get()

    if not number.startswith("+27"):
        messagebox.showerror("Invalid Number", "Please enter a valid +27 number")
        return

    if not message:
        messagebox.showerror("Empty Message", "Please enter a message")
        return

    # Get date and time from UI
    selected_date = date_entry.get_date()
    selected_hour = int(hour_combo.get())
    selected_minute = int(minute_combo.get())

    # Combine into datetime object
    run_time = datetime.datetime.combine(selected_date, datetime.time(selected_hour, selected_minute))

    # Check if it's in the future
    if run_time <= datetime.datetime.now():
        messagebox.showerror("Time Error", "Please choose a future time")
        return

    try:
        pywhatkit.sendwhatmsg(number, message, selected_hour, selected_minute, wait_time=20)
        messagebox.showinfo("Success", f"Message scheduled to {number} at {selected_hour}:{selected_minute:02d} on {selected_date.strftime('%Y-%m-%d')}")
    except Exception as e:
        messagebox.showerror("Error", str(e))


# GUI Setup
root = tk.Tk()
root.title("WhatsApp Message Scheduler")
root.geometry("400x300")

# Phone number input
tk.Label(root, text="Phone Number (+27...)").grid(row=0, column=0, padx=10, pady=10, sticky="e")
phone_entry = tk.Entry(root, width=25)
phone_entry.grid(row=0, column=1, padx=10)

# Message input
tk.Label(root, text="Message").grid(row=1, column=0, padx=10, pady=10, sticky="e")
message_entry = tk.Entry(root, width=25)
message_entry.grid(row=1, column=1, padx=10)

# Date picker
tk.Label(root, text="Date").grid(row=2, column=0, padx=10, pady=10, sticky="e")
date_entry = DateEntry(root, width=22, background='darkblue', foreground='white', borderwidth=2)
date_entry.grid(row=2, column=1, padx=10)

# Time picker (hour + minute dropdowns)
tk.Label(root, text="Time (HH:MM)").grid(row=3, column=0, padx=10, pady=10, sticky="e")

time_frame = tk.Frame(root)
time_frame.grid(row=3, column=1)

hour_combo = ttk.Combobox(time_frame, values=[f"{i:02d}" for i in range(24)], width=5)
hour_combo.current(12)
hour_combo.grid(row=0, column=0)

minute_combo = ttk.Combobox(time_frame, values=[f"{i:02d}" for i in range(60)], width=5)
minute_combo.current(0)
minute_combo.grid(row=0, column=1)

# Button
send_btn = tk.Button(root, text="Schedule Message", command=schedule_msg)
send_btn.grid(row=4, column=0, columnspan=2, pady=20)

root.mainloop()
