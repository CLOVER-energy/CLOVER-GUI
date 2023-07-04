import tkinter as tk

import ttkbootstrap as ttk

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
        self.general_om_label = ttk.Label(self, text="General O&M Emissions")
        self.general_om_label.grid(row=1, column=1, sticky="w")
        self.general_om = tk.DoubleVar(value=0)

        self.general_om_entry = ttk.Entry(
        self, bootstyle=DANGER, textvariable=self.general_om
        )
        self.general_om_entry.grid(row=1, column=2, sticky="w")

        self.general_om_units = ttk.Label(self, text="kgCO2 p.a.")
        self.general_om_units.grid(row=1, column=3, sticky="w")

        # Miscellaneous Emissions
        self.misc_label = ttk.Label(self, text="Miscellaneous Emissions")
        self.misc_label.grid(row=2, column=1, sticky="w")
        self.misc = tk.DoubleVar(value=0)

        self.misc_entry = ttk.Entry(
            self, bootstyle=DANGER, textvariable=self.misc
        )
        self.misc_entry.grid(row=2, column=2, sticky="w")

        self.misc_units = ttk.Label(self, text="kgCO2 p.a.")
        self.misc_units.grid(row=2, column=3, sticky="w")

        # GHG Emissions from BOS
        self.bos_label = ttk.Label(self, text="GHG Emissions from BOS")
        self.bos_label.grid(row=3, column=1, sticky="w")
        self.bos = tk.DoubleVar(value=0)

        self.bos_entry = ttk.Entry(
            self, bootstyle=DANGER, textvariable=self.bos
        )
        self.bos_entry.grid(row=3, column=2, sticky="w")

        self.bos_units = ttk.Label(self, text="kgCO2/kWp")
        self.bos_units.grid(row=3, column=3, sticky="w")

        # GHG Emissions from Diesel Fuel
        self.diesel_fuel_label = ttk.Label(self, text="GHG Emissions from Diesel Fuel")
        self.diesel_fuel_label.grid(row=4, column=1, sticky="w")
        self.diesel_fuel = tk.DoubleVar(value=0)

        self.diesel_fuel_entry = ttk.Entry(
            self, bootstyle=DANGER, textvariable=self.diesel_fuel
        )
        self.diesel_fuel_entry.grid(row=4, column=2, sticky="w")
        
        self.diesel_fuel_units = ttk.Label(self, text="kgCO2/litre")
        self.diesel_fuel_units.grid(row=4, column=3, sticky="w")

        # GHG Emissions from Diesel O&M
        self.diesel_om_label = ttk.Label(self, text="GHG Emissions from Diesel O&M")
        self.diesel_om_label.grid(row=5, column=1, sticky="w")
        self.diesel_om = tk.DoubleVar(value=0)

        self.diesel_om_entry = ttk.Entry(
            self, bootstyle=DANGER, textvariable=self.diesel_om
        )
        self.diesel_om_entry.grid(row=5, column=2, sticky="w")

        self.diesel_om_units = ttk.Label(self, text="kgCO2/kWp")
        self.diesel_om_units.grid(row=5, column=3, sticky="w")

        # # GHG Emissions from Grid Extension
        # self.grid_extension_label = ttk.Label(self, text="GHG Emissions from Grid Extension")
        # self.grid_extension_label.grid(row=6, column=1, sticky="w")
        # self.grid_extension = tk.DoubleVar(value=0)

        # self.grid_extension_entry = ttk.Entry(
        #     self, bootstyle=DANGER, textvariable=self.grid_extension
        # )
        # self.grid_extension_entry.grid(row=6, column=2, sticky="w")

        # self.grid_extension_units = ttk.Label(self, text="kgCO2/km")
        # self.grid_extension_units.grid(row=6, column=3, sticky="w")

        # Initial Grid Emissions
        self.initial_grid_label = ttk.Label(self, text="Initial Grid Emissions")
        self.initial_grid_label.grid(row=7, column=1, sticky="w")
        self.initial_grid = tk.DoubleVar(value=0)

        self.initial_grid_entry = ttk.Entry(
            self, bootstyle=DANGER, textvariable=self.initial_grid
        )
        self.initial_grid_entry.grid(row=7, column=2, sticky="w")

        self.initial_grid_units = ttk.Label(self, text="kgCO2/kWh")
        self.initial_grid_units.grid(row=7, column=3, sticky="w")

        # Final Grid Emissions
        self.final_grid_label = ttk.Label(self, text="Final Grid Emissions")
        self.final_grid_label.grid(row=8, column=1, sticky="w")
        self.final_grid = tk.DoubleVar(value=0)

        self.final_grid_entry = ttk.Entry(
            self, bootstyle=DANGER, textvariable=self.final_grid
        )
        self.final_grid_entry.grid(row=8, column=2, sticky="w")

        self.final_grid_units = ttk.Label(self, text="kgCO2/kWh")
        self.final_grid_units.grid(row=8, column=3, sticky="w") 

        # GHG Emissions from Connection Costs
        self.households_label = ttk.Label(self, text="GHG Emissions from Connections")
        self.households_label.grid(row=9, column=1, sticky="w")
        self.households = tk.DoubleVar(value=0)

        self.households_entry = ttk.Entry(
            self, bootstyle=DANGER, textvariable=self.households
        )
        self.households_entry.grid(row=9, column=2, sticky="w")

        self.households_units = ttk.Label(self, text="kgCO2/household")
        self.households_units.grid(row=9, column=3, sticky="w")

        # GHG Emissions from Inverter
        self.inverter_label = ttk.Label(self, text="GHG Emissions from Inverter")
        self.inverter_label.grid(row=10, column=1, sticky="w")
        self.inverter = tk.DoubleVar(value=0)

        self.inverter_entry = ttk.Entry(
            self, bootstyle=DANGER, textvariable=self.inverter
        )
        self.inverter_entry.grid(row=10, column=2, sticky="w")

        self.inverter_units = ttk.Label(self, text="kgCO2/kWp")
        self.inverter_units.grid(row=10, column=3, sticky="w")

        # GHG Emissions inverter decrease
        self.inverter_decrease_label = ttk.Label(self, text="Inverter GHG Emissions decrease")
        self.inverter_decrease_label.grid(row=11, column=1, sticky="w")
        self.inverter_decrease = tk.DoubleVar(value=0)

        self.inverter_decrease_entry = ttk.Entry(
            self, bootstyle=DANGER, textvariable=self.inverter_decrease
        )
        self.inverter_decrease_entry.grid(row=11, column=2, sticky="w")

        self.inverter_decrease_units = ttk.Label(self, text="% p.a.")
        self.inverter_decrease_units.grid(row=11, column=3, sticky="w")

        # GHG Emissions from Kerosene
        self.kerosene_label = ttk.Label(self, text="GHG Emissions from Kerosene")
        self.kerosene_label.grid(row=12, column=1, sticky="w")
        self.kerosene = tk.DoubleVar(value=0)

        self.kerosene_entry = ttk.Entry(
            self, bootstyle=DANGER, textvariable=self.kerosene
        )
        self.kerosene_entry.grid(row=12, column=2, sticky="w")

        self.kerosene_units = ttk.Label(self, text="kgCO2/hour")
        self.kerosene_units.grid(row=12, column=3, sticky="w")

    


        """
        general:
        o&m: 200 # [kgCO2 p.a.]
        misc:
        ghgs: 0 # [kgCO2/kW]
        bos:
        ghgs: 200 # [kgCO2/kW]
        ghg_decrease: 2 # [% p.a.]
        diesel_fuel:
        ghgs: 2 # [kgCO2/litre]
        o&m: 10 # [kgCO2/kW p.a.]
        grid:
        extension_ghgs: 290000 # [kgCO2/km]
        infrastructure_GHGs: 1200000 # [kgCO2]
        initial_ghgs: 0.8 # [kgCO2/kWh]
        final_ghgs: 0.4 # [kgCO2/kWh]
        households:
        connection_ghgs: 10 # [kgCO2/household]
        inverter:
        ghgs: 75 # [kgCO2/kW]
        ghg_decrease: 2 # [2,% p.a.]
        lifetime: 4 # [years]
        size_increment: 1 # [kW]
        kerosene:
        ghgs: 0.055 # [kgCO2/hour]
        
        """