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

Sublime Text 3 only

Installation
------------

1. Open the Sublime Text Packages folder
    - OS X: ~/Library/Application Support/Sublime Text 3/Packages/
    - Windows: %APPDATA%/Sublime Text 3/Packages/
    - Linux: ~/.Sublime Text 3/Packages/ or ~/.config/sublime-text-3/Packages

2. clone this repo
3. Install keymaps for the commands (see Example.sublime-keymap for my preferred keys)

Limitations
-----------

Currently does not work with multiple selections.

License
-------

Copyright 2011 Alexander Staubo. MIT license. See `LICENSE` file for license.
Modified by Colin Gray
