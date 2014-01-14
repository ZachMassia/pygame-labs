import argparse
import pygame
from os import path, getcwd
from time import sleep
from pygame.mixer import Sound


def play_song_sync(song):
    """Synchronously play the given song."""
    song.play()
    sleep(song.get_length())


def load_song(filename):
    """Attempt to load the song, catching any exceptions."""
    try:
        return Sound(file=filename)
    except pygame.error as e:
        return None


def format_song_info(name, song):
    """Print song info. Format: 'Playing NAME (min:sec)'"""
    m, s = divmod(song.get_length(), 60)
    return 'Playing {} ({}:{})'.format(name, int(m), int(s))


def parse_path(args):
    """Return the full path to the file."""
    if args.directory:
        return path.join(args.directory, args.filename)

    return path.join(getcwd(), args.filename)


def get_args():
    """Init the parser and return the arguments."""
    parser = argparse.ArgumentParser(description='Lab 1 Part 1: Play a sound')

    parser.add_argument('filename', help='the .wav file to play')
    parser.add_argument('-d', '--directory', help='the directory for the file')
    return parser.parse_args()


if __name__ == '__main__':
    pygame.init()

    # Load the song
    args = get_args()
    path = parse_path(args)
    song = load_song(path)

    # Attempt to play it
    if song:
        print(format_song_info(args.filename, song))
        play_song_sync(song)
