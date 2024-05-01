import os
import sys
import logging
from os.path import expandvars
import psutil

from overlay import Overlay, GracefulExit

logger = logging.getLogger(__name__)

def check_process() -> bool:
    for process in psutil.process_iter():
        if process.name() in ['Gw2.exe', 'Gw2-64.exe']:
            return True
    return False

def run_overlay():
    if check_process():
        overlay = Overlay(
            initial_text="Testing overlay",
            initial_delay=500
        )
        overlay.run()
    else:
        logger.exception('Guild Wars 2 doesnt appear to be running')


def main():
    run_overlay()

if __name__ == '__main__':
    try:
        main()
    except Exception:
        logger.exception('Gw2 translator terminated with exception:')
