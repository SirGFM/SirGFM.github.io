# SirGFM's homepage source

This directory contains every script and input file used to generate the static
HTML pages.

## Updating the website

To update the website, run the following from the repository's root directory:

```sh
$ PYTHONPATH=${PYTHONPATH}:${PWD}/src python src/update_site.py
$ exit $?
```

The script `update_site.sh` (on the repository's root directory) has those exact
lines and may be directly executed (using `/bin/bash`) to update everything.

## Creating a new page

Every page must be a python script located on `src/page`. The update script
navigates through that package and imports the class `Page` from every module
found there.

Those classes must inherit from `src.generator.page.PageWriter`, take a single
parameter on its initializer (the site's navigation bar) and implement two
methods:

* `insert_content`: Called from `PageWriter.insert` to insert the page's
  content.
* `do_create`: Called from the update script so each page may specify every css
  a javascript required when calling its `create` method.

Note that the scripts are navigated in alphabetic order. That order is relevant
when creating the navigation bar!
