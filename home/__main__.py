from flask.ext.migrate import MigrateCommand
from flask.ext.script import Manager, Server, prompt_pass

from home import create_app, db
from home.collect.loop import collect as collect_loop
from home.dash.models import User

app = create_app()

manager = Manager(app, with_default_commands=False)

manager.add_command('db', MigrateCommand)
manager.add_command("dashboard", Server(host='0.0.0.0', use_debugger=False,
                    use_reloader=False))


@manager.option('--device', help='Serial device.')
def collect(device):
    "Start collecting data from the given serial device"
    collect_loop(device)


@manager.option('username', help='Username.')
def create_user(username):
    "Create a new user."
    password = prompt_pass("Enter password")
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()


def main():
    manager.run()

if __name__ == '__main__':
    main()
