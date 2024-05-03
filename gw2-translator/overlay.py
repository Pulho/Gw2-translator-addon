# Standard Library
import sys
import logging
import time
import tkinter as tk
import pygetwindow as gw
from typing import Callable, Any


logger = logging.getLogger(__name__)


def report_callback_exception(exc_type, val, tb):
    if issubclass(exc_type, GracefulExit):
        sys.exit(0)

    logger.error('Exception occured, exiting:', exc_info=(exc_type, val, tb))
    sys.exit(1)


class GracefulExit(Exception):
    "Allows callbacks to gracefully exit without logging error"


class Overlay:
    def __init__(self,
                 initial_text: str,
                 initial_delay: int
                 ):
        
        self.initial_text = initial_text
        self.initial_delay = initial_delay
        self.minimized_status = False
        self.root = tk.Tk()
        self.root.report_callback_exception = report_callback_exception

        # Set up Close Label
        self.close_label = tk.Label(
            self.root,
            text='[X] | Close label',
            font=('Consolas', '14'),
            fg='slategray',
            bg='slategray2'
        )

        self.close_label.bind("<Button-1>", self.close_overlay)
        self.close_label.grid(row=0, column=0)

        # Define Window Geometry
        self.root.overrideredirect(True)
        self.root.geometry("+5+5")
        self.root.lift()
        self.root.wm_attributes("-topmost", True)

        # Monitoring process window
        self.monitor_process_window()

    def close_overlay(self, event):
        self.root.destroy()

    def monitor_process_window(self):
        while True:
            gw_window = gw.getWindowsWithTitle('Guild Wars 2')
            if gw_window and not gw_window[0].isActive:
                self.root.state('withdrawn')
                self.minimized_status = True
            elif self.minimized_status:
                self.root.state('normal')
                self.minimized_status = False
            self.root.update()
            time.sleep(1)

    def run(self) -> None:
        self.text = "Gw2 translator addon"
        self.root.mainloop()


# /