import sounddevice as sd
import soundfile as sf

SAMPLE_RATE = 16000

def record_audio(duration=5):

    print("\nSpeak now...")

    audio = sd.rec(
        int(duration * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1
    )

    sd.wait()

    sf.write("audio.wav", audio, SAMPLE_RATE)

    print("Saved audio.wav")


if __name__ == "__main__":
    record_audio()