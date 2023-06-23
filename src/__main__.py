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
import sys
import tkinter as tk
import time

from types import FunctionType

import ttkbootstrap as ttk

from RangeSlider.RangeSlider import RangeSliderH
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import *

from .__utils__ import BaseScreen

# CLOVER splash-screen image:
#   The name of the CLOVER splash-screen image.
CLOVER_SPLASH_SCREEN_IMAGE: str = "clover_splash_screen.png"

# Images directory:
#   The directory containing the images to display.
IMAGES_DIRECTORY: str = "images"

# Main-window geometry:
#   The geometry to use for the main window, specified in width and height.
MAIN_WINDOW_GEOMETRY: str = "1220x800"


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


# Screens
class SplashScreen(BaseScreen):
    """
    Represents a splash screen.

    """

    def __init__(self, parent, data_directory: str) -> None:
        """
        Instantiate the :class:`SplashScreen` instance.

        :param: parent
            The parent screen.

        :param: data_directory
            The path to the data directory.

        """

        tk.Toplevel(self, parent)

        self.title("CLOVER-GUI Splash")
        self.background_image = tk.PhotoImage(
            file=os.path.join(
                data_directory, IMAGES_DIRECTORY, CLOVER_SPLASH_SCREEN_IMAGE
            )
        )
        self.background_image = self.background_image.subsample(2)
        self.splash_label = tk.Label(self, image=self.background_image)
        self.splash_label.pack()

        # Create an updatable progress bar.
        self.progress_bar = ttk.Progressbar(
            self, bootstyle=f"{SUCCESS}-striped", mode="determinate"
        )
        self.progress_bar.pack(pady=20, padx=20, fill="x")
        self.progress_bar.start()

        # Disable the in-built minimise, maximise and close buttons.
        self.overrideredirect(True)

        # Required to make the splash screen visible.
        self.update()

    def set_progress_bar_progerss(self, value) -> None:
        """
        Sets the value of the progress bar.

        :param: value
            The value to use for setting the progress bar position.

        """

        self.progress_bar["value"] = value
        self.update()


class ConfigurationFrame(ttk.Frame):
    """
    Represents the configuration frame.

    The configure frame contains toggles for configuration top-level settings for each
    run.

    TODO: Update attributes.

    """

    def __init__(self, parent):
        super().__init__(parent)

        # TODO: Add configuration frame widgets and layout

class SimulationFrame(ttk.Frame):
    """
    Represents the simulation frame.

    The simulation frame contains the necessary parameters needed to launch a simulation
    in CLOVER as well as a launch button for initiating the run.

    TODO: Update attributes.

    """

    def __init__(self, parent):
        super().__init__(parent)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=4)
        self.columnconfigure(1, weight=1)

        self.start_year = tk.DoubleVar()
        self.end_year = tk.DoubleVar()

        self.years_slider = RangeSliderH(self, [self.start_year, self.end_year])

        self.years_slider.grid(parent, row=3, column=1, padx=20)

        # TODO: Add configuration frame widgets and layout

class OptimisationFrame(ttk.Frame):
    """
    Represents the optimisation frame.

    The optimisation frame contains the launch parameters needed for launching an
    optimisation in CLOVER as well as a launch button for initiating the run.

    TODO: Update attributes.

    """

    def __init__(self, parent):
        super().__init__(parent)

        # TODO: Add configuration frame widgets and layout

class ConfigurationScreen(ttk.Frame):
    """
    Represents the configuration screen.

    The configure screen contains tabbed information for configuring the screen.

    TODO: Update attributes.

    """

    def __init__(
        self,
    ) -> None:
        """
        Instantiate a :class:`ConfigureFrame` instance.

        """

        super().__init__()

        self.pack(fill="both", expand=True)

        self.configuration_notebook = ttk.Notebook(self, bootstyle=f"{INFO}")

        style = ttk.Style()
        style.configure("TNotebook.Tab", width=int(self.winfo_screenwidth() / 4))

        self.configuration_frame = ConfigurationFrame(self.configuration_notebook)
        self.configuration_notebook.add(self.configuration_frame, text="Configure")

        self.simulation_frame = ConfigurationFrame(self.configuration_notebook)
        self.configuration_notebook.add(self.simulation_frame, text="Simulate")

        self.optimisation_frame = ConfigurationFrame(self.configuration_notebook)
        self.configuration_notebook.add(self.optimisation_frame, text="Optimise")

        self.configuration_notebook.pack(fill="both", expand=True, padx=60, pady=40)

class MainMenuScreen(ttk.Frame):
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
        new_location_callback: FunctionType,
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


class NewLocationScreen(ttk.Frame):
    """
    Represents the new-location frame.

    The new-location frame enables a user to create a new location within CLOVER.

    TODO: Update attributes.

    """

    def __init__(
        self, splash_screen: SplashScreen, create_location_callback: FunctionType
    ) -> None:
        """
        Instantiate a :class:`MainMenuFrame` instance.

        :param: splash_screen
            The :class:`SplashScreen` being displayed.

        :param: create_location_callback:
            The callback function for when a new location is created.

        """

        super().__init__()

        self.pack(fill="both", expand=True)

        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=4)
        self.columnconfigure(4, weight=4)
        self.columnconfigure(5, weight=4)

        self.label = ttk.Label(
            self, text="Create a new location", style=f"{PRIMARY}", font=80
        )
        self.label.grid(row=0, column=3, columnspan=3, pady=10)

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
        x = max((self.winfo_screenwidth() // 2) - (width // 2), 0)
        y = max((self.winfo_screenheight() // 2) - (height // 2), 0)
        self.geometry(f"+{x}+{y}")

    def create_new_location(self) -> None:
        """Called when the create-location button is depressed."""

        self.new_location_frame.pack_forget()
        self.configuration_screen.pack(fill="both", expand=True)


    @property
    def data_directory(self) -> str:
        """The path to the data directory."""

        if self._data_directory is None:
            # self._data_directory: str | None = os.path.dirname(sys.executable)
            self._data_directory: str = "src"

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
        self.splash.set_progress_bar_progerss(25)

        # Main-menu
        self.main_menu_frame = MainMenuScreen(
            self.splash, self.open_new_location_frame, self.data_directory
        )
        self.splash.set_progress_bar_progerss(50)

        # New-location
        self.new_location_frame = NewLocationScreen(
            self.splash, self.create_new_location
        )
        self.new_location_frame.pack_forget()
        self.splash.set_progress_bar_progerss(75)

        # Configuration
        self.configuration_screen = ConfigurationScreen()
        self.splash.set_progress_bar_progerss(100)
        self.configuration_screen.pack_forget()

    def setup_menubar(self) -> None:
        """Setup the menu bar."""

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

    def destroy_splash(self):
        self.splash.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
