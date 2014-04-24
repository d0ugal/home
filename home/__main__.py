from flask.ext.script import Server

from home import app, manager

@manager.option('--device', help='Serial device.')
def collect(device):
    "Start collecting data from the given serial device"
    from home.collect import run
    run(device)

manager.add_command("dashboard", Server(host='0.0.0.0', use_debugger=False,
    use_reloader=False))


def main():
    manager.run()

if __name__ == '__main__':
    main()
