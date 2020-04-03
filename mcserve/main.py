# -*- coding: utf-8 -*-
#
# This file is part of MCServe.
#
# Copyright (C) 2020 Aakash Hemadri <aakashhemadri123@gmail.com>
#
# You should have received a copy of the MIT License
# along with this program. If not, see <https://choosealicense.com/licenses/mit/>.

import argparse
import sys

from mcserve import __version__
from mcserve.config import Config

class MCServeMain(object):
    """Main class to manage MCServe instance."""
    usage = """
Examples of use:
  Launch to create default standalone vanilla instance of minecraft on local machine.
    $ mcserve [ACTION/]

  Launch using custom config 
    $ mcserve -c /path/to/config [ACTION]

  Launch an existing pre-configured git repository. 
  (Configured based on the guidelines provided by mcserve)
    $ mcserve --path /path/to/local/repository [ACTION]
    $ mcserve --url_http http://github.com/aakashhemadri/minecraft-server.git [ACTION]
    $ mcserve --url_ssh git@github.com:aakashhemadri/minecraft-server [ACTION]
"""

    def __init__(self):
        """Manage the command line arguments"""
        self.args = self.parse_args()

    def init_args(self):
        """Init all the command line arguments"""
        version = 'mcserve v{}'.format(__version__)
        parser = argparse.ArgumentParser(
            prog='mcserve',
            conflict_handler='resolve',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=self.usage
        )
        parser.add_argument('-v','--version',action='version', version=version)
        parser.add_argument('-c','--config',dest='conf_file',help='path to configuration file')
        parser.add_argument('action',action='store',help='start/stop/log/exec docker-compose commands')
        parser.add_argument('--path',action='store',help='launch an existing pre-configured git repository. (local)')
        parser.add_argument('--url_http',action='store',help='launch an existing pre-configured git repository. (http)')
        parser.add_argument('--url_ssh',action='store',help='launch an existing pre-configured git repository. (ssh)')

        return parser

    def parse_args(self):
        args = self.init_args().parse_args()
        self.config = Config(args.conf_file)
        return args

    def get_config(self):
        return self.config
    
    def get_args(self):
        return self.args