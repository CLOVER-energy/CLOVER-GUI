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

import time
import ttkbootstrap as ttk

from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import *

from .__utils__ import (
    MAIN_WINDOW_GEOMETRY,
)
from .configuration import ConfigurationScreen
from .load_location import LoadLocationWindow
from .main_menu import MainMenuScreen
from .new_location import NewLocationScreen
from .splash_screen import SplashScreenWindow


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
        self.splash = SplashScreenWindow(self, self.data_directory)

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
        self.splash.set_progress_bar_progerss(25)

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

    def load_location(self) -> None:
        """
        Called when the load-location button is deptressed in the load-location window.

        """

        self.load_location_window.display_progress_bar()

        time.sleep(0.5)
        self.load_location_window.set_progress_bar_progerss(25)
        time.sleep(0.5)
        self.load_location_window.set_progress_bar_progerss(50)
        time.sleep(0.5)
        self.load_location_window.set_progress_bar_progerss(75)
        time.sleep(0.5)
        self.load_location_window.set_progress_bar_progerss(100)

        self.load_location_window.withdraw()
        self.load_location_window.load_location_frame.pack_forget()
        self.main_menu_frame.pack_forget()
        self.configuration_screen.pack(fill="both", expand=True)

    def open_new_location_frame(self) -> None:
        """Opens the new-location frame."""

        self.main_menu_frame.pack_forget()
        self.new_location_frame.pack(fill="both", expand=True)

    def open_load_location_window(self) -> None:
        """Open the load-location window."""

        if self.load_location_window is None:
            self.load_location_window: LoadLocationWindow | None = LoadLocationWindow(self.load_location)
        else:
            self.load_location_window.deiconify()
        self.load_location_window.mainloop()

    def setup(self) -> None:
        """
        Setup the window.

        """

        # Main-menu
        self.main_menu_frame = MainMenuScreen(
             self.data_directory, self.open_load_location_window, self.open_new_location_frame,
        )
        self.splash.set_progress_bar_progerss(50)

        # New-location
        self.new_location_frame = NewLocationScreen(
            self.splash, self.create_new_location
        )
        self.new_location_frame.pack_forget()
        self.splash.set_progress_bar_progerss(75)

        # Load-location
        self.load_location_window = None

        # Configuration
        self.configuration_screen = ConfigurationScreen()
        self.splash.set_progress_bar_progerss(100)
        self.configuration_screen.pack_forget()

    def destroy_splash(self):
        self.splash.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
