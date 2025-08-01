import json
import time
import datetime
import random
import os
from plyer import notification

# Function to stop notifications using a stop.txt file
def should_stop():
    return os.path.exists("stop.txt")

# Load break times
with open("break_schedule.json", "r") as f:
    break_times = json.load(f)

# ✅ Show initial notification
notification.notify(
    title="🍿 Plot Hole Plotter",
    message="import json
import time
import datetime
import random
import os
from plyer import notification

# Function to stop notifications using a stop.txt file
def should_stop():
    return os.path.exists("stop.txt")

# Load break times
with open("break_schedule.json", "r") as f:
    break_times = json.load(f)

# ✅ Show initial notification
notification.notify(
    title="🍿 Plot Hole Plotter",
    message="Notifier has begun! You'll get a joke at the right time.",
    timeout=5
)

print("✅ Notifier started. Waiting for break times...")

# Random jokes list
JOKES = [
    "Why don’t scientists trust atoms? Because they make up everything!",
    "What did the 0 say to the 8? Nice belt!",
    "Movie’s slow, but your snack game is strong.",
    "Don't worry, you’re not missing much.",
    "Perfect time to grab popcorn or pet your dog!",
    "This scene is like a filler episode—skip guilt-free!",
    "Even the movie fell asleep here!",
    "Use this moment to question your life choices... or make tea.",
    "Back in my day, we called this a bathroom intermission!"
]

sent_times = set()

while not should_stop():
    now = datetime.datetime.now().strftime("%H:%M:%S")
    for entry in break_times:
        if entry["time"] == now and entry["time"] not in sent_times:
            joke = random.choice(JOKES)
            notification.notify(
                title="🤣 Joke Time!",
                message=joke,
                timeout=10
            )
            print(f"🔔 Joke sent at {now}: {joke}")
            sent_times.add(entry["time"])
    time.sleep(1)
",
    timeout=5
)

print("c")

# Random jokes list
JOKES = [
    "Why don’t scientists trust atoms? Because they make up everything!",
    "What did the 0 say to the 8? Nice belt!",
    "Movie’s slow, but your snack game is strong.",
    "Don't worry, you’re not missing much.",
    "Perfect time to grab popcorn or pet your dog!",
    "This scene is like a filler episode—skip guilt-free!",
    "Even the movie fell asleep here!",
    "Use this moment to question your life choices... or make tea.",
    "Back in my day, we called this a bathroom intermission!"
]

sent_times = set()

while not should_stop():
    now = datetime.datetime.now().strftime("%H:%M:%S")
    for entry in break_times:
        if entry["time"] == now and entry["time"] not in sent_times:
            joke = random.choice(JOKES)
            notification.notify(
                title="🤣 Joke Time!",
                message=joke,
                timeout=10
            )
            print(f"🔔 Joke sent at {now}: {joke}")
            sent_times.add(entry["time"])
    time.sleep(1)
