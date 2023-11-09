# Hey, this is Christian. Thanks for checking out my video. Hope this code helps you edit faster my friend. See ya.

# Libraries
# Video editing functions from moviepy.
from moviepy.editor import VideoFileClip, concatenate_videoclips
from pydub import AudioSegment  # Represents and manipulates audio clips.
# Detect non-silent parts in an audio segment.
from pydub.silence import detect_nonsilent
import tempfile  # Generate temporary files and directories.
import os  # Interface with the operating system, e.g., file operations.


def remove_silence_from_video(input_file,  # Path to the input video to be processed.
                              # Path where the processed video will be saved.
                              output_file,
                              # Threshold (in dB) below which audio is considered silent.
                              silence_thresh=-40.0,
                              # Minimum length (in ms) of silence to be considered for removal.
                              min_silence_len=500
                              ):

    BUFFER_TIME = 0.05  # in seconds, which is 50 milliseconds

    # Load video
    clip = VideoFileClip(input_file)

    # Save audio to a temporary file
    with tempfile.NamedTemporaryFile(delete=True) as temp_audio_file:
        temp_filename = temp_audio_file.name + ".wav"
        clip.audio.write_audiofile(temp_filename, codec='pcm_s16le')

        # Load audio from temporary file using pydub
        audio = AudioSegment.from_wav(temp_filename)

        # Delete temporary audio file
        os.remove(temp_filename)

    # Detect non-silent sections
    nonsilent_ranges = detect_nonsilent(
        audio, silence_thresh=silence_thresh, min_silence_len=min_silence_len)

    # Convert to time ranges in seconds with added buffer
    nonsilent_times = [(max(0, start / 1000.0 - BUFFER_TIME), min(clip.duration,
                        end / 1000.0 + BUFFER_TIME)) for start, end in nonsilent_ranges]

    # Cut out the silent sections from the video
    final_clip = concatenate_videoclips(
        [clip.subclip(start, end) for start, end in nonsilent_times])

    # Save the final video
    final_clip.write_videofile(
        output_file, codec="libx264", audio_codec="aac", audio_bitrate="256k")


# Usage:
remove_silence_from_video('b roll.mp4', 'output.mp4')
