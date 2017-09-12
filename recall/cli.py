from os import path, makedirs
import argparse
import yaml
from shutil import copy

def parse_args():
    parser = argparse.ArgumentParser(description='recall')
    parser.add_argument('-c', '--config', default='~/.recall/config.yml',
                        help='The recall config file')
    return parser.parse_args()


def get_config(file):
    expanded_path = path.expanduser(file)
    if not path.exists(expanded_path):
        makedirs(path.dirname(expanded_path))
        copy(path.join(path.dirname(__file__), 'config/default.yml'), expanded_path)

    with open(expanded_path, 'r') as config_file:
        return yaml.load(config_file)


def main():
    args = parse_args()
    config = get_config(args.config)


if __name__ == '__main__':
    main()
