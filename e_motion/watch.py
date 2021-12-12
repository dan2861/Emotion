import os
import random

from flask import Blueprint
from flask import current_app
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

from e_motion.auth import login_required

from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from e_motion.db import get_db

bp = Blueprint("watch", __name__)

def get_all_videos(db):
    # Fetch all rows from the video table.
    videos = db.execute(
        "SELECT id, url, title, description, type"
        " FROM video"
    ).fetchall()
    return videos

def get_my_videos(db, user_id):
    # Fetch all rows from the video table.
    videos = db.execute(
        "SELECT id, url, title, description, type"
        " FROM video WHERE uploader_id = ?", (user_id,)
    ).fetchall()
    return videos

@bp.route("/")
def index():
    """Populate the relevant video files for the current user."""
    db = get_db()
    # Get all videos in the system.
    all_videos = get_all_videos(db)
    random.shuffle(all_videos)

    # Get my videos if logged in.
    if g.user:
        my_videos = get_my_videos(db, user_id=g.user['id'])
    else:
        my_videos = []
    recent_videos = []
    return render_template("index.html",
    	my_vids=my_videos,
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

    # We only store watchevent for logged in user.
    if user_id:
        db = get_db()
        db.execute(
            'INSERT INTO watchevent (viewer_id, video_id)'
            ' VALUES (?, ?)', (user_id, videoid)
        )
        db.commit()
    return ""


# Src: https://flask.palletsprojects.com/en/2.0.x/patterns/fileuploads/
ALLOWED_EXTENSIONS = ['mp4']
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Converts youtube watch url to embed link.
def get_embed_link(watch_url):
    return watch_url.replace("watch?v=", 'embed/')

# Insert video metadata into database.
def insert_video(db, uploader_id, title, description, url, video_type):
    db.execute(
        'INSERT INTO video (uploader_id, title, description, url, type)'
        ' VALUES (?, ?, ?, ?, ?)',
        (uploader_id, title, description, url, video_type)
    )
    db.commit()

@bp.route("/upload", methods=("GET", "POST"))
@login_required
def upload():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        embedlink = get_embed_link(request.form['embedlink'])

        if embedlink:
            # Insert metadata into db.
            insert_video(get_db(), g.user['id'], title, description, url=embedlink, video_type="embed")
            flash('Upload Successful')
            return redirect(url_for('watch.upload'))

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('Select a File or an Embed Link')
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash('Only mp4 files supported.')
            return redirect(request.url)

        # Save file in the saved directory.
        if file:
            filename = secure_filename(file.filename)

            # Upload File
            upload_folder = current_app.config['UPLOAD_FOLDER']
            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)

            # Insert metadata into db.
            video_folder = current_app.config['UPLOADED_ASSETS']
            videopath = os.path.join(video_folder, filename)
            videourl = url_for('static', filename=videopath)
            insert_video(get_db(), g.user['id'], title, description, url=videourl, video_type="mp4")

            flash('Upload Successful')
            return redirect(url_for('watch.upload'))

    return render_template("upload.html")