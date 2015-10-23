import setuptools

setuptools.setup(
    name='hardlink',
    version='0.1',
    description='Copy files and merge directories using hard links.',
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
