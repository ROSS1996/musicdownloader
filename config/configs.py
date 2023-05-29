import configparser
import os
import re
import platform
from pathlib import Path
import logging
from logging import FileHandler


def clean_path(string):
    pattern = r'[^A-Za-z0-9\-_. /\\():]'
    cleaned_string = re.sub(pattern, '', str(string))
    return cleaned_string


def get_music_folder():
    system = platform.system()
    if system == 'Windows':
        return Path.home() / 'Music'
    else:
        return Path.home() / 'Music'


# Get the current directory
config_dir = Path(__file__).resolve().parent
root_dir = config_dir.parent
music_folder = get_music_folder()

# Create a ConfigParser object and read the config.ini file
config = configparser.ConfigParser()
config_file = config_dir / 'config.ini'
config.read(config_file)

config_downloads_dir = clean_path(config.get(
    'Locations', 'downloads_dir', fallback=music_folder))
config_links_dir = clean_path(config.get(
    'Locations', 'links_dir', fallback=root_dir))
config_library_dir = clean_path(config.get(
    'Locations', 'library_dir', fallback=root_dir))

downloads_dir = next((Path(p) for p in (config_downloads_dir, music_folder)
                     if p and Path(p).exists()), root_dir / "downloads")
library_file = Path(config_library_dir, "library.json") if config_library_dir and Path(
    config_library_dir).exists() else root_dir / "library.json"
links_file = Path(config_links_dir, "links.txt") if config_links_dir and Path(
    config_links_dir).exists() else root_dir / "links.txt"


# Get the values of devmode and verbose variables as booleans
devmode = config.getboolean('Logging', 'devmode', fallback=False)
verbose = config.getboolean('Logging', 'verbose', fallback=False)


def get_logger():
    # Create the logger
    logger = logging.getLogger("root")
    logger.setLevel(logging.DEBUG)

    # Create a formatter for the console
    console_formatter = logging.Formatter('%(message)s')

    # Create a formatter for the file
    file_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s')

    # Clear existing handlers to avoid duplicates
    logger.handlers = []

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.INFO)  # Set console level to INFO

    # Add the console handler to the logger
    logger.addHandler(console_handler)

    if devmode:
        # Create a file handler only if devmode is True
        file_handler = FileHandler(Path('logs.log'))
        file_handler.setFormatter(file_formatter)

        # Add the file handler to the logger
        logger.addHandler(file_handler)

    return logger
