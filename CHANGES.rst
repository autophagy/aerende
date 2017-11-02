=========
Changelog
=========

Unreleased
----------

* Changed the data options category in the configuration file from ``data_path``
  to ``data_options``.

* Fixed bug where aerende would crash if the directory structure for the config
  file existed, but the `config.yml` file was missing.

* Added super increment and decrement, which increases/decreases a note's
  priority by 10.

* Stripped whitespace from note text returned from editor.

* Added an explanatory banner to the beginning of the default configuration.

29 Hærfest 226 :: 0.1.1
-----------------------

First release of ærende ! 🎉🎉🎉

Includes the ability to create, update and delete notes. Also includes the
ability to increment and decrement a note's priority, which affects sorting
and colouration.
