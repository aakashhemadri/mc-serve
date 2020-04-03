# -*- coding: utf-8 -*-
#
# This file is part of mc-serve.
#
# Copyright (C) 2020 Aakash Hemadri <aakashhemadri123@gmail.com>
#
# You should have received a copy of the MIT License
# along with this program. If not, see <https://choosealicense.com/licenses/mit/>.


class MCServe(object):
    def __init__(self, config=None, args=None):
        self.config = config
        self.args = args
    
    def run(self):
        print("Initializing mc-serve")
        if self.args.action == 'start':
            self.start()
        elif self.args.action == 'stop':
            self.stop()
        elif self.args.action == 'stop':
            self.logs()
        elif self.args.action == 'stop':
            self.execute()
        print("bye bye")
    
    def execute(self):
        print("Executing command on minecraft-server instance")
    
    def start(self):
        print("Starting minecraft-server instance")
    
    def stop(self):
        print("Stopping minecraft-server instance")

    def logs(self):
        print("Following logs of the minecraft-server instance")