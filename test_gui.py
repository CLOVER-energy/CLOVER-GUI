#!/home/bewinche/anaconda3/envs/py310/bin/python
# Test space for playing with GUI features.

import os
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
#         self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
#         self.sidebar_button_3 = customtkinter.CTkButton(
#             self.sidebar_frame, command=self.sidebar_button_event
#         )
#         self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
#         self.appearance_mode_label = customtkinter.CTkLabel(
#             self.sidebar_frame, text="Appearance Mode:", anchor="w"
#         )
#         self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
#         self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(
#             self.sidebar_frame,
#             values=["Light", "Dark", "System"],
#             command=self.change_appearance_mode_event,
#         )
#         self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
#         self.scaling_label = customtkinter.CTkLabel(
#             self.sidebar_frame, text="UI Scaling:", anchor="w"
#         )
#         self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
#         self.scaling_optionemenu = customtkinter.CTkOptionMenu(
#             self.sidebar_frame,
#             values=["80%", "90%", "100%", "110%", "120%"],
#             command=self.change_scaling_event,
#         )
#         self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

#         # create main entry and button
#         self.entry = customtkinter.CTkEntry(self, placeholder_text="CTkEntry")
#         self.entry.grid(
#             row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew"
#         )

#         self.main_pv_button = customtkinter.CTkButton(
#             master=self,
#             fg_color="transparent",
#             border_width=2,
#             text_color=("gray10", "#DCE4EE"),
#         )
#         self.main_pv_button.grid(
#             row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew"
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
#         self.string_input_button.grid(row=2, column=0, padx=20, pady=(10, 10))
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
#         self.radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="n")
#         self.radio_button_3 = customtkinter.CTkRadioButton(
#             master=self.radiobutton_frame, variable=self.radio_var, value=2
#         )
#         self.radio_button_3.grid(row=3, column=2, pady=10, padx=20, sticky="n")

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
#             row=2, column=0, padx=(20, 10), pady=(10, 10), sticky="ew"
#         )
#         def action_azimuthal_orientation(value: float) -> None:
#             print(value - 180)
#         self.slider_1 = customtkinter.CTkSlider(
#             self.slider_progressbar_frame, from_=0, to=1, number_of_steps=360, command=action_azimuthal_orientation
#         )
#         self.slider_1.grid(row=3, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
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
#         self.checkbox_2.grid(row=2, column=0, pady=(20, 0), padx=20, sticky="n")
#         self.checkbox_3 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
#         self.checkbox_3.grid(row=3, column=0, pady=20, padx=20, sticky="n")

#         # set default values
#         self.sidebar_button_3.configure(state="disabled", text="Disabled CTkButton")
#         self.checkbox_3.configure(state="disabled")
#         self.checkbox_1.select()
#         self.scrollable_frame_switches[0].select()
#         self.scrollable_frame_switches[4].select()
#         self.radio_button_3.configure(state="disabled")
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


def simple_example() -> None:
    customtkinter.set_appearance_mode(
        "System"
    )  # Modes: "System" (standard), "Dark", "Light"
    customtkinter.set_default_color_theme(
        "dark-blue"
    )  # Themes: "blue" (standard), "green", "dark-blue"

    app = customtkinter.CTk()
    app.geometry("800x780")
    app.title("CustomTkinter simple_example.py")

    def pv_button_callback():
        print("Button click", combobox_1.get())
        solar_pv_selected.set(not solar_pv_selected.get())
        pv_button.configure(image=solar_images[solar_pv_selected.get()])

    def battery_button_callback():
        print("Button click", combobox_1.get())
        battery_selected.set(not battery_selected.get())
        battery_button.configure(image=battery_images[battery_selected.get()])

    def slider_callback(value):
        progressbar_1.set(value)
        print(int(value * 360 - 180))

    frame_1 = customtkinter.CTkFrame(master=app)
    frame_1.grid(row=20, column=20, columnspan=20, pady=20, padx=60, sticky="ew")
    # frame_1.pack(pady=20, padx=60, fill="both", expand=True)

    label_1 = customtkinter.CTkLabel(master=frame_1, justify=customtkinter.LEFT)
    label_1.grid(pady=10, padx=10)

    progressbar_1 = customtkinter.CTkProgressBar(master=frame_1)
    progressbar_1.grid(row=0, column=0, pady=10, padx=10)

    # Selecting system components
    solar_images: dict[bool, tkinter.PhotoImage] = {
        True: tkinter.PhotoImage(file=os.path.join("images", "solar_gui_selected.png")),
        False: tkinter.PhotoImage(
            file=os.path.join("images", "solar_gui_deselected.png")
        ),
    }
    solar_pv_selected: customtkinter.BooleanVar = customtkinter.BooleanVar(value=False)
    pv_button = customtkinter.CTkButton(
        master=frame_1,
        command=pv_button_callback,
        fg_color="transparent",
        image=solar_images[solar_pv_selected.get()],
        text="",
    )
    pv_button.grid(row=1, column=0, pady=10, padx=10)

    battery_images: dict[bool, tkinter.PhotoImage] = {
        True: tkinter.PhotoImage(
            file=os.path.join("images", "battery_gui_selected.png")
        ),
        False: tkinter.PhotoImage(
            file=os.path.join("images", "battery_gui_deselected.png")
        ),
    }
    battery_selected: customtkinter.BooleanVar = customtkinter.BooleanVar(value=False)
    battery_button = customtkinter.CTkButton(
        master=frame_1,
        command=battery_button_callback,
        fg_color="transparent",
        image=battery_images[battery_selected.get()],
        text="",
    )
    battery_button.grid(row=1, column=1, pady=10, padx=10)

    slider_1 = customtkinter.CTkSlider(
        master=frame_1, command=slider_callback, from_=0, to=1, number_of_steps=360
    )
    slider_1.grid(row=2, column=0, pady=10, padx=10)
    slider_1.set(0.5)

    entry_1 = customtkinter.CTkEntry(master=frame_1, placeholder_text="CTkEntry")
    entry_1.grid(row=3, column=0, pady=10, padx=10)

    optionmenu_1 = customtkinter.CTkOptionMenu(
        frame_1, values=["Option 1", "Option 2", "Option 42 long long long..."]
    )
    optionmenu_1.grid(row=4, column=0, pady=10, padx=10)
    optionmenu_1.set("CTkOptionMenu")

    combobox_1 = customtkinter.CTkComboBox(
        frame_1, values=["Option 1", "Option 2", "Option 42 long long long..."]
    )
    combobox_1.grid(row=5, column=0, pady=10, padx=10)
    combobox_1.set("CTkComboBox")

    checkbox_1 = customtkinter.CTkCheckBox(master=frame_1)
    checkbox_1.grid(row=6, column=0, pady=10, padx=10)

    radiobutton_var = customtkinter.IntVar(value=1)

    def radiobutton_event():
        print("radiobutton toggled, current value:", radiobutton_var.get())

    radiopv_button = customtkinter.CTkRadioButton(
        master=frame_1, variable=radiobutton_var, value=1, command=radiobutton_event
    )
    radiopv_button.grid(row=7, column=0, pady=10, padx=10)

    radiobutton_2 = customtkinter.CTkRadioButton(
        master=frame_1, variable=radiobutton_var, value=2, command=radiobutton_event
    )
    radiobutton_2.grid(row=8, column=0, pady=10, padx=10)

    switch_1 = customtkinter.CTkSwitch(
        master=frame_1, text="the switch", onvalue=True, offvalue=False
    )
    switch_1.grid(row=9, column=0, pady=10, padx=10)

    text_1 = customtkinter.CTkTextbox(master=frame_1, width=200, height=70)
    text_1.grid(row=10, column=0, pady=10, padx=10)
    text_1.insert("0.0", "CTkTextbox\n\n\n\n")

    segmented_pv_button = customtkinter.CTkSegmentedButton(
        master=frame_1, values=["CTkSegmentedButton", "Value 2"]
    )
    segmented_pv_button.grid(row=11, column=0, pady=10, padx=10)

    tabview_1 = customtkinter.CTkTabview(master=frame_1, width=200, height=70)
    tabview_1.grid(row=12, column=0, pady=10, padx=10)
    tabview_1.add("CTkTabview")
    tabview_1.add("Tab 2")

    app.mainloop()


if __name__ == "__main__":
    # main()
    # app = App()
    # app.mainloop()
    simple_example()
