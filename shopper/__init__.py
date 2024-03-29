import os

from flask import Flask


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that is overridden by instance config
        SECRET_KEY='dev',
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, 'shopper.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/s3cr3t')
    def hello():
        return 'Hello, hacker!'

    # register the database commands
    from shopper import db
    db.init_app(app)

    # apply the blueprints to the app
    from shopper import auth, main
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)

    # make url_for('index') == url_for('list.index')
    app.add_url_rule('/', endpoint='index')

    return app
