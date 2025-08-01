# audio_analysis.py
import librosa
import numpy as np

def analyze_audio(file, frame_duration=60):
    """
    Analyze .mp3 audio file and return energy levels per minute.
    `file` can be a file path or a file-like object (BytesIO from Streamlit).
    """
    y, sr = librosa.load(file, sr=None)  # Supports mp3 directly if ffmpeg/audioread is set up
    duration = librosa.get_duration(y=y, sr=sr)
    total_minutes = int(duration // frame_duration)

    energy_per_minute = []
    for i in range(total_minutes):
        start = int(i * frame_duration * sr)
        end = int((i + 1) * frame_duration * sr)
        frame = y[start:end]
        energy = np.mean(np.abs(frame))
        energy_per_minute.append(energy)

    return energy_per_minute
