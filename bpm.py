import asyncio
import sounddevice as sd
import numpy as np
import librosa
from aalink import Link
from collections import deque

# Configuration
SAMPLE_RATE = 44100
BUFFER_SIZE = 1024
WINDOW_DURATION = 5  # seconds for tempo analysis
BPM_SMOOTHING = 5  # Number of BPM readings to average for smoothing

# Real-time buffer and Ableton Link initialization
audio_buffer = deque(maxlen=int(WINDOW_DURATION * SAMPLE_RATE))

def audio_callback(indata, frames, time, status):
    """Callback to handle incoming audio stream."""
    if status:
        print(f"Audio stream status: {status}")
    audio_buffer.extend(indata[:, 0])  # Assuming mono input

def detect_bpm():
    """Analyze the current buffer and detect the BPM."""
    if len(audio_buffer) < SAMPLE_RATE:
        return None  # Not enough data to analyze

    # Convert buffer to numpy array
    audio_array = np.array(audio_buffer, dtype=np.float32)
    audio_array /= np.max(np.abs(audio_array))  # Normalize

    # Estimate tempo using librosa
    onset_env = librosa.onset.onset_strength(y=audio_array, sr=SAMPLE_RATE)
    tempo, _ = librosa.beat.beat_track(onset_envelope=onset_env, sr=SAMPLE_RATE)
    return tempo

async def update_link_bpm(link):
    """Asynchronously update Ableton Link BPM."""
    bpm_history = deque(maxlen=BPM_SMOOTHING)
    print("Starting Ableton Link BPM synchronization...")
    
    while True:
        bpm = detect_bpm()
        if bpm:
            bpm_history.append(bpm)
            smoothed_bpm = np.mean(bpm_history)

            # Update aalink BPM
            #link.bpm = smoothed_bpm
            #smoothed_bpm = int(smoothed_bpm)
            link.tempo = smoothed_bpm
            print(f"Updated Ableton Link BPM: {smoothed_bpm:.2f}")

        #await asyncio.sleep(0.1)  # Small delay to avoid high CPU usage
        await link.sync(1)

async def main():
    """Main asynchronous function to handle audio and Link BPM updates."""
    
    # list all available device
    devices = sd.query_devices()
    print("List of available devices:")
    print(devices)
    
    #get the device number
    selected_device = input("Enter the number of selected input device: ")
    selected_device = int(selected_device)
    sd.default.device = selected_device
    device_info = sd.query_devices(selected_device, 'input')
    print(device_info)
    
    print("Starting real-time BPM detection...")
    loop = asyncio.get_running_loop()
    link = Link(120, loop)  # Default BPM
    link.enabled = True
    await link.sync(1)
    print('bang!')
    # Open the audio input stream
    with sd.InputStream(callback=audio_callback, channels=1, samplerate=SAMPLE_RATE, blocksize=BUFFER_SIZE):
        try:
            await update_link_bpm(link)
        except KeyboardInterrupt:
            print("Stopping BPM detection...")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
