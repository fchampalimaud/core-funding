#!/usr/bin/python2
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import re

setup(
	name='Core funding newsletter',
	version=0.0,
	description="""""",
	author=['Ricardo Ribeiro'],
	author_email=['ricardojvr@gmail.com'],
	url='https://bitbucket.org/fchampalimaud/research-core-funding-newsletter',
	packages=find_packages(),
	package_data={'funding_newsletter': ['templates/funding_newsletter/*.html']},
)
