#!/usr/bin/python3.10
########################################################################################
# __init__.py - The init module for CLOVER-GUI application.                            #
#                                                                                      #
# Author: Ben Winchester, Hamish Beath                                                 #
# Copyright: Ben Winchester, 2022                                                      #
# Date created: 19/07/2023                                                             #
# License: MIT, Open-source                                                            #
# For more information, contact: benedict.winchester@gmail.com                         #
########################################################################################

import os
import tkinter as tk

from io import TextIOWrapper
from subprocess import Popen
from threading import Event, Thread
from typing import Callable

import ttkbootstrap as ttk


from clover.scripts.clover import clover_main
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import *

from .__utils__ import BaseScreen, CLOVER_SPLASH_SCREEN_IMAGE, IMAGES_DIRECTORY

__all__ = ("RunScreen",)


class StoppableThread(Thread):
    """
    Thread class with a stop() method.

    The thread itself has to check regularly for the stopped() condition.

    """

    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


class RunScreen(BaseScreen, show_navigation=True):

    """
    Represents the Run Screen.

    Displays running information when CLOVER is running simulation or optimisation.

    """

    def __init__(self, data_directory: str, open_post_run_screen: Callable) -> None:
        """
        Instantiate a :class:`RunFrame` instance.

        :param: data_directory
            The path to the data directory.

        :param:

        """

        super().__init__()

        self.open_post_run_screen = open_post_run_screen

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=4)
        self.columnconfigure(4, weight=1)

        self.running_image = tk.PhotoImage(
            file=os.path.join(
                data_directory, IMAGES_DIRECTORY, CLOVER_SPLASH_SCREEN_IMAGE
            )
        )
        self.running_image = self.running_image.subsample(2)
        self.image_label = ttk.Label(self, image=self.running_image)
        self.image_label.grid(row=0, column=0, columnspan=5, sticky="news")

        self.clover_thread: Popen | None = None

        # Create a progress bar
        self.clover_progress_bar: ttk.Progressbar = ttk.Progressbar(
            self, bootstyle=f"{SUCCESS}-striped", mode="determinate"
        )
        self.clover_progress_bar.grid(
            row=1, column=0, columnspan=4, sticky="ew", ipadx=60, padx=20, pady=5
        )

        # Stop the clover thread with a button.
        self.stop_button = ttk.Button(
            self, text="STOP", bootstyle=f"{DANGER}-inverted", command=self.stop
        )
        self.stop_button.grid(
            row=1, column=4, padx=20, pady=5, ipadx=80, ipady=10, sticky="e"
        )

        self.sub_process_frame = ScrolledFrame(self)
        self.sub_process_frame.grid(
            row=2, column=0, columnspan=5, sticky="news", padx=10, pady=5
        )

        self.courier_style = ttk.Style()
        self.courier_style.configure("Courier.Label", font=("Courier", 16))

        self.sub_process_label = ttk.Label(
            self.sub_process_frame, bootstyle=f"{DARK}.Courier.Label"
        )
        self.sub_process_label.grid(row=0, column=0, sticky="news", padx=10, pady=5)

        # Add navigation buttons
        self.back_button = ttk.Button(
            self,
            text="Back",
            bootstyle=f"{PRIMARY}-{OUTLINE}",
            command=lambda self=self: BaseScreen.go_back(self),
        )
        self.back_button.grid(row=3, column=0, padx=10, pady=5)

        self.home_button = ttk.Button(
            self,
            text="Home",
            bootstyle=f"{PRIMARY}-{OUTLINE}",
            command=lambda self=self: BaseScreen.go_home(self),
        )
        self.home_button.grid(row=3, column=1, padx=10, pady=5)

        self.forward_button = ttk.Button(
            self,
            text="Forward",
            bootstyle=f"{PRIMARY}-{OUTLINE}",
            command=lambda self=self: BaseScreen.go_forward(self),
        )
        self.forward_button.grid(row=3, column=2, padx=10, pady=5)

        self.post_run_button = ttk.Button(
            self,
            bootstyle=SUCCESS,
            text="View outputs",
            command=self.open_post_run_screen,
            state=DISABLED,
        )
        self.post_run_button.grid(
            row=3, column=4, sticky="e", padx=20, pady=5, ipadx=80, ipady=20
        )

        # Create a buffer for the stdout
        self.stdout_data: str = " " * 180

    def read_output(self, pipe: TextIOWrapper):
        """
        Read subprocess' output and store it in `self.stdout_data`.

        """
        while True:
            data = os.read(pipe.fileno(), 1 << 20)
            # Windows uses: "\r\n" instead of "\n" for new lines.
            data = data.replace(b"\r\n", b"\n")
            if data:
                self.stdout_data += (
                    new_data := "\n".join(
                        [
                            entry
                            for entry in (data.decode().split("\n"))
                            if (
                                "hourly computation" not in entry
                                and "FutureWarning" not in entry
                                and "return float(" not in entry
                                and entry != "\n"
                                and entry != ""
                            )
                        ]
                    )
                )

                if "100%" in new_data:
                    self.push_progress_bar(20)

                # Scroll to the bottom
                self.sub_process_frame.yview_moveto(1)
            else:  # clean up
                self.after(1000, self.stop)  # stop in 5 seconds
                return None

            # Reduce the length of the data to contain 20 lines only.
            # self.stdout_data = "\n".join(self.stdout_data.split("\n")[-20:])

    def run_with_clover(self, clover_thread: Popen) -> None:
        """
        Create a new thread that will read stdout and write the data to the buffer.

        :param: clover_thread
            A thread in which CLOVER runs.

        """

        self.clover_thread = clover_thread

        # Create a thread with the target to read the output.
        self.reading_thread = Thread(
            target=self.read_output, args=(clover_thread.stdout,)
        )
        self.reading_thread.start()

        # A tkinter loop that will show `self.stdout_data` on the screen
        self.screen_thread = StoppableThread(target=self.show_stdout)
        self.screen_thread.start()

    def push_progress_bar(self, value: float) -> None:
        """
        Pushes the progress bar forward.

        :param: value
            The value to use for pushing forward the progress bar position.

        """

        self.clover_progress_bar["value"] += value

    def show_stdout(self):
        """Read `self.stdout_data` and put the data in the GUI."""
        self.sub_process_label.config(
            text=self.stdout_data.strip("\n"), bootstyle=f"dark-inverse"
        )
        self.after(1, self.show_stdout)

    def stop(self, stopping=[]):
        """Stop subprocess and quit GUI."""
        clover_return_code = self.clover_thread.poll()

        self.clover_thread.kill()  # tell the subprocess to exit
        self.screen_thread.stop()
        self.sub_process_frame.enable_scrolling()

        # Enable the post-run button if the run completed successfully.
        self.push_progress_bar(100)

        if clover_return_code == 0:
            self.post_run_button.configure(state="enabled")
        else:
            self.clover_progress_bar.configure(bootstyle=f"{DANGER}-striped")
