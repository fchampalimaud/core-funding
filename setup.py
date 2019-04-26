#!/usr/bin/python2
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import re

setup(
	name='Core funding newsletter',
	version=0.0,
	description="Application to manage the funding opportunities.",
	author=['Ricardo Ribeiro'],
	author_email=['ricardojvr@gmail.com'],
	url='https://github.com/fchampalimaud/core-funding',
	packages=find_packages(),
	package_data={'funding': ['templates/funding/*.html']},
)
