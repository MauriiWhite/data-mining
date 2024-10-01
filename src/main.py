import tkinter as tk

from tkinter import ttk
from tkinter.font import Font

from metrics import results
from components import General, Metric


class MetricsApp:
    PADDING = 5
    MARGIN_PERCENT = 0.25
    CONFIG_FONT = ("", 10)

    def __init__(self, root: tk.Tk, name: str = "Metrics") -> None:
        self.root = root
        self.root.title(name)
        self.results = results()

        self._font = Font(family="Verdana", size=10)
        self._build_ui()
        self._globals_config()
        self._window_center()

    def _globals_config(self) -> None:
        self.root.option_add("*Font", self.CONFIG_FONT)
        self.root.option_add("*padding", self.PADDING)
        self.root.resizable(True, True)

    def _build_ui(self) -> None:
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        general = General(self.notebook, self.results.get("general"))
        self.notebook.add(general, text="General")

        for key, value in self.results.items():
            if key == "general":
                continue
            self.metric_tab = Metric(self.notebook, value)
            self.notebook.add(self.metric_tab, text=key.capitalize())

    def _calc_margin(self, size: int) -> int:
        return int(size - (size * self.MARGIN_PERCENT))

    def _window_center(self) -> None:
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        width = self._calc_margin(screen_width)
        height = self._calc_margin(screen_height)

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.root.geometry(f"{width}x{height}+{x}+{y}")


if __name__ == "__main__":
    root = tk.Tk()
    app = MetricsApp(root)
    root.mainloop()
