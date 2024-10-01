import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt

from tkinter import ttk
from tkinter.font import Font
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Metric(tk.Frame):
    def __init__(self, root: tk.Tk, metrics: dict) -> None:
        super().__init__(root)
        self.pack(fill=tk.BOTH, expand=True)

        self.metrics = metrics
        self.current_metric = None
        self.current_graph_type = "Bar"
        self.max_value = max(self.extract_values(metrics), default=None)
        self.min_value = min(self.extract_values(metrics), default=None)

        self._font = Font(family="Verdana", size=10)
        self._build_buttons(metrics)
        self._build_max_and_min()

        self._configure_grid()
        self._initialize_plot()

        # ComboBox para seleccionar el tipo de gráfico
        self.graph_type_combo = ttk.Combobox(
            self, values=["Bar", "Line", "Pie"], state="readonly"
        )
        self.graph_type_combo.set("Bar")
        self.graph_type_combo.grid(
            row=0, column=0, sticky="we", padx=5, pady=3, ipadx=5, ipady=3
        )
        self.graph_type_combo.bind("<<ComboboxSelected>>", self.on_graph_type_change)

    def extract_values(self, metrics: dict) -> list:
        """Extrae todos los valores de las métricas."""
        return [
            value
            for value in metrics.values()
            if isinstance(value, dict)
            for value in value.values()
        ]

    def _configure_grid(self) -> None:
        """Configura el grid de la interfaz."""
        cols = 5
        for col in range(cols):
            self.grid_columnconfigure(
                col, weight=1 if col == 0 or col == cols - 1 else 2
            )
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=10)

    def _initialize_plot(self) -> None:
        """Inicializa el área de dibujo."""
        self.figure, self.ax = plt.subplots(figsize=(8, 6))
        self.figure.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.2)
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=5, sticky="nsew")

    def _build_buttons(self, metrics: dict) -> None:
        """Construye los botones para las métricas."""
        for count, (key, value) in enumerate(metrics.items(), start=1):
            if isinstance(value, dict):
                button = ttk.Button(
                    self,
                    text=key.replace("_", " ").capitalize(),
                    command=lambda m=value: self.update_graph(m),
                )
                button.grid(
                    row=0, column=count, sticky="we", padx=5, pady=3, ipadx=5, ipady=3
                )

    def _build_max_and_min(self) -> None:
        """Construye el panel de máximos y mínimos."""
        self.frame = tk.Frame(self)
        self.frame.grid(
            row=0, column=4, sticky="nswe", padx=5, pady=3, ipadx=5, ipady=3
        )
        self.max_label = tk.Label(
            self.frame,
            text=f"Max: {self.max_value}",
            justify="center",
            font=self._font,
            fg="red",
        ).grid(row=0, column=0, sticky="nswe", padx=5, pady=3, ipadx=5, ipady=3)
        self.min_label = tk.Label(
            self.frame,
            text=f"Min: {self.min_value}",
            justify="center",
            font=self._font,
            fg="red",
        ).grid(row=0, column=1, sticky="nswe", padx=5, pady=3, ipadx=5, ipady=3)

    def on_graph_type_change(self, event):
        """Maneja el cambio del tipo de gráfico."""
        self.current_graph_type = self.graph_type_combo.get()
        if self.current_metric is not None:
            self.update_graph(self.current_metric)

    def update_graph(self, metric):
        """Actualiza el gráfico con la métrica seleccionada."""
        self.current_metric = metric
        self.ax.clear()

        plot_methods = {
            "Bar": self.plot_bar,
            "Line": self.plot_line,
            "Pie": self.plot_pie,
        }
        plot_methods.get(self.current_graph_type, self.plot_bar)()
        self.canvas.draw()

    def plot_bar(self):
        """Dibuja un gráfico de barras con cantidad y porcentaje."""
        keys = list(self.current_metric.keys())
        values = list(self.current_metric.values())

        self.ax.bar(
            keys,
            values,
            color="royalblue",
            width=0.6,
        )

        for i, value in enumerate(values):
            self.ax.text(
                i,
                value,
                value,
                ha="center",
                va="bottom",
                fontsize=9,
            )

        self._set_common_plot_properties("Gráfico de Barras")

    def plot_line(self):
        """Dibuja un gráfico de líneas con las cantidades en cada punto."""
        # Dibuja el gráfico de líneas
        self.ax.plot(
            self.current_metric.keys(),
            self.current_metric.values(),
            marker="o",
            linestyle="-",
            color="royalblue",
        )

        # Anotar cada punto con la cantidad
        for i, value in enumerate(self.current_metric.values()):
            self.ax.text(
                i,
                value,
                str(value),
                ha="center",
                va="bottom",
                fontsize=9,
            )

        self._set_common_plot_properties("Gráfico de Líneas")
        self.ax.tick_params(axis="x", rotation=45)

    def plot_pie(self):
        """Dibuja un gráfico de sectores con cantidad y porcentaje."""
        # Datos de las métricas actuales
        values = self.current_metric.values()
        labels = self.current_metric.keys()

        # Función para mostrar cantidad y porcentaje
        def autopct_format(values):
            def inner_autopct(pct):
                total = sum(values)
                val = int(round(pct * total / 100.0))
                return f"{val} ({pct:.1f}%)"

            return inner_autopct

        # Dibuja el gráfico de sectores
        self.ax.pie(
            values,
            labels=labels,
            autopct=autopct_format(values),
            startangle=140,
            colors=plt.cm.viridis(np.linspace(0, 1, len(self.current_metric))),
        )
        self.ax.set_title("Gráfico de Sectores", fontsize=16, color="navy")

    def _set_common_plot_properties(self, title):
        """Configura propiedades comunes de los gráficos."""
        self.ax.set_title(title, fontsize=16, color="navy")
        self.ax.set_xlabel("Categorías")
        self.ax.set_ylabel("Valores")
        self.ax.yaxis.grid(True, linestyle="--", alpha=0.7)
        self.ax.set_axisbelow(True)


# Ejemplo de uso
if __name__ == "__main__":
    metrics_data = {
        "metric_a": {"Category A": 10, "Category B": 15, "Category C": 7},
        "metric_b": {"Category D": 20, "Category E": 5, "Category F": 12},
    }

    root = tk.Tk()
    app = Metric(root, metrics_data)
    root.mainloop()
