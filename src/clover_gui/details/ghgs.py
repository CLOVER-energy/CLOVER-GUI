#!/usr/bin/python3.10
########################################################################################
# ghgs.py - The ghgs module for CLOVER-GUI application.                                #
#                                                                                      #
# Author: Ben Winchester, Hamish Beath                                                 #
# Copyright: Ben Winchester, 2022                                                      #
# Date created: 23/06/2023                                                             #
# License: MIT, Open-source                                                            #
# For more information, contact: benedict.winchester@gmail.com                         #
########################################################################################

import tkinter as tk

from logging import Logger

import ttkbootstrap as ttk

from clover.impact import ImpactingComponent
from clover.impact.finance import *
from clover.impact.ghgs import (
    CONNECTION_GHGS,
    FINAL_GHGS,
    GHGS,
    GHG_DECREASE,
    INITIAL_GHGS,
    OM_GHGS,
)
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import *


__all__ = ("FinanceFrame",)


class GHGFrame(ttk.Frame):
    """
    Represents the Finance frame.

    Contains financial inputs for the system.

    TODO: Update attributes.

    """

    def __init__(self, parent):
        super().__init__(parent)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(7, weight=1)
        self.rowconfigure(8, weight=1)
        self.rowconfigure(9, weight=1)
        self.rowconfigure(10, weight=1)
        self.rowconfigure(11, weight=1)
        self.rowconfigure(12, weight=1)
        self.rowconfigure(13, weight=1)
        # self.rowconfigure(14, weight=1)
        # self.rowconfigure(15, weight=1)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)

        # General O&M Emissions
        self.general_om_label = ttk.Label(self, text="General O&M emissions")
        self.general_om_label.grid(row=1, column=1, sticky="w")
        self.general_om = ttk.DoubleVar(value=0)

        self.general_om_entry = ttk.Entry(self, textvariable=self.general_om)
        self.general_om_entry.grid(row=1, column=2, sticky="w")

        self.general_om_units = ttk.Label(self, text="kgCO2eq / year.")
        self.general_om_units.grid(row=1, column=3, sticky="w")

        # Miscellaneous Emissions
        self.misc_label = ttk.Label(self, text="Miscellaneous emissions")
        self.misc_label.grid(row=2, column=1, sticky="w")
        self.misc = ttk.DoubleVar(value=0)

        self.misc_entry = ttk.Entry(self, textvariable=self.misc)
        self.misc_entry.grid(row=2, column=2, sticky="w")

        self.misc_units = ttk.Label(self, text="kgCO2eq / kWp installed PV + kW installed diesel")
        self.misc_units.grid(row=2, column=3, sticky="w")

        # GHG Emissions from BOS
        self.bos_label = ttk.Label(self, text="GHG emissions from BOS")
        self.bos_label.grid(row=3, column=1, sticky="w")
        self.bos = ttk.DoubleVar(value=0)

        self.bos_entry = ttk.Entry(self, textvariable=self.bos)
        self.bos_entry.grid(row=3, column=2, sticky="w")

        self.bos_units = ttk.Label(self, text="kgCO2eq / kWp installed PV")
        self.bos_units.grid(row=3, column=3, sticky="w")

        self.bos_decrease_label = ttk.Label(self, text="BOS GHG emissions change")
        self.bos_decrease_label.grid(row=4, column=1, sticky="w")
        self.bos_decrease = ttk.DoubleVar(value=0)

        self.bos_decrease_entry = ttk.Entry(self, textvariable=self.bos_decrease)
        self.bos_decrease_entry.grid(row=4, column=2, sticky="w")

        self.bos_decrease_units = ttk.Label(self, text="% / year")
        self.bos_decrease_units.grid(row=4, column=3, sticky="w")

        # GHG Emissions from Connection Costs
        self.households_label = ttk.Label(self, text="GHG emissions from connections")
        self.households_label.grid(row=5, column=1, sticky="w")
        self.households = ttk.DoubleVar(value=0)

        self.households_entry = ttk.Entry(self, textvariable=self.households)
        self.households_entry.grid(row=5, column=2, sticky="w")

        self.households_units = ttk.Label(self, text="kgCO2eq / household")
        self.households_units.grid(row=5, column=3, sticky="w")

        # GHG Emissions from Inverter
        self.inverter_label = ttk.Label(self, text="GHG emissions from inverter(s)")
        self.inverter_label.grid(row=6, column=1, sticky="w")
        self.inverter = ttk.DoubleVar(value=0)

        self.inverter_entry = ttk.Entry(self, textvariable=self.inverter)
        self.inverter_entry.grid(row=6, column=2, sticky="w")

        self.inverter_units = ttk.Label(self, text="kgCO2eq / kW")
        self.inverter_units.grid(row=6, column=3, sticky="w")

        # GHG Emissions inverter decrease
        self.inverter_decrease_label = ttk.Label(
            self, text="Inverter GHG emissions change"
        )
        self.inverter_decrease_label.grid(row=7, column=1, sticky="w")
        self.inverter_decrease = ttk.DoubleVar(value=0)

        self.inverter_decrease_entry = ttk.Entry(
            self, textvariable=self.inverter_decrease
        )
        self.inverter_decrease_entry.grid(row=7, column=2, sticky="w")

        self.inverter_decrease_units = ttk.Label(self, text="% / year")
        self.inverter_decrease_units.grid(row=7, column=3, sticky="w")

        # GHG Emissions from Kerosene
        self.kerosene_label = ttk.Label(self, text="GHG emissions from kerosene")
        self.kerosene_label.grid(row=8, column=1, sticky="w")
        self.kerosene = ttk.DoubleVar(value=0)

        self.kerosene_entry = ttk.Entry(self, textvariable=self.kerosene)
        self.kerosene_entry.grid(row=8, column=2, sticky="w")

        self.kerosene_units = ttk.Label(self, text="kgCO2eq / hour")
        self.kerosene_units.grid(row=8, column=3, sticky="w")

    def set_ghg_inputs(
        self, ghg_inputs: dict[str, float | dict[str, float]], logger: Logger
    ) -> None:
        """
        Set the GHG inputs.

        :param: ghg_inputs
            The GHG inputs.

        :param: logger
            The :class:`logging.Logger` to use for the run.

        """

        self.general_om.set(ghg_inputs[ImpactingComponent.GENERAL.value][OM])
        self.general_om_entry.update()

        # Misc.
        self.misc.set(ghg_inputs[ImpactingComponent.MISC.value][GHGS])
        self.misc_entry.update()

        # BOS
        self.bos.set(ghg_inputs[ImpactingComponent.BOS.value][GHGS])
        self.bos_entry.update()

        self.bos_decrease.set(-(ghg_inputs[ImpactingComponent.BOS.value][GHG_DECREASE]))
        self.bos_decrease_entry.update()

        # Household
        self.households.set(
            ghg_inputs[ImpactingComponent.HOUSEHOLDS.value][CONNECTION_GHGS]
        )
        self.households_entry.update()

        # Inverter
        self.inverter.set(ghg_inputs[ImpactingComponent.INVERTER.value][GHGS])
        self.inverter_entry.update()

        self.inverter_decrease.set(
            -(ghg_inputs[ImpactingComponent.INVERTER.value][GHG_DECREASE])
        )
        self.inverter_decrease_entry.update()

        # Kerosene
        self.kerosene.set(ghg_inputs[ImpactingComponent.KEROSENE.value][GHGS])
        self.kerosene_entry.update()

    @property
    def as_dict(self) -> dict[str, dict[str, float] | float]:
        """
        Return the finance screen information as a `dict`.

        :return:
            The information as a `dict`.

        """

        return {
            ImpactingComponent.GENERAL.value: {OM: self.general_om.get()},
            ImpactingComponent.MISC.value: {GHGS: self.misc.get()},
            ImpactingComponent.BOS.value: {
                GHGS: self.bos.get(),
                GHG_DECREASE: -(self.bos_decrease.get()),
            },
            ImpactingComponent.HOUSEHOLDS.value: {
                CONNECTION_GHGS: self.households.get(),
            },
            ImpactingComponent.INVERTER.value: {
                GHGS: self.inverter.get(),
                GHG_DECREASE: -(self.inverter_decrease.get()),
            },
            ImpactingComponent.KEROSENE.value: {GHGS: self.kerosene.get()},
        }
