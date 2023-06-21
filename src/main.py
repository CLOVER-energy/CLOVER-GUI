#!python3

import tkinter as tk
import time

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import *

# Main-window geometry:
#   The geometry to use for the main window, specified in width and height.
MAIN_WINDOW_GEOMETRY: str = "1220x800"

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


def open_preferences_window() -> None:
    """
    Opens the user-preferences popup window.
    """

    pass


def open_help_window() -> None:
    """
    Opens the help popup window.
    """

    pass


# Screens
class SplashScreen(tk.Toplevel):
    """
    Represents a splash screen.

    """

    def __init__(self, parent) -> None:
        """Instantiate the :class:`SplashScreen` instance."""
        tk.Toplevel.__init__(self, parent)

        self.title("CLOVER-GUI Splash")
        self.background_image = tk.PhotoImage(file="clover_splash_screen.png")
        self.background_image = self.background_image.subsample(2)
        self.splash_label = tk.Label(self, image=self.background_image)
        self.splash_label.pack()

        # Create an updatable progress bar.
        self.progress_bar = ttk.Progressbar(
            self, bootstyle=f"{SUCCESS}-striped", mode="determinate"
        )
        self.progress_bar.pack(pady=20, fill="x")
        self.progress_bar.start()

        # Disable the in-built minimise, maximise and close buttons.
        self.overrideredirect(True)

        # Required to make the splash screen visible.
        self.update()

    def set_progress_bar_progerss(self, value) -> None:
        """
        Sets the value of the progress bar.

        :param: value
            The value to use for setting the progress bar position.

        """

        self.progress_bar["value"] = value
        self.update()


class MainMenuFrame(ttk.Frame):
    """
    Represents the main-menu frame.

    The main-menu frame contains two buttons:
        - A "new-location" button, which takes the user to a screen where they can set up a new location,
        - A "load-location" button, which creates a popup prompting the user to load an existing location.

    .. attribute:: label
        The label instance holding the main-menu image.

    .. attribute:: load_location_button
        A button which provides the user the option of loading an existing location.

    .. attribute:: main_menu_image
        The image to display at the top of the main-menu screen.

    .. attribute:: new_location_button
        A button which which provides the user the option of creating a new location.

    """

    def __init__(self, splash_screen: SplashScreen, new_location_callback) -> None:
        """
        Instantiate a :class:`MainMenuFrame` instance.

        :param: splash_screen
            The splash screen, passed in to update the progress bar if necessary.

        :param: new_location_callback
            The callback function to use when the new-location button is pressed.

        """

        super().__init__()

        self.pack(fill="both", expand=True)
        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.main_menu_image = tk.PhotoImage(file="clover_splash_screen.png")
        self.main_menu_image = self.main_menu_image.subsample(2)
        self.label = ttk.Label(self, image=self.main_menu_image)
        self.label.grid(row=0, column=0, columnspan=2, sticky="news")

        self.new_location_button = ttk.Button(
            self,
            text="New location",
            bootstyle=f"{SUCCESS}-outline",
            command=new_location_callback,
        )
        self.new_location_button.grid(
            row=1, column=0, padx=5, pady=5, ipadx=80, ipady=20
        )

        self.load_location_button = ttk.Button(
            self, text="Load location", bootstyle=f"{PRIMARY}-outline"
        )
        self.load_location_button.grid(
            row=1, column=1, padx=5, pady=5, ipadx=80, ipady=20
        )


class NewLocationFrame(ttk.Frame):
    """
    Represents the new-location frame.

    The new-location frame enables a user to create a new location within CLOVER.

    .. attribute:: label
        The label instance holding the main-menu image.

    .. attribute:: load_location_button
        A button which provides the user the option of loading an existing location.

    .. attribute:: main_menu_image
        The image to display at the top of the main-menu screen.

    .. attribute:: new_location_button
        A button which which provides the user the option of creating a new location.

    """

    def __init__(self, splash_screen: SplashScreen) -> None:
        """
        Instantiate a :class:`MainMenuFrame` instance.

        """

        super().__init__()

        self.pack(fill="both", expand=True)
        self.rowconfigure(0, weight=6)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.columnconfigure(0, weight=1)

        self.label = ttk.Label(self, text="New location")
        self.label.grid(row=0, column=0, sticky="news")


class App(ttk.Window):
    """
    Represents the main app window for user naviagtion.

    """

    def __init__(self) -> None:
        """Instantiate the CLOVER-GUI main app window."""

        # Set the theme and styles
        ttk.Window.__init__(self)
        self.theme = "journal"

        # Display the splash screen whilst loading
        self.withdraw()
        self.splash = SplashScreen(self)

        # Setup the CLOVER-GUI application.
        self.title("CLOVER")
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
        x = max((self.winfo_screenwidth() // 2) - (width // 2), 0)
        y = max((self.winfo_screenheight() // 2) - (height // 2), 0)
        self.geometry(f"+{x}+{y}")

    def open_new_location_frame(self):
        """Opens the new-location frame."""

        self.main_menu_frame.pack_forget()
        self.new_location_frame.pack(fill="both", expand=True)

    def setup(self) -> None:
        """
        Setup the window.

        """

        # Menu-bar
        self.setup_menubar()
        self.splash.set_progress_bar_progerss(33)

        # Main-menu
        self.main_menu_frame = MainMenuFrame(self.splash, self.open_new_location_frame)
        self.splash.set_progress_bar_progerss(67)

        # New-location
        self.new_location_frame = NewLocationFrame(self.splash)
        self.new_location_frame.pack_forget()
        self.splash.set_progress_bar_progerss(100)

    def setup_menubar(self) -> None:
        """Setup the menu bar."""

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
        self.edit_menu.add_command(label="Preferences", command=open_preferences_window)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)

        # Help menu
        self.help_menu = ttk.Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="Help", command=open_help_window)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)

        self.config(menu=self.menu_bar)

    def destroy_splash(self):
        self.splash.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
