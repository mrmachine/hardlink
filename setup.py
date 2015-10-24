import codecs
import os
import setuptools


def read(*parts):
    path = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(path, 'rb', 'utf-8') as f:
        return f.read()

if __name__ == '__main__':
    setuptools.setup(
        name='hardlink',
        version='0.2.dev0',
        description='Copy files and merge directories using hard links.',
        long_description=read('README.rst'),
        url='https://github.com/mrmachine/hardlink',
        license='MIT',
        author='Tai Lee',
        author_email='real.human@mrmachine.net',
        packages=setuptools.find_packages(where='src'),
        package_dir={
            '': 'src',
        },
        entry_points={
            'console_scripts': [
                'hardlink = hardlink.base:main',
            ],
        },
    )
