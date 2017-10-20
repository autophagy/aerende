import argparse

from .controller import Controller
from .interface import AerendeInterface
from .configuration import Configuration


def parse_args():
    parser = argparse.ArgumentParser(description='aerende')
    parser.add_argument('-c', '--config',
                        default='~/.andgeloman/aerende/config.yml',
                        help='The aerende config file')
    return parser.parse_args()


def main():
    try:
        args = parse_args()
        config = Configuration(args.config)
        interface = AerendeInterface()

        Controller(config=config, interface=interface)
    except KeyboardInterrupt:
        exit(0)


if __name__ == '__main__':
    main()
