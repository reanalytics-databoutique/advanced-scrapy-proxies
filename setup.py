#!/usr/bin/env python
import sys
from setuptools import setup

setup(	name='advanced-scrapy-proxies',
		version='0.1.1',
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
