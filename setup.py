from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1b1'
DESCRIPTION = "Discord.py simplifier"
LONG_DESCRIPTION = 'This package extends the discord.py library by making complex commands  and functions easier to use. This library will most certainly work with any other library based on d.py like Pycord. I am still working on this lib and looking forward to adding new features [5/7/2022]. This is an early alpha and might be buggy. If you want to report a bug or suggest a feature add me on discord: Wever#3255.'

# Setting up
setup(
    name="dpy-toolbox",
    version=VERSION,
    author="TheWever (Wever#3255)",
    author_email="<nonarrator@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['discord.py'],
    keywords=['discord.py', 'discord', 'utils', 'tools', 'toolbox'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    project_urls = {
 	'Github': 'https://github.com/TheWever/dpy-toolbox',
	'Documentation': 'https://dpy-toolbox.rtfd.io/',
	'Discord': 'https://discord.gg/rnEwUJ7Fhc'
    }
)
