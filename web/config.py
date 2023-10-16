"""
Based on the configuration setup for project-1.
Configures from default.ini and credentials.ini, in that order (if present).
"""


import configparser
import os
import logging
logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.INFO)

log = logging.getLogger(__name__)
HERE = os.path.dirname(__file__)


def config_file_args(config_file_paths, section) -> dict:
    """Returns dict of values from the configuration files,
    accessing them in the order they appear in config_file_paths.
    If the project kwarg is provided, we will take configuration
    values from that section of the configuration file if it exists,
    otherwise from SERVER section.
    """
    log.debug("-> config file args")
    config = configparser.ConfigParser()
    for path in config_file_paths:
        relative = os.path.join(HERE, path)
        if os.path.exists(path):
            log.info("Configuring from {}".format(path))
            config.read(path)
        elif os.path.exists(relative):
            log.info("Configuring from {}".format(relative))
            config.read(relative)
        else:
            log.info("No configuration file {}; skipping".format(path))

    log.debug("Using configuration section {}".format(section))
    config_dict = {a: b for a, b in config.items(section)}
    imply_types(config_dict)
    return config_dict


def imply_types(ns: dict):
    """Convert values to implied types.  We assume that strings of
    digits should be integers, and True/False (with any casing) should
    be boolean. """
    for var in ns:
        val = ns[var]
        if type(val) != str:
            continue
        if val.lower() == "true":
            ns[var] = True
        elif val.lower() == "false":
            ns[var] = False
        elif val.isdecimal():
            ns[var] = int(val)


def configuration() -> dict:
    """
    Returns a dictionary of configs, parsed from any present .ini files.
    """
    # Load config.
    log.debug("-> configuration")
    config_file_paths = ["default.ini", "credentials.ini"]
    ini = config_file_args(config_file_paths, section='SERVER')
    log.debug("Config file args: {}".format(ini))
    return ini
