import streamlit as st
import srt
import datetime
import json
import os
from datetime import timedelta

st.set_page_config(page_title="Plot Hole Plotter", page_icon="🍿")
st.title("🍿 Plot Hole Plotter")
st.markdown("Find ideal break times in your movie using subtitle gaps (>30s).")

SUBTITLE_PATH = "subtitles/movie.srt"  # sample SRT file location

# Stop notifier
if st.button("🛑 Stop Notifications"):
    with open("stop.txt", "w") as f:
        f.write("stop")
    st.success("🛑 Notification script will stop.")

# Upload and analyze the sample subtitle
if st.button("📥 Upload Sample Subtitle"):
    if not os.path.exists(SUBTITLE_PATH):
        st.error(f"❌ Sample subtitle file not found at `{SUBTITLE_PATH}`.")
        st.stop()

    with open(SUBTITLE_PATH, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    try:
        subtitles = list(srt.parse(content))
    except Exception as e:
        st.error("❌ Could not parse subtitle file.")
        st.stop()

    gaps = []
    for i in range(1, len(subtitles)):
        prev_end = subtitles[i - 1].end
        curr_start = subtitles[i].start
        gap_duration = curr_start - prev_end

        if gap_duration.total_seconds() > 30:
            gaps.append({
                "start": prev_end,
                "duration": gap_duration
            })

    if not gaps:
        st.warning("😬 No low-activity scenes over 30 seconds found.")
    else:
        st.success(f"🎉 Found {len(gaps)} break opportunities!")

        st.write("📋 Break Schedule:")
        for g in gaps:
            mins = int(g["duration"].total_seconds() // 60)
            secs = int(g["duration"].total_seconds() % 60)
            st.markdown(f"- ⏱️ Start: `{g['start']}`, Duration: `{mins}m {secs}s`")

        break_times = []
        movie_start_time = datetime.datetime.now()

        for g in gaps:
            break_at = movie_start_time + g["start"]
            break_times.append({
                "time": break_at.strftime("%H:%M:%S"),
                "duration": int(g["duration"].total_seconds())
            })

        with open("break_schedule.json", "w") as f:
            json.dump(break_times, f, indent=2)

        if os.path.exists("stop.txt"):
            os.remove("stop.txt")

        st.success("✅ Break schedule saved. You can now run `notifier.py`.")
