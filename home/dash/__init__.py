def run():
    from home import app
    app.debug = True
    app.run(host='0.0.0.0')
