import os
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

from data.basic.generator import generate_data
from data.basic.handler.csv_dict import write_cars_csv, write_mechanics_csv, write_services_csv
from data.basic.handler.my_json import write_cars_json, write_mechanics_json, write_services_json
from data.basic.handler.xlsx import write_data_xlsx
from data.basic.handler import oracle_db


PROJECT_DIR = Path(__file__).resolve().parent

class AutoServiceGUI:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("AutoService - Data Manager")
        self.root.geometry("610x435")
        self.root.minsize(560, 520)

        self.cars = []
        self.services = []
        self.mechanics = []
        self.has_data = False

        self.amount_var = tk.StringVar(value="20")
        self.count_var = tk.StringVar(value="Cars: 0   |   Mechanics: 0   |   Services: 0")
        self.status_var = tk.StringVar(value="Enter an amount, then generate data.")

        style = ttk.Style()
        if "clam" in style.theme_names():
            style.theme_use("clam")
        style.configure("Title.TLabel", font=("Segoe UI", 17, "bold"))
        style.configure("Count.TLabel", font=("Segoe UI", 11, "bold"))
        style.configure("Action.TButton", padding=(12, 9))

        container = ttk.Frame(root, padding=22)
        container.pack(fill="both", expand=True)

        ttk.Label(container, text="AutoService Data Manager", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            container,
            text="Generate sample data and export it to files or Oracle SQL.",
        ).pack(anchor="w", pady=(4, 18))

        generate_frame = ttk.LabelFrame(container, text="Data generation", padding=14)
        generate_frame.pack(fill="x")

        input_row = ttk.Frame(generate_frame)
        input_row.pack(fill="x")
        ttk.Label(input_row, text="Number of cars / mechanics:").pack(side="left")
        ttk.Entry(input_row, textvariable=self.amount_var, width=10).pack(side="left", padx=12)
        ttk.Button(
            input_row, text="Generate Data", command=self.generate, style="Action.TButton"
        ).pack(side="right")

        ttk.Label(generate_frame, textvariable=self.count_var, style="Count.TLabel").pack(
            anchor="w", pady=(15, 2)
        )

        export_frame = ttk.LabelFrame(container, text="File export", padding=14)
        export_frame.pack(fill="x", pady=(16, 0))

        export_buttons = ttk.Frame(export_frame)
        export_buttons.pack(fill="x")
        for label, action in (
            ("Export CSV", self.export_csv),
            ("Export JSON", self.export_json),
            ("Export XLSX", self.export_xlsx),
            ("Export All", self.export_all),
        ):
            ttk.Button(export_buttons, text=label, command=action).pack(
                side="left", padx=(0, 8)
            )

        oracle_frame = ttk.LabelFrame(container, text="Oracle database", padding=14)
        oracle_frame.pack(fill="x", pady=(16, 0))
        ttk.Button(
            oracle_frame,
            text="Replace Oracle Data",
            command=self.upload_oracle,
            style="Action.TButton",
        ).pack(anchor="w")
        ttk.Label(
            oracle_frame,
            text="Warning: replaces ALL existing rows in CAR, MECHANIC and SERVICE.",
        ).pack(anchor="w", pady=(8, 0))

        ttk.Label(container, textvariable=self.status_var, wraplength=550).pack(
            anchor="w", pady=(15, 0)
        )

    def require_data(self) -> bool:
        if not self.has_data:
            messagebox.showwarning("No data", "Generate data first.", parent=self.root)
            return False
        return True

    def generate(self) -> None:
        try:
            amount = int(self.amount_var.get())
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Invalid amount", "Enter a positive whole number.", parent=self.root
            )
            return

        try:
            cars, services, mechanics = generate_data(amount)
        except Exception as error:
            self.show_error("Data generation failed", error)
            return

        self.cars, self.services, self.mechanics = cars, services, mechanics
        self.has_data = True
        self.count_var.set(
            f"Cars: {len(cars)}   |   Mechanics: {len(mechanics)}   |   "
            f"Services: {len(services)}"
        )
        self.status_var.set("New data generated successfully. Ready to export.")

    def export_csv(self) -> None:
        if not self.require_data():
            return
        try:
            folder = str(PROJECT_DIR / "csv_files")
            Path(folder).mkdir(parents=True, exist_ok=True)
            write_cars_csv(self.cars, folder)
            write_services_csv(self.services, folder)
            write_mechanics_csv(self.mechanics, folder)
            self.status_var.set("CSV files saved to csv_files/.")
        except Exception as error:
            self.show_error("CSV export failed", error)

    def export_json(self) -> None:
        if not self.require_data():
            return
        try:
            folder = str(PROJECT_DIR / "json_files")
            Path(folder).mkdir(parents=True, exist_ok=True)
            write_cars_json(self.cars, folder)
            write_services_json(self.services, folder)
            write_mechanics_json(self.mechanics, folder)
            self.status_var.set("JSON files saved to json_files/.")
        except Exception as error:
            self.show_error("JSON export failed", error)

    def export_xlsx(self) -> None:
        if not self.require_data():
            return
        try:
            (PROJECT_DIR / "xlsx_files").mkdir(parents=True, exist_ok=True)
            write_data_xlsx(
                self.cars, self.services, self.mechanics,
                str(PROJECT_DIR / "xlsx_files"),
            )
            self.status_var.set("Excel workbook saved to xlsx_files/.")
        except Exception as error:
            self.show_error("XLSX export failed", error)

    def export_all(self) -> None:
        if not self.require_data():
            return
        try:
            csv_folder = str(PROJECT_DIR / "csv_files")
            json_folder = str(PROJECT_DIR / "json_files")
            xlsx_folder = str(PROJECT_DIR / "xlsx_files")
            for folder in (csv_folder, json_folder, xlsx_folder):
                Path(folder).mkdir(parents=True, exist_ok=True)

            write_cars_csv(self.cars, csv_folder)
            write_services_csv(self.services, csv_folder)
            write_mechanics_csv(self.mechanics, csv_folder)

            write_cars_json(self.cars, json_folder)
            write_services_json(self.services, json_folder)
            write_mechanics_json(self.mechanics, json_folder)

            write_data_xlsx(self.cars, self.services, self.mechanics, xlsx_folder)
            self.status_var.set("All formats exported successfully.")
        except Exception as error:
            self.show_error("File export failed", error)

    def upload_oracle(self) -> None:
        if not self.require_data():
            return

        if not messagebox.askyesno(
            "Confirm database replacement",
            "Replace ALL rows in the CAR, MECHANIC and SERVICE tables "
            "with the currently generated data?",
            icon="warning",
            parent=self.root,
        ):
            return

        missing = [
            key for key in ("ORACLE_USER", "ORACLE_PASSWORD", "ORACLE_DSN")
            if not os.environ.get(key)
        ]
        if missing:
            messagebox.showerror(
                "Oracle configuration missing",
                "Set these environment variables in the gui.py run configuration: "
                + ", ".join(missing),
                parent=self.root,
            )
            return

        try:
            oracle_db.create_car_table()
            oracle_db.create_mechanic_table()
            oracle_db.create_service_table()
            oracle_db.insert_data(self.cars, self.services, self.mechanics)
            oracle_db.check_table_counts()
            self.status_var.set("Oracle database updated successfully.")
            messagebox.showinfo(
                "Success", "Oracle database updated successfully.", parent=self.root
            )
        except Exception as error:
            self.show_error("Oracle upload failed", error)

    def show_error(self, title: str, error: Exception) -> None:
        self.status_var.set(f"{title}: {error}")
        messagebox.showerror(title, str(error), parent=self.root)


def main() -> None:
    root = tk.Tk()
    AutoServiceGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()