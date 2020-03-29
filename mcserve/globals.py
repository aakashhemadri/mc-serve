# -*- coding: utf-8 -*-
#
# This file is part of MCServe.
#
# Copyright (C) 2020 Aakash Hemadri <aakashhemadri123@gmail.com>
#
# You should have received a copy of the MIT License
# along with this program. If not, see <https://choosealicense.com/licenses/mit/>.


import sys

BSD = sys.platform.find('bsd') != -1
LINUX = sys.platform.startswith('linux')
MACOS = sys.platform.startswith('darwin')
SUNOS = sys.platform.startswith('sunos')