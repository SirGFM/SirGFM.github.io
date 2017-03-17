# SirGFM website

My personal website, written in Python, Markdown and JSON.


## Quick guide

To render it to HTML, run:

```
# Clone Mistune, a Markdown parser in pure Python
git clone https://github.com/SirGFM/mistune.git
# Run the Makefile overriden the default lib path
make MISTUNE_PATH=${PWD}/mistune/
```

It automatically reads every markdown file on the `src/` directory and renders it
to HTML. It also creates dependency tracking files, so a rendered HTML shall be
updated even when it's indirectly modified (e.g., by editing a JSON file that it
includes).


## Dependencies

All tools are written in pure Python. [Mistune](https://github.com/lepture/mistune),
a Markdown parser, is used for parsing the contents of the pages.


## The sidebar/navigation menu

The sidebar is described by the file `src/nav.txt`.

It has a list of `(name, relative url)` tuples, separated by newlines.

Modifying this file issues a rebuild of the entire site!


## Creating a new page

In order to create everything from the Markdown, some custom rules were created:

* `$add_game(list_name, json_file)`: Insert the path to a game's JSON file into
  a list of games.
* `$add_style(css_file)`: Store a css file to be added on the header.
* `$add_script(js_file)`: Store a javascript file to be added on the header.
* `$write_header`: Writes a HTML header to the current file (if any). The
  presence of any game triggers the addition of the game overlay.
* `$begin_content`: Output the content's "prologue".
* `$insert_game_list(list_name)`: Insert the icons for the given list of games.
* `$end_content`: Output the content's "epilogue" and finish writing to the
  output.
* `!<[Alternative text](image_url)`: Insert a left-aligned image.

Every page must have `$add_style()` declarations at the start (before
`$write_header`) of the file. Skipping that causes the page to have no styling
at all!

If any script is required by the page, it must also be added through a
`$add_script()` call before the `$write_header` directive.

Page's content shall be described in "pure" Markdown, between the directives
`$begin_content` and `$end_content`. Note that the `$begin_content` must be
preceded by a `$write_header`!

To add a list of games to a page, the games' JSON should be included with the
`$add_game(,)` directive. Then, to render the list, insert a
`$insert_game_list()` with the previously used `game_list`.


## How does it work

The Makefile looks for files ending in `.md` under the `src/` directory. It run
any matches through `src/generator/md_renderer.py`, which actually parses the
Markdown and outputs a HTML to the supplied file.

To ease, and speed up, rendering time, the Makefile calls
`src/generator/dependency_tracker.py` for each output file, so it may generated
a list of dependencies. This script looks into the input file and add every
static dependency (e.g., every JSON file included with `$add_game(,)`
directives) to a dependency list. It also checks if any of the included JSONs
should have their own page and add rules to generate those.

Pages for games are generated from the game's JSON and the script
`src/generator/web_game_renderer.py`.

