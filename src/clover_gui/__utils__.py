#!/usr/bin/python3.10
########################################################################################
# __utils__.py - The utility module for CLOVER-GUI application.                        #
#                                                                                      #
# Author: Ben Winchester, Hamish Beath                                                 #
# Copyright: Ben Winchester, 2022                                                      #
# Date created: 23/06/2023                                                             #
# License: MIT, Open-source                                                            #
# For more information, contact: benedict.winchester@gmail.com                         #
########################################################################################

import collections
import os


from logging import Logger
from subprocess import PIPE, Popen, STDOUT

from typing import Any, DefaultDict

import ttkbootstrap as ttk

from clover import read_yaml
from clover.fileparser import DIESEL_CONSUMPTION, DIESEL_GENERATORS, MINIMUM_LOAD
from clover.simulation.diesel import DieselGenerator
from clover.generation.solar import PVPanel, SolarPanelType
from clover.scripts.clover import clover_main
from clover.simulation.storage_utils import Battery

__all__ = (
    "BaseScreen",
    "BATTERIES",
    "CLOVER_SPLASH_SCREEN_IMAGE",
    "clover_thread",
    "COSTS",
    "DEFAULT_END_YEAR",
    "DEFAULT_GUI_THEME",
    "DEFAULT_RENEWABLES_NINJA_TOKEN",
    "DEFAULT_START_YEAR",
    "DEFAULT_SYSTEM_LIFETIME",
    "DEVIES",
    "EMISSIONS",
    "END_YEAR",
    "GLOBAL_SETTINGS_FILEPATH",
    "IMAGES_DIRECTORY",
    "LOAD_LOCATION_GEOMETRY",
    "MAIN_WINDOW_GEOMETRY",
    "RENEWABLES_NINJA_TOKEN",
    "PANELS",
    "parse_battery_inputs",
    "parse_diesel_inputs",
    "parse_solar_inputs",
    "RENEWABLES_NINJA_DATA_PERIOD",
    "START_YEAR",
    "SYSTEM_LIFETIME",
    "THEME",
)

# Batteries:
#   Keyword for battery input information.
BATTERIES: str = "batteries"

# Battery inputs file:
#   The battery inputs file.
BATTERY_INPUTS_FILE: str = os.path.join("simulation", "battery_inputs.yaml")

# Clover icon image:
#   The name of the CLOVER icon to use.
CLOVER_ICON_IMAGE: str = "clover_logo.png"

# CLOVER splash-screen image:
#   The name of the CLOVER splash-screen image.
CLOVER_SPLASH_SCREEN_IMAGE: str = "clover_splash_screen_5_2.png"

# Costs:
#   Keyword for costs.
COSTS: str = "costs"

# Default end year:
#   The default end year.
DEFAULT_END_YEAR: int = 2016

# Default GUI theme:
#   The default theme for the GUI.
DEFAULT_GUI_THEME: str = "solar"

# Default renewables.ninja token:
#   The default text to display for the renewables.ninja token.
DEFAULT_RENEWABLES_NINJA_TOKEN: str = "CONFIGURE TOKEN IN PREFERENCES"

# Renewables-ninja data period:
#   The number of years for which the renewables.ninja interface needs to run.
RENEWABLES_NINJA_DATA_PERIOD: int = 9

# Default start year:
#   The deafult start year.
DEFAULT_START_YEAR: int = DEFAULT_END_YEAR - RENEWABLES_NINJA_DATA_PERIOD

# Default system lifetime:
#   The defailt lifetime for the system, in years.
DEFAULT_SYSTEM_LIFETIME: int = 30

# Details geometry:
#   The geometry to use for the details window.
DETAILS_GEOMETRY: str = "1080x800"

# Devices:
#   Keyword for device input information.
DEVICES: str = "devices"

# Diesel:
#   Keyword for diesel input information.
DIESEL: str = "diesel_inputs"

# Diesel inputs file:
#   The diesel inputs file.
DIESEL_INPUTS_FILE: str = os.path.join("generation", "diesel_inputs.yaml")

# Emissions:
#   Keyword for emissions.
EMISSIONS: str = "emissions"

# End year:
#   Keyword for end year.
END_YEAR: str = "end_year"

# Global settings filepath:
#   Path to the global-settings file.
GLOBAL_SETTINGS_FILEPATH: str = "global_settings.yaml"

# Images directory:
#   The directory containing the images to display.
IMAGES_DIRECTORY: str = os.path.join("images")

# Load-location geometry:
#   The geometry to use for the load-location window, specified in width and height.
LOAD_LOCATION_GEOMETRY: str = "800x600"

# Locations input file:
#   The locations input file.
LOCATIONS_INPUT_FILE: str = os.path.join("location_data", "location_inputs.yaml")

# Main-window geometry:
#   The geometry to use for the main window, specified in width and height.
MAIN_WINDOW_GEOMETRY: str = "1260x800"

# Max start year:
#   The maximum start year for renewables.ninja.
MAX_START_YEAR: int = 2007

# Min start year:
#   The minimum start year for renewables.ninja.
MIN_START_YEAR: int = 1985

# Panels:
#   Keyword for saving panel names.
PANELS: str = "panels"

# Renewables-ninja token:
#   Keyword for parsing the renewables.ninja token.
RENEWABLES_NINJA_TOKEN: str = "renewables_ninja_token"

# Start year:
#   Keyword for start year.
START_YEAR: str = "start_year"

# Solar inputs file:
#   The solar inputs file.
SOLAR_INPUTS_FILE: str = os.path.join("generation", "solar_generation_inputs.yaml")

# System lifetime:
#   Keyword for parsing the system lifetime.
SYSTEM_LIFETIME: str = "system_lifetime"

# Theme:
#   Keyword for parsing the GUI theme.
THEME: str = "theme"

# Emissions:
#   Keyword for emissions.
_LATITUDE: str = "latitude"

# Emissions:
#   Keyword for emissions.
_LONGITUDE: str = "longitude"

# Name:
#   Keyword for name.
_NAME: str = "name"

# Time zone:
#   Keyword for time zone.
_TIME_ZONE: str = "time_zone"


class BaseScreen(ttk.Frame):
    """
    Abstract class that represents a screen within the CLOVER-GUI application.

    .. attribute:: show_navigation
        Whether to show the navigation buttons.

    """

    # Private attributes:
    #   .. attribute:: _backward_journey
    #       Keeps track of the backward journey within the GUI.
    #
    #   .. attribute:: _forward_journey
    #       Keeps track of the forward journey within the GUI if applicable.
    #

    _backward_journey: list = []
    _forward_journey: list = []
    show_navigation: bool

    def __init_subclass__(cls, show_navigation: bool) -> None:
        """
        Sub-class hook to ensure that forward and backward navigation are present if
        applicable.

        :param: show_navigation

        """

        cls.show_navigation = show_navigation

        return super().__init_subclass__()

    @classmethod
    def add_screen_moving_forward(cls, screen: Any) -> None:
        """
        Add a screen to the backward journey.

        :param: screen
            The screen to add.

        """

        cls._backward_journey.append(screen)
        try:
            cls._forward_journey.pop()
        except IndexError:
            pass

    @classmethod
    def add_screen_moving_back(cls, screen: Any) -> None:
        """
        Add a screen to the backward journey.

        :param: screen
            The screen to add.

        """

        cls._forward_journey.append(screen)
        try:
            cls._backward_journey.pop()
        except IndexError:
            pass

    @classmethod
    def go_back(cls, self) -> None:
        """Go back a screen."""

        # Return if there is no frame to go back to.
        try:
            previous_frame = cls._backward_journey.pop()
        except IndexError:
            return

        self.pack_forget()

        cls._forward_journey.append(self)
        previous_frame.pack(fill="both", expand=True)

    @classmethod
    def go_forward(cls, self) -> None:
        """Go forward a screen."""

        # Return if there is no frame to go towards.
        try:
            next_frame = cls._forward_journey.pop()
        except IndexError:
            return

        self.pack_forget()

        cls._backward_journey.append(self)
        next_frame.pack(fill="both", expand=True)

    @classmethod
    def go_home(cls, self) -> None:
        """Go to the home screen."""

        # Assume that the home frame is the first frame in the journey.
        home_frame = cls._backward_journey[0]

        self.pack_forget()
        cls._backward_journey.append(self)

        home_frame.pack(fill="both", expand=True)


def clover_thread(clover_args: list[str]) -> Popen:
    """
    Run CLOVER in the background.

    :param: clover_args
        Arguments to pass through to CLOVER.

    """

    return Popen(["clover"] + clover_args, stdout=PIPE, stderr=STDOUT)


def parse_battery_inputs(
    inputs_directory_relative_path: str,
    logger: Logger,
) -> tuple[list[Battery, dict[str, dict[str, float], dict[str, float]]]]:
    """
    Parses the battery inputs file.

    :param: inputs_directory_relative_path
        The relative path to the inputs folder directory.
    :param: logger
            The :class:`logging.Logger` to use for the run.

    :returns:
        A `tuple` containing:
        - The `list` of :class:`storage_utils.Battery` instances defined;
        - The battery cost information;
        - The battery emissions information;

    """

    # Parse the battery inputs file.
    battery_inputs_filepath = os.path.join(
        inputs_directory_relative_path, BATTERY_INPUTS_FILE
    )
    battery_inputs = read_yaml(battery_inputs_filepath, logger)
    if not isinstance(battery_inputs, list):
        raise Exception("Battery input file is not of type `list`.")
    logger.info("Battery inputs successfully parsed.")

    batteries = [Battery.from_dict(entry) for entry in battery_inputs]
    battery_costs: dict[str, dict[str, float]] = {
        entry[_NAME]: entry[COSTS] for entry in battery_inputs
    }
    battery_emissions: dict[str, dict[str, float]] = {
        entry[_NAME]: entry[EMISSIONS] for entry in battery_inputs
    }

    return batteries, battery_costs, battery_emissions


def parse_diesel_inputs(
    inputs_directory_relative_path: str,
    logger: Logger,
) -> tuple[list[DieselGenerator, dict[str, dict[str, float], dict[str, float]]]]:
    """
    Parses the battery inputs file.

    :param: inputs_directory_relative_path
        The relative path to the inputs folder directory.
    :param: logger
            The :class:`logging.Logger` to use for the run.

    :returns:
        A `tuple` containing:
        - The `list` of :class:`generation.diesel.DieselGenerator` instances defined;
        - The diesel cost information;
        - The diesel emissions information;

    """

    # Parse the diesel inputs file.
    diesel_inputs_filepath = os.path.join(
        inputs_directory_relative_path, DIESEL_INPUTS_FILE
    )
    diesel_inputs = read_yaml(diesel_inputs_filepath, logger)
    if not isinstance(diesel_inputs, dict):
        raise Exception("Diesel input file is not of type `dict`.")
    logger.info("Diesel inputs successfully parsed.")

    diesel_generators: list[DieselGenerator] = [
        DieselGenerator(entry[DIESEL_CONSUMPTION], entry[MINIMUM_LOAD], entry[_NAME])
        for entry in diesel_inputs[DIESEL_GENERATORS]
    ]
    diesel_generator_costs: dict[str, dict[str, float]] = {
        entry[_NAME]: entry[COSTS] for entry in diesel_inputs[DIESEL_GENERATORS]
    }
    diesel_generator_emissions: dict[str, dict[str, float]] = {
        entry[_NAME]: entry[EMISSIONS] for entry in diesel_inputs[DIESEL_GENERATORS]
    }

    return diesel_generators, diesel_generator_costs, diesel_generator_emissions


def parse_solar_inputs(
    inputs_directory_relative_path: str,
    logger: Logger,
) -> tuple[list[PVPanel], dict[str, float], dict[str, float],]:
    """
    Parses the solar inputs file.

    :param: inputs_directory_relative_path:
        The relative path to the inputs folder directory.
    :param: logger
            The :class:`logging.Logger` to use for the run.

    :return:
        A `tuple` containing:
        - The `list` of :class:`solar.PVPanel` instances defined;
        - The pv-panel cost information;
        - The pv-panel emissions information;

    """

    solar_generation_inputs_filepath = os.path.join(
        inputs_directory_relative_path,
        SOLAR_INPUTS_FILE,
    )
    solar_generation_inputs = read_yaml(
        solar_generation_inputs_filepath,
        logger,
    )
    if not isinstance(solar_generation_inputs, dict):
        raise Exception("Solar generation inputs are not of type `dict`.")
    logger.info("Solar generation inputs successfully parsed.")

    # Parse the PV-panel information.
    pv_panels: list[PVPanel] = [
        PVPanel.from_dict(logger, panel_input)
        for panel_input in solar_generation_inputs[PANELS]
        if panel_input["type"] == SolarPanelType.PV.value
    ]

    # Determine the PV panel costs.
    try:
        pv_panel_costs: dict[str, DefaultDict[str, float]] = {
            pv_panel.name: [
                collections.defaultdict(float, panel_data[COSTS])
                for panel_data in solar_generation_inputs[PANELS]
                if panel_data[_NAME] == pv_panel.name
            ][0]
            for pv_panel in pv_panels
        }
    except (KeyError, IndexError):
        logger.error(
            "Failed to determine costs for PV panels.",
        )
        raise
    logger.info("PV panel costs successfully determined.")

    # Determine the PV panel emissions.
    try:
        pv_panel_emissions: dict[str, DefaultDict[str, float]] = {
            pv_panel.name: [
                collections.defaultdict(float, panel_data[EMISSIONS])
                for panel_data in solar_generation_inputs[PANELS]
                if panel_data[_NAME] == pv_panel.name
            ][0]
            for pv_panel in pv_panels
        }
    except (KeyError, IndexError):
        logger.error(
            "Failed to determine emissions for PV panels.",
        )
    logger.info("PV panel emissions successfully determined.")

    return (
        pv_panels,
        pv_panel_costs,
        pv_panel_emissions,
    )


def update_location_information(
    inputs_directory_relative_path: str,
    latitude: float,
    logger: Logger,
    longitude: float,
    timezone: int,
) -> None:
    """
    Called to update the location inputs when created.

    :param: latitude
        The latitude for the location to use.

    :param: logger
        The :class:`logging.Logger` to use.

    :param: longitude
        The longitude for the location to use

    :param: timezone
        The timezone for the location to use.

    """

    locations_inputs = read_yaml(
        os.path.join(inputs_directory_relative_path, LOCATIONS_INPUT_FILE), logger
    )
    locations_inputs[_LATITUDE] = latitude
    locations_inputs[_LONGITUDE] = longitude
    locations_inputs[_TIME_ZONE] = timezone
