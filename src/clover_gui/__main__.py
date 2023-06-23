#!/usr/bin/python3.10
########################################################################################
# __main__.py - The main module for CLOVER-GUI application.                            #
#                                                                                      #
# Author: Ben Winchester, Hamish Beath                                                 #
# Copyright: Ben Winchester, 2022                                                      #
# Date created: 22/06/2023                                                             #
# License: MIT, Open-source                                                            #
# For more information, contact: benedict.winchester@gmail.com                         #
########################################################################################

import os
import tkinter as tk

from typing import Callable

import ttkbootstrap as ttk

from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import *

from .__utils__ import BaseScreen, CLOVER_SPLASH_SCREEN_IMAGE, IMAGES_DIRECTORY,  MAIN_WINDOW_GEOMETRY
from .configuration import ConfigurationScreen
from .splash_screen import SplashScreen


# All-purpose callback commands
def open_configuration() -> None:
    """
    Opens a user-pre-defined configuration.

    """

    pass


def save_configuration() -> None:
    """
    Saves the current configuration.

    """

    pass


def open_preferences_window() -> None:
    """
    Opens the user-preferences popup window.
    """

    pass


def open_help_window() -> None:
    """
    Opens the help popup window.
    """

    pass


class MainMenuScreen(BaseScreen, show_navigation=False):
    """
    Represents the main-menu frame.

    The main-menu frame contains two buttons:
        - A "new-location" button, which takes the user to a screen where they can set
          up a new location,
        - A "load-location" button, which creates a popup prompting the user to load an
          existing location.

    .. attribute:: label
        The label instance holding the main-menu image.

    .. attribute:: load_location_button
        A button which provides the user the option of loading an existing location.

    .. attribute:: main_menu_image
        The image to display at the top of the main-menu screen.

    .. attribute:: new_location_button
        A button which which provides the user the option of creating a new location.

    """

    def __init__(
        self,
        splash_screen: SplashScreen,
        new_location_callback: Callable,
        data_directory: str,
    ) -> None:
        """
        Instantiate a :class:`MainMenuFrame` instance.

        :param: splash_screen
            The splash screen, passed in to update the progress bar if necessary.

        :param: new_location_callback
            The callback function to use when the new-location button is pressed.

        :param: data_directory
            The name of the data directory to use.

        """

        super().__init__()

        self.pack(fill="both", expand=True)
        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.main_menu_image = tk.PhotoImage(
            file=os.path.join(
                data_directory, IMAGES_DIRECTORY, CLOVER_SPLASH_SCREEN_IMAGE
            )
        )
        self.main_menu_image = self.main_menu_image.subsample(2)
        self.label = ttk.Label(self, image=self.main_menu_image)
        self.label.grid(row=0, column=0, columnspan=2, sticky="news")

        self.new_location_button = ttk.Button(
            self,
            text="New location",
            bootstyle=f"{SUCCESS}-outline",
            command=new_location_callback,
        )
        self.new_location_button.grid(
            row=1, column=0, padx=5, pady=5, ipadx=80, ipady=20
        )

        self.load_location_button = ttk.Button(
            self, text="Load location", bootstyle=f"{PRIMARY}-outline"
        )
        self.load_location_button.grid(
            row=1, column=1, padx=5, pady=5, ipadx=80, ipady=20
        )


class NewLocationScreen(BaseScreen, show_navigation=True):
    """
    Represents the new-location frame.

    The new-location frame enables a user to create a new location within CLOVER.

    TODO: Update attributes.

    """

    def __init__(
        self, splash_screen: SplashScreen, create_location_callback: Callable
    ) -> None:
        """
        Instantiate a :class:`MainMenuFrame` instance.

        :param: splash_screen
            The :class:`SplashScreen` being displayed.

        :param: create_location_callback:
            The callback function for when a new location is created.

        """

        # Instntiate the parent class
        super().__init__()

        self.pack(fill="both", expand=True)

        # Set the physical distance weights of the rows and columns
        self.rowconfigure(0, weight=2)  # First row has the header
        self.rowconfigure(1, weight=1)  # These rows have entries
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)

        self.columnconfigure(0, weight=1)  # First three have forward, home, back
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=4)  # These three have the entries
        self.columnconfigure(4, weight=4)
        self.columnconfigure(5, weight=4)

        self.label = ttk.Label(
            self, text="Create a new location", style=f"{PRIMARY}", font=80
        )
        self.label.grid(row=0, column=0, columnspan=6, pady=10)

        self.new_location_label = ttk.Label(self, text="Location name")
        self.new_location_label.grid(row=1, column=3, sticky="e")

        self.new_location_entry = ttk.Entry(self, bootstyle="primary")
        self.new_location_entry.grid(
            row=1, column=4, padx=10, pady=5, sticky="e", ipadx=80
        )

        self.latitude_label = ttk.Label(self, text="Latitude")
        self.latitude_label.grid(row=2, column=3, sticky="e")

        self.latitude_entry = ttk.Entry(self, bootstyle="primary")
        self.latitude_entry.grid(row=2, column=4, padx=10, pady=5, sticky="e", ipadx=80)

        self.latitude_unit = ttk.Label(self, text="degrees North")
        self.latitude_unit.grid(row=2, column=5, padx=10, pady=5, sticky="w")

        self.longitude_label = ttk.Label(self, text="Longitude")
        self.longitude_label.grid(row=3, column=3, sticky="e")

        self.longitude_entry = ttk.Entry(self, bootstyle="primary")
        self.longitude_entry.grid(
            row=3, column=4, padx=10, pady=5, sticky="e", ipadx=80
        )

        self.longitude_unit = ttk.Label(self, text="degrees East")
        self.longitude_unit.grid(row=3, column=5, padx=10, pady=5, sticky="w")

        self.time_zone_label = ttk.Label(self, text="Time zone")
        self.time_zone_label.grid(row=4, column=3, sticky="e")

        self.time_zone_entry = ttk.Spinbox(
            self, bootstyle="primary", from_=-13, to=13, increment=0.25, format="%.2f"
        )
        self.time_zone_entry.grid(
            row=4, column=4, padx=10, pady=5, sticky="e", ipadx=68
        )

        self.time_zone_unit = ttk.Label(self, text="hours from UTC")
        self.time_zone_unit.grid(row=4, column=5, padx=10, pady=5, sticky="w")

        self.create_location_button = ttk.Button(
            self,
            text="Create",
            bootstyle=f"{PRIMARY}-outline",
            command=create_location_callback,
        )
        self.create_location_button.grid(
            row=5, column=5, padx=5, pady=5, ipadx=80, ipady=20, sticky="w"
        )


class App(ttk.Window):
    """
    Represents the main app window for user naviagtion.

    """

    def __init__(self) -> None:
        """Instantiate the CLOVER-GUI main app window."""

        # Set the theme and styles
        ttk.Window.__init__(self)
        self.theme = "journal"

        # Set attributes
        self._data_directory: str | None = None

        # Display the splash screen whilst loading
        self.withdraw()
        self.splash = SplashScreen(self, self.data_directory)

        # Setup the CLOVER-GUI application.
        self.title("CLOVER")

        # Setup the menubar
        self.menu_bar = ttk.Menu()

        # File menu
        self.file_menu = ttk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Open", command=open_configuration)
        self.file_menu.add_command(label="Save", command=save_configuration)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # Edit menu
        self.edit_menu = ttk.Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="Preferences", command=open_preferences_window)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)

        # Help menu
        self.help_menu = ttk.Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="Help", command=open_help_window)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)

        self.config(menu=self.menu_bar)
        self.splash.set_progress_bar_progerss(20)

        self.setup()

        # Show the window once setup is complete.
        self.geometry(MAIN_WINDOW_GEOMETRY)
        self.center_window()
        self.destroy_splash()
        self.deiconify()

    def center_window(self) -> None:
        """
        Helper function to aid centering the window.

        """

        self.update_idletasks()

        # Compute the x and y coordinates of the window based on the size of the screen.
        width = self.winfo_width()
        height = self.winfo_height()
        x_coordinate = max((self.winfo_screenwidth() // 2) - (width // 2), 0)
        y_coordinate = max((self.winfo_screenheight() // 2) - (height // 2), 0)
        self.geometry(f"+{x_coordinate}+{y_coordinate}")

    def create_new_location(self) -> None:
        """Called when the create-location button is depressed."""

        self.new_location_frame.pack_forget()
        self.configuration_screen.pack(fill="both", expand=True)

    @property
    def data_directory(self) -> str:
        """The path to the data directory."""

        if self._data_directory is None:
            # self._data_directory: str | None = os.path.dirname(sys.executable)
            self._data_directory = "src"

        return self._data_directory

    def open_new_location_frame(self) -> None:
        """Opens the new-location frame."""

        self.main_menu_frame.pack_forget()
        self.new_location_frame.pack(fill="both", expand=True)

    def setup(self) -> None:
        """
        Setup the window.

        """

        # Menu-bar
        self.setup_menubar()
        self.splash.set_progress_bar_progerss(40)

        # Main-menu
        self.main_menu_frame = MainMenuScreen(
            self.splash, self.open_new_location_frame, self.data_directory
        )
        self.splash.set_progress_bar_progerss(60)

        # New-location
        self.new_location_frame = NewLocationScreen(
            self.splash, self.create_new_location
        )
        self.new_location_frame.pack_forget()
        self.splash.set_progress_bar_progerss(80)

        # Configuration
        self.configuration_screen = ConfigurationScreen()
        self.splash.set_progress_bar_progerss(100)
        self.configuration_screen.pack_forget()

    def destroy_splash(self):
        self.splash.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
