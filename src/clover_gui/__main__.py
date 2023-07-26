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
import pkgutil
import ttkbootstrap as ttk

from logging import Logger
from subprocess import Popen

from clover import (
    get_logger,
    LOCATIONS_FOLDER_NAME,
    INPUTS_DIRECTORY,
    parse_input_files,
    read_yaml,
)
from clover.scripts.new_location import create_new_location
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import *

from .__utils__ import (
    BaseScreen,
    DEFAULT_GUI_THEME,
    DEFAULT_RENEWABLES_NINJA_TOKEN,
    DEFAULT_SYSTEM_LIFETIME,
    GLOBAL_SETTINGS_FILEPATH,
    MAIN_WINDOW_GEOMETRY,
    parse_battery_inputs,
    parse_diesel_inputs,
    parse_solar_inputs,
    RENEWABLES_NINJA_TOKEN,
    SYSTEM_LIFETIME,
    THEME,
    update_location_information,
)
from .configuration import ConfigurationScreen
from .details.details import DetailsWindow
from .load_location import LoadLocationWindow
from .main_menu import MainMenuScreen
from .new_location import NewLocationScreen
from .splash_screen import SplashScreenWindow
from .preferences import PreferencesWindow
from .post_run import PostRunScreen
from .running import RunScreen

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

        # Set attributes
        self._data_directory: str | None = None
        self.location_name: ttk.StringVar = ttk.StringVar(self, "")
        self.logger = get_logger("clover_gui", False)

        # Open the settings file
        renewables_ninja_token, system_lifetime, theme = self.read_global_settings(
            self.logger
        )
        self.renewables_ninja_token = renewables_ninja_token
        self.system_lifetime = system_lifetime
        self.theme = theme
        self.style.theme_use(self.theme.get())

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
        self.edit_menu.add_command(
            label="Preferences", command=self.open_preferences_window
        )
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)

        # Help menu
        self.help_menu = ttk.Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="Help", command=open_help_window)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)

        self.config(menu=self.menu_bar)
        self.splash.set_progress_bar_progress(20)

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

    def new_location_callback(self) -> None:
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

        self.new_location_progress_bar: ttk.Progressbar = ttk.Progressbar(
            self.new_location_frame, bootstyle=f"{SUCCESS}-striped", mode="determinate"
        )
        self.new_location_progress_bar.grid(
            row=7, column=0, columnspan=7, pady=5, padx=10, sticky="ew"
        )
        self.new_location_progress_bar.start()
        self.new_location_progress_bar["value"] = 0

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

        self.new_location_progress_bar["value"] = 50

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
        self.load_location(new_location_name, self.new_location_progress_bar)

        self.new_location_frame.pack_forget()
        BaseScreen.add_screen_moving_forward(self.new_location_frame)
        self.configuration_screen.pack(fill="both", expand=True)

    @property
    def data_directory(self) -> str:
        """The path to the data directory."""

        if self._data_directory is None:
            data_directory: str | None = pkgutil.get_data("clovergui", "data")
            if data_directory is None:
                data_directory = os.path.join("src", "clover_gui", "data")

            self._data_directory = data_directory

        return self._data_directory

    def load_location(
        self,
        load_location_name: str | None = None,
        progress_bar: ttk.Progressbar | None = None,
    ) -> None:
        """
        Called when the load-location button is deptressed in the load-location window.

        """

        if load_location_name is None:
            load_location_name = (
                self.load_location_window.load_location_frame.load_location_name.get()
            )

        if progress_bar is None:
            progress_bar = self.load_location_window.load_location_frame.progress_bar
            self.load_location_window.display_progress_bar()

        def set_progress_bar_progress(value) -> None:
            """
            Sets the value of the progress bar.

            :param: value
                The value to use for setting the progress bar position.

            """

            progress_bar["value"] = value
            self.update()
            if self.load_location_window is not None:
                self.load_location_window.update()
            self.new_location_frame.update()

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
        set_progress_bar_progress(100 * (percent_fraction := 1 / 12))

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

        diesel_generators, diesel_costs, diesel_emissions = parse_diesel_inputs(
            self.inputs_directory_relative_path, self.logger
        )

        # Set all inputs accordingly
        self.configuration_screen.configuration_frame.set_scenarios(scenarios)
        set_progress_bar_progress(200 * percent_fraction)

        self.configuration_screen.simulation_frame.set_simulation(simulations[0])
        set_progress_bar_progress(300 * percent_fraction)

        self.configuration_screen.optimisation_frame.set_optimisation(
            optimisations[0], optimisation_inputs
        )
        set_progress_bar_progress(400 * percent_fraction)

        self.details_window.solar_frame.set_solar(
            pv_panels, pv_panel_costs, pv_panel_emissions
        )
        set_progress_bar_progress(500 * percent_fraction)

        # self.details_window.solar_frame.set_solar(
        #     pv_panels, pv_panel_costs, pv_panel_emissions
        # )
        # set_progress_bar_progress(50 * percent_fraction)

        self.details_window.storage_frame.battery_frame.set_batteries(
            batteries, battery_costs, battery_emissions
        )
        set_progress_bar_progress(600 * percent_fraction)

        self.details_window.load_frame.set_loads(device_utilisations)
        set_progress_bar_progress(700 * percent_fraction)

        self.details_window.diesel_frame.generator_frame.set_generators(
            minigrid.diesel_generator, diesel_generators, diesel_costs, diesel_emissions
        )
        # self.details_window.diesel_frame.heater_frame.set_water_heaters(minigrid.diesel_water_heater)
        set_progress_bar_progress(800 * percent_fraction)

        self.details_window.grid_frame.set_profiles(grid_times)
        set_progress_bar_progress(900 * percent_fraction)

        self.details_window.finance_frame.set_finance_inputs(
            finance_inputs, self.logger
        )
        set_progress_bar_progress(1000 * percent_fraction)

        self.details_window.ghgs_frame.set_ghg_inputs(ghg_inputs, self.logger)
        set_progress_bar_progress(1100 * percent_fraction)

        self.details_window.system_frame.set_system(
            batteries, diesel_generators, minigrid, pv_panels
        )
        set_progress_bar_progress(1200 * percent_fraction)

        # Close the load-location window once completed
        if self.load_location_window is not None:
            self.load_location_window.withdraw()
            BaseScreen.add_screen_moving_forward(self.main_menu_frame)
        progress_bar.stop()
        progress_bar.grid_forget()
        self.main_menu_frame.pack_forget()
        self.configuration_screen.pack(fill="both", expand=True)
        self.location_name.set(load_location_name)

    def open_configuration_frame(self) -> None:
        """Opens the configuration frame after a CLOVER run."""

        self.post_run_screen.pack_forget()
        BaseScreen.add_screen_moving_forward(self.post_run_screen)
        self.configuration_screen.pack(fill="both", expand=True)

    def open_details_window(self, tab_id: int = 0) -> None:
        """Opens the details window."""

        if self.details_window is None:
            self.details_window: DetailsWindow | None = DetailsWindow(
                self.system_lifetime, self.renewables_ninja_token
            )
        else:
            self.details_window.deiconify()
        self.details_window.details_notebook.select(tab_id)
        self.details_window.mainloop()

    def open_new_location_frame(self) -> None:
        """Opens the new-location frame."""

        self.main_menu_frame.pack_forget()
        BaseScreen.add_screen_moving_forward(self.main_menu_frame)
        self.new_location_frame.pack(fill="both", expand=True)

    def open_new_location_frame_post_run(self) -> None:
        """Opens the new-location frame after a CLOVER run."""

        self.post_run_screen.pack_forget()
        BaseScreen.add_screen_moving_forward(self.post_run_screen)
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

    def open_load_location_window_post_run(self) -> None:
        """Open the load-location window after a CLOVER run."""

        if self.load_location_window is None:
            self.load_location_window: LoadLocationWindow | None = LoadLocationWindow(
                self.load_location
            )
        else:
            self.load_location_window.deiconify()
        self.load_location_window.mainloop()

    def open_post_run_screen(self) -> None:
        """Moves to the post-run screen."""

        self.run_screen.pack_forget()
        BaseScreen.add_screen_moving_forward(self.run_screen)
        self.post_run_screen.pack(fill="both", expand=True)

    def open_preferences_window(self) -> None:
        """
        Opens the user-preferences popup window.
        """

        if self.preferences_window is None:
            self.preferences_window: PreferencesWindow | None = PreferencesWindow(
                self.renewables_ninja_token,
                self.select_theme,
                self.system_lifetime,
                self.theme,
            )
        else:
            self.preferences_window.deiconify()
        self.preferences_window.mainloop()

    def open_run_screen(self, clover_thread: Popen) -> None:
        """Moves to the run page"""

        self.configuration_screen.pack_forget()
        BaseScreen.add_screen_moving_forward(self.configuration_screen)
        self.run_screen.pack(fill="both", expand=True)
        self.run_screen.stdout_data = ""
        self.run_screen.run_with_clover(clover_thread)

    def read_global_settings(
        self, logger: Logger
    ) -> tuple[ttk.IntVar, ttk.StringVar, ttk.StringVar]:
        """
        Read the global settings.

        :returns:
            - The renewables.ninja API token,
            - The system lifetime in years,
            - The theme.

        """

        try:
            global_settings_yaml = read_yaml(GLOBAL_SETTINGS_FILEPATH, logger)
        except FileNotFoundError:
            return (
                ttk.StringVar(self, DEFAULT_RENEWABLES_NINJA_TOKEN),
                ttk.IntVar(self, DEFAULT_SYSTEM_LIFETIME),
                ttk.StringVar(self, DEFAULT_GUI_THEME),
            )

        return (
            ttk.StringVar(
                self,
                global_settings_yaml.get(
                    RENEWABLES_NINJA_TOKEN, DEFAULT_RENEWABLES_NINJA_TOKEN
                ),
            ),
            ttk.IntVar(
                self, global_settings_yaml.get(SYSTEM_LIFETIME, DEFAULT_SYSTEM_LIFETIME)
            ),
            ttk.StringVar(self, global_settings_yaml.get(THEME, DEFAULT_GUI_THEME)),
        )

    def select_theme(self, theme: str) -> None:
        """Set the theme for the window."""
        self.style.theme_use(theme)

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
        self.splash.set_progress_bar_progress(40)

        # Preferences
        self.preferences_window: PreferencesWindow | None = None

        # New-location
        self.new_location_frame = NewLocationScreen(
            self.splash, self.new_location_callback
        )
        self.new_location_frame.pack_forget()
        self.splash.set_progress_bar_progress(60)

        # Load-location
        self.load_location_window: LoadLocationWindow | None = None

        # Configuration
        self.configuration_screen = ConfigurationScreen(
            self.data_directory,
            self.location_name,
            self.open_details_window,
            self.system_lifetime,
            self.open_run_screen,
        )
        self.configuration_screen.pack_forget()

        # Details
        self.details_window: DetailsWindow | None = DetailsWindow(
            self.system_lifetime, self.renewables_ninja_token
        )
        self.details_window.withdraw()
        self.splash.set_progress_bar_progress(80)

        # Run
        self.run_screen = RunScreen(self.data_directory, self.open_post_run_screen)

        # Post run
        self.post_run_screen = PostRunScreen(
            self.open_configuration_frame,
            self.open_load_location_window_post_run,
            self.open_new_location_frame_post_run,
        )

        self.splash.set_progress_bar_progress(100)

    def destroy_splash(self):
        self.splash.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
