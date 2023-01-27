import youtube_dl


def playlist(link):
    """
    Function take link as a parameter from post request and extract
    info from given link and return the list of playlist.
    
    return:-
        playlist_info contains the list of playlist of a course.
    """
    ydl = youtube_dl.YoutubeDL({"ignoreerrors": True, "quiet": True})
    with ydl:
        result = ydl.extract_info(
            link, download=False  # We just want to extract the info
        )
    playlist_info = []
    for video in result["entries"]:
        video_url = dict(
            (k, video[k])
            for k in ["title", "duration", "webpage_url"]
            if k in video
        )
        playlist_info.append(video_url.copy())
        
    return (playlist_info, result.get("title"))


def upload_course_excel_file(link):
    """
    Function take link as a parameter from excel file and extract
    info from given link and return the list of playlist.
    
    return:-
        playlist_info contains the list of playlist of a course.
    """
    ydl = youtube_dl.YoutubeDL({"ignoreerrors": True, "quiet": True})
    with ydl:
        result = ydl.extract_info(
            # We just want to extract the info
            link,
            download=False,
        )
    
    playlist_info = []
    for video in result["entries"]:
        video_url = dict(
            (k, video[k])
            for k in ["title", "duration", "webpage_url"]
            if k in video
        )
        playlist_info.append(video_url.copy())
    
    return (playlist_info, result.get("title"))


def watch_later_playlist_info(watch_later):
    """
    Function takes wacth_later as parameter and return the playlist
    to be added in watch_later section
    
    return:-
        playlist_info contains the title, duration, thumbnail, and webpage_url
    """
    playlist_info = []
    for item in watch_later:
        ydl = youtube_dl.YoutubeDL({"ignoreerrors": True, "quiet": True})
        with ydl:
            result = ydl.extract_info(
                item.link, download=False  # We just want to extract the info
            )
        video_url = dict(
            (k, result[k])
            for k in ["title", "duration", "webpage_url", "thumbnail"]
            if k in result
        )
        video_url["id"] = item.id
        playlist_info.append(video_url) 
        
    return playlist_info
