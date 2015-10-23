#!/usr/bin/env python
"""
Copy files and merge directories using hard links.
"""

import argparse
import errno
import logging
import os
import shutil
import sys

logging.basicConfig(format='%(message)s')
logger = logging.getLogger(__name__)


class Command(object):

    def __init__(self, dry_run=False, force=False):
        self.dry_run = dry_run
        self.force = force
        self._created_dirs = set()
        self._removed = set()

    def __call__(self, src, dst):
        src = os.path.abspath(src)
        logger.debug('Source: %s' % src)

        dst = os.path.abspath(dst)
        logger.debug('Destination: %s' % dst)

        # Validate source.
        if not os.path.exists(src):
            self._err('No such file or directory: %s' % src)

        # Merge directories, link files, overwrite existing files. We don't
        # want to leak hard links outside the destination (by following
        # symlinks). Replace directory symlinks with directories, and file
        # symlinks with hard links. Do not allow files to be replaced with
        # directories, and vice versa.
        if os.path.isdir(src):
            logger.info('Linking directory: %s -> %s' % (src, dst))

            cwd = os.getcwd()
            logger.debug('Current working directory: %s' % cwd)

            logger.debug('Changing current working directory: %s' % src)
            os.chdir(src)

            self._makedirs(dst)

            # Pass a unicode path to `os.walk` to get unicode values back for
            # `local`, `dirs` and `files`.
            for local, dirs, files in os.walk(u'.', followlinks=True):
                logger.debug('Walking directory: %s' % os.path.realpath(
                    os.path.join(dst, local)))

                # Directories.
                for d in dirs:
                    self._makedirs(
                        os.path.abspath(os.path.join(dst, local, d)))

                # Files.
                for f in files:
                    srcfile = os.path.realpath(
                        os.path.abspath(os.path.join('.', local, f)))
                    dstfile = os.path.abspath(os.path.join(dst, local, f))
                    if not os.path.exists(srcfile):
                        logger.warning(
                            'No such file or directory: %s' % srcfile)
                        continue
                    if srcfile == dstfile:
                        logger.warning(
                            'Cannot link file to itself: %s' % srcfile)
                        continue
                    self._link(srcfile, dstfile)

            logger.debug('Changing current working directory: %s' % cwd)
            os.chdir(cwd)

        # Link files.
        elif os.path.isfile(src):
            logger.info('Linking file: %s -> %s' % (src, dst))
            self._link(src, dst)

    def _err(self, *args):
        """
        Log error and exit.
        """
        logger.error(*args)
        exit(1)

    def _link(self, src, dst):
        if os.path.exists(dst):
            if self.force:
                self._remove(dst)
            else:
                logger.warning('File or directory already exists: %s' % dst)
                return
        self._makedirs(os.path.dirname(dst))
        logger.debug('Linking file: %s -> %s' % (src, dst))
        if not self.dry_run:
            os.link(src, dst)

    def _makedirs(self, path):
        if os.path.isfile(path) or os.path.islink(path):
            if self.force:
                self._remove(path)
            else:
                logger.warning('File or directory already exists: %s' % path)
                return False
        if not os.path.exists(path):
            # Only log created directories once. In a dry run, this code path
            # will be executed again for every file within a directory that is
            # missing from the destination.
            if path not in self._created_dirs:
                logger.debug('Creating directory: %s' % path)
                self._created_dirs.add(path)
            if not self.dry_run:
                try:
                    os.makedirs(path)
                except OSError as e:
                    # Check if any intermediate path is a file. Don't complain
                    # if the directory already exists.
                    if e.errno not in (errno.EEXIST, errno.ENOTDIR):
                        raise
                    if not os.path.isdir(path):
                        bits = os.path.split(path)
                        bitpath = ''
                        for bit in bits:
                            bitpath = os.path.join(bitpath, bit)
                            if not os.path.isdir(bitpath):
                                logger.warning(
                                    'Cannot replace file with directory: %s' %
                                    bitpath)
                            # No need to check any further.
                            break
                    return False
        return True

    def _remove(self, path):
        # Only log removed directories once. In a dry run, this code path will
        # be executed again for every file within a directory that is a
        # symbolic link in the destination.
        if path not in self._removed:
            logger.debug('Removing file or directory: %s' % path)
            self._removed.add(path)
        if not self.dry_run:
            try:
                shutil.rmtree(path)
            except OSError:
                os.remove(path)


def main():
    # Parse arguments.
    parser = argparse.ArgumentParser(
        description='Recursively hard link a file or directory. If the source '
                    'and destination are both directories, the two will be '
                    'merged. Directory and file symbolic links in the '
                    'destination will be replaced with directories or hard '
                    'links.',
    )
    parser.add_argument('src', help='source file or directory')
    parser.add_argument('dst', help='destination file or directory')
    parser.add_argument(
        '-d',
        '--dry-run',
        action='store_true',
        help='simulate results',
    )
    parser.add_argument(
        '-f',
        '--force',
        action='store_true',
        help='overwrite existing files',
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '-q',
        '--quiet',
        action='store_true',
        help='silence standard output',
    )
    group.add_argument(
        '-v',
        '--verbose',
        action='count',
        default=0,
        dest='verbosity',
        help='increase verbosity of standard output for each occurrence, e.g. '
             '-vv',
    )
    args = parser.parse_args()

    # Configure log level with verbosity argument.
    levels = (
        # logging.CRITICAL,
        # logging.ERROR,
        logging.WARNING,
        logging.INFO,
        logging.DEBUG,
    )
    try:
        logger.setLevel(levels[args.verbosity])
    except IndexError:
        logger.setLevel(logging.DEBUG)

    # Silence standard output.
    stdout = sys.stdout
    if args.quiet:
        sys.stdout = open(os.devnull, 'w')
    # Execute.
    Command(args.dry_run, args.force)(args.src, args.dst)
    # Restore standard output.
    sys.stdout = stdout

if __name__ == '__main__':
    main()
