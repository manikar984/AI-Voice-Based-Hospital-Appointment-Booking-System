import sounddevice as sd
import soundfile as sf
import numpy as np
import webrtcvad
import time


# ============================================================
# AUDIO SETTINGS
# ============================================================

SAMPLE_RATE = 16000

# WebRTC VAD supports 10, 20, or 30 ms frames.
FRAME_DURATION_MS = 20

FRAME_SIZE = int(
    SAMPLE_RATE * FRAME_DURATION_MS / 1000
)

# Maximum total recording duration
MAX_DURATION = 30

# Background noise calibration
NOISE_CALIBRATION_DURATION = 0.7

# RMS threshold
NOISE_MULTIPLIER = 3.0
MIN_THRESHOLD = 0.003

# ------------------------------------------------------------
# SPEECH / SILENCE SMOOTHING
# ------------------------------------------------------------

# Number of consecutive speech frames required
# before we consider speech to have started.
SPEECH_CONFIRMATION_FRAMES = 3

# Silence must continue for this long AFTER speech
# before recording stops.
SILENCE_DURATION = 2.0

SILENCE_FRAMES_REQUIRED = int(
    SILENCE_DURATION
    / (FRAME_DURATION_MS / 1000)
)


# ============================================================
# VAD
# ============================================================

vad = webrtcvad.Vad()

# 0 = least aggressive
# 3 = most aggressive
#
# Mode 2 is a good starting point for normal speech.
vad.set_mode(2)


# ============================================================
# RMS
# ============================================================

def calculate_rms(audio):
    """
    Calculate RMS using float32 audio.
    """

    audio = np.asarray(audio, dtype=np.float32)

    return float(
        np.sqrt(
            np.mean(
                np.square(audio)
            )
        )
    )


# ============================================================
# WEBRTC VAD
# ============================================================

def is_speech(audio):
    """
    WebRTC VAD expects:
        - 16-bit PCM
        - 16 kHz
        - 10/20/30 ms frame

    Our microphone gives float32 audio in approximately
    the range -1.0 to +1.0.

    Therefore convert float32 -> int16 only for VAD.
    """

    audio = np.asarray(
        audio,
        dtype=np.float32
    ).flatten()

    # Prevent clipping
    audio = np.clip(
        audio,
        -1.0,
        1.0
    )

    # Convert to signed 16-bit PCM
    pcm16 = (
        audio * 32767
    ).astype(
        np.int16
    )

    return vad.is_speech(
        pcm16.tobytes(),
        SAMPLE_RATE
    )


# ============================================================
# RECORD AUDIO
# ============================================================

def record_audio():

    print("\nListening for speech...")

    # --------------------------------------------------------
    # STEP 1: CALIBRATE BACKGROUND NOISE
    # --------------------------------------------------------

    noise_levels = []

    calibration_frames = int(
        NOISE_CALIBRATION_DURATION
        / (FRAME_DURATION_MS / 1000)
    )

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32",
        blocksize=FRAME_SIZE
    ) as stream:

        for _ in range(calibration_frames):

            audio, overflowed = stream.read(
                FRAME_SIZE
            )

            audio = audio[:, 0]

            rms = calculate_rms(audio)

            noise_levels.append(rms)

    # Median is more stable than maximum
    noise_floor = float(
        np.median(noise_levels)
    )

    threshold = max(
        noise_floor * NOISE_MULTIPLIER,
        MIN_THRESHOLD
    )

    print(
        f"Background RMS: {noise_floor:.5f}"
    )

    print(
        f"Speech RMS threshold: {threshold:.5f}"
    )

    print("Speak now...")

    # --------------------------------------------------------
    # STATE
    # --------------------------------------------------------

    audio_blocks = []

    speech_started = False

    consecutive_speech_frames = 0

    consecutive_silence_frames = 0

    recording_start_time = time.time()

    # --------------------------------------------------------
    # STEP 2: RECORD
    # --------------------------------------------------------

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32",
        blocksize=FRAME_SIZE
    ) as stream:

        while True:

            audio, overflowed = stream.read(
                FRAME_SIZE
            )

            audio = audio[:, 0]

            # Always save the frame
            audio_blocks.append(
                audio.copy()
            )

            # ------------------------------------------------
            # MEASURE AUDIO
            # ------------------------------------------------

            rms = calculate_rms(audio)

            vad_result = is_speech(audio)

            # We require BOTH:
            #
            # 1. WebRTC says speech
            # 2. Audio is above our RMS threshold
            #
            speech_frame = (
                vad_result
                and rms >= threshold
            )

            # ------------------------------------------------
            # SPEECH DETECTION
            # ------------------------------------------------

            if speech_frame:

                consecutive_speech_frames += 1

                # Any speech immediately cancels
                # the silence timer.
                consecutive_silence_frames = 0

            else:

                consecutive_speech_frames = 0

            # ------------------------------------------------
            # SPEECH START CONFIRMATION
            # ------------------------------------------------

            if (
                not speech_started
                and
                consecutive_speech_frames
                >= SPEECH_CONFIRMATION_FRAMES
            ):

                speech_started = True

                print(
                    "Speech detected..."
                )

                # Reset silence counter
                consecutive_silence_frames = 0

            # ------------------------------------------------
            # AFTER SPEECH HAS STARTED
            # ------------------------------------------------

            if speech_started:

                if speech_frame:

                    # User is speaking again.
                    #
                    # This is very important:
                    # even if there was a short pause,
                    # we continue recording.
                    consecutive_silence_frames = 0

                else:

                    consecutive_silence_frames += 1

                    # ------------------------------------------------
                    # LONG SILENCE DETECTION
                    # ------------------------------------------------

                    if (
                        consecutive_silence_frames
                        >= SILENCE_FRAMES_REQUIRED
                    ):

                        print(
                            "Speech ended."
                        )

                        break

            # ------------------------------------------------
            # MAXIMUM RECORDING TIME
            # ------------------------------------------------

            elapsed = (
                time.time()
                - recording_start_time
            )

            if elapsed >= MAX_DURATION:

                print(
                    "Maximum recording duration reached."
                )

                break

            # ------------------------------------------------
            # CONSOLE OUTPUT
            # ------------------------------------------------

            # Print only occasionally instead of flooding
            # the terminal with hundreds of lines.
            #
            # Every 10 frames = approximately 200 ms.
            if len(audio_blocks) % 10 == 0:

                state = (
                    "SPEECH"
                    if speech_frame
                    else "SILENCE"
                )

                if speech_started:

                    silence_seconds = (
                        consecutive_silence_frames
                        * FRAME_DURATION_MS
                        / 1000
                    )

                    print(
                        f"RMS: {rms:.5f} | "
                        f"VAD: {state} | "
                        f"Silence: {silence_seconds:.1f}s"
                    )

                else:

                    print(
                        f"RMS: {rms:.5f} | "
                        f"VAD: {state}"
                    )

    # --------------------------------------------------------
    # STEP 3: SAVE AUDIO
    # --------------------------------------------------------

    if not audio_blocks:

        print(
            "No audio captured."
        )

        return "audio.wav"

    audio_data = np.concatenate(
        audio_blocks,
        axis=0
    )

    sf.write(
        "audio.wav",
        audio_data,
        SAMPLE_RATE
    )

    print(
        "Saved audio.wav"
    )

    return "audio.wav"


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    record_audio()