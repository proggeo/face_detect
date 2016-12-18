#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: config.sample.py
Description: unittest configuration for Python SDK of the Cognitive Face API.

- Copy `config.sample.py` to `config.py`.
- Assign the `KEY` with a valid Subscription Key.
"""

# Subscription Key for calling the Cognitive Face API.
KEY = '8262413521f94489855a7a90190ea21d'

# Time (in seconds) for sleep between each call to avoid exceed quota.
# Default to 3 as free subscription have limit of 20 calls per minute.
TIME_SLEEP = 2.5
