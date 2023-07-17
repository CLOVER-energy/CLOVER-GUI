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
import ttkbootstrap as ttk

from clover import (
    get_logger,
    LOCATIONS_FOLDER_NAME,
    INPUTS_DIRECTORY,
    parse_input_files,
)
from clover.scripts.new_location import create_new_location
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import *

from .__utils__ import (
    MAIN_WINDOW_GEOMETRY,
    parse_battery_inputs,
    parse_solar_inputs,
    update_location_information,
)
from .configuration import ConfigurationScreen
from .details.details import DetailsWindow
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
        super().__init__()
        self.theme = "journal"

        # Set attributes
        self._data_directory: str | None = None
        self.logger = get_logger("clover_gui", False)
        self.system_lifetime: ttk.IntVar = ttk.IntVar(self, 30, "system_lifetime")

        # Setup the CLOVER-GUI application.
        self.withdraw()
        self.splash = SplashScreenWindow(self, self.data_directory)

        # Display the splash screen whilst loading
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

        # Return if not all the inputs have been provided.
        warning_messages: list[str] = []
        if (
            new_location_name := self.new_location_frame.new_location_entry.get()
        ) == "":
            warning_messages.append("name")
        if (latitude := self.new_location_frame.latitude_entry.get()) == "":
            warning_messages.append("latitude")
        if (longitude := self.new_location_frame.longitude_entry.get()) == "":
            warning_messages.append("longitude")
        if (time_zone := self.new_location_frame.time_zone_entry.get()) == "":
            warning_messages.append("time zone")

        if len(warning_messages) > 0:
            self.new_location_frame.warning_text_label.configure(
                text=f"Missing new-location {', '.join(warning_messages)}."
            )
            return

        # Create the new location.
        try:
            create_new_location(None, new_location_name, self.logger, False)
        except SystemExit:
            self.logger.error("New location name already used.")
            self.new_location_frame.warning_text_label.configure(
                text=f"Failed to create '{new_location_name}'. Check that the location "
                "does not already exist."
            )
            return

        self.inputs_directory_relative_path = os.path.join(
            LOCATIONS_FOLDER_NAME,
            new_location_name,
            INPUTS_DIRECTORY,
        )

        # Update the entries in the files wrt latitude, longitude and time zone.
        update_location_information(
            self.inputs_directory_relative_path,
            latitude,
            self.logger,
            longitude,
            time_zone,
        )

        # Open the location being considered.
        self.load_location(new_location_name)

        self.new_location_frame.pack_forget()
        self.configuration_screen.pack(fill="both", expand=True)

    @property
    def data_directory(self) -> str:
        """The path to the data directory."""

        if self._data_directory is None:
            # self._data_directory: str | None = os.path.dirname(sys.executable)
            self._data_directory = "src"

        return self._data_directory

    def load_location(self, load_location_name: str | None = None) -> None:
        """
        Called when the load-location button is deptressed in the load-location window.

        """

        if load_location_name is None:
            load_location_name = (
                self.load_location_window.load_location_frame.load_location_name.get()
            )

        self.load_location_window.display_progress_bar()

        # Parse input files
        (
            converters,
            device_utilisations,
            minigrid,
            finance_inputs,
            generation_inputs,
            ghg_inputs,
            grid_times,
            location,
            optimisation_inputs,
            optimisations,
            scenarios,
            simulations,
            electric_load_profile,
            water_source_times,
            input_file_info,
        ) = parse_input_files(
            False,
            None,
            load_location_name,
            self.logger,
            None,
        )
        self.load_location_window.set_progress_bar_progerss(
            10 * (percent_fraction := 1 / 12)
        )

        # Load the PV and battery input files as these are not returned in CLOVER as a whole
        self.inputs_directory_relative_path = os.path.join(
            LOCATIONS_FOLDER_NAME,
            load_location_name,
            INPUTS_DIRECTORY,
        )
        pv_panels, pv_panel_costs, pv_panel_emissions = parse_solar_inputs(
            self.inputs_directory_relative_path,
            self.logger,
        )

        batteries, battery_costs, battery_emissions = parse_battery_inputs(
            self.inputs_directory_relative_path, self.logger
        )

        # Set all inputs accordingly
        self.configuration_screen.configuration_frame.set_scenarios(scenarios)
        self.load_location_window.set_progress_bar_progerss(20 * percent_fraction)

        self.configuration_screen.simulation_frame.set_simulation(simulations[0])
        self.load_location_window.set_progress_bar_progerss(30 * percent_fraction)

        self.configuration_screen.optimisation_frame.set_optimisation(
            optimisations[0], optimisation_inputs
        )
        self.load_location_window.set_progress_bar_progerss(40 * percent_fraction)

        self.details_window.solar_frame.set_solar(
            pv_panels, pv_panel_costs, pv_panel_emissions
        )
        self.load_location_window.set_progress_bar_progerss(40 * percent_fraction)

        # self.details_window.solar_frame.set_solar(
        #     pv_panels, pv_panel_costs, pv_panel_emissions
        # )
        # self.load_location_window.set_progress_bar_progerss(50 * percent_fraction)

        self.details_window.storage_frame.set_batteries(
            batteries, battery_costs, battery_emissions
        )
        self.load_location_window.set_progress_bar_progerss(60 * percent_fraction)

        self.details_window.load_frame.set_loads(device_utilisations)
        self.load_location_window.set_progress_bar_progerss(70 * percent_fraction)

        self.details_window.diesel_frame.set_generators(minigrid.diesel_generator)
        self.details_window.diesel_frame.set_water_heaters(minigrid.diesel_water_heater)
        self.load_location_window.set_progress_bar_progerss(80 * percent_fraction)

        self.details_window.grid_frame.set_profiles(grid_times)
        self.load_location_window.set_progress_bar_progerss(90 * percent_fraction)

        self.details_window.finance_frame.set_finance_inputs(finance_inputs)
        self.load_location_window.set_progress_bar_progerss(100 * percent_fraction)

        self.details_window.ghgs_frame.set_ghg_inputs(ghg_inputs)
        self.load_location_window.set_progress_bar_progerss(110 * percent_fraction)

        self.details_window.system_frame.set_profiles(minigrid, scenarios)
        self.load_location_window.set_progress_bar_progerss(120 * percent_fraction)

        # Close the load-location window once completed
        self.load_location_window.withdraw()
        self.load_location_window.load_location_frame.pack_forget()
        self.main_menu_frame.pack_forget()
        self.configuration_screen.pack(fill="both", expand=True)

    def open_details_window(self) -> None:
        """Opens the details window."""

        if self.details_window is None:
            self.details_window: DetailsWindow | None = DetailsWindow()
        else:
            self.details_window.deiconify()
        self.details_window.mainloop()

    def open_new_location_frame(self) -> None:
        """Opens the new-location frame."""

        self.main_menu_frame.pack_forget()
        self.new_location_frame.pack(fill="both", expand=True)

    def open_load_location_window(self) -> None:
        """Open the load-location window."""

        if self.load_location_window is None:
            self.load_location_window: LoadLocationWindow | None = LoadLocationWindow(
                self.load_location
            )
        else:
            self.load_location_window.deiconify()
        self.load_location_window.mainloop()

    def setup(self) -> None:
        """
        Setup the window.

        """

        # Main-menu
        self.main_menu_frame = MainMenuScreen(
            self.data_directory,
            self.open_load_location_window,
            self.open_new_location_frame,
        )
        self.splash.set_progress_bar_progerss(40)

        # New-location
        self.new_location_frame = NewLocationScreen(
            self.splash, self.create_new_location
        )
        self.new_location_frame.pack_forget()
        self.splash.set_progress_bar_progerss(60)

        # Load-location
        self.load_location_window = None

        # Configuration
        self.configuration_screen = ConfigurationScreen(
            self.open_details_window, self.system_lifetime
        )
        self.splash.set_progress_bar_progerss(80)
        self.configuration_screen.pack_forget()

        # Details
        self.details_window: DetailsWindow | None = DetailsWindow(self.system_lifetime)
        self.details_window.withdraw()
        self.splash.set_progress_bar_progerss(100)

    def destroy_splash(self):
        self.splash.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
