from moviepy.editor import concatenate_audioclips, AudioFileClip

count = 2
audio_clip_paths = ["testX4.mp3"]* count
clips = [AudioFileClip(c) for c in audio_clip_paths]
final_clip = concatenate_audioclips(clips)
final_clip.write_audiofile(f"testX{count}.mp3")