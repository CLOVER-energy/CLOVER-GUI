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
import re
import tkinter as tk

from io import TextIOWrapper
from subprocess import Popen
from threading import Event, Thread
from typing import Callable, Pattern

import ttkbootstrap as ttk

from clover.scripts.clover import clover_main
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import *

from .__utils__ import BaseScreen, CLOVER_SPLASH_SCREEN_IMAGE, IMAGES_DIRECTORY

__all__ = ("RunScreen",)

# Beginning CLOVER simulation runs regex:
#   Regex used for determining whether CLOVER simulation runs are finished.
BEGINNING_CLOVER_RUNS_REGEX: Pattern[str] = re.compile(
    r"Beginning CLOVER (simulation|optimisation) runs \.*\s*\[\s*(?P<donefail>DONE|FAILED)\s*\]"
)

# CLOVER Optimisation regex:
#   Regex used for determining whether CLOVER is running an optimisation.
CLOVER_OPTIMISATION_REGEX: Pattern[str] = re.compile(
    r"Beginning CLOVER optimisation runs"
)

# Done-fail:
#   Match name for done-fail group.
DONE_FAIL: str = "donefail"

# Fail:
#   Keyword used for matching failed steps.
FAILED: str = "FAILED"

# Inputs file parsing regex:
#   Regx used for determining whether the input files were parsed successfully or not.
INPUTS_FILE_PARSING_REGEX: Pattern[str] = re.compile(
    r"Parsing input files \.*\s*\[\s*(?P<donefail>DONE|FAILED)\s*\]"
)

# Location verification regex:
#   Regex used for determining whether the location verification was successful or not.
LOCATION_VERIFICATION_REGEX: Pattern[str] = re.compile(
    r"Verifying location information \.*\s*\[\s*(?P<donefail>DONE|FAILED)\s*\]"
)

# Optimisation regex:
#   Regex used for determining whether CLOVER is running an optimisation.
OPTIMISATION_REGEX: Pattern[str] = re.compile(r"optimisations\:")

# Plots regex:
#   Regex used for determining whether the plots are being generated.
PLOTS_REGEX: Pattern[str] = re.compile(r"plots\:")

# Profile generation regex:
#   Regex used for determining whether the profile generation was successful or not.
PROFILE_GENERATION_REGEX: Pattern[str] = re.compile(
    r"Generating necessary profiles \.*\s*\[\s*(?P<donefail>DONE|FAILED)\s*\]"
)

# Renewables ninja error regex:
#   Regex used for determining whether a renewables.ninja error has occurred.
RENEWABLES_NINJA_ERROR_REGEX: Pattern[str] = re.compile(r"RenewablesNinjaError\(")

# Saving ouptut files regex:
#   Regec used for determinng whether CLOVER has begun saving ouptut files.
SAVING_OUTPUT_FILES_REGEX: Pattern[str] = re.compile(r"saving output files:")

# Simulation regex:
#   Regex used for determining whether CLOVER is running a simulation.
SIMULATION_REGEX: Pattern[str] = re.compile(r"Running a simulation with\:")


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
        self.rowconfigure(4, weight=1, minsize=80)

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

        # Create progress text
        self.message_text_label: ttk.Label = ttk.Label(
            self, bootstyle=SUCCESS, text="Launching CLOVER", font=("TkDefaultFont", 14)
        )
        self.message_text_label.grid(
            row=1, column=0, columnspan=4, sticky="w", padx=20, pady=5
        )

        # Create a progress bar
        self.clover_progress_bar: ttk.Progressbar = ttk.Progressbar(
            self, bootstyle=f"{SUCCESS}-striped", mode="determinate"
        )
        self.clover_progress_bar.grid(
            row=2, column=0, columnspan=4, sticky="ew", ipadx=60, padx=20, pady=5
        )

        # Stop the clover thread with a button.
        self.stop_button = ttk.Button(
            self, text="STOP", bootstyle=f"{DANGER}-inverted", command=self.stop
        )
        self.stop_button.grid(
            row=1, column=4, rowspan=2, padx=20, pady=5, ipadx=80, ipady=30, sticky="e"
        )

        self.sub_process_frame = ScrolledFrame(self)
        self.sub_process_frame.grid(
            row=3, column=0, columnspan=5, sticky="news", padx=10, pady=5
        )

        self.courier_style = ttk.Style()
        self.courier_style.configure("Courier.Label", font=("Courier", 16))

        self.sub_process_label = ttk.Label(
            self.sub_process_frame,
            bootstyle=f"{DARK}.Courier.Label",
            text="",
            width=300,
        )
        self.sub_process_label.grid(
            row=0, column=0, sticky="news", padx=10, pady=5, ipadx=300
        )

        # Add navigation buttons
        self.bottom_bar_frame = ttk.Frame(self)
        self.bottom_bar_frame.grid(
            row=4, column=0, columnspan=5, sticky="news", pady=20
        )

        self.bottom_bar_frame.columnconfigure(0, weight=1)
        self.bottom_bar_frame.columnconfigure(1, weight=1)
        self.bottom_bar_frame.columnconfigure(2, weight=1)
        self.bottom_bar_frame.columnconfigure(3, weight=10, minsize=400)
        self.bottom_bar_frame.columnconfigure(4, weight=1)

        self.back_button_image = ttk.PhotoImage(
            file=os.path.join(
                data_directory,
                IMAGES_DIRECTORY,
                "back_arrow.png",
            )
        )
        self.back_button = ttk.Button(
            self.bottom_bar_frame,
            bootstyle=f"{SECONDARY}-{OUTLINE}",
            command=lambda self=self: BaseScreen.go_back(self),
            image=self.back_button_image,
        )
        self.back_button.grid(
            row=0, column=0, padx=(60, 20), pady=(10, 0), ipadx=18, sticky="news"
        )

        self.home_button_image = ttk.PhotoImage(
            file=os.path.join(
                data_directory,
                IMAGES_DIRECTORY,
                "home_icon.png",
            )
        )
        self.home_button = ttk.Button(
            self.bottom_bar_frame,
            bootstyle=f"{SECONDARY}-{OUTLINE}",
            command=lambda self=self: BaseScreen.go_home(self),
            image=self.home_button_image,
        )
        self.home_button.grid(
            row=0, column=1, padx=20, pady=(10, 0), ipadx=18, sticky="news"
        )

        self.forward_button_image = ttk.PhotoImage(
            file=os.path.join(
                data_directory,
                IMAGES_DIRECTORY,
                "forward_arrow.png",
            )
        )
        self.forward_button = ttk.Button(
            self.bottom_bar_frame,
            bootstyle=f"{SECONDARY}-{OUTLINE}",
            command=lambda self=self: BaseScreen.go_forward(self),
            image=self.forward_button_image,
        )
        self.forward_button.grid(
            row=0, column=2, padx=20, pady=(10, 0), ipadx=18, sticky="news"
        )

        self.post_run_button = ttk.Button(
            self.bottom_bar_frame,
            bootstyle=SUCCESS,
            text="View outputs",
            command=self.open_post_run_screen,
            state=DISABLED,
        )
        self.post_run_button.grid(
            row=0, column=4, sticky="e", padx=20, pady=5, ipadx=80, ipady=20
        )

        # Create a buffer for the stdout
        self.stdout_data: str = " " * 180

    def _update_progress_bar_and_text(self, new_data: str) -> None:
        """
        Update the progress bar and explainer text based on the stdout data.

        :param: new_data
            The stdout output text.

        """

        if "Copyright" in new_data:
            self.message_text_label.configure(text="Verifying location")

        # Move the progress bar if location verification completed.
        if (
            location_verification_match := re.search(
                LOCATION_VERIFICATION_REGEX, new_data
            )
        ) is not None:
            if location_verification_match.group(DONE_FAIL) == FAILED:
                self.message_text_label.configure(
                    text="Location verification failed. Please check that all input\n"
                    "files are present. See below for more information",
                    style=DANGER,
                )
            else:
                self.push_progress_bar(20)
                self.message_text_label.configure(text="Parsing input files")

        # Move the progress bar if input files were successfully parsed.
        if (
            input_file_parsing_match := re.search(INPUTS_FILE_PARSING_REGEX, new_data)
        ) is not None:
            if input_file_parsing_match.group(DONE_FAIL) == FAILED:
                self.message_text_label.configure(
                    text="Input file parsing failed. Please check that all input \n"
                    "files are of the correct format. See below for more information",
                    style=DANGER,
                )
            else:
                self.push_progress_bar(20)
                self.message_text_label.configure(
                    text="Generating load profiles and fetching solar data"
                )

        # Move the progress bar if profiles were generated and fetched correctly.
        if (
            profile_generation_match := re.search(PROFILE_GENERATION_REGEX, new_data)
        ) is not None:
            if profile_generation_match.group(DONE_FAIL) == FAILED:
                self.message_text_label.configure(
                    text="Failed to generate load profiles. See below for more "
                    "information",
                    style=DANGER,
                )
            else:
                self.push_progress_bar(20)
                self.message_text_label.configure(text="Running CLOVER")

        # If renewables ninja failed, display an error.
        if re.search(RENEWABLES_NINJA_ERROR_REGEX, new_data) is not None:
            self.message_text_label.configure(
                text="Error fetching data from renewables.ninja. Please check your "
                "API \nkey under 'edit > preferences'."
            )

        # Update the message if a simulation is being run.
        if re.search(SIMULATION_REGEX, new_data) is not None:
            self.message_text_label.configure(text="Running a CLOVER simulation")

        # Update the message if an optimisation is being run.
        if re.search(OPTIMISATION_REGEX, new_data) is not None:
            self.message_text_label.configure(text="Running a CLOVER optimisation")

        # If CLOVER is generating plots, update the output
        if re.search(PLOTS_REGEX, new_data) is not None:
            self.message_text_label.configure(text="Generating plots")

        if re.search(SAVING_OUTPUT_FILES_REGEX, new_data) is not None:
            self.push_progress_bar(20)
            self.message_text_label.configure(text="Saving output files")

        if (
            clover_runs_match := re.search(BEGINNING_CLOVER_RUNS_REGEX, new_data)
        ) is not None:
            if clover_runs_match.group(DONE_FAIL) == FAILED:
                self.message_text_label.configure(
                    text="CLOVER runs failed. See below for more information."
                )
            else:
                self.push_progress_bar(20)
                self.message_text_label.configure(text="CLOVER runs completed")

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

                self._update_progress_bar_and_text(new_data)

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
        if clover_return_code == 0:
            self.post_run_button.configure(state="enabled")
            self.push_progress_bar(100)
        else:
            self.clover_progress_bar.configure(bootstyle=f"{DANGER}-striped")
