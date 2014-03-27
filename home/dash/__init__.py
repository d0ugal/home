from home.dash.routes import app


def run():
    app.debug = True
    app.run(host='0.0.0.0')
