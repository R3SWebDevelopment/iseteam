# Return youtube video id
def get_youtube_id(url):
    return url.split("v=")[1]