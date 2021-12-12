from flask import Blueprint
from flask import current_app
from flask import g
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.exceptions import abort

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

@bp.route("/watchevent", methods = ['POST'])
def watchevent():
    """Route for receiving video watch events"""

    user_id = session.get("user_id")
    videoidraw = request.form["videoid"]

    if not videoidraw:
        abort(400, 'videoid not found in form')

    # Extract Video Id
    videoid = int(videoidraw[len('videowithid'):])
    current_app.logger.info('video id: '+ str(videoid))

    # We only store watchevent for logged in user.
    if user_id is None:
        current_app.logger.info('No user logged in')
    else:
        current_app.logger.info('Logged in user ' + str(user_id))
    return ""

@bp.route("/upload")
def upload():
    return render_template("upload.html")