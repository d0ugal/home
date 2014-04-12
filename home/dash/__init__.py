from argparse import ArgumentParser

parser = ArgumentParser(description='.')
parser.add_argument('--debug', action='store_true')


def run():

    args = parser.parse_args()

    from home import app
    app.debug = args.debug

    try:
        from flask_debugtoolbar import DebugToolbarExtension
        DebugToolbarExtension(app)
    except ImportError:
        pass

    app.run(host='0.0.0.0')
