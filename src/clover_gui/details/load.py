#!/usr/bin/python3.10
########################################################################################
# load.py - The load module for CLOVER-GUI application.                                #
#                                                                                      #
# Author: Ben Winchester, Hamish Beath                                                 #
# Copyright: Ben Winchester, 2022                                                      #
# Date created: 23/06/2023                                                             #
# License: MIT, Open-source                                                            #
# For more information, contact: benedict.winchester@gmail.com                         #
########################################################################################

import csv
import os
import platform
import subprocess
import tkinter as tk

from typing import Any, Callable

import pandas as pd
import ttkbootstrap as ttk

from clover.load.load import (
    AVAILABLE,
    DemandType,
    Device,
    DEVICE,
    ELECTRIC_POWER,
    INITIAL_OWNERSHIP,
    FINAL_OWNERSHIP,
    INNOVATION,
    IMITATION,
)
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import *
from ttkbootstrap.tableview import Tableview

__all__ = ("LoadFrame",)


# Default utilisation:
#   Default device utilisation to use.
DEFAULT_UTILISATION: pd.DataFrame = pd.DataFrame([[0] * 12] * 24)

# _Break:
#   Keyword used in the CSV code.
_BREAK: str = "break"

# _Months:
#   A `list` of all months.
_MONTHS: list[str] = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]


class GUIDevice:
    """
    Contains settings for a device.

    TODO: Update docstring.

    """

    def __init__(
        self,
        parent: Any,
        name: str,
        active: bool,
        electric_power: float,
        initial_ownership: float,
        final_ownership: float,
        innovation: float,
        imitation: float,
        device_type: DemandType,
        device_utilisation: pd.DataFrame,
        clean_water_consumption: float = 0,
    ) -> None:
        self.name: ttk.StringVar = ttk.StringVar(parent, name)
        self.electric_power: ttk.DoubleVar = ttk.DoubleVar(parent, electric_power)
        self.initial_ownership: ttk.DoubleVar = ttk.DoubleVar(parent, initial_ownership)
        self.final_ownership: ttk.DoubleVar = ttk.DoubleVar(parent, final_ownership)
        self.innovation: ttk.DoubleVar = ttk.DoubleVar(parent, innovation)
        self.imitation: ttk.DoubleVar = ttk.DoubleVar(parent, imitation)
        self.device_type: ttk.StringVar = ttk.StringVar(parent, device_type.value)
        self.clean_water_consumption: ttk.DoubleVar = ttk.DoubleVar(
            parent, clean_water_consumption
        )
        self.active: ttk.BooleanVar = ttk.BooleanVar(
            parent, active, f"{self.name}-active"
        )
        self.device_utilisation: pd.DataFrame = device_utilisation

    @property
    def as_dict(self) -> dict[str, bool | float | str]:
        """
        Return a dictionary containing the information about the device.

        :return:
            A dictionary representing the :class:`GUIDevice` for saving purposes.

        """

        return {
            DEVICE: self.name.get(),
            AVAILABLE: self.active.get(),
            ELECTRIC_POWER: self.electric_power.get(),
            INITIAL_OWNERSHIP: self.initial_ownership.get(),
            FINAL_OWNERSHIP: self.final_ownership.get(),
            IMITATION: self.imitation.get(),
            INNOVATION: self.innovation.get(),
            "type": self.device_type.get(),
        }

    @property
    def device_utilisation_columns(self) -> list[str]:
        """Return nice-looking column headers."""

        return _MONTHS

    @property
    def device_utilisation_row_data(self) -> Any:
        """
        Return the device-utilisation row data as entries.

        :return:
            A `list` where each entry is a `tuple` expressing the contents of the device
            utilisation.

        """

        return self.device_utilisation.to_numpy().tolist()


class CSVEntryFrame(ttk.Frame):
    """
    A CSVEntryFrame, taken from Sebastian Safari under MIT license.

    Please note, in addition to the license below, modifications have been made to
    tailor the software under the https://github.com/ssebs/csveditor repository such
    that it is appropriate to this specific use within the CLOVER-GUI application.

    License is as follows:

    Copyright (c) 2017 Sebastian Safari

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

    """

    cell_list: list[ttk.Entry | ttk.Text] = []
    current_cells: list[ttk.Entry | ttk.Text] = []
    current_cell: ttk.Entry | ttk.Text | None = None

    def __init__(self, master=None):
        """
        Instantiate the :class:`CSVEntryFrame` instance.

        :param: master
            The parent instance.

        """

        ttk.Frame.__init__(self, master)

        self.filename: str | None = None

        # Place the frame on the screen.
        self.grid()
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.columnconfigure(5, weight=1)
        self.columnconfigure(6, weight=1)
        self.columnconfigure(7, weight=1)
        self.columnconfigure(8, weight=1)
        self.columnconfigure(9, weight=1)
        self.columnconfigure(10, weight=1)
        self.columnconfigure(11, weight=1)
        self.columnconfigure(12, weight=1)

        # # Instantiate with a default set of widgets.
        # self.create_default_widgets()

    def focus_tab(self, event):
        """
        Focus which occurs when the tab key is pressed.

        :param: event
            The event instance.

        """

        event.widget.tk_focusNext().focus()
        return _BREAK

    def focus_sh_tab(self, event):
        event.widget.tk_focusPrev().focus()
        return _BREAK

    def focus_right(self, event):
        # event.widget.tk_focusNext().focus()
        widget = event.widget.focus_get()

        for row in range(len(self.current_cells)):
            for column in range(len(self.current_cells[0])):
                if widget == self.current_cells[row][column]:
                    if column >= len(self.current_cells[0]) - 1:
                        column = -1
                    self.current_cells[row][column + 1].focus()
        return _BREAK

    def focus_left(self, event):
        # event.widget.tk_focusNext().focus()
        widget = event.widget.focus_get()

        for row in range(len(self.current_cells)):
            for column in range(len(self.current_cells[0])):
                if widget == self.current_cells[row][column]:
                    if column == 0:
                        column = len(self.current_cells[0])
                    self.current_cells[row][column - 1].focus()
        return _BREAK

    def focus_up(self, event):
        # event.widget.tk_focusNext().focus()
        widget = event.widget.focus_get()

        for row in range(len(self.current_cells)):
            for column in range(len(self.current_cells[0])):
                if widget == self.current_cells[row][column]:
                    if row < 0:
                        row = len(self.current_cells)
                    self.current_cells[row - 1][column].focus()
        return _BREAK

    def focus_down(self, event):
        # event.widget.tk_focusNext().focus()
        widget = event.widget.focus_get()

        for row in range(len(self.current_cells)):
            for column in range(len(self.current_cells[0])):
                if widget == self.current_cells[row][column]:
                    if row >= len(self.current_cells) - 1:
                        row = -1
                    self.current_cells[row + 1][column].focus()
        return _BREAK

    def selectall(self, event):
        event.widget.tag_add("sel", "1.0", "end")
        event.widget.mark_set(INSERT, "1.0")
        event.widget.see(INSERT)
        return _BREAK

    def save_file(self, event):
        self.save_cells()

    # TODO: Create bind for arrow keys and enter

    def create_default_widgets(self):
        cell_width, cell_height = 7, 1
        self.size_x = 4
        self.size_y = 6
        self.default_cells = []
        for row in range(self.size_y):
            self.default_cells.append([])
            for column in range(self.size_x):
                self.default_cells[row].append([])

        for row in range(self.size_y):
            for column in range(self.size_x):
                tmp = ttk.Text(self, width=cell_width, height=cell_height)
                tmp.bind("<Tab>", self.focus_tab)
                tmp.bind("<Shift-Tab>", self.focus_sh_tab)
                tmp.bind("<Return>", self.focus_down)
                tmp.bind("<Shift-Return>", self.focus_up)
                tmp.bind("<Shift-Right>", self.focus_right)
                tmp.bind("<Shift-Left>", self.focus_left)
                tmp.bind("<Shift-Up>", self.focus_up)
                tmp.bind("<Shift-Down>", self.focus_down)
                tmp.bind("<Control-a>", self.selectall)
                tmp.bind("<Control-s>", self.save_file)
                # TODO: Add resize check on column when changing focus
                tmp.insert(END, "")
                tmp.grid(padx=2, pady=1, column=column, row=row, sticky="ew")

                self.default_cells[row][column] = tmp
                self.cell_list.append(tmp)

        self.default_cells[0][0].focus_force()
        self.current_cells = self.default_cells
        self.current_cell = self.current_cells[0][0]

        # TODO: Add buttons to create new rows/columns

    def new_cells(self):
        self.remove_cells()
        self.create_default_widgets()

    def remove_cells(self):
        while len(self.cell_list) > 0:
            for cell in self.cell_list:
                # print str(row) + str(column)
                cell.destroy()
                self.cell_list.remove(cell)

    def load_cells(self, filename: str):
        if self.filename is not None:
            self.save_cells()

        self.filename = filename
        ary = []
        col = -1
        rows = []

        # Create the file if it does not exist already, e.g., a new device.
        if not os.path.isfile(filename):
            with open(filename, "w", encoding="UTF-8") as new_csvfile:
                new_csvfile.write("\n".join(["0," * 11 + "0"] * 24))

        # get array size & get contents of rows
        with open(filename, "r", encoding="UTF-8") as csvfile:
            rd = csv.reader(csvfile, delimiter=",", quotechar='"')
            for row in rd:
                ary.append([])
                col = len(row)
                rows.append(row)

        # create the array
        for row in range(len(ary)):
            for column in range(col):
                ary[row].append([])

        # fill the array
        for row in range(len(ary)):
            for column in range(col):
                # print rows[row][column]
                ary[row][column] = rows[row][column]

        self.remove_cells()

        # Determine the maximum width of the cells
        # max_cell_width = 0
        # for row in range(len(ary)):
        #     for column in range(len(ary[0])):
        #         max_cell_width = max(len(ary[row][column]), max_cell_width)

        # Cap this at a specific width
        cell_width = 4

        load_cells = []
        for row in range(len(ary)):
            load_cells.append([])
            for column in range(len(ary[0])):
                load_cells[row].append([])

        # Create the labels
        for index, row in enumerate(range(len(ary) + 1)):
            if row == 0:
                tmp = ttk.Label(
                    self, width=cell_width, bootstyle=f"{SUCCESS}-{INVERSE}", text=""
                )
            else:
                tmp = ttk.Label(
                    self,
                    width=cell_width,
                    bootstyle=f"{SUCCESS}-{INVERSE}",
                    text=(" " if row < 10 else "") + str(row),
                )

            tmp.grid(
                padx=2,
                pady=1,
                column=0,
                row=row,
                sticky="ew",
            )

        for index, column in enumerate(range(len(ary[0]))):
            tmp = ttk.Label(
                self,
                width=cell_width,
                bootstyle=f"{SUCCESS}-{INVERSE}",
                text=_MONTHS[column],
            )
            tmp.grid(
                padx=(2, 2 if index != (len(ary[0]) - 1) else 15),
                pady=1,
                row=0,
                column=column + 1,
                sticky="ew",
            )

        # Create the new cells
        for row in range(len(ary)):
            for index, column in enumerate(range(len(ary[0]))):
                tmp = ttk.Entry(self, width=cell_width)
                tmp.bind("<Tab>", self.focus_tab)
                tmp.bind("<Shift-Tab>", self.focus_sh_tab)
                tmp.bind("<Shift-Return>", self.focus_up)
                tmp.bind("<Shift-Right>", self.focus_right)
                tmp.bind("<Shift-Left>", self.focus_left)
                tmp.bind("<Shift-Up>", self.focus_up)
                tmp.bind("<Shift-Down>", self.focus_down)
                tmp.bind("<Return>", lambda cell=tmp: self._round(cell))
                tmp.bind("<Control-a>", self.selectall)
                tmp.bind("<Control-s>", self.save_file)
                tmp.insert(END, ary[row][column])

                if row % 2 == 0:
                    tmp.config(bootstyle=f"{SUCCESS}")
                else:
                    tmp.config(bootstyle=f"{SECONDARY}")

                load_cells[row][column] = tmp
                tmp.focus_force()
                self.cell_list.append(tmp)

                tmp.grid(
                    padx=(2, 2 if index != (len(ary[0]) - 1) else 15),
                    pady=1,
                    column=column + 1,
                    row=row + 1,
                    sticky="ew",
                )

        self.current_cells = load_cells
        self.current_cell = self.current_cells[0][0]

    def _round(self, event) -> None:
        """
        Round a cell's value.

        :param: cell
            The cell to round.

        """

        cell = event.widget.focus_get()
        cell_value = cell.get()
        cell.delete(0, END)
        cell.insert(END, str(min(max(float(cell_value), 0), 1)))

    def save_cells(self):
        filename = self.filename

        vals = []
        for row in range(len(self.current_cells)):
            for column in range(len(self.current_cells[0])):
                vals.append(str(self.current_cells[row][column].get()).strip())

        with open(filename, "w", encoding="UTF-8") as csvfile:
            for rw in range(len(self.current_cells)):
                row = ""
                for row_index in range(len(self.current_cells[0])):
                    x = rw * len(self.current_cells[0])
                    if row_index != len(self.current_cells[0]) - 1:
                        row += vals[x + row_index] + ","
                    else:
                        row += vals[x + row_index]

                csvfile.write(row + "\n")

    def update_device_name(self, device_name: str) -> None:
        """
        Set the filename on the CSV editor with the updated device name.

        :param: device_name
            The new device name to set.

        """

        # Determine the new filename
        new_basename = f"{device_name}_times.csv"
        new_filename = os.path.join(os.path.dirname(self.filename), new_basename)

        # Copy and move the old file and set the filename attribute
        try:
            os.rename(self.filename, new_filename)
        except FileNotFoundError:
            pass

        self.filename = new_filename


class DeviceSettingsFrame(ttk.Labelframe):
    """
    Represents the device-settings frame.

    Contains settings the device selected.

    TODO: Update attributes.

    """

    def __init__(self, parent: Any, set_device_type: Callable):
        """
        Instantiate a :class:`DeviceSettingsFrame` instance.

        :param: parent
            The parent frame.

        :param: set_device_type
            Callable function to call when setting the device type.

        """
        super().__init__(parent, text="Device settings", style=SUCCESS)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.scrollable_frame = ScrolledFrame(
            self,
            # bootstyle=SUCCESS
        )
        self.scrollable_frame.grid(row=0, column=0, padx=0, pady=0, sticky="news")

        self.scrollable_frame.columnconfigure(0, weight=4)
        self.scrollable_frame.columnconfigure(1, weight=4)
        self.scrollable_frame.columnconfigure(2, weight=1)

        self.scrollable_frame.rowconfigure(0, weight=1)
        self.scrollable_frame.rowconfigure(1, weight=1)
        self.scrollable_frame.rowconfigure(2, weight=1)
        self.scrollable_frame.rowconfigure(3, weight=1)
        self.scrollable_frame.rowconfigure(4, weight=1)
        self.scrollable_frame.rowconfigure(5, weight=1)
        self.scrollable_frame.rowconfigure(6, weight=1)
        self.scrollable_frame.rowconfigure(7, weight=4)

        # Device name
        self.name_label = ttk.Label(
            self.scrollable_frame, text="Device name", style=SUCCESS
        )
        self.name_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.name_entry = ttk.Entry(
            self.scrollable_frame, textvariable=parent.active_device.name, style=SUCCESS
        )
        self.name_entry.grid(row=0, column=1, padx=10, pady=5, ipadx=10, sticky="ew")

        self.name_entry.bind("<Return>", parent.update_button_label)

        # Save device name button
        self.save_device_name_button = ttk.Button(
            self.scrollable_frame,
            bootstyle=f"{SUCCESS}-{TOOLBUTTON}",
            text="Save",
            command=parent.update_button_label,
        )
        self.save_device_name_button.grid(
            row=0, column=2, padx=10, pady=5, sticky="w", ipadx=20
        )

        # Device type
        self.device_type_label = ttk.Label(self.scrollable_frame, text="Load type")
        self.device_type_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.device_type_combobox = ttk.Combobox(
            self.scrollable_frame,
            textvariable=parent.active_device.device_type,
            style=SUCCESS,
        )
        self.device_type_combobox.grid(
            row=1, column=1, padx=10, pady=5, ipadx=10, sticky="ew"
        )
        self.device_type_combobox.bind("<<ComboboxSelected>>", set_device_type)

        self.device_type_combobox["values"] = [str(e.value) for e in DemandType]

        # Electric Power
        self.electric_power_label = ttk.Label(
            self.scrollable_frame, text="Electric Power"
        )
        self.electric_power_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.electric_power_entry = ttk.Entry(
            self.scrollable_frame,
            textvariable=parent.active_device.electric_power.get(),
        )
        self.electric_power_entry.grid(
            row=2, column=1, padx=10, pady=5, sticky="ew", ipadx=10
        )

        self.electric_power_unit = ttk.Label(self.scrollable_frame, text="W (Watts)")
        self.electric_power_unit.grid(row=2, column=2, padx=10, pady=5, sticky="w")

        # Initial Ownership
        self.initial_ownership_label = ttk.Label(
            self.scrollable_frame, text="Initial Ownership"
        )
        self.initial_ownership_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        self.initial_ownership_entry = ttk.Entry(
            self.scrollable_frame,
            textvariable=parent.active_device.initial_ownership.get(),
        )
        self.initial_ownership_entry.grid(
            row=3, column=1, padx=10, pady=5, sticky="ew", ipadx=10
        )

        self.initial_ownership_unit = ttk.Label(
            self.scrollable_frame, text="devices / household"
        )
        self.initial_ownership_unit.grid(row=3, column=2, padx=10, pady=5, sticky="w")

        # Final Ownership
        self.final_ownership_label = ttk.Label(
            self.scrollable_frame, text="Final Ownership"
        )
        self.final_ownership_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")

        self.final_ownership_entry = ttk.Entry(
            self.scrollable_frame,
            textvariable=parent.active_device.final_ownership.get(),
        )
        self.final_ownership_entry.grid(
            row=4, column=1, padx=10, pady=5, sticky="ew", ipadx=10
        )

        self.final_ownership_unit = ttk.Label(
            self.scrollable_frame, text="devices / household"
        )
        self.final_ownership_unit.grid(row=4, column=2, padx=10, pady=5, sticky="w")

        # Innovation
        self.innovation_label = ttk.Label(self.scrollable_frame, text="Innovation")
        self.innovation_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")

        self.innovation_entry = ttk.Entry(
            self.scrollable_frame, textvariable=parent.active_device.innovation.get()
        )
        self.innovation_entry.grid(
            row=5, column=1, padx=10, pady=5, sticky="ew", ipadx=10
        )

        self.innovation_unit = ttk.Label(self.scrollable_frame, text="innovation_units")
        self.innovation_unit.grid(row=5, column=2, padx=10, pady=5, sticky="w")

        # Imitation
        self.imitation_label = ttk.Label(self.scrollable_frame, text="Imitation")
        self.imitation_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")

        self.imitation_entry = ttk.Entry(
            self.scrollable_frame, textvariable=parent.active_device.imitation.get()
        )
        self.imitation_entry.grid(
            row=6, column=1, padx=10, pady=5, sticky="ew", ipadx=10
        )

        self.imitation_unit = ttk.Label(self.scrollable_frame, text="imitation unit")
        self.imitation_unit.grid(row=6, column=2, padx=10, pady=5, sticky="w")

        # Clean Water Consumption
        self.clean_water_consumption_label = ttk.Label(
            self.scrollable_frame, text="Clean Water Consumption"
        )
        self.clean_water_consumption_label.grid(
            row=7, column=0, padx=10, pady=5, sticky="w"
        )

        self.clean_water_consumption_entry = ttk.Entry(
            self.scrollable_frame,
            textvariable=parent.active_device.clean_water_consumption.get(),
            state=DISABLED,
        )
        self.clean_water_consumption_entry.grid(
            row=7,
            column=1,
            padx=10,
            pady=5,
            sticky="ew",
            ipadx=10,
        )

        self.clean_water_consumption_unit = ttk.Label(
            self.scrollable_frame, text="litres / hour", style=SUCCESS, state=DISABLED
        )
        self.clean_water_consumption_unit.grid(
            row=7, column=2, padx=10, pady=5, sticky="w"
        )

        # Empty row
        self.empty_row = ttk.Label(self.scrollable_frame, text="")
        self.empty_row.grid(row=8, column=0, columnspan=3, padx=10, pady=5, sticky="w")

        # Line separator
        self.line_separator = ttk.Separator(self.scrollable_frame, orient="horizontal")
        self.line_separator.grid(
            row=9, column=0, columnspan=3, padx=10, pady=5, sticky="ew"
        )

        # Device Utilisation Header
        # bold_head = ttk.Style()
        # bold_head.configure("Bold.TLabel", font=("TkDefaultFont", 13, "bold"))
        self.device_utilisation_header = ttk.Label(
            self.scrollable_frame,
            text="Device Utilisation Profile",
            style=SUCCESS,
            font=("TkDefaultFont", 12, "bold"),
        )
        self.device_utilisation_header.grid(
            row=10, column=0, padx=10, pady=5, sticky="w", columnspan=3
        )

        self.edit_file_text = ttk.Label(
            self.scrollable_frame,
            text="Edit the device utilisation below or in your native CSV editor",
        )
        self.edit_file_text.grid(
            row=11, column=0, padx=10, pady=5, sticky="news", columnspan=2
        )

        self.edit_file_button = ttk.Button(
            self.scrollable_frame,
            command=parent.open_utilisation_profile_file,
            bootstyle=f"{SUCCESS}",
            text="Edit file",
        )
        if platform.system() != "Windows":
            self.edit_file_button.grid(
                row=11, column=2, padx=10, pady=5, ipadx=20, sticky="ew"
            )

        # Device utilisation
        self.csv_entry_frame: CSVEntryFrame = CSVEntryFrame(
            master=self.scrollable_frame,
        )
        self.csv_entry_frame.grid(
            row=12, column=0, columnspan=3, sticky="news", padx=5, pady=5
        )


class DevicesFrame(ScrolledFrame):
    """
    Represents the scrollable frame where devices can be selected.

    TODO: Update attributes.

    """

    def __init__(
        self, parent, select_device: Callable, update_device_settings_frame: Callable
    ):
        super().__init__(parent)

        # Duplicate functional call
        self.update_device_settings_frame = update_device_settings_frame

        self.device_active_buttons: dict[GUIDevice, ttk.Button] = {
            device: ttk.Checkbutton(
                self,
                style=f"{SUCCESS}.{ROUND}.{TOGGLE}",
                variable=device.active,
            )
            for device in parent.devices
        }

        self.device_selected_buttons: dict[GUIDevice, ttk.Button] = {
            device: ttk.Button(
                self,
                text=device.name.get().capitalize(),
                style=f"{SUCCESS}.{OUTLINE}",
            )
            for device in parent.devices
        }

        for index, button in enumerate(self.device_active_buttons.values()):
            # Check button
            button.grid(row=index, column=0, padx=10, pady=5)

        for index, button in enumerate(self.device_selected_buttons.values()):
            button.grid(row=index, column=1, padx=10, pady=5, sticky="w")


class LoadFrame(ttk.Frame):
    """
    Represents the Load frame.

    Contains settings for load management.

    TODO: Update attributes.

    """

    def __init__(self, parent):
        super().__init__(parent)

        self.device_utilisations_directory: str | None = None

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1, minsize=100)
        self.columnconfigure(2, weight=1, minsize=300)
        self.columnconfigure(3, weight=3, minsize=300)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=8, minsize=400)

        self.devices = [
            GUIDevice(
                self,
                "light",
                True,
                3,
                2,
                4,
                0.04,
                0.5,
                DemandType.DOMESTIC,
                DEFAULT_UTILISATION,
            ),
        ]

        self.active_device: GUIDevice = self.devices[0]

        # Create the from-file vs auto-genrated entry
        self.from_file: ttk.BooleanVar = ttk.BooleanVar(self, False)
        self.from_file_button = ttk.Checkbutton(
            self,
            command=self._from_file_callback,
            bootstyle=f"{SUCCESS}-{TOOLBUTTON}",
            text="From an input file",
            variable=self.from_file,
        )
        self.from_file_button.grid(
            row=0, column=0, padx=10, pady=5, ipadx=20, sticky="ew"
        )

        self.open_file_button = ttk.Button(
            self,
            command=self._open_load_file,
            bootstyle=f"{SUCCESS}",
            text="Select file",
            state=DISABLED,
        )
        self.open_file_button.grid(
            row=0, column=1, padx=10, pady=5, ipadx=20, sticky="ew"
        )

        self.filename: ttk.StringVar = ttk.StringVar(self, "")
        self.load_file_path_entry = ttk.Entry(
            self,
            bootstyle=f"{SUCCESS}-inverted",
            textvariable=self.filename,
            state=DISABLED,
        )
        self.load_file_path_entry.grid(
            row=0, column=2, columnspan=3, padx=10, pady=5, sticky="ew"
        )

        self.from_utilisations: ttk.BooleanVar = ttk.BooleanVar(self, True)
        self.generate_loads_button = ttk.Checkbutton(
            self,
            command=self._from_utilisations_callback,
            bootstyle=f"{SUCCESS}-{TOOLBUTTON}",
            text="From device utilisations",
            variable=self.from_utilisations,
        )
        self.generate_loads_button.grid(
            row=1, column=0, padx=10, pady=5, ipadx=20, sticky="ew"
        )

        # Place a seperator between the two
        self.separator = ttk.Separator(self, orient="horizontal")
        self.separator.grid(
            row=2, column=0, pady=5, padx=10, columnspan=4, sticky="news"
        )

        # Create the right-hand frame for adjusting device settings
        self.settings_frame = DeviceSettingsFrame(self, self.set_device_type)
        self.settings_frame.grid(
            row=3, column=1, columnspan=3, padx=20, pady=10, sticky="news", rowspan=2
        )

        # Create the button for creating devices
        self.add_device_button = ttk.Button(
            self,
            bootstyle=f"{SUCCESS}-{OUTLINE}",
            command=self.add_device,
            text="New device",
        )
        self.add_device_button.grid(row=3, column=0, padx=10, pady=5, ipadx=80)

        # Create the left-hand frame for selecting the devices
        self.devices_frame = DevicesFrame(
            self, self.select_device, self.update_device_settings_frame
        )
        self.devices_frame.grid(row=4, column=0, padx=20, pady=10, sticky="news")

        for device, button in self.devices_frame.device_selected_buttons.items():
            button.configure(command=lambda device=device: self.select_device(device))

        self.select_device(self.devices[0])

    def _from_file_callback(self) -> None:
        """Function called when the 'from-file button' is depressed."""

        # Update the toggle buttons.
        self.from_file.set(True)
        self.from_utilisations.set(False)

        # Update the load button
        self.open_file_button.configure(state=(_enabled := "enabled"))
        self.load_file_path_entry.configure(state=_enabled)

        # Update the device frames
        for child in self.devices_frame.winfo_children():
            child.configure(state=DISABLED)

        self.add_device_button.configure(state=DISABLED)

        for child in self.settings_frame.scrollable_frame.winfo_children():
            child.configure(state=DISABLED)

        # for row in self.settings_frame.scrollable_frame.csv_entry_frame.current_cells:
        #     for cell in row:
        #         cell.configure(state=DISABLED)

    def _from_utilisations_callback(self) -> None:
        """Function called when the 'from-utilisation button' is depressed."""

        # Update the toggle buttons.
        self.from_file.set(False)
        self.from_utilisations.set(True)

        # Update the load button
        self.open_file_button.configure(state=DISABLED)
        self.load_file_path_entry.configure(state=DISABLED)

        # Update the device frames
        for child in self.devices_frame.winfo_children():
            child.configure(state="enabled")

        self.add_device_button.configure(state="enabled")

        for child in self.settings_frame.scrollable_frame.winfo_children():
            child.configure(state="enabled")

        # for row in self.settings_frame.scrollable_frame.csv_entry_frame.current_cells:
        #     for cell in row:
        #         cell.configure(state="enabled")

    def open_utilisation_profile_file(self) -> None:
        """
        Function called when the open-utilisation file button is depressed.

        The open-utilisation button enables a user to edit a device's utilsiation
        profile in their native CSV editor. When depressed, this button should cause the
        native CSV editor to load.

        """

        subprocess.Popen(["open", self.settings_frame.csv_entry_frame.filename])

    def _open_load_file(self) -> None:
        """Function called when the open-load file button is depressed."""

        self.filename.set(tk.filedialog.askopenfilename())

    def add_device(
        self,
        seed_device: Device | None = None,
        seed_utilisation: pd.DataFrame = DEFAULT_UTILISATION,
        batch_loading: bool = False,
    ) -> None:
        """
        Creates a new device when called.

        :param: seed_device
            If specified, the :class:`clover.load.load.Device` to use to determine
            parameters for the device.

        :param: seed_utilisation
            If specified, the seed device utilisation profile.

        :param: batch_loading
            Whether multiple devices are being loaded (True) or a single device is being
            added (False).

        """

        if seed_device is None:
            # Determine the name of the new device
            new_name = "New_device{suffix}"
            index = 0
            suffix = ""
            while new_name.format(suffix=suffix) in {
                entry.name.get() for entry in self.devices
            }:
                index += 1
                suffix = f"_{index}"

            new_name = new_name.format(suffix=suffix)

            # Create the new device and select it.
            self.devices.append(
                (
                    device := GUIDevice(
                        self,
                        new_name,
                        True,
                        0,
                        0,
                        0,
                        0,
                        0,
                        DemandType.DOMESTIC,
                        seed_utilisation,
                    )
                )
            )

        else:
            self.devices.append(
                (
                    device := GUIDevice(
                        self,
                        seed_device.name,
                        seed_device.available,
                        seed_device.electric_power,
                        seed_device.initial_ownership,
                        seed_device.final_ownership,
                        seed_device.innovation,
                        seed_device.imitation,
                        seed_device.demand_type,
                        seed_utilisation,
                        seed_device.clean_water_usage,
                    )
                )
            )

        self.active_device = device

        # Add a new set of buttons for the device
        self.devices_frame.device_active_buttons[device] = ttk.Checkbutton(
            self.devices_frame,
            style=f"{SUCCESS}.{ROUND}.{TOGGLE}",
            variable=device.active,
        )
        self.devices_frame.device_active_buttons[device].grid(
            row=len(self.devices_frame.device_active_buttons), column=0, padx=10, pady=5
        )

        self.devices_frame.device_selected_buttons[device] = ttk.Button(
            self.devices_frame,
            text=device.name.get().capitalize(),
            style=f"{SUCCESS}",
            command=lambda device=device: self.select_device(device),
        )
        self.devices_frame.device_selected_buttons[device].grid(
            row=len(self.devices_frame.device_selected_buttons),
            column=1,
            padx=10,
            pady=5,
            sticky="w",
        )

        # Set the other device-selected buttons to look disabled.
        self.select_device(device, batch_loading=batch_loading)

        # Update the screen
        self.devices_frame.update()
        self.update_device_settings_frame(device)

    def update_device_settings_frame(self, device: GUIDevice) -> None:
        """Updates the information for the device currently being considered."""

        self.settings_frame.name_entry.configure(textvariable=device.name)
        self.settings_frame.device_type_combobox.configure(
            textvariable=device.device_type
        )
        self.settings_frame.device_type_combobox.set(device.device_type.get())
        self.settings_frame.electric_power_entry.configure(
            textvariable=device.electric_power
        )
        self.settings_frame.initial_ownership_entry.configure(
            textvariable=device.initial_ownership
        )
        self.settings_frame.final_ownership_entry.configure(
            textvariable=device.final_ownership
        )
        self.settings_frame.innovation_entry.configure(textvariable=device.innovation)
        self.settings_frame.imitation_entry.configure(textvariable=device.imitation)
        self.settings_frame.clean_water_consumption_entry.configure(
            textvariable=device.clean_water_consumption
        )
        # self.settings_frame.device_utilisation_entry.pack_forget()
        # self.settings_frame.device_utilisation_entry: Tableview = Tableview(
        #     self.settings_frame.device_utilisation_label_frame,
        #     coldata=list(device.device_utilisation_columns),
        #     rowdata=device.device_utilisation_row_data,
        #     autofit=True,
        #     autoalign=True,
        #     bootstyle=SUCCESS,
        # )
        # self.settings_frame.device_utilisation_entry.grid(
        #     row=0, column=0, sticky="news", padx=5, pady=5
        # )

    def select_device(self, device: GUIDevice, batch_loading: bool = False) -> None:
        """
        Called to select a device in the left-hand devices pane.

        :param: device
            The :class:`GUIDevice` to select.

        :param: batch_loading
            Whether multiple devices are being loaded at once.

        """
        for button in self.devices_frame.device_selected_buttons.values():
            button.configure(style="success.Outline.TButton")
        self.active_device = device
        self.devices_frame.device_selected_buttons[self.active_device].configure(
            style="success.TButton"
        )

        if self.device_utilisations_directory is not None and not batch_loading:
            self.settings_frame.csv_entry_frame.load_cells(
                os.path.join(
                    self.device_utilisations_directory, f"{device.name.get()}_times.csv"
                )
            )

        self.update_device_settings_frame(device)

    def set_device_type(self) -> None:
        """Set the device type on the active device."""

        self.active_device.device_type.set(
            self.settings_frame.device_type_combobox.get()
        )

    def set_loads(
        self,
        device_utilisations: dict[Device, pd.DataFrame],
        device_utilisations_directory: str,
    ) -> None:
        """
        Set the load information for the frame based on the inputs provided.

        :param: device_utilisations
            A mapping between the devices and the device utilisations.

        :param: device_utilisations_directory
            The path to the device utilisations directory.

        """

        # Set the device utilisations directory.
        self.device_utilisations_directory = device_utilisations_directory

        # Delete and forget the old devices buttons.
        for old_device in self.devices:
            old_active_button = self.devices_frame.device_active_buttons.pop(old_device)
            old_active_button.grid_forget()

            old_selected_button = self.devices_frame.device_selected_buttons.pop(
                old_device
            )
            old_selected_button.grid_forget()

        self.devices: list[GUIDevice] = []

        for device, utilisation in device_utilisations.items():
            # Create a GUI for the device
            self.add_device(device, utilisation, batch_loading=True)

        self.active_device = self.devices[0]
        self.select_device(self.active_device)

    def update_button_label(self, _=None) -> None:
        """Updates the button label of the active device."""

        self.devices_frame.device_selected_buttons[self.active_device].configure(
            text=self.active_device.name.get().capitalize()
        )
        self.active_device.name.set(self.active_device.name.get().replace(" ", "_"))
        self.settings_frame.csv_entry_frame.update_device_name(
            self.active_device.name.get()
        )
