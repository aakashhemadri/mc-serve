# -*- coding: utf-8 -*-
#
# This file is part of MCServe.
#
# Copyright (C) 2020 Aakash Hemadri <aakashhemadri123@gmail.com>
#
# You should have received a copy of the MIT License
# along with this program. If not, see <https://choosealicense.com/licenses/mit/>.

"""Init the MCServe software."""

import signal
import sys
import locale

# Global names
__version__ = '0.0.2'
__author__ = 'Aakash Hemadri <aakashhemadri123@gmail.com>'
__license__ = 'MIT'

from mcserve.main import MCServeMain
from mcserve.serve import MCServe

# Check locale
try:
    locale.setlocale(locale.LC_ALL, '')
except locale.Error:
    print("Warning: Unable to set locale. Expect encoding problems.")



def __signal_handler(signal, frame):
    """Callback for CTRL-C."""
    end()

def end():
    """Stop mcserve"""
    sys.exit(0)

def start(config, args):
    """Start MCServe"""
    # Possible logging and pre-requistes for scripts.

    serve = MCServe(config=config, args=args)
    serve.run()

def main():
    """Entry point for MCServe."""

    signal.signal(signal.SIGINT, __signal_handler)

    core = MCServeMain()
    config = core.get_config()
    args = core.get_args()

    start(config=config, args=args)