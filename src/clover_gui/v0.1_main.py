#!/home/bewinche/anaconda3/envs/py310/bin/python
# Test space for playing with GUI features.

import enum
import functools
import os
import sys
import tkinter
import tkinter.messagebox

import customtkinter

# COLOR_THEME:
#   The default colour theme to use.
#
COLOR_THEME: str = "dark-blue"

# MODE:
#   The system mode to use.
#   Allowed values are
#   - "System" (standard),
#   - "Dark",
#   - and "Light".
#
MODE: str = "System"


# class App(customtkinter.CTk):
#     def __init__(self):
#         super().__init__()

#         # configure window
#         self.title("CustomTkinter complex_example.py")
#         self.geometry(f"{1100}x{580}")

#         # configure grid layout (4x4)
#         self.grid_columnconfigure(1, weight=1)
#         self.grid_columnconfigure((2, 3), weight=0)
#         self.grid_rowconfigure((0, 1, 2), weight=1)

#         # create sidebar frame with widgets
#         self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
#         self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
#         self.sidebar_frame.grid_rowconfigure(4, weight=1)
#         self.logo_label = customtkinter.CTkLabel(
#             self.sidebar_frame,
#             text="CustomTkinter",
#             font=customtkinter.CTkFont(size=20, weight="bold"),
#         )
#         self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
#         self.sidebar_pv_button = customtkinter.CTkButton(
#             self.sidebar_frame, command=self.sidebar_button_event
#         )
#         self.sidebar_pv_button.grid(row=1, column=0, padx=20, pady=10)
#         self.sidebar_button_2 = customtkinter.CTkButton(
#             self.sidebar_frame, command=self.sidebar_button_event
#         )
#         self.sidebar_button_2.grid(row=3, column=0, padx=20, pady=10)
#         self.sidebar_button_3 = customtkinter.CTkButton(
#             self.sidebar_frame, command=self.sidebar_button_event
#         )
#         self.sidebar_button_3.grid(row=4, column=0, padx=20, pady=10)
#         self.appearance_mode_label = customtkinter.CTkLabel(
#             self.sidebar_frame, text="Appearance Mode:", anchor="w"
#         )
#         self.appearance_mode_label.grid(row=6, column=0, padx=20, pady=(10, 0))
#         self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(
#             self.sidebar_frame,
#             values=["Light", "Dark", "System"],
#             command=self.change_appearance_mode_event,
#         )
#         self.appearance_mode_optionemenu.grid(row=7, column=0, padx=20, pady=(10, 10))
#         self.scaling_label = customtkinter.CTkLabel(
#             self.sidebar_frame, text="UI Scaling:", anchor="w"
#         )
#         self.scaling_label.grid(row=8, column=0, padx=20, pady=(10, 0))
#         self.scaling_optionemenu = customtkinter.CTkOptionMenu(
#             self.sidebar_frame,
#             values=["80%", "90%", "100%", "110%", "120%"],
#             command=self.change_scaling_event,
#         )
#         self.scaling_optionemenu.grid(row=9, column=0, padx=20, pady=(10, 20))

#         # create main entry and button
#         self.entry = customtkinter.CTkEntry(self, placeholder_text="CTkEntry")
#         self.entry.grid(
#             row=4, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew"
#         )

#         self.main_pv_button = customtkinter.CTkButton(
#             master=self,
#             fg_color="transparent",
#             border_width=2,
#             text_color=("gray10", "#DCE4EE"),
#         )
#         self.main_pv_button.grid(
#             row=4, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew"
#         )

#         # create textbox
#         self.textbox = customtkinter.CTkTextbox(self, width=250)
#         self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

#         # create tabview
#         self.tabview = customtkinter.CTkTabview(self, width=250)
#         self.tabview.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
#         self.tabview.add("CTkTabview")
#         self.tabview.add("Tab 2")
#         self.tabview.add("Tab 3")
#         self.tabview.tab("CTkTabview").grid_columnconfigure(
#             0, weight=1
#         )  # configure grid of individual tabs
#         self.tabview.tab("Tab 2").grid_columnconfigure(0, weight=1)

#         self.optionmenu_1 = customtkinter.CTkOptionMenu(
#             self.tabview.tab("CTkTabview"),
#             dynamic_resizing=False,
#             values=["Value 1", "Value 2", "Value Long Long Long"],
#         )
#         self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))
#         self.combobox_1 = customtkinter.CTkComboBox(
#             self.tabview.tab("CTkTabview"),
#             values=["Value 1", "Value 2", "Value Long....."],
#         )
#         self.combobox_1.grid(row=1, column=0, padx=20, pady=(10, 10))
#         self.string_input_button = customtkinter.CTkButton(
#             self.tabview.tab("CTkTabview"),
#             text="Open CTkInputDialog",
#             command=self.open_input_dialog_event,
#         )
#         self.string_input_button.grid(row=3, column=0, padx=20, pady=(10, 10))
#         self.label_tab_2 = customtkinter.CTkLabel(
#             self.tabview.tab("Tab 2"), text="CTkLabel on Tab 2"
#         )
#         self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)

#         # create radiobutton frame
#         self.radiobutton_frame = customtkinter.CTkFrame(self)
#         self.radiobutton_frame.grid(
#             row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew"
#         )
#         self.radio_var = tkinter.IntVar(value=0)
#         self.label_radio_group = customtkinter.CTkLabel(
#             master=self.radiobutton_frame, text="CTkRadioButton Group:"
#         )
#         self.label_radio_group.grid(
#             row=0, column=2, columnspan=1, padx=10, pady=10, sticky=""
#         )
#         self.radio_pv_button = customtkinter.CTkRadioButton(
#             master=self.radiobutton_frame, variable=self.radio_var, value=0
#         )
#         self.radio_pv_button.grid(row=1, column=2, pady=10, padx=20, sticky="n")
#         self.radio_button_2 = customtkinter.CTkRadioButton(
#             master=self.radiobutton_frame, variable=self.radio_var, value=1
#         )
#         self.radio_button_2.grid(row=3, column=2, pady=10, padx=20, sticky="n")
#         self.radio_button_3 = customtkinter.CTkRadioButton(
#             master=self.radiobutton_frame, variable=self.radio_var, value=2
#         )
#         self.radio_button_3.grid(row=4, column=2, pady=10, padx=20, sticky="n")

#         # create slider and progressbar frame
#         self.slider_progressbar_frame = customtkinter.CTkFrame(
#             self, fg_color="transparent"
#         )
#         self.slider_progressbar_frame.grid(
#             row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew"
#         )
#         self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
#         self.slider_progressbar_frame.grid_rowconfigure(4, weight=1)
#         self.seg_pv_button = customtkinter.CTkSegmentedButton(
#             self.slider_progressbar_frame
#         )
#         self.seg_pv_button.grid(
#             row=0, column=0, padx=(20, 10), pady=(10, 10), sticky="ew"
#         )
#         self.progressbar_1 = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
#         self.progressbar_1.grid(
#             row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="ew"
#         )
#         self.progressbar_2 = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
#         self.progressbar_2.grid(
#             row=3, column=0, padx=(20, 10), pady=(10, 10), sticky="ew"
#         )
#         def action_azimuthal_orientation(value: float) -> None:
#             print(value - 180)
#         self.slider_1 = customtkinter.CTkSlider(
#             self.slider_progressbar_frame, from_=0, to=1, number_of_steps=360, command=action_azimuthal_orientation
#         )
#         self.slider_1.grid(row=4, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
#         self.slider_2 = customtkinter.CTkSlider(
#             self.slider_progressbar_frame, orientation="vertical"
#         )
#         self.slider_2.grid(
#             row=0, column=1, rowspan=5, padx=(10, 10), pady=(10, 10), sticky="ns"
#         )
#         self.progressbar_3 = customtkinter.CTkProgressBar(
#             self.slider_progressbar_frame, orientation="vertical"
#         )
#         self.progressbar_3.grid(
#             row=0, column=2, rowspan=5, padx=(10, 20), pady=(10, 10), sticky="ns"
#         )

#         # create scrollable frame
#         self.scrollable_frame = customtkinter.CTkScrollableFrame(
#             self, label_text="CTkScrollableFrame"
#         )
#         self.scrollable_frame.grid(
#             row=1, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew"
#         )
#         self.scrollable_frame.grid_columnconfigure(0, weight=1)
#         self.scrollable_frame_switches = []
#         for i in range(100):
#             switch = customtkinter.CTkSwitch(
#                 master=self.scrollable_frame, text=f"CTkSwitch {i}"
#             )
#             switch.grid(row=i, column=0, padx=10, pady=(0, 20))
#             self.scrollable_frame_switches.append(switch)

#         # create checkbox and switch frame
#         self.checkbox_slider_frame = customtkinter.CTkFrame(self)
#         self.checkbox_slider_frame.grid(
#             row=1, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew"
#         )
#         self.checkbox_1 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
#         self.checkbox_1.grid(row=1, column=0, pady=(20, 0), padx=20, sticky="n")
#         self.checkbox_2 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
#         self.checkbox_2.grid(row=3, column=0, pady=(20, 0), padx=20, sticky="n")
#         self.checkbox_3 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
#         self.checkbox_3.grid(row=4, column=0, pady=20, padx=20, sticky="n")

#         # set default values
#         self.sidebar_button_3.configure(state=DISABLED, text="Disabled CTkButton")
#         self.checkbox_3.configure(state=DISABLED)
#         self.checkbox_1.select()
#         self.scrollable_frame_switches[0].select()
#         self.scrollable_frame_switches[4].select()
#         self.radio_button_3.configure(state=DISABLED)
#         self.appearance_mode_optionemenu.set("Dark")
#         self.scaling_optionemenu.set("100%")
#         self.optionmenu_1.set("CTkOptionmenu")
#         self.combobox_1.set("CTkComboBox")
#         self.slider_1.configure(command=self.progressbar_2.set)
#         self.slider_2.configure(command=self.progressbar_3.set)
#         self.progressbar_1.configure(mode="indeterminnate")
#         self.progressbar_1.start()
#         self.textbox.insert(
#             "0.0",
#             "CTkTextbox\n\n"
#             + "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n"
#             * 20,
#         )
#         self.seg_pv_button.configure(values=["CTkSegmentedButton", "Value 2", "Value 3"])
#         self.seg_pv_button.set("Value 2")

#     def open_input_dialog_event(self) -> None:
#         dialog = customtkinter.CTkInputDialog(
#             text="Type in a number:", title="CTkInputDialog"
#         )
#         print("CTkInputDialog:", dialog.get_input())

#     def change_appearance_mode_event(self, new_appearance_mode: str) -> None:
#         """
#         Event initiated when a request is made to change the appearance mode.

#         :param: new_appearance_mode
#             The name of the new appearance mode to apply.

#         """

#         customtkinter.set_appearance_mode(new_appearance_mode)

#     def change_scaling_event(self, new_scaling: str) -> None:
#         """
#         Event initiated when a request is made to change the scaling.

#         :param: new_scaling
#             The new scaling to apply.

#         """

#         customtkinter.set_widget_scaling(int(new_scaling.replace("%", "")) / 100)

#     def sidebar_button_event(self):
#         print("sidebar_button click")


# def main() -> None:
#     """
#     Main function.

#     """
#     root_window = customtkinter.CTk()

#     customtkinter.set_appearance_mode(MODE)
#     customtkinter.set_default_color_theme(COLOR_THEME)

#     button = customtkinter.CTkButton(master=root_window, text="Hello World!")
#     button.place(relx=0.5, rely=0.5, anchor=CENTER)

#     root_window.mainloop()


##################
# Simple example #
##################


class BatterySettingsWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")
        self.grid(row=3, column=3, columnspan=3, pady=20, padx=60, sticky="")

        self.label = customtkinter.CTkLabel(self, text="Electric battery settings")
        self.label.grid(row=0, column=0, columnspan=3, padx=20, pady=20)

        self.protocol("WM_DELETE_WINDOW", self.withdraw)


class PVSettingsWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

        # Create a frame to contain the contents.
        self.frame = customtkinter.CTkFrame(self)
        self.frame.grid(padx=60, pady=20, sticky="")

        self.label = customtkinter.CTkLabel(self.frame, text="Solar PV settings")
        self.label.grid(row=0, column=0, columnspan=5, padx=20, pady=20)

        self.protocol("WM_DELETE_WINDOW", self.withdraw)

        # Azimuthal orientation
        self.azimuthal_bar = customtkinter.CTkProgressBar(master=self.frame)
        self.azimuthal_bar.grid(row=1, column=0, columnspan=3, pady=10, padx=10)

        self.azimuthal_slider = customtkinter.CTkSlider(
            master=self.frame,
            command=self.azimuthal_slider_callback,
            from_=0,
            to=1,
            number_of_steps=360,
        )
        self.azimuthal_slider.grid(row=2, column=0, columnspan=3, pady=10, padx=10)
        self.azimuthal_slider.set(0.5)

        # Tilt
        self.tilt_bar = customtkinter.CTkProgressBar(
            master=self.frame, orientation="vertical"
        )
        self.tilt_bar.grid(row=0, column=3, pady=10, padx=10)

        self.tilt_slider = customtkinter.CTkSlider(
            master=self.frame,
            command=self.tilt_slider_callback,
            from_=0,
            to=1,
            number_of_steps=90,
            orientation="vertical",
        )
        self.tilt_slider.grid(row=0, column=4, pady=10, padx=10)
        self.tilt_slider.set(0.5)

    def azimuthal_slider_callback(self, value):
        self.azimuthal_bar.set(value)
        print(int(value * 360 - 180))

    def tilt_slider_callback(self, value):
        self.tilt_bar.set(value)
        print(int(value * 360))


class ResourceType(enum.Enum):
    """
    Used for differentiating buttons by resource type.

    - ELECTRIC:
        Represents electric buttons.

    - HOT_WATER:
        Represents hot-water buttons.

    - COLD_WATER:
        Represents cold-water buttons.

    """

    ELECTRIC: str = "electric"
    HOT_WATER: str = "hot_water"
    COLD_WATER: str = "cold_water"


class ScenarioPage(customtkinter.CTkScrollableFrame):
    """
    Page for the scenario settings.

    """

    def __init__(self, master):
        """
        Instnatiate the scenario page.

        """

        super().__init__(master=master, width=680, height=680)
        self.grid(row=15, column=4, columnspan=4, pady=20, padx=60, sticky="")

        def pv_button_callback():
            print("Button click", combobox_1.get())
            solar_pv_selected.set(not solar_pv_selected.get())
            pv_button.configure(image=solar_images[solar_pv_selected.get()])

        def battery_button_callback():
            print("Button click", combobox_1.get())
            battery_selected.set(not battery_selected.get())
            battery_button.configure(image=battery_images[battery_selected.get()])

        def diesel_button_callback():
            print("Button click", combobox_1.get())
            diesel_selected.set(not diesel_selected.get())
            diesel_button.configure(image=diesel_images[diesel_selected.get()])

        def grid_button_callback():
            print("Button click", combobox_1.get())
            grid_selected.set(not grid_selected.get())
            grid_button.configure(image=grid_images[grid_selected.get()])

        def resource_button_callback(resource_type: ResourceType):
            print("Button click", combobox_1.get())
            resource_selected[resource_type].set(
                not resource_selected[resource_type].get()
            )
            resource_buttons[resource_type].configure(
                image=resource_images[resource_type][
                    resource_selected[resource_type].get()
                ]
            )

            # If loads are enabled, colour these buttons in
            if resource_selected[resource_type].get():
                domestic_buttons[resource_type].configure(
                    image=domestic_images[domestic_selected[resource_type].get()]
                )
                commercial_buttons[resource_type].configure(
                    image=commercial_images[commercial_selected[resource_type].get()]
                )
                public_buttons[resource_type].configure(
                    image=public_images[public_selected[resource_type].get()]
                )
            else:
                domestic_buttons[resource_type].configure(
                    image=domestic_button_disabled_image
                )
                commercial_buttons[resource_type].configure(
                    image=commercial_button_disabled_image
                )
                public_buttons[resource_type].configure(
                    image=public_button_disabled_image
                )

        def domestic_button_callback(resource_type: ResourceType) -> None:
            print("Button click", combobox_1.get())
            # Return if electric loads are not selected
            if not resource_selected[resource_type].get():
                return
            domestic_selected[resource_type].set(
                not domestic_selected[resource_type].get()
            )
            domestic_buttons[resource_type].configure(
                image=domestic_images[domestic_selected[resource_type].get()]
            )

        def commercial_button_callback(resource_type: ResourceType) -> None:
            print("Button click", combobox_1.get())
            # Return if electric loads are not selected
            if not resource_selected[resource_type].get():
                return
            commercial_selected[resource_type].set(
                not commercial_selected[resource_type].get()
            )
            commercial_buttons[resource_type].configure(
                image=commercial_images[commercial_selected[resource_type].get()]
            )

        def public_button_callback(resource_type: ResourceType) -> None:
            print("Button click", combobox_1.get())
            # Return if electric loads are not selected
            if not resource_selected[resource_type].get():
                return
            public_selected[resource_type].set(not public_selected[resource_type].get())
            public_buttons[resource_type].configure(
                image=public_images[public_selected[resource_type].get()]
            )

        # frame_1 = customtkinter.CTkScrollableFrame(master=app, width=680, height=680)
        # frame_1.grid(row=15, column=4, columnspan=4, pady=20, padx=60, sticky="")
        # frame_1.pack(pady=20, padx=60, fill="both", expand=True)

        label_1 = customtkinter.CTkLabel(
            master=self,
            justify=customtkinter.CENTER,
            text="Scenario specification page",
        )
        label_1.grid(row=0, column=0, columnspan=4, pady=10, padx=10)

        # Selecting system components
        solar_images: dict[bool, tkinter.PhotoImage] = {
            True: tkinter.PhotoImage(
                file=os.path.join(
                    (data_directory := os.path.dirname(sys.executable)),
                    "images",
                    "solar_gui_selected.png",
                )
            ),
            False: tkinter.PhotoImage(
                file=os.path.join(data_directory, "images", "solar_gui_deselected.png")
            ),
        }
        solar_pv_selected: customtkinter.BooleanVar = customtkinter.BooleanVar(
            value=False
        )
        pv_button = customtkinter.CTkButton(
            master=self,
            command=pv_button_callback,
            fg_color="transparent",
            image=solar_images[solar_pv_selected.get()],
            text="",
        )
        pv_button.grid(row=1, column=0, pady=10, padx=10)

        self.pv_settings = customtkinter.CTkButton(
            self, text="PV settings", command=self.open_pv_settings
        )
        self.pv_settings.grid(row=2, column=0, padx=20)
        self.pv_settings_window = None

        battery_images: dict[bool, tkinter.PhotoImage] = {
            True: tkinter.PhotoImage(
                file=os.path.join(data_directory, "images", "battery_gui_selected.png")
            ),
            False: tkinter.PhotoImage(
                file=os.path.join(
                    data_directory, "images", "battery_gui_deselected.png"
                )
            ),
        }
        battery_selected: customtkinter.BooleanVar = customtkinter.BooleanVar(
            value=False
        )
        battery_button = customtkinter.CTkButton(
            master=self,
            command=battery_button_callback,
            fg_color="transparent",
            image=battery_images[battery_selected.get()],
            text="",
        )
        battery_button.grid(row=1, column=1, pady=10, padx=10, sticky="")

        self.battery_settings = customtkinter.CTkButton(
            self, text="Battery settings", command=self.open_battery_settings
        )
        self.battery_settings.grid(row=2, column=1, padx=20)
        self.battery_settings_window = None

        diesel_images: dict[bool, tkinter.PhotoImage] = {
            True: tkinter.PhotoImage(
                file=os.path.join(data_directory, "images", "diesel_gui_selected.png")
            ),
            False: tkinter.PhotoImage(
                file=os.path.join(data_directory, "images", "diesel_gui_deselected.png")
            ),
        }
        diesel_selected: customtkinter.BooleanVar = customtkinter.BooleanVar(
            value=False
        )
        diesel_button = customtkinter.CTkButton(
            master=self,
            command=diesel_button_callback,
            fg_color="transparent",
            image=diesel_images[diesel_selected.get()],
            text="",
        )
        diesel_button.grid(row=1, column=2, pady=10, padx=10)

        grid_images: dict[bool, tkinter.PhotoImage] = {
            True: tkinter.PhotoImage(
                file=os.path.join(data_directory, "images", "grid_gui_selected.png")
            ),
            False: tkinter.PhotoImage(
                file=os.path.join(data_directory, "images", "grid_gui_deselected.png")
            ),
        }
        grid_selected: customtkinter.BooleanVar = customtkinter.BooleanVar(value=False)
        grid_button = customtkinter.CTkButton(
            master=self,
            command=grid_button_callback,
            fg_color="transparent",
            image=grid_images[grid_selected.get()],
            text="",
        )
        grid_button.grid(row=1, column=3, pady=10, padx=10)

        # Resource types selection
        resource_images: dict[ResourceType, dict[bool, tkinter.PhotoImage]] = {
            ResourceType.ELECTRIC: {
                True: tkinter.PhotoImage(
                    file=os.path.join(
                        data_directory, "images", "electric_gui_selected_filled.png"
                    )
                ),
                False: tkinter.PhotoImage(
                    file=os.path.join(
                        data_directory, "images", "electric_gui_selected_outline.png"
                    )
                ),
            },
            ResourceType.HOT_WATER: {
                True: tkinter.PhotoImage(
                    file=os.path.join(
                        data_directory, "images", "hot_water_gui_selected_filled.png"
                    )
                ),
                False: tkinter.PhotoImage(
                    file=os.path.join(
                        data_directory, "images", "hot_water_gui_selected_outline.png"
                    )
                ),
            },
            ResourceType.COLD_WATER: {
                True: tkinter.PhotoImage(
                    file=os.path.join(
                        data_directory, "images", "cold_water_gui_selected_filled.png"
                    )
                ),
                False: tkinter.PhotoImage(
                    file=os.path.join(
                        data_directory, "images", "cold_water_gui_selected_outline.png"
                    )
                ),
            },
        }

        resource_selected: dict[ResourceType : customtkinter.BooleanVa] = {
            ResourceType.ELECTRIC: customtkinter.BooleanVar(value=True),
            ResourceType.HOT_WATER: customtkinter.BooleanVar(value=False),
            ResourceType.COLD_WATER: customtkinter.BooleanVar(value=False),
        }

        electric_button = customtkinter.CTkButton(
            master=self,
            command=functools.partial(resource_button_callback, ResourceType.ELECTRIC),
            fg_color="transparent",
            image=resource_images[ResourceType.ELECTRIC][
                resource_selected[ResourceType.ELECTRIC].get()
            ],
            text="",
        )
        electric_button.grid(row=3, column=0, pady=10, padx=10, sticky="")
        hot_water_button = customtkinter.CTkButton(
            master=self,
            command=functools.partial(resource_button_callback, ResourceType.HOT_WATER),
            fg_color="transparent",
            image=resource_images[ResourceType.HOT_WATER][
                resource_selected[ResourceType.HOT_WATER].get()
            ],
            text="",
        )
        hot_water_button.grid(row=4, column=0, pady=10, padx=10, sticky="")
        cold_water_button = customtkinter.CTkButton(
            master=self,
            command=functools.partial(
                resource_button_callback, ResourceType.COLD_WATER
            ),
            fg_color="transparent",
            image=resource_images[ResourceType.COLD_WATER][
                resource_selected[ResourceType.COLD_WATER].get()
            ],
            text="",
        )
        cold_water_button.grid(row=5, column=0, pady=10, padx=10, sticky="")
        resource_buttons: dict[ResourceType, customtkinter.CTkButton] = {
            ResourceType.ELECTRIC: electric_button,
            ResourceType.HOT_WATER: hot_water_button,
            ResourceType.COLD_WATER: cold_water_button,
        }

        domestic_images: dict[bool, tkinter.PhotoImage] = {
            True: tkinter.PhotoImage(
                file=os.path.join(data_directory, "images", "domestic_gui_selected.png")
            ),
            False: tkinter.PhotoImage(
                file=os.path.join(
                    data_directory, "images", "domestic_gui_deselected.png"
                )
            ),
        }
        domestic_button_disabled_image: tkinter.PhotoImage = tkinter.PhotoImage(
            file=os.path.join(data_directory, "images", "domestic_gui_disabled.png")
        )

        commercial_images: dict[bool, tkinter.PhotoImage] = {
            True: tkinter.PhotoImage(
                file=os.path.join(
                    data_directory, "images", "commercial_gui_selected.png"
                )
            ),
            False: tkinter.PhotoImage(
                file=os.path.join(
                    data_directory, "images", "commercial_gui_deselected.png"
                )
            ),
        }
        commercial_button_disabled_image: tkinter.PhotoImage = tkinter.PhotoImage(
            file=os.path.join(data_directory, "images", "commercial_gui_disabled.png")
        )

        public_images: dict[bool, tkinter.PhotoImage] = {
            True: tkinter.PhotoImage(
                file=os.path.join(data_directory, "images", "public_gui_selected.png")
            ),
            False: tkinter.PhotoImage(
                file=os.path.join(data_directory, "images", "public_gui_deselected.png")
            ),
        }
        public_button_disabled_image: tkinter.PhotoImage = tkinter.PhotoImage(
            file=os.path.join(data_directory, "images", "public_gui_disabled.png")
        )

        # Domestic buttons
        domestic_selected: dict[ResourceType, customtkinter.BooleanVar] = {
            ResourceType.ELECTRIC: customtkinter.BooleanVar(value=False),
            ResourceType.HOT_WATER: customtkinter.BooleanVar(value=False),
            ResourceType.COLD_WATER: customtkinter.BooleanVar(value=False),
        }
        electric_domestic_button = customtkinter.CTkButton(
            master=self,
            command=functools.partial(domestic_button_callback, ResourceType.ELECTRIC),
            fg_color="transparent",
            image=domestic_images[domestic_selected[ResourceType.ELECTRIC].get()],
            text="",
        )
        electric_domestic_button.grid(row=3, column=1, pady=10, padx=10, sticky="")

        hot_water_domestic_button = customtkinter.CTkButton(
            master=self,
            command=functools.partial(domestic_button_callback, ResourceType.HOT_WATER),
            fg_color="transparent",
            image=domestic_button_disabled_image,
            text="",
        )
        hot_water_domestic_button.grid(row=4, column=1, pady=10, padx=10, sticky="")

        cold_water_domestic_button = customtkinter.CTkButton(
            master=self,
            command=functools.partial(
                domestic_button_callback, ResourceType.COLD_WATER
            ),
            fg_color="transparent",
            image=domestic_button_disabled_image,
            text="",
        )
        cold_water_domestic_button.grid(row=5, column=1, pady=10, padx=10, sticky="")
        domestic_buttons: dict[ResourceType, customtkinter.CTkButton] = {
            ResourceType.ELECTRIC: electric_domestic_button,
            ResourceType.HOT_WATER: hot_water_domestic_button,
            ResourceType.COLD_WATER: cold_water_domestic_button,
        }

        # Commercial buttons
        commercial_selected: dict[ResourceType, customtkinter.BooleanVar] = {
            ResourceType.ELECTRIC: customtkinter.BooleanVar(value=False),
            ResourceType.HOT_WATER: customtkinter.BooleanVar(value=False),
            ResourceType.COLD_WATER: customtkinter.BooleanVar(value=False),
        }

        electric_commercial_button = customtkinter.CTkButton(
            master=self,
            command=functools.partial(
                commercial_button_callback, ResourceType.ELECTRIC
            ),
            fg_color="transparent",
            image=commercial_images[commercial_selected[ResourceType.ELECTRIC].get()],
            text="",
        )
        electric_commercial_button.grid(row=3, column=2, pady=10, padx=10)

        hot_water_commercial_button = customtkinter.CTkButton(
            master=self,
            command=functools.partial(
                commercial_button_callback, ResourceType.HOT_WATER
            ),
            fg_color="transparent",
            image=commercial_button_disabled_image,
            text="",
        )
        hot_water_commercial_button.grid(row=4, column=2, pady=10, padx=10)

        cold_water_commercial_button = customtkinter.CTkButton(
            master=self,
            command=functools.partial(
                commercial_button_callback, ResourceType.COLD_WATER
            ),
            fg_color="transparent",
            image=commercial_button_disabled_image,
            text="",
        )
        cold_water_commercial_button.grid(row=5, column=2, pady=10, padx=10)
        commercial_buttons: dict[ResourceType, customtkinter.CTkButton] = {
            ResourceType.ELECTRIC: electric_commercial_button,
            ResourceType.HOT_WATER: hot_water_commercial_button,
            ResourceType.COLD_WATER: cold_water_commercial_button,
        }

        # Public buttons
        public_selected: dict[ResourceType, customtkinter.BooleanVar] = {
            ResourceType.ELECTRIC: customtkinter.BooleanVar(value=False),
            ResourceType.HOT_WATER: customtkinter.BooleanVar(value=False),
            ResourceType.COLD_WATER: customtkinter.BooleanVar(value=False),
        }

        electric_public_button = customtkinter.CTkButton(
            master=self,
            command=functools.partial(public_button_callback, ResourceType.ELECTRIC),
            fg_color="transparent",
            image=public_images[public_selected[ResourceType.ELECTRIC].get()],
            text="",
        )
        electric_public_button.grid(row=3, column=3, pady=10, padx=10)

        hot_water_public_button = customtkinter.CTkButton(
            master=self,
            command=functools.partial(public_button_callback, ResourceType.HOT_WATER),
            fg_color="transparent",
            image=public_button_disabled_image,
            text="",
        )
        hot_water_public_button.grid(row=4, column=3, pady=10, padx=10)

        cold_water_public_button = customtkinter.CTkButton(
            master=self,
            command=functools.partial(public_button_callback, ResourceType.COLD_WATER),
            fg_color="transparent",
            image=public_button_disabled_image,
            text="",
        )
        cold_water_public_button.grid(row=5, column=3, pady=10, padx=10)
        public_buttons: dict[ResourceType, customtkinter.CTkButton] = {
            ResourceType.ELECTRIC: electric_public_button,
            ResourceType.HOT_WATER: hot_water_public_button,
            ResourceType.COLD_WATER: cold_water_public_button,
        }

        entry_1 = customtkinter.CTkEntry(master=self, placeholder_text="CTkEntry")
        entry_1.grid(row=6, columnspan=4, column=0, pady=10, padx=10)

        optionmenu_1 = customtkinter.CTkOptionMenu(
            self, values=["Option 1", "Option 2", "Option 42 long long long..."]
        )
        optionmenu_1.grid(row=7, columnspan=4, column=0, pady=10, padx=10)
        optionmenu_1.set("CTkOptionMenu")

        combobox_1 = customtkinter.CTkComboBox(
            self, values=["Option 1", "Option 2", "Option 42 long long long..."]
        )
        combobox_1.grid(row=8, columnspan=4, column=0, pady=10, padx=10)
        combobox_1.set("CTkComboBox")

        checkbox_1 = customtkinter.CTkCheckBox(master=self)
        checkbox_1.grid(row=9, columnspan=4, column=0, pady=10, padx=10)

        radiobutton_var = customtkinter.IntVar(value=1)

        def radiobutton_event():
            print("radiobutton toggled, current value:", radiobutton_var.get())

        radiopv_button = customtkinter.CTkRadioButton(
            master=self, variable=radiobutton_var, value=1, command=radiobutton_event
        )
        radiopv_button.grid(row=10, columnspan=4, column=0, pady=10, padx=10)

        radiobutton_2 = customtkinter.CTkRadioButton(
            master=self, variable=radiobutton_var, value=2, command=radiobutton_event
        )
        radiobutton_2.grid(row=11, columnspan=4, column=0, pady=10, padx=10)

        switch_1 = customtkinter.CTkSwitch(
            master=self, text="the switch", onvalue=True, offvalue=False
        )
        switch_1.grid(row=12, columnspan=4, column=0, pady=10, padx=10)

        text_1 = customtkinter.CTkTextbox(master=self, width=200, height=70)
        text_1.grid(row=13, columnspan=4, column=0, pady=10, padx=10)
        text_1.insert("0.0", "CTkTextbox\n\n\n\n")

        segmented_pv_button = customtkinter.CTkSegmentedButton(
            master=self, values=["CTkSegmentedButton", "Value 2"]
        )
        segmented_pv_button.grid(row=14, columnspan=4, column=0, pady=10, padx=10)

        tabview_1 = customtkinter.CTkTabview(master=self, width=200, height=70)
        tabview_1.grid(row=15, columnspan=4, column=0, pady=10, padx=10)
        tabview_1.add("CTkTabview")
        tabview_1.add("Tab 2")

    def open_pv_settings(self) -> None:
        if self.pv_settings_window is None:
            self.pv_settings_window = PVSettingsWindow(self)
        else:
            self.pv_settings_window.deiconify()
        self.pv_settings_window.mainloop()

    def open_battery_settings(self) -> None:
        if self.battery_settings_window is None:
            self.battery_settings_window = BatterySettingsWindow(self)
        else:
            self.battery_settings_window.deiconify()
        self.battery_settings_window.mainloop()


def simple_example() -> None:
    customtkinter.set_appearance_mode(
        "System"
    )  # Modes: "System" (standard), "Dark", "Light"
    customtkinter.set_default_color_theme(
        "dark-blue"
    )  # Themes: "blue" (standard), "green", "dark-blue"

    app = customtkinter.CTk()
    app.geometry("820x720")
    app.title("CustomTkinter simple_example.py")

    scenario_page = ScenarioPage(app)

    app.mainloop()


if __name__ == "__main__":
    # main()
    # app = App()
    # app.mainloop()
    simple_example()
