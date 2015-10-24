Overview
========

This package provides a ``hardlink`` module and command line script that will
copy a file or directory using hard links.

Why? Because OS X doesn't support ``cp -lR``, and Python is my favourite
scripting language.

Installation
============

Latest code direct from the repository::

    $ pip install hardlink

Usage
=====

Via the command line script::

    $ hardlink -h
    usage: hardlink [-h] [-d] [-f] [-q | -v] src dst

    Copy files and merge directories using hard links.

    positional arguments:
      src            Source file or directory. Follow symbolic links.
      dst            Destination file or directory. Merge existing directories.

    optional arguments:
      -h, --help     show this help message and exit
      -d, --dry-run  Do not link files or create directories. Only log operations.
      -f, --force    Replace existing files and symbolic links.
      -q, --quiet    Silence standard output.
      -v, --verbose  Increase verbosity for each occurrence.

Via the module::

    import hardlink
    link = hardlink.Command(dry_run=False, force=True)
    link(src, dst)
