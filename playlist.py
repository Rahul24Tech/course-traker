import youtube_dl

ydl = youtube_dl.YoutubeDL({"ignoreerrors": True, "quiet": True})

with ydl:
    result = ydl.extract_info(
        'https://www.youtube.com/watch?v=7wnove7K-ZQ&list=PLu0W_9lII9agwh1XjRt242xIpHhPT2llg',
        download=False # We just want to extract the info
    )

playlist_info = []

for video in result['entries']:
    video_url = dict((k, video[k]) for k in ['title', 'duration'] if k in video)
    playlist_info.append(video_url.copy())

print(playlist_info)
