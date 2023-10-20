#!/usr/bin/python3.10
########################################################################################
# post_run.py - The post-run module for CLOVER-GUI application.                        #
#                                                                                      #
# Author: Ben Winchester, Hamish Beath                                                 #
# Copyright: Ben Winchester, 2022                                                      #
# Date created: 23/06/2023                                                             #
# License: MIT, Open-source                                                            #
# For more information, contact: benedict.winchester@gmail.com                         #
########################################################################################

import json
import os
import platform
import subprocess

from dataclasses import dataclass
from typing import Callable

import ttkbootstrap as ttk

from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import *
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.tooltip import ToolTip

from .__utils__ import BaseScreen, IMAGES_DIRECTORY


__all__ = ("PostRunScreen",)

# Plot base name:
#   The base name to use for plots.
PLOT_BASE_NAME: str = f"simulation_1_plots{os.path.sep}" + "{filename}"

# Displayable outputs:
#   A map between output titles and filenames which can be displayed in the outputs.
DISAPLYABLE_OUTPUTS: dict[str, str] = {
    "Summary": "info_file.json",
    "Annaul electric demand": PLOT_BASE_NAME.format(
        filename="electric_demand_annual_variation.png"
    ),
    "Grid power availability": PLOT_BASE_NAME.format(
        filename="grid_availability_heatmap.png"
    ),
    "Electric demands by demand type": PLOT_BASE_NAME.format(
        filename="electric_demands.png"
    ),
    "Electric demands by device": PLOT_BASE_NAME.format(
        filename="electric_device_loads.png"
    ),
    "Electric demands by device": PLOT_BASE_NAME.format(
        filename="electric_device_loads.png"
    ),
    "Electric load growth": PLOT_BASE_NAME.format(filename="electric_load_growth.png"),
    "Electricity availability": PLOT_BASE_NAME.format(
        filename="electricity_availability_on_average_day.png"
    ),
    "Electricity use on average": PLOT_BASE_NAME.format(
        filename="electricity_use_on_average_day.png"
    ),
    "Electricity use on day one": PLOT_BASE_NAME.format(
        filename="electricity_use_on_first_day.png"
    ),
    "Seasonal electricity supplies": PLOT_BASE_NAME.format(
        filename="seasonal_electricity_supply_variations.png"
    ),
    "Solar PV output heatmap": PLOT_BASE_NAME.format(
        filename="solar_output_hetamap.png"
    ),
    "Solar PV output year one": PLOT_BASE_NAME.format(
        filename="solar_output_yearly.png"
    ),
    "Validation of grid randomisation": PLOT_BASE_NAME.format(
        filename="grid_availability_randomisation_comparison.png"
    ),
}

OUTPUT_UNAVAILABLE_TOOLTIP_TEXT: str = (
    "This output can't be viewed. This is likely due to it not being applicable to the "
    "type of CLOVER run you launched.",
)


@dataclass
class Output:
    """
    Represents an output that can be displayed.

    .. attribute:: available
        Whether the output is available for viewing.

    .. attribute:: filepath
        The filepath to the output.

    .. attribute:: title
        The title of the plot to display.

    """

    filepath: ttk.StringVar
    title: ttk.StringVar

    def __hash__(self) -> int:
        """Return a hash of the output for sorting and dictionary mappings."""

        return hash(self.filepath.get())

    @property
    def available(self) -> ttk.BooleanVar:
        """Return whether the output is available for displaying."""

        return os.path.isfile(self.filepath.get())


class OutputsSelectionFrame(ScrolledFrame):
    """
    Represents the scrollable frame where outputs can be selected for viewing.

    TODO: Update attributes.

    """

    def __init__(self, parent, outputs: list[Output], select_output: Callable):
        super().__init__(parent)

        self.output_selected_buttons: dict[Output, ttk.Button] = {
            output: ttk.Button(
                self,
                command=lambda output=output: select_output(output),
                style=f"info.Outline.TButton",
                text=output.title.get().capitalize(),
            )
            for output in outputs
        }

        # Configure column and row weights
        for row_index in range(len(self.output_selected_buttons)):
            self.rowconfigure(row_index, weight=1)

        self.columnconfigure(0, weight=1)

        for index, output in enumerate(self.output_selected_buttons.keys()):
            (button := self.output_selected_buttons[output]).grid(
                row=index, column=0, padx=(10, 40), pady=5, sticky="ew"
            )

            # Disable the button if the output isn't available.
            if not output.available:
                button.configure(state=DISABLED)
                ToolTip(
                    button,
                    bootstyle=f"{INFO}.{OUTLINE}.TButton",
                    text=OUTPUT_UNAVAILABLE_TOOLTIP_TEXT,
                )


class OutputsViewerFrame(ScrolledFrame):
    """Frame used for viewing outputs."""

    def __init__(self, parent) -> None:
        """
        A frame used for viewing outputs.

        :param: parent
            The parent for the frame.

        """

        super().__init__(parent)

        self.output_filepath: ttk.StringVar = ttk.StringVar(self, "")

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=4, minsize=400)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # Label for the name of the output and a short description of the figure being
        # displayed or the table being viewed.
        self.output_name = ttk.Label(
            self,
            bootstyle=INFO,
            text="",
            font=("TkDefaultFont", "16", "bold"),
        )
        self.output_name.grid(row=0, column=0, sticky="news", padx=20, pady=10)

        self.open_file_button = ttk.Button(
            self,
            style="info.Outline.TButton",
            text="Open file",
            command=self._open_file,
        )
        if platform.system() != "Windows":
            self.open_file_button.grid(row=0, column=1, sticky="e", padx=20, pady=10)

        self.output_description = ttk.Label(
            self, text="Select an output on the left to begin visualising your results."
        )
        self.output_description.grid(
            row=1, column=0, columnspan=2, sticky="news", padx=20, pady=10
        )

        # Table viewer
        self.table_output_viewer = Tableview(
            self,
            paginated=True,
            searchable=True,
            bootstyle=INFO,
            height=50,
            autofit=True,
            pagesize=50,
        )
        self.table_output_viewer.insert_column(
            END, "Parameter", width=400, minwidth=400
        )
        self.table_output_viewer.insert_column(END, "Value", width=400, minwidth=400)

        # Image viewer
        self.image_output_viewer = ttk.Label(self, text="")
        self.photo_image: ttk.PhotoImage | None = None

        # Table rows
        self.table_rows: list[tuple[str]] = []

    def _open_file(self) -> None:
        """Opens the file that is currently open."""

        subprocess.Popen(["open", self.output_filepath.get()])

    def display_output(self, output: Output) -> None:
        """
        Display the output requested.

        :param: output
            The output that should be displayed.

        """

        # Update the label for the output
        self.output_name.configure(text=output.title.get())
        self.output_filepath.set(output.filepath.get())

        # If a CSV is being viewed, display the output as a table.
        if output.filepath.get().endswith(".json"):
            # Remove the image output viewer from the screen.
            self.image_output_viewer.grid_forget()
            self.table_output_viewer.grid(
                row=1, column=0, columnspan=2, sticky="news", padx=20, pady=5
            )

            # Load the data from the file.
            try:
                with open(output.filepath.get(), "r", encoding="UTF-8") as output_file:
                    data = json.load(output_file)
            except FileNotFoundError:
                return

            self.table_rows = []

            # Parse the technical data.
            self.table_rows.extend(
                sorted(
                    [
                        (key.replace("_", " ").capitalize(), value)
                        for key, value in data["simulation_1"]["system_appraisal"][
                            "technical_appraisal"
                        ].items()
                    ],
                    reverse=True,
                )
            )
            self.table_rows.append(
                (
                    "Technical appraisal".upper(),
                    "Technical results from the simulation run",
                )
            )

            # Parse the environmental data.
            self.table_rows.extend(
                sorted(
                    [
                        (key.replace("_", " ").capitalize(), value)
                        for key, value in data["simulation_1"]["system_appraisal"][
                            "environmental_appraisal"
                        ].items()
                    ],
                    reverse=True,
                )
            )
            self.table_rows.append(
                (
                    "Environmental appraisal".upper(),
                    "An environmental impact assessment of the system simulated",
                )
            )

            # Parse the financial data.
            self.table_rows.extend(
                sorted(
                    [
                        (key.replace("_", " ").capitalize(), value)
                        for key, value in data["simulation_1"]["system_appraisal"][
                            "financial_appraisal"
                        ].items()
                    ],
                    reverse=True,
                )
            )
            self.table_rows.append(
                (
                    "Financial appraisal".upper(),
                    "Financial results of the system simulated",
                )
            )

            # Parse the evaluated criteria data.
            self.table_rows.extend(
                sorted(
                    [
                        (
                            key.replace("_", " ").capitalize()
                            if key != "lcue"
                            else "LCUE (Leveilised cost of electricity) / USD/kWh",
                            value,
                        )
                        for key, value in data["simulation_1"]["system_appraisal"][
                            "criteria"
                        ].items()
                    ],
                    reverse=True,
                )
            )
            self.table_rows.append(
                ("Evalued critera".upper(), "Performance and financial characteristics")
            )

            # Parse analysis data to plot from the data.
            self.table_rows.extend(
                sorted(
                    [
                        (key.replace("_", " ").capitalize(), value)
                        for key, value in data["simulation_1"][
                            "analysis_results"
                        ].items()
                    ],
                    reverse=True,
                )
            )
            self.table_rows.append(
                ("Analysis results".upper(), "The high-level results of the simulation")
            )

            # Remove the rows from the table view as it is currently.
            self.table_output_viewer.delete_rows()

            # Add the new rows to the table.
            self.table_output_viewer.insert_rows(END, self.table_rows)

            # Display the table viewer on the screen.
            self.table_output_viewer.load_table_data()

        # Otherwise, if an image is beind displayed, display these results.
        if output.filepath.get().endswith(".png"):
            # Remove the tabl output viewer from the screen.
            self.table_output_viewer.grid_forget()
            self.image_output_viewer.grid(
                row=1, column=0, columnspan=2, sticky="news", padx=20, pady=5
            )

            # Load the image from the file into a ttk PhotoImage.
            self.photo_image = ttk.PhotoImage(file=output.filepath.get())

            # Set the photo image to be the background of the label.
            self.image_output_viewer.configure(image=self.photo_image)


class PostRunScreen(BaseScreen, show_navigation=True):
    """
    Represents the post-run screen.

    The post-run screen contains options for a user when a CLOVER run has completed.

    TODO: Update attributes.

    """

    def __init__(
        self,
        data_directory: str,
        open_configuration_screen: Callable,
        open_load_location_post_run: Callable,
        open_new_location_post_run: Callable,
        output_directory_name: ttk.StringVar,
    ) -> None:
        """
        Instantiate a :class:`ConfigureFrame` instance.

        :param: data_directory
            The path to the directory containing data.

        :param: open_configuration_screen
            Function that opens the configuration screen.

        :param: open_load_location_post_run
            Function that opens the load-location window post-run.

        :param: open_new_location_post_run
            Function that opens the new-location screen post-run.

        :param: output_filename
            The output filename for displaying files once a run has compmleted.

        """

        super().__init__()

        self.output_directory_name: ttk.StringVar = output_directory_name

        # Create the list of outputs available for viewing.
        self.outputs: list[Output] = [
            Output(
                ttk.StringVar(self, self._output_filename(output_filename)),
                ttk.StringVar(self, output_title),
            )
            for output_title, output_filename in DISAPLYABLE_OUTPUTS.items()
        ]

        # Configure the row and column weights.
        self.columnconfigure(0, weight=1)

        self.rowconfigure(0, weight=1, minsize=20)
        self.rowconfigure(1, weight=1, minsize=20)
        self.rowconfigure(2, weight=1, minsize=500)
        self.rowconfigure(3, weight=2, minsize=80)

        # Finished label
        self.finished_label = ttk.Label(
            self, bootstyle=INFO, text="CLOVER RUN FINISHED", font="80"
        )
        self.finished_label.grid(row=0, column=0, sticky="ew", padx=60, pady=20)

        # Next-step options
        self.next_steps_frame = ttk.Frame(self)
        self.next_steps_frame.grid(row=1, column=0, sticky="news", padx=60, pady=20)

        self.next_steps_frame.columnconfigure(0, weight=1)
        self.next_steps_frame.columnconfigure(1, weight=1)
        self.next_steps_frame.columnconfigure(2, weight=1)
        self.next_steps_frame.columnconfigure(3, weight=1)

        self.next_steps_frame.rowconfigure(0, weight=1)

        self.next_steps_label = ttk.Label(self.next_steps_frame, text="Next steps:")
        self.next_steps_label.grid(row=0, column=0, sticky="ew", padx=(0, 10), pady=5)

        self.configure_button = ttk.Button(
            self.next_steps_frame,
            bootstyle=f"{INFO}-inverted",
            text="Re-configure/re-run\nthe same location",
            command=open_configuration_screen,
        )
        self.configure_button.grid(row=0, column=1, sticky="news", padx=10, pady=5)

        self.new_location_button = ttk.Button(
            self.next_steps_frame,
            bootstyle=f"{INFO}-inverted",
            text="Create a new location",
            command=open_new_location_post_run,
        )
        self.new_location_button.grid(row=0, column=2, sticky="news", padx=10, pady=5)

        self.load_location_button = ttk.Button(
            self.next_steps_frame,
            bootstyle=f"{INFO}-inverted",
            text="Load a different location",
            command=open_load_location_post_run,
        )
        self.load_location_button.grid(
            row=0, column=3, sticky="news", padx=(10, 0), pady=5
        )

        # Output viewer
        self.outputs_frame = ttk.Frame(self)
        self.outputs_frame.grid(row=2, column=0, sticky="news")

        self.outputs_frame.columnconfigure(0, weight=1)
        self.outputs_frame.columnconfigure(1, weight=4, minsize=600)

        self.outputs_frame.rowconfigure(0, weight=1)

        # Outputs selection frame
        self.outputs_selection_frame = OutputsSelectionFrame(
            self.outputs_frame, self.outputs, self._select_output
        )
        self.outputs_selection_frame.grid(
            row=0, column=0, sticky="news", padx=(60, 0), pady=5
        )

        self.outputs_viewer_frame = OutputsViewerFrame(
            self.outputs_frame,
        )
        self.outputs_viewer_frame.grid(
            row=0, column=1, sticky="news", padx=(0, 60), pady=5
        )

        # Navigation buttons
        self.bottom_bar_frame = ttk.Frame(self)
        self.bottom_bar_frame.grid(row=3, column=0, sticky="news")

        self.bottom_bar_frame.columnconfigure(0, weight=1)
        self.bottom_bar_frame.columnconfigure(1, weight=1)
        self.bottom_bar_frame.columnconfigure(2, weight=1)
        self.bottom_bar_frame.columnconfigure(3, weight=10, minsize=400)
        self.bottom_bar_frame.columnconfigure(4, weight=1)

        self.bottom_bar_frame.rowconfigure(0, weight=1)

        self.back_button_image = ttk.PhotoImage(
            file=os.path.join(
                data_directory,
                IMAGES_DIRECTORY,
                "back_arrow.png",
            )
        )
        self.back_button = ttk.Button(
            self.bottom_bar_frame,
            bootstyle=f"{SECONDARY}-{OUTLINE}",
            command=lambda self=self: BaseScreen.go_back(self),
            image=self.back_button_image,
        )
        self.back_button.grid(
            row=0, column=0, padx=(60, 20), pady=(10, 0), sticky="new"
        )

        self.home_button_image = ttk.PhotoImage(
            file=os.path.join(
                data_directory,
                IMAGES_DIRECTORY,
                "home_icon.png",
            )
        )
        self.home_button = ttk.Button(
            self.bottom_bar_frame,
            bootstyle=f"{SECONDARY}-{OUTLINE}",
            command=lambda self=self: BaseScreen.go_home(self),
            image=self.home_button_image,
        )
        self.home_button.grid(row=0, column=1, padx=20, pady=(10, 0), sticky="new")

        self.forward_button_image = ttk.PhotoImage(
            file=os.path.join(
                data_directory,
                IMAGES_DIRECTORY,
                "forward_arrow.png",
            )
        )
        self.forward_button = ttk.Button(
            self.bottom_bar_frame,
            bootstyle=f"{SECONDARY}-{OUTLINE}",
            command=lambda self=self: BaseScreen.go_forward(self),
            image=self.forward_button_image,
        )
        self.forward_button.grid(row=0, column=2, padx=20, pady=(10, 0), sticky="new")

        self._select_output(self.outputs[0])

    def _output_filename(self, output_filename: str) -> str:
        """
        Determine the path to the output file based on the location.

        :param: output_filename
            The name of the file to find.

        """

        return os.path.join(self.output_directory_name.get(), output_filename)

    def _select_output(self, selected_output: Output) -> None:
        """
        Select the output for viewing..

        :param: selected_output
            The output to select.

        """

        # Make all buttons greyed out in style
        for (
            output,
            button,
        ) in self.outputs_selection_frame.output_selected_buttons.items():
            if output.filepath.get() == selected_output.filepath.get():
                button.configure(style="info.TButton")
                continue
            button.configure(style="info.Outline.TButton")

        self.outputs_selection_frame.update()

        # Display the output
        self.outputs_viewer_frame.display_output(selected_output)

    def update_output_directory_name(self, output_directory_name: str) -> None:
        """
        Update the output directory path based on the inputs.

        :param: output_directory_name
            The name of the outputs directory to set.

        """

        # Update the output directory name
        self.output_directory_name.set(output_directory_name)

        # Update the output directory on all buttons.
        self.outputs: list[Output] = [
            Output(
                ttk.StringVar(self, self._output_filename(output_filename)),
                ttk.StringVar(self, output_title),
            )
            for output_title, output_filename in DISAPLYABLE_OUTPUTS.items()
        ]

        for (
            output,
            button,
        ) in self.outputs_selection_frame.output_selected_buttons.items():
            new_output_name: str = [
                new_output.filepath.get()
                for new_output in self.outputs
                if (
                    os.path.basename(new_output.filepath.get())
                    == os.path.basename(output.filepath.get())
                )
            ][0]
            output.filepath.set(new_output_name)
            button.configure(command=lambda output=output: self._select_output(output))

    def update_outputs_availability(self) -> None:
        """Update the buttons for toggling outputs based on their availability."""

        for (
            output,
            button,
        ) in self.outputs_selection_frame.output_selected_buttons.items():
            if not output.available:
                button.configure(state=DISABLED)
                ToolTip(
                    button,
                    bootstyle=f"{INFO}.{OUTLINE}.TButton",
                    text=OUTPUT_UNAVAILABLE_TOOLTIP_TEXT,
                )
            else:
                button.configure(state="enabled")
                ToolTip(button, bootstyle=f"{INFO}.TButton", text="")

        # Display the first output
        self._select_output(self.outputs[0])
