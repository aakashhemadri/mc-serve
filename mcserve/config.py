# -*- coding: utf-8 -*-
#
# This file is part of MCServe.
#
# Copyright (C) 2020 Aakash Hemadri <aakashhemadri123@gmail.com>
#
# You should have received a copy of the MIT License
# along with this program. If not, see <https://choosealicense.com/licenses/mit/>.

import re
import os
import sys

from mcserve.globals import BSD, LINUX, MACOS, SUNOS
from configparser import ConfigParser

def user_config_dir():
    r"""Return the per-user config dir (full path).

    - Linux, *BSD, SunOS: ~/.config/mcserve
    - macOS: ~/Library/Application Support/mcserve
    """
    if MACOS:
        path = os.path.expanduser('~/Library/Application Support')
    else:
        path = os.environ.get('XDG_CONFIG_HOME') or os.path.expanduser('~/.config')
    if path is None:
        path = ''
    else:
        path = os.path.join(path, 'mcserve')

    return path

def system_config_dir():
    r"""Return the system-wide config dir (full path).

    - Linux, SunOS: /etc/mcserve
    """
    if LINUX or SUNOS:
        path = '/etc'
    elif BSD or MACOS:
        path = '/usr/local/etc'
    if path is None:
        path = ''
    else:
        path = os.path.join(path, 'glances')

    return path

class Config(object):
    
    """This class is used to access/read config file, if it exists.

    :param config_dir: the path to search for config file
    :type config_dir: str or None
    """

    def __init__(self, config_dir=None):
        self.config_dir = config_dir
        self.config_filename = 'mcserve.conf'
        self._loaded_config_file = None

        # Re pattern for optimize research of `foo`
        self.re_pattern = re.compile(r'(\`.+?\`)')

        self.parser = ConfigParser()
        self.read()

    def config_file_paths(self):
        r"""Get a list of config file paths.

        The list is built taking into account of the OS, priority and location.

        * custom path: /path/to/mcserve
        * Linux, SunOS: ~/.config/mcserve, /etc/mcserve
        * *BSD: ~/.config/mcserve, /usr/local/etc/mcserve
        * macOS: ~/Library/Application Support/mcserve, /usr/local/etc/mcserve

        The config file will be searched in the following order of priority:
            * /path/to/file (via -C flag)
            * user's home directory (per-user settings)
            * system-wide directory (system-wide settings)
        """
        paths = []

        if self.config_dir:
            paths.append(self.config_dir)

        paths.append(os.path.join(user_config_dir(), self.config_filename))
        paths.append(os.path.join(system_config_dir(), self.config_filename))

        return paths

    def read(self):
        """Read the config file, if it exists. Using defaults otherwise."""
        for config_file in self.config_file_paths():
            if os.path.exists(config_file):
                try:
                    with open(config_file, encoding='utf-8') as f:
                        self.parser.read_file(f)
                        self.parser.read(f)
                except UnicodeDecodeError as err:
                    sys.exit(1)
                # Save the loaded configuration file path (issue #374)
                self._loaded_config_file = config_file
                break
        
        if not self.parser.has_section('source'):
            sys.exit(1)

        if not self.parser.has_section('environment'):
            sys.exit(1)

    @property
    def loaded_config_file(self):
        """Return the loaded configuration file."""
        return self._loaded_config_file

    def as_dict(self):
        """Return the configuration as a dict"""
        dictionary = {}
        for section in self.parser.sections():
            dictionary[section] = {}
            for option in self.parser.options(section):
                dictionary[section][option] = self.parser.get(section, option)
        return dictionary

    def sections(self):
        """Return a list of all sections."""
        return self.parser.sections()
    
    def set_default(self, section, option,
                    default):
        """If the option did not exist, create a default value."""
        if not self.parser.has_option(section, option):
            self.parser.set(section, option, default)

    def items(self, section):
        """Return the items list of a section."""
        return self.parser.items(section)

    def has_section(self, section):
        """Return info about the existence of a section."""
        return self.parser.has_section(section)
    
    def get_value(self, section, option,
                  default=None):
        """Get the value of an option, if it exists.

        If it did not exist, then return the default value.
        """
        ret = default
        try:
            ret = self.parser.get(section, option)
        except NoOptionError:
            pass

        # Search a substring `foo` and replace it by the result of its exec
        if ret is not None:
            try:
                match = self.re_pattern.findall(ret)
                for m in match:
                    ret = ret.replace(m, system_exec(m[1:-1]))
            except TypeError:
                pass
        return ret

    def get_int_value(self, section, option, default=0):
        """Get the int value of an option, if it exists."""
        try:
            return self.parser.getint(section, option)
        except NoOptionError:
            return int(default)

    def get_float_value(self, section, option, default=0.0):
        """Get the float value of an option, if it exists."""
        try:
            return self.parser.getfloat(section, option)
        except NoOptionError:
            return float(default)

    def get_bool_value(self, section, option, default=True):
        """Get the bool value of an option, if it exists."""
        try:
            return self.parser.getboolean(section, option)
        except NoOptionError:
            return bool(default)
