import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        name = 'e-motion',
        SECRET_KEY='dev',
        UPLOAD_FOLDER = 'e_motion/static/assets/uploaded_videos',
        UPLOADED_ASSETS = 'assets/uploaded_videos',
        DATABASE=os.path.join(app.instance_path, 'e-motion.sqlite'),
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # register the database commands
    from e_motion import db

    db.init_app(app)

    # apply the blueprints to the app
    from e_motion import auth, watch

    app.register_blueprint(auth.bp)
    app.register_blueprint(watch.bp)

    # make url_for('index') == url_for('watch.index')
    app.add_url_rule("/", endpoint="index")

    return app