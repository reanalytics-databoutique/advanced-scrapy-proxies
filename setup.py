#!/usr/bin/env python
import sys
import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent
# The text of the README file
README = (HERE / "README.md").read_text()

setup(	name='advanced-scrapy-proxies',
		version='0.1.2',
		description='Advanced Scrapy Proxies: random proxy middleware for Scrapy with advanced features',
		long_description=README,
		long_description_content_type="text/markdown",
		author='Pierluigi Vinciguerra',
		author_email='pierluigivinciguerra@gmail.com',
		license="GNU GPLv2",
		url='https://github.com/PVinciguerra/advanced-scrapy-proxies',
		packages=['advanced-scrapy-proxies'],
		setup_requires=['wheel', 'requests', 'pip']
		)
