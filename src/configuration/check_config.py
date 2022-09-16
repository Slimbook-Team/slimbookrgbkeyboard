#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
import configparser
import logging
import os
import pwd
import shutil
import subprocess
import sys

# We want load first current location
CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
if CURRENT_PATH not in sys.path:
    sys.path = [CURRENT_PATH] + sys.path

parent_path = os.path.join(CURRENT_PATH,'..')

sys.path.append(parent_path)
import utils

APP_NAME= 'slimbookrgbkeyboard'

USER_NAME = utils.get_user()

HOMEDIR = os.path.expanduser('~{}'.format(USER_NAME))

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))

DEFAULT_CONF = os.path.join(CURRENT_PATH, '{}.conf'.format(APP_NAME))

CONFIG_FOLDER = os.path.join(HOMEDIR, '.config', APP_NAME)

CONFIG_FILE = os.path.join(CONFIG_FOLDER, '{}.conf'.format(APP_NAME))

uid, gid = pwd.getpwnam(USER_NAME).pw_uid, pwd.getpwnam(USER_NAME).pw_gid

logger = logging.getLogger()


def main():
    logger.info('Checking configuration')
    if not os.path.isdir(CONFIG_FOLDER):
        logger.info('Creating config folder ...')
        os.umask(0)
        os.makedirs(CONFIG_FOLDER, mode=0o766)  # creates with perms
        os.chown(CONFIG_FOLDER, uid, gid)  # set user:group
        logger.info(subprocess.getoutput('ls -la ' + CONFIG_FOLDER))
    else:
        logger.info('Configuration folder ({}) found!'.format(CONFIG_FOLDER))

    config_folder_stat = os.stat(CONFIG_FOLDER)
    logger.debug("uid={} file_uid={}".format(uid, config_folder_stat.st_uid))
    f_uid = config_folder_stat.st_uid
    f_gid = config_folder_stat.st_gid
    
    if not uid == f_uid or not gid == f_gid:
        logger.info('Setting folder ownership')

        for dir_path, dir_name, filenames in os.walk(CONFIG_FOLDER):
            logger.debug(dir_path)
            os.chown(dir_path, uid, gid)
            for filename in filenames:
                file_path = os.path.join(dir_path, filename)
                logger.debug(file_path)
                os.chown(file_path, uid, gid)

    check_config_file()

def check_config_file():
    logger.info("Checking {}'s Configuration".format(APP_NAME.capitalize()))
    if os.path.isfile(CONFIG_FILE):
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)

        default_config = configparser.ConfigParser()
        default_config.read(DEFAULT_CONF)
        incidences = False

        for section in default_config.sections():
            logger.info('Checking section: {} ...'.format(section))
            if not config.has_section(section):
                incidences = True
                config.add_section(section)
                logger.info('Section added')

            for var in default_config.options(section):
                if not config.has_option(section, var):
                    incidences = True
                    logger.info('Not found: {}'.format(var))
                    config.set(section, var, default_config.get(section, var))

        if incidences:
            try:
                with open(CONFIG_FILE, 'w') as configfile:
                    config.write(configfile)
                logger.info('Incidences corrected.')
            except Exception:
                logger.exception('Incidences could not be corrected.')
        else:
            logger.info('Incidences not found.')

    else:
        logger.info('Creating config file ...')
        shutil.copy(DEFAULT_CONF, CONFIG_FOLDER)
        os.chown(CONFIG_FILE, uid, gid)  # set user:group

if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(funcName)s:%(lineno)d - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logger.info('Config check executed as {}'.format(USER_NAME))
    main()