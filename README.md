Alternative autocompletion
==========================

This plugin adds an autocompletion command to Sublime Text that acts similarly to TextMate:

* Hitting the autocomplete key will attempt to complete the current word by looking at similar words in the current document.

* Hitting the autocomplete key multiple times will cycle through the available words.

* The last autocomplete position is remembered, so you can perform an autocompletion, move the cursor around, move back to where you were, and continue cycling through the completions.

* Candidate completions are selected prioritized by distance to the cursor.

The plugin improves on TextMate in one respect: If no candidates are found, the plugin reverts to using a simple fuzzy, case-insensitive matching algorithm that is similar to Sublime's file/class matching algorithm. For example, typing `appc` might match `ApplicationController`.

Compatibility
-------------

Tested with Sublime Text 2 (`st2` branch) and Sublime Text 3 (`master` branch)

Installation
------------

1. Open the Sublime Text Packages folder
    - OS X: ~/Library/Application Support/Sublime Text 3/Packages/
    - Windows: %APPDATA%/Sublime Text 3/Packages/
    - Linux: ~/.Sublime Text 3/Packages/ or ~/.config/sublime-text-3/Packages

2. clone this repo

### Sublime Text 2

1. Open the Sublime Text 2 Packages folder
2. clone this repo, but use the `st2` branch

       git clone -b st2 git@github.com:colinta/colinta_alternative_autocompletion.tmLanguage

Instructions
------------

To map to the escape key, like TextMate:

    { "keys": ["escape"], "command": "alternative_autocomplete", "context":
      [
        { "key": "num_selections", "operator": "equal", "operand": 1 },
        { "key": "overlay_visible", "operator": "equal", "operand": false },
        { "key": "panel_visible", "operator": "equal", "operand": false }
      ]
    },
    { "keys": ["shift+escape"], "command": "alternative_autocomplete", "args": {"cycle": "previous"}, "context":
      [
        { "key": "num_selections", "operator": "equal", "operand": 1 },
        { "key": "overlay_visible", "operator": "equal", "operand": false },
        { "key": "panel_visible", "operator": "equal", "operand": false }
      ]
    },

To map to the tab key, you don't need to worry about the 'overlay_visible/panel_visible' options:

    { "keys": ["tab"], "command": "alternative_autocomplete", "args": {"tab": true}, "context":
      [
        { "key": "num_selections", "operator": "equal", "operand": 1 }
      ]
    },
    { "keys": ["shift+tab"], "command": "alternative_autocomplete", "args": {"cycle": "previous"}, "context":
      [
        { "key": "num_selections", "operator": "equal", "operand": 1 }
      ]
    },

Limitations
-----------

Currently does not work with multiple selections.

License
-------

Copyright 2011 Alexander Staubo. MIT license. See `LICENSE` file for license.
Modified by Colin Gray
