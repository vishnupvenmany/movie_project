import json
import time
from datetime import datetime
from plyer import notification
import os
import random

# Show startup notification
notification.notify(
    title="🍿 Plot Hole Plotter",
    message="Notifier has started!",
    timeout=5
)

# Load break schedule
with open("break_schedule.json", "r") as f:
    schedule = json.load(f)

# Track notified times
notified = set()

# Funny jokes to show
JOKES = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "Why did the scarecrow win an award? He was outstanding in his field.",
    "I'm on a seafood diet. I see food and I eat it.",
    "Parallel lines have so much in common… it's a shame they'll never meet.",
    "What do you call fake spaghetti? An impasta!",
    "Time to pause – your popcorn needs a break too!"
]

while True:
    if os.path.exists("stop.txt"):
        break

    now = datetime.now().strftime("%H:%M:%S")
    for b in schedule:
        if b["time"] == now and b["time"] not in notified:
            notified.add(b["time"])
            notification.notify(
                title="🍿 Break Time!",
                message=random.choice(JOKES),
                timeout=10
            )

    time.sleep(1)
