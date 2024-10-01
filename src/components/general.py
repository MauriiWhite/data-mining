import tkinter as tk

from tkinter import ttk
from tkinter.font import Font


class General(tk.Frame):
    def __init__(self, root: tk.Tk, metrics: dict) -> None:
        super().__init__(root)
        self.pack(fill=tk.BOTH, expand=True)
        self.metrics = metrics

        self._font = Font(family="Verdana", size=10)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)
        self.columnconfigure(0, weight=1)

        self._build_scrollable_tree()

    def _build_scrollable_tree(self) -> None:
        tree_frame = tk.Frame(self)
        tree_frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=5,
            pady=3,
            ipadx=5,
            ipady=3,
        )

        tree_scrollbar = tk.Scrollbar(tree_frame)
        tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("key", "value"),
            show="headings",
            yscrollcommand=tree_scrollbar.set,
        )
        self.tree.heading("key", text="Dato")
        self.tree.heading("value", text="Valor")
        self.tree.pack(fill=tk.BOTH, expand=True)

        tree_scrollbar.config(command=self.tree.yview)

        for key, value in self.metrics.items():
            self.tree.insert(
                "", tk.END, values=(key.replace("_", " ").capitalize(), value)
            )
