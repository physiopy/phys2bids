#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A parallel CLI utility to segment the physiological input file
into multiple runs with padding

"""

import os
import logging

from pathlib import Path

from phys2bids.cli.split import _get_parser
from phys2bids.physio_obj import BlueprintInput
