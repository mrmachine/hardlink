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

    Recursively hard link a file or directory. If the source and destination are
    both directories, the two will be merged. Directory and file symbolic links in
    the destination will be replaced with directories or hard links.

    positional arguments:
      src            source file or directory
      dst            destination file or directory

    optional arguments:
      -h, --help     show this help message and exit
      -d, --dry-run  simulate results
      -f, --force    overwrite existing files
      -q, --quiet    silence standard output
      -v, --verbose  increase verbosity of standard output for each occurrence,
                     e.g. -vv

Via the module::

    import hardlink
    link = hardlink.Command(dry_run=False, force=True)
    link(src, dst)

How It Works
============

Symbolic links in ``src`` are followed.

If ``dry_run=True``, no files will actually be linked and no directories will
be created, but logging is unaffected.

If ``force=True``, existing files and symbolic links are replaced. Otherwise a
warning is logged. Existing directories are always merged.
