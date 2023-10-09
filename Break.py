import pystray
from PIL import Image
import threading
import time

from playsound import playsound

# Load an image for the icon
image = Image.open("coffee.png")

# Variable to control the main loop
running = True

# Default interval for break reminders in seconds
default_interval = 45 * 60

# Current interval (can be changed by the user)
interval = 45

# Path to the audio file to be played as a reminder
audio_file_path = "water.mp3"

# Function to exit the application
def exit():
    global running
    running = False
    icon.stop()

# Function to show a notification
def show(icon, query):
    show_notification("hi")

# Function to set a new break interval (in minutes) via a dialog box
def setInterval():
    global interval
    global default_interval
    from tkinter import simpledialog
    minutes = simpledialog.askinteger("Set Interval", "Enter minutes:")
    if minutes is None or minutes < 1:
        minutes = 1
    seconds = minutes * 60
    default_interval = seconds
    interval = seconds

# Function to update the icon's title
def update_icon_title(new_title):
    icon.title = new_title

# Create the system tray icon with a menu
icon = pystray.Icon("Break", image, "Break", menu=pystray.Menu(
    pystray.MenuItem("Change minute break", setInterval),
    pystray.MenuItem("Exit", exit)))
update_icon_title("Break")

# Function to show a notification with a message and title
def show_notification(message, title):
    icon.notify(message, title)

# Function to convert seconds to a time format (HH:MM:SS)
def convertSecToTimeFormat(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"

# Function to send reminders at specified intervals
def remindering():
    global interval
    while running:
        interval = default_interval
        show_notification(f"Next break in {convertSecToTimeFormat(interval)}", "Take a break now!")
        playsound(audio_file_path)  # Play an audio reminder
        while interval > 0:
            title = f"{convertSecToTimeFormat(interval)} until break"
            update_icon_title(title)
            time.sleep(5)  # Wait for 5 seconds
            interval -= 5
        update_icon_title("Take a break!")

# Create a new thread to run the remindering() function
thread = threading.Thread(target=remindering)
# Start the thread
thread.start()

# Run the system tray icon application
icon.run()
