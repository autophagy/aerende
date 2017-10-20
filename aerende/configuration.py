from os import path, makedirs
import yaml


class Configuration(object):

    DEFAULT_PALETTE = {
        'status_bar': ['black', 'white'],
        'edit_bar': ['black', 'light red'],
        'highlight_note': ['light blue', 'default'],
        'high_priority': ['light red', 'default']
    }

    DEFAULT_DATA_PATH = {
        'data_path': '~/.andgeloman/aerende/data.yml'
    }

    DEFAULT_KEY_BINDINGS = {
        'new_note': 'n',
        'delete_note': 'd',
        'edit_note': 'e',
        'increment_note_priority': '+',
        'decrement_note_priority': '-',
        'quit': 'q',
        'next_note': ['j', 'down'],
        'previous_note': ['k', 'up']
    }

    DEFAULT_CONFIG = {
        'palette': DEFAULT_PALETTE,
        'data_path': DEFAULT_DATA_PATH,
        'key_bindings': DEFAULT_KEY_BINDINGS
    }

    def __init__(self, configuration_path):
        self.__load_configuration(configuration_path)

    def __load_configuration(self, configuration_path):
        expanded_path = path.expanduser(configuration_path)
        if not path.exists(expanded_path):
            makedirs(path.dirname(expanded_path))
            with open(expanded_path, 'w') as config_file:
                yaml.dump(self.DEFAULT_CONFIG, config_file,
                          default_flow_style=False)
            self.palette = self.DEFAULT_PALETTE
            self.data_path = self.DEFAULT_DATA_PATH
            self.key_bindings = self.DEFAULT_KEY_BINDINGS
        else:
            self.__load_configuration_values(expanded_path)

    def __load_configuration_values(self, path):
        with open(path, 'r') as config_file:
            config_dict = yaml.load(config_file)
            if 'palette' in config_dict:
                self.palette = self.__validate_configuration(
                    'palette', config_dict, self.DEFAULT_PALETTE)
            else:
                self.palette = self.DEFAULT_PALETTE

            if 'data_path' in config_dict:
                self.data_path = self.__validate_configuration(
                    'data_path', config_dict, self.DEFAULT_DATA_PATH)
            else:
                self.data_path = self.DEFAULT_DATA_PATH

            if 'key_bindings' in config_dict:
                self.key_bindings = self.__validate_configuration(
                    'key_bindings', config_dict, self.DEFAULT_KEY_BINDINGS)
            else:
                self.key_bindings = self.DEFAULT_KEY_BINDINGS

    def __validate_configuration(self, config_key, config_dict, defaults):
        config_item = {}
        for key, default_value in defaults.items():
            if key in config_dict[config_key]:
                config_item[key] = config_dict[config_key][key]
            else:
                config_item[key] = default_value
        return config_item

    def get_palette(self):
        return [[k] + v for k, v in self.palette.items()]

    def get_data_path(self):
        return self.data_path['data_path']

    def get_key_bindings(self):
        return self.key_bindings
