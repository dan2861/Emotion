from flask import Blueprint
from flask import render_template
from flask import url_for

from e_motion.db import get_db

bp = Blueprint("watch", __name__)

@bp.route("/")
def index():
    """Populate the relevant video files for the current user."""
    # Use db once it is intialized
    # db = get_db()
    recent_videos = [
    	"https://www.youtube.com/embed/6hgVihWjK2c",
    	"https://player.vimeo.com/video/84910153?title=0&amp;byline=0&amp;portrait=0&amp;badge=0&amp;color=ffffff",
    	"https://www.youtube.com/embed/oiKj0Z_Xnjc",
    	# Local uploaded video
    	url_for('static', filename='assets/videos/video1.mp4'),
    	url_for('static', filename='assets/videos/video2.mp4'),
    	# TODO: If upload youtube link convert from watch to embed.
    	"https://www.youtube.com/embed/Dd7FixvoKBw",
    ]
    return render_template("index.html", recent_vids=recent_videos,title="Dani's Template", subtitle="The temppate Subtitle")