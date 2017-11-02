# -*- coding: utf-8 -*-

"""
aerende.configuration
------------------

This module contains the configuration logic for aerende. This includes the
logic for loading a config file, writing a config file none is present, and
the loading of default configuration options.

There are 3 seperate configuration categories, at the moment. They are:

palette   :: defines the colour palettes used various elements.
data_options :: defines settings for aerende's data
key_bindings :: defaults the key bindings for aerende
"""

from os import path, makedirs
import yaml


class Configuration(object):

    # Default Configuration Options

    # Default options for the palettes
    # For more information on valid palette settings, see:
    # http://urwid.org/manual/displayattributes.html#standard-foreground-colors
    # status_bar :: the palette for the status bar at the bottom
    # edit_bar :: the palette for the note editing bar
    # highlight_note :: the palette for the currently focused note
    # high_priority :: the palette for any high priority (>= 10) note

    DEFAULT_PALETTE = {
        'status_bar': ['black', 'white'],
        'edit_bar': ['black', 'light red'],
        'highlight_note': ['light blue', 'default'],
        'high_priority': ['light red', 'default']
    }

    # Default options for the data options.
    # data_path :: path to the aerende YAML data file

    DEFAULT_DATA_OPTIONS = {
        'data_path': '~/.andgeloman/aerende/data.yml'
    }

    # Default key bindings
    # new_note :: key to create a new note
    # delete_note :: key to delete the focused note
    # edit_note :: key to edit the focused note
    # increment_note_priority :: key to increment the focused note's priority
    # super_increment_note_priorty :: as above, but by +10
    # decrement_note_priority :: key to decrement the focused note's priority
    # super_decrement_note_priority :: as above, but by -10
    # quit :: key to exit aerende
    # next_note :: focus the next note
    # previous_note :: focus the previous note

    DEFAULT_KEY_BINDINGS = {
        'new_note': 'n',
        'delete_note': 'd',
        'edit_note': 'e',
        'increment_note_priority': '+',
        'super_increment_note_priority': 'meta +',
        'decrement_note_priority': '-',
        'super_decrement_note_priority': 'meta -',
        'quit': 'q',
        'next_note': ['j', 'down'],
        'previous_note': ['k', 'up']
    }

    DEFAULT_CONFIG = {
        'palette': DEFAULT_PALETTE,
        'data_options': DEFAULT_DATA_OPTIONS,
        'key_bindings': DEFAULT_KEY_BINDINGS
    }

    # Banner to prepend to the default configuration if it does not exist.

    CONFIG_BANNER = """# Aerende :: Configuration File
#
# Please see
# https://aerende.readthedocs.io/en/latest/usage/configuration.html for a
# complete reference of configuration options, as well as their effects.

"""

    def __init__(self, configuration_path):
        """ On initialisation, preload the configuration options from the
        defaults.
        """
        self.palette = self.DEFAULT_PALETTE
        self.data_path = self.DEFAULT_DATA_OPTIONS
        self.key_bindings = self.DEFAULT_KEY_BINDINGS
        self.__load_configuration(configuration_path)

    def __load_configuration(self, configuration_path):
        """ Load the configuration from the supplied path. If the file does
        not exist at this path, create it from the default config settings.
        """
        expanded_path = path.expanduser(configuration_path)
        if not path.exists(path.dirname(expanded_path)):
            makedirs(path.dirname(expanded_path))

        if not path.exists(expanded_path):
            with open(expanded_path, 'w') as config_file:
                config_file.write(self.CONFIG_BANNER)
                yaml.dump(self.DEFAULT_CONFIG, config_file,
                          default_flow_style=False)
            self.palette = self.DEFAULT_PALETTE
            self.data_path = self.DEFAULT_DATA_OPTIONS
            self.key_bindings = self.DEFAULT_KEY_BINDINGS
        else:
            self.__load_configuration_values(expanded_path)

    def __load_configuration_values(self, path):
        """ Load the configuration file, update the config values from this
        file.
        """
        with open(path, 'r') as config_file:
            config_dict = yaml.load(config_file)

            config_variables = {
                'palette': self.palette,
                'data_options': self.data_path,
                'key_bindings': self.key_bindings
            }

            for key, value in config_variables.items():
                self.__update_configuration(key, config_dict, value)

    def __update_configuration(self, config_key, config_dict, var):
        """ Update a config dictionary given a category key
        """
        if config_key in config_dict:
            var.update(config_dict[config_key])

    def get_palette(self):
        return [[k] + v for k, v in self.palette.items()]

    def get_data_path(self):
        return self.data_path['data_path']

    def get_key_bindings(self):
        return self.key_bindings
