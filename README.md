Alternative autocompletion
==========================

This plugin adds an autocompletion command to Sublime Text that acts similarly to TextMate:

* Hitting the autocomplete key will attempt to complete the current word by
  looking at similar words in the current document.
* Hitting the autocomplete key multiple times will cycle through the available
  words.
* The last autocomplete position is remembered, so you can perform an
  autocompletion, move the cursor around, move back to where you were, and
  continue cycling through the completions.
* Candidate completions are selected prioritized by distance to the cursor.

The plugin improves on TextMate in one respect: If no candidates are found, the
plugin reverts to using a simple fuzzy, case-sensitive matching algorithm that
is similar to Sublime's file/class matching algorithm. For example, typing
`AppC` might match `ApplicationController`.

Installation
------------

Using Package Control, install "AlternativeAutocompletion"  or clone this repo in your packages folder.

I recommended you add key bindings for the commands. I've included my preferred bindings below.
Copy them to your key bindings file (⌘⇧,).

Key Bindings
------------

Copy these to your user key bindings file.

<!-- keybindings start -->
    { "keys": ["escape"], "command": "alternative_autocomplete", "context":
      [
        { "key": "num_selections", "operator": "equal", "operand": 1 },
        { "key": "panel_visible", "operator": "equal", "operand": false },
        { "key": "overlay_visible", "operator": "equal", "operand": false },
        { "key": "has_prev_field", "operator": "equal", "operand": false },
        { "key": "has_next_field", "operator": "equal", "operand": false }
      ]
    },
    { "keys": ["shift+escape"], "command": "alternative_autocomplete", "args": {"cycle": "previous"}, "context":
      [
        { "key": "num_selections", "operator": "equal", "operand": 1 },
        { "key": "overlay_visible", "operator": "equal", "operand": false },
        { "key": "panel_visible", "operator": "equal", "operand": false },
        { "key": "has_prev_field", "operator": "equal", "operand": false },
        { "key": "has_next_field", "operator": "equal", "operand": false }
      ]
    },
    { "keys": ["tab"], "command": "alternative_autocomplete", "args": {"tab": true}, "context":
      [
        { "key": "num_selections", "operator": "equal", "operand": 1 }
      ]
    },
    { "keys": ["tab"], "command": "next_field", "context":
      [
        { "key": "has_next_field", "operator": "equal", "operand": true }
      ]
    },
    { "keys": ["shift+tab"], "command": "alternative_autocomplete", "args": {"tab" : true, "cycle": "previous"}, "context":
      [
        { "key": "num_selections", "operator": "equal", "operand": 1 }
      ]
    },
    { "keys": ["shift+tab"], "command": "prev_field", "context":
      [
        { "key": "has_prev_field", "operator": "equal", "operand": true }
      ]
    },
<!-- keybindings stop -->


Limitations
-----------

Currently does not work with multiple selections.

License
-------

Copyright 2011 Alexander Staubo. MIT license. See `LICENSE` file for license.
Modified by Colin Gray
