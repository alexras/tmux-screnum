#!/usr/bin/env python

import subprocess
import tempfile
import os, sys
import re
import time

def checked_call(cmd, expected_status=0):
    """
    Execute the given command in a subprocess shell, and abort if the error
    code isn't what you expected.

    I would use check_output here, but I wanted to make the script compatible
    with Python 2.6.
    """
    proc_obj = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
    output = proc_obj.communicate()[0]

    if proc_obj.returncode != expected_status:
        sys.exit("Command '%s' failed: %s" % (cmd, output))

    return output

def get_windows():
    window_list = checked_call("tmux list-windows")
    window_extractor_regex = re.compile('^(\d+): (.*?) \[\d+x\d+\]$')

    windows = {}

    print window_list

    for line in window_list.split('\n'):
        line = line.strip()

        match = window_extractor_regex.search(line)

        if match is not None:
            windows[int(match.group(1))] = match.group(2)

    return windows

def screnum():
    print "Reading window list ..."
    windows = get_windows()

    def swap(i, j):
        """
        Moves the given window number in the given session from window number i
        to window number j, swapping it with the window currently at window
        number j if necessary
        """

        if j in windows:
            movement_cmd = "swap-window"
            tmp = windows[i]
            windows[i] = windows[j]
            windows[j] = tmp

            print "Swapping windows %d and %d" % (i, j)
        else:
            movement_cmd = "move-window"
            windows[j] = windows[i]
            del windows[i]

            print "Moving window %d to %d" % (i, j)

        checked_call("tmux %s -d -s %d -t %d" % (movement_cmd, i, j))

    def min_window(start_index):
        """
        Find the window in the subset of windows whose numbers are >=
        start_index with the smallest name (sorted lexicographically)
        """
        min_window_number = None

        for window_number in windows:
            if (window_number >= start_index and
                (min_window_number == None or
                 windows[window_number] < windows[min_window_number])):
                min_window_number = window_number

        return min_window_number

    # Perform insertion sort on the windows.
    num_windows = len(windows)

    for i in xrange(num_windows):
        smallest_window_number = min_window(i)

        if smallest_window_number == None:
            break
        elif smallest_window_number == i:
            continue
        else:
            swap(smallest_window_number, i)

if __name__ == "__main__":
    screnum()
