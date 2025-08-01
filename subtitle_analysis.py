# subtitle_analysis.py
import srt
from collections import defaultdict

def parse_subtitles(srt_content):
    subtitles = list(srt.parse(srt_content))
    minute_counts = defaultdict(int)

    for sub in subtitles:
        minute = sub.start.seconds // 60
        minute_counts[minute] += 1

    return subtitles, minute_counts
