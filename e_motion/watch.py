from flask import Blueprint
from flask import render_template
from flask import url_for

from e_motion.db import get_db

bp = Blueprint("watch", __name__)

all_videos = [
    { 
        "id": 1,
    	"url" : "https://www.youtube.com/embed/6hgVihWjK2c",
    	"title" : "Radio Head Jonny Tom",
    	"description": "",
        "type" : "embed"
    },
    { 
        "id": 2,
    	"url" : "https://player.vimeo.com/video/84910153?title=0&amp;byline=0&amp;portrait=0&amp;badge=0&amp;color=ffffff",
    	"title" : "Kewti Animation",
    	"description": "This is deep kewti animation by dani",
        "type" : "embed"
    },
    { 
        "id": 3,
    	"url" : "https://www.youtube.com/embed/oiKj0Z_Xnjc",
    	"title" : "Stromae - Papouti",
    	"description": "",
        "type" : "embed"
    },
    # Local uploaded video
    {
        "id": 4, 
    	"url" : "/static/assets/videos/video1.mp4",
    	"title" : "Random Lady",
    	"description": "A nice video by random lady",
        "type" : "mp4"
    },
    { 
        "id": 5,
    	"url" : "/static/assets/videos/video2.mp4",
    	"title" : "Break Dancer",
    	"description": "",
        "type" : "mp4"
    },
    # TODO: If upload youtube link convert from watch to embed.
    { 
        "id": 6,
    	"url" : "https://www.youtube.com/embed/Dd7FixvoKBw",
    	"title" : "Blaaake!",
    	"description": "",
        "type" : "embed"
    },
]

recent_videos = [
    { 
        "id": 1,
    	"url" : "https://www.youtube.com/embed/6hgVihWjK2c",
    	"title" : "Radio Head Jonny Tom",
    	"description": "",
        "type" : "embed"
    },
    # Local uploaded video
    { 
        "id": 4,
    	"url" : "/static/assets/videos/video1.mp4",
    	"title" : "Random Lady",
    	"description": "A nice video by random lady",
        "type" : "mp4"
    },
    { 
        "id": 5,
    	"url" : "/static/assets/videos/video2.mp4",
    	"title" : "Break Dancer",
    	"description": "",
        "type" : "mp4"
    },
    # TODO: If upload youtube link convert from watch to embed.
    { 
        "id": 6,
    	"url" : "https://www.youtube.com/embed/Dd7FixvoKBw",
    	"title" : "Blaaake!",
    	"description": "",
        "type" : "embed"
    },
]

my_videos = [
    { 
    	"url" : "/static/assets/videos/video2.mp4",
    	"title" : "Break Dancer",
    	"description": "",
        "type" : "mp4"
    },
    # TODO: If upload youtube link convert from watch to embed.
    { 
    	"url" : "https://www.youtube.com/embed/Dd7FixvoKBw",
    	"title" : "Blaaake!",
    	"description": "",
        "type" : "embed"
    },
]

@bp.route("/")
def index():
    """Populate the relevant video files for the current user."""
    # Use db once it is intialized
    # db = get_db()
    
    return render_template("index.html",
    	my_vids=[],
    	all_vids = all_videos,
    	recent_vids=recent_videos)