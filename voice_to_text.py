import os
import pyaudio
import wave
from faster_whisper import WhisperModel
import datetime

def record_chunks(audio, stream, file_path, chunk_length=10):
    print("Recording...")
    frames = []
    
    num_frames = int(16000 / 1024 * chunk_length)
    for _ in range(num_frames):
        data = stream.read(1024)
        frames.append(data)

    with wave.open(file_path, 'wb') as sound_file:
        sound_file.setnchannels(1)  
        sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))  
        sound_file.setframerate(16000)  
        sound_file.writeframes(b''.join(frames))
    
    print("Recording complete.")

def transcribe_chunk(model, file_path):
    print(f"Transcribing: {file_path}")
    segments, _ = model.transcribe(file_path, beam_size=10)
    transcription = ' '.join(segment.text for segment in segments)
    return transcription

try:
    audio = pyaudio.PyAudio()
    
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, 
                        input=True, frames_per_buffer=1024)

    model_size = "large"  # Options: "base", "small", "medium", "large"
    model = WhisperModel(model_size, device="cuda", compute_type="float16")

    acc_transcription = ""
    
    while True:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        temp_file_path = f"temp_{timestamp}.wav"
        
        record_chunks(audio, stream, temp_file_path)
        
        transcription = transcribe_chunk(model, temp_file_path)
        print("Transcription:", transcription)
        
        os.remove(temp_file_path)
        
        acc_transcription += transcription + "\n"

except KeyboardInterrupt:
    print("Recording interrupted.")

finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    print("Done recording")
    print("Full transcription:\n", acc_transcription)

    with open(timestamp+".txt", "w", encoding="utf-8") as f:
        f.write(acc_transcription)
