import os
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='recall')
    parser.add_argument('-d', '--data', default='~/.recall/data.yml',
                        help='The recall data yaml')
    return parser.parse_args()


def validate_data_path(file):
    expanded_path = os.path.expanduser(file)
    os.makedirs(os.path.dirname(expanded_path), exist_ok=True)


def main():
    args = parse_args()
    validate_data_path(args.data)


if __name__ == '__main__':
    main()
