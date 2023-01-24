import os
import time
import random

def pause(max_time=10):
    time.sleep(random.randint(1, max_time))

def n_current_downloads(path_to_downloads):
    """Return the number of files currently downloading"""
    return len([f for f in os.listdir(path_to_downloads) if f.endswith('.crdownload')])

def download_wait(path_to_downloads, timeout=20, max_downloads=3):
    seconds = 0
    dl_wait = True
    while dl_wait:
        time.sleep(1)
        dl_wait = False

        n_dl = n_current_downloads(path_to_downloads)

        # If the number of downloads is greater than the max number of downloads
        # wait for the downloads to finish
        if (n_dl >= max_downloads):
            dl_wait = True
        elif (n_dl == 0):
            # If there are no downloads, wait for 1 second
            dl_wait = False
        elif (seconds >= timeout):
            # If the timeout is reached, wait for 1 second
            dl_wait = False
           
        seconds += 1

    return seconds