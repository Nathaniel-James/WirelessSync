from datetime import datetime
import os
from subprocess import DEVNULL, STDOUT, Popen
import mutagen
import math
import random

def __get_time():
    return datetime.now().timestamp()


def __get_duration(root, file):
    return mutagen.File(os.path.join(root, file)).info.length


def __create_playlist(path):
    """
    Parameters
    ----------
    path: str

    Returns
    -------
    {
        "titles": str[],
        "durations": int[],
        "paths": str[],
    }
    """

    playlist = {                                                    # Playlist object (could be class)
        "titles": [],                                               # Each list element relates to the same index in another list
        "durations": [],
        "paths": [],
    }

    for root, dirs, files in os.walk(os.path.abspath(path)):
        for file in files:
            playlist["titles"].append( os.path.splitext(file)[0] )
            playlist["durations"].append( __get_duration(root, file) )
            playlist["paths"].append( os.path.join(root, file) )

    return playlist


def get_song(time, durations):
    """
    Parameters
    ----------
    time: int
    durations: int[]

    Returns
    -------
    (song: int, duration: int)
    """

    DURATION_LENGTH = len(durations)-1
    BIT_LENGTH = int((math.log(DURATION_LENGTH) / math.log(2)))
    current_time = 0                                                # 1675036800 # 2023/01/30 00:00:00
    previous_time = 0
    song_index = 0

    random.seed(0)                                                  # Set constant seed so each output is the same

    while current_time < time:                                      # Run through each song from epoch
        song_index = random.getrandbits(BIT_LENGTH)                 # Pick random song
        previous_time = current_time                                
        current_time += durations[song_index]                       # Add duration to current_time until current_time > time

    duration = time - previous_time                                 # Subtract previous time with current time to get current "live" duration

    return (song_index, duration)


def play(path, command):
    playlist = __create_playlist(path)

    print(f"Created playlist at {path}:")
    for song in playlist["titles"]: print(song)
    print("\nStarting...")

    while True:
        current_song = get_song( __get_time(), playlist["durations"])
        play_command = command.format(                              # The first "{}" in the command is the path
            playlist["paths"][current_song[0]],                     # The second "{}" in the command is the duration (in seconds)
            current_song[1]
        ) 
        output = Popen(play_command).wait()
        print(f"\"{play_command}\" exited with \"{output}\", moving to next song...")
    
if __name__ == "__main__":
    play("D:\\Music\\Jet Set Radio\\Jet Set Radio Future", "D:\\Japanese\\Immersion\\ffplay.exe -autoexit -i \"{}\" -ss {}")

