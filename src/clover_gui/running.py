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
from threading import Thread

# from tkinter.messagebox import showwarning
# import subprocess
# import xterm
import ttkbootstrap as ttk


from clover.scripts.clover import clover_main
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import *

from .__utils__ import BaseScreen, CLOVER_SPLASH_SCREEN_IMAGE, IMAGES_DIRECTORY

__all__ = ("RunScreen",)


class RunScreen(BaseScreen, show_navigation=False):

    """
    Represents the Run Screen.

    Displays running information when CLOVER is running simulation or optimisation.

    """

    def __init__(
        self,
        data_directory: str,
    ) -> None:
        """
        Instantiate a :class:`RunFrame` instance.

        :param: data_directory
            The path to the data directory.

        """

        super().__init__()

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.running_image = tk.PhotoImage(
            file=os.path.join(
                data_directory, IMAGES_DIRECTORY, CLOVER_SPLASH_SCREEN_IMAGE
            )
        )
        self.running_image = self.running_image.subsample(2)
        self.image_label = ttk.Label(self, image=self.running_image)
        self.image_label.grid(
            row=0, column=0, columnspan=2, sticky="news", padx=10, pady=5
        )

        self.clover_thread: Popen | None = None

        # Stop the clover thread with a button.
        self.stop_button = ttk.Button(
            self, text="STOP", bootstyle=f"{WARNING}-inverted", command=self.stop
        )
        self.stop_button.grid(row=1, column=1, padx=10, pady=5)

        self.sub_process_label = ttk.Label(self)  # put subprocess output here
        self.sub_process_label.grid(
            row=2, column=0, columnspan=2, sticky="news", padx=10, pady=5
        )

        # Create a buffer for the stdout
        self.stdout_data: ttk.StringVar = ttk.StringVar(self, "")

    def read_output(self, pipe: TextIOWrapper):
        """
        Read subprocess' output and store it in `self.stdout_data`.

        """
        while True:
            data = os.read(pipe.fileno(), 1 << 20)
            # Windows uses: "\r\n" instead of "\n" for new lines.
            data = data.replace(b"\r\n", b"\n")
            if data:
                self.stdout_data += data.decode()
            else:  # clean up
                self.root.after(5000, self.stop)  # stop in 5 seconds
                return None

    def run_with_clover(self, clover_thread: Popen) -> None:
        """
        Create a new thread that will read stdout and write the data to the buffer.

        :param: clover_thread
            A thread in which CLOVER runs.

        """

        self.clover_thread = clover_thread

        # Create a thread with the target to read the output.
        thread = Thread(target=self.read_output, args=(clover_thread.stdout,))
        thread.start()

        # A tkinter loop that will show `self.stdout_data` on the screen
        self.show_stdout()

    def show_stdout(self):
        """Read `self.stdout_data` and put the data in the GUI."""
        self.sub_process_label.config(text=self.stdout_data.strip("\n"))
        self.after(100, self.show_stdout)

    def stop(self, stopping=[]):
        """Stop subprocess and quit GUI."""
        if stopping:
            return  # avoid killing subprocess more than once
        stopping.append(True)

        self.clover_thread.terminate()  # tell the subprocess to exit

        # kill subprocess if it hasn't exited after a countdown
        def kill_after(countdown):
            if self.clover_thread.poll() is None:  # subprocess hasn't exited yet
                countdown -= 1
                if countdown < 0:  # do kill
                    self.clover_thread.kill()  # more likely to kill on *nix
                else:
                    self.after(1000, kill_after, countdown)
                    return  # continue countdown in a second

            self.clover_thread.stdout.close()  # close fd
            self.clover_thread.wait()  # wait for the subprocess' exit
            self.clover_thread.destroy()  # exit GUI

        kill_after(countdown=5)

        # label = tk.Label(root, text="CLOVER is running.")
        # label.pack(fill=tk.X)

        # xterm_frame = tk.Frame(root)
        # xterm_frame.pack(fill=tk.BOTH, expand=True)

        # xterm_frame_id = xterm_frame.winfo_id()

        # try:
        #     p = subprocess.Popen(
        #         ["xterm", "-into", str(xterm_frame_id), "-geometry", "80x20"],
        #         stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        # except FileNotFoundError:
        #     showwarning("Error", "xterm is not installed")
        #     raise SystemExit

        # root.mainloop()
