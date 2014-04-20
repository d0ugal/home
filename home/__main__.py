from home import manager


@manager.option('--device', help='Serial device.')
def collect(device):
    "Start collecting data from the given serial device"
    from home.collect import run
    run(device)


def main():
    manager.run()

if __name__ == '__main__':
    main()
