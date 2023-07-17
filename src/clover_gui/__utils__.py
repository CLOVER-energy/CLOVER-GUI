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
from typing import DefaultDict

import ttkbootstrap as ttk

from clover import read_yaml
from clover.generation.solar import PVPanel, SolarPanelType
from clover.simulation.storage_utils import Battery

__all__ = (
    "BaseScreen",
    "CLOVER_SPLASH_SCREEN_IMAGE",
    "IMAGES_DIRECTORY",
    "LOAD_LOCATION_GEOMETRY",
    "MAIN_WINDOW_GEOMETRY",
    "parse_solar_inputs",
)

# Battery inputs file:
#   The battery inputs file.
BATTERY_INPUTS_FILE: str = os.path.join("simulation", "battery_inputs.yaml")

# CLOVER splash-screen image:
#   The name of the CLOVER splash-screen image.
CLOVER_SPLASH_SCREEN_IMAGE: str = "clover_splash_screen.png"

# Details geometry:
#   The geometry to use for the details window.
DETAILS_GEOMETRY: str = "1080x720"

# Images directory:
#   The directory containing the images to display.
IMAGES_DIRECTORY: str = os.path.join("clover_gui", "images")

# Load-location geometry:
#   The geometry to use for the load-location window, specified in width and height.
LOAD_LOCATION_GEOMETRY: str = "800x600"

# Locations input file:
#   The locations input file.
LOCATIONS_INPUT_FILE: str = os.path.join("location_data", "location_inputs.yaml")

# Locations directory:
#   The name of the locations directory.
LOCATIONS_DIRECTORY: str = "locations"

# Main-window geometry:
#   The geometry to use for the main window, specified in width and height.
MAIN_WINDOW_GEOMETRY: str = "1220x800"

# Solar inputs file:
#   The solar inputs file.
SOLAR_INPUTS_FILE: str = os.path.join("generation", "solar_generation_inputs.yaml")

# Costs:
#   Keyword for costs.
_COSTS: str = "costs"

# Emissions:
#   Keyword for emissions.
_EMISSIONS: str = "emissions"

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
        entry[_NAME]: entry[_COSTS] for entry in battery_inputs
    }
    battery_emissions: dict[str, dict[str, float]] = {
        entry[_NAME]: entry[_EMISSIONS] for entry in battery_inputs
    }

    return batteries, battery_costs, battery_emissions


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
        for panel_input in solar_generation_inputs["panels"]
        if panel_input["type"] == SolarPanelType.PV.value
    ]

    # Determine the PV panel costs.
    try:
        pv_panel_costs: dict[str, DefaultDict[str, float]] = {
            pv_panel.name: [
                collections.defaultdict(float, panel_data[_COSTS])
                for panel_data in solar_generation_inputs["panels"]
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
                collections.defaultdict(float, panel_data[_EMISSIONS])
                for panel_data in solar_generation_inputs["panels"]
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
