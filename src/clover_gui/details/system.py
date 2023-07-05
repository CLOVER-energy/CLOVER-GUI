import tkinter as tk

import ttkbootstrap as ttk

from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import *


__all__ = ("FinanceFrame",)


class SystemFrame(ttk.Frame):
    """
    Represents the System frame.

    Contains System inputs for the system.

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
        self.rowconfigure(14, weight=1)
        self.rowconfigure(15, weight=1)
        self.rowconfigure(16, weight=1)
        self.rowconfigure(17, weight=1)
        self.rowconfigure(18, weight=1)
        self.rowconfigure(19, weight=1)
        self.rowconfigure(20, weight=1)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)

        """
        ac_transmission_efficiency: 0.95 # Efficiency of AC distribution network
        dc_transmission_efficiency: 0.95 # Efficiency of DC distribution network
        battery: default_battery
        # clean_water_tank: cold_water_tank
        conversion:
        dc_to_ac: 0.95 # Conversion efficiency (0.0-1.0)
        dc_to_dc: 0.95 # Conversion efficiency (0.0-1.0)
        ac_to_dc: 0.8 # Conversion efficiency (0.0-1.0)
        ac_to_ac: 0.98 # Conversion efficiency (0.0-1.0)
        diesel_generator: default_diesel
        # heat_exchanger: default_heat_exchanger
        # hot_water_tank: hot_water_tank
        pv_panel: default_pv
        # pvt_panel: default_pvt
        
        """

        # AC transmission efficiency
        self.ac_transmission_label = ttk.Label(self, text="AC transmission efficiency")
        self.ac_transmission_label.grid(row=1, column=1, sticky="w")

        self.ac_transmission = ttk.DoubleVar(self, 0, "ac_transmission")

        def scalar_ac_transmission(_):
            self.ac_tranmission.set(self.ac_tranmission_slider.get())
            # self.lifetime_capacity_loss_entry.configure(str(self.lifetime_capacity_loss.get()))
            self.ac_transmission_entry.update()

        self.ac_transmission_slider = ttk.Scale(
            self,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            length=320,
            command=scalar_ac_transmission,
            bootstyle=INFO,
            variable=self.ac_transmission,
            # state=DISABLED
        )
        self.ac_transmission_slider.grid(
            row=1, column=2, padx=10, pady=5, sticky="ew"
        )

        def enter_ac_transmission(_):
            self.ac_transmission.set(self.ac_transmission_entry.get())
            self.ac_transmission_slider.set(self.ac_transmission.get())

        self.ac_transmission_entry = ttk.Entry(
            self, bootstyle=INFO, textvariable=self.ac_transmission
        )
        self.ac_transmission_entry.grid(
            row=1, column=3, padx=10, pady=5, sticky="ew"
        )
        self.ac_transmission_entry.bind("<Return>", enter_ac_transmission)

        self.ac_transmission_unit = ttk.Label(self, text=f"%")
        self.ac_transmission_unit.grid(
            row=1, column=4, padx=10, pady=5, sticky="ew"
        )