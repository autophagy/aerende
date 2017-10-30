.. _configuration:

Configuration
=============

The configuration file for ærende is located in `~/.andgeloman/aerende/config.yml`.

Data Path Options
-----------------

========= ========================== ==============================
Option    Description                Default
========= ========================== ==============================
data_path Path to note data yml file ~/.andgeloman/aerende/data.yml
========= ========================== ==============================

Key Binding Options
-------------------

=============================== ================================= ===============
Option                          Description                       Default
=============================== ================================= ===============
next_note                       Move the note focus down the list ``j``, ``down``
previous_note                   Move the note focus up the list   ``k``, ``up``
new_note                        Create a new note                 ``n``
edit_note                       Edit the focused note             ``e``
delete_note                     Delete the focused note           ``d``
increment_note_priority         Increment the focused note's      ``+``
                                priority.
super_increment_note_priority   Increment the focused note's      ``meta +``
                                priority by 10.
decrement_note_priority         Decrement the focused note's      ``-``
                                priority.
super_decrement_note_priority   Increment the focused note's      ``meta -``
                                priority by 10.
=============================== ================================= ===============

Palette Options
---------------

Palette options are in the form of::

    palette_name:
      - foreground
      - background


============== ============================= ==============================
Option         Description                   Default
============== ============================= ==============================
status_bar     Palette for the status bar    black, white
edit_bar       Palette for the note metadata black, light red
               edit bar.
highlight_note Palette for the currently     light blue, default
               focused note.
high_priority  Palette for a high priority   light red, default
               (>= 10) note.
============== ============================= ==============================
