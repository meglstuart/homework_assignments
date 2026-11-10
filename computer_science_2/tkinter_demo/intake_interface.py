"""
Veterinary Office Patient Intake

MODEL       Holds the data and the rules. Knows nothing about tkinter.
VIEW        Draws the widgets. Knows nothing about the rules. No decisions.
CONTROLLER  Reacts to button clicks, asks the model to do work,
            then tells the view what to show.

Flow of a "Check In" click:
    View button  ->  Controller.on_submit()
                 ->  Model.add_patient()   (validates, may raise ValueError)
                 ->  Controller tells View to refresh / show an error
"""

import tkinter as tk
from tkinter import ttk
from dataclasses import dataclass


# ----------------------------------------------------------------------
# MODEL
# ----------------------------------------------------------------------
@dataclass
class Patient:
    owner_name: str
    phone: str
    pet_name: str
    species: str
    breed: str
    age: float
    weight: float
    reason: str
    vaccinated: bool


class IntakeModel:
    """Stores patients and enforces the intake rules."""

    SPECIES = ["Dog", "Cat", "Rabbit", "Bird", "Reptile", "Other"]

    def __init__(self):
        self._patients = []

    def add_patient(self, data):
        """Validate raw form data (a dict of strings) and store a Patient.
        Raises ValueError with a friendly message if anything is wrong."""
        owner = data["owner_name"].strip()
        phone = data["phone"].strip()
        pet = data["pet_name"].strip()
        species = data["species"].strip()
        breed = data["breed"].strip()
        reason = data["reason"].strip()

        if not owner:
            raise ValueError("Owner name is required.")
        digits = [c for c in phone if c.isdigit()]
        if len(digits) != 10:
            raise ValueError("Phone number must have 10 digits.")
        if not pet:
            raise ValueError("Pet name is required.")
        if species not in self.SPECIES:
            raise ValueError("Please choose a species.")
        if not reason:
            raise ValueError("Please enter a reason for the visit.")

        try:
            age = float(data["age"])
        except ValueError:
            raise ValueError("Age must be a number (in years).")
        if age < 0 or age > 50:
            raise ValueError("Age must be between 0 and 50 years.")

        try:
            weight = float(data["weight"])
        except ValueError:
            raise ValueError("Weight must be a number (in lbs).")
        if weight <= 0 or weight > 400:
            raise ValueError("Weight must be between 0 and 400 lbs.")

        patient = Patient(owner, phone, pet, species, breed or "Unknown",
                          age, weight, reason, bool(data["vaccinated"]))
        self._patients.append(patient)
        return patient

    def get_patients(self):
        return list(self._patients)

# ----------------------------------------------------------------------
# VIEW
# ----------------------------------------------------------------------
class IntakeView(ttk.Frame):
    """Only builds widgets and exposes simple get/set methods.
    Buttons call whatever handlers the controller gives it."""
 
    def __init__(self, parent, species_options):
        super().__init__(parent, padding=10)
        self.pack(fill="both", expand=True)
 
        # One tk variable per input field
        self.vars = {
            "owner_name": tk.StringVar(),
            "phone": tk.StringVar(),
            "pet_name": tk.StringVar(),
            "species": tk.StringVar(),
            "breed": tk.StringVar(),
            "age": tk.StringVar(),
            "weight": tk.StringVar(),
            "vaccinated": tk.BooleanVar(),
        }
 
        form = ttk.LabelFrame(self, text="Patient Intake", padding=10)
        form.pack(fill="x")
 
        rows = [
            ("Owner name", "owner_name"),
            ("Phone", "phone"),
            ("Pet name", "pet_name"),
            ("Species", "species"),
            ("Breed", "breed"),
            ("Age (years)", "age"),
            ("Weight (lbs)", "weight"),
        ]
        for r, (label, key) in enumerate(rows):
            ttk.Label(form, text=label).grid(row=r, column=0, sticky="w", pady=2)
            if key == "species":
                widget = ttk.Combobox(form, textvariable=self.vars[key],
                                      values=species_options, state="readonly",
                                      width=27)
            else:
                widget = ttk.Entry(form, textvariable=self.vars[key], width=30)
            widget.grid(row=r, column=1, sticky="w", padx=8, pady=2)
 
        r = len(rows)
        ttk.Label(form, text="Reason for visit").grid(row=r, column=0,
                                                      sticky="nw", pady=2)
        self.reason_text = tk.Text(form, width=30, height=3)
        self.reason_text.grid(row=r, column=1, sticky="w", padx=8, pady=2)
 
        ttk.Checkbutton(form, text="Vaccinations up to date",
                        variable=self.vars["vaccinated"]
                        ).grid(row=r + 1, column=1, sticky="w", padx=8, pady=4)
 
        # Buttons (commands are attached later by the controller)
        buttons = ttk.Frame(form)
        buttons.grid(row=r + 2, column=0, columnspan=2, pady=(8, 0))
        self.submit_button = ttk.Button(buttons, text="Check In")
        self.submit_button.pack(side="left", padx=4)
        self.clear_button = ttk.Button(buttons, text="Clear Form")
        self.clear_button.pack(side="left", padx=4)
 
        # Status message line
        self.status_label = ttk.Label(self, text="", foreground="gray")
        self.status_label.pack(fill="x", pady=6)
 
        # The list of checked-in patients. How it looks is decided by
        # _build_patient_list(), which subclasses can override.
        list_frame = ttk.LabelFrame(self, text="Checked-In Patients", padding=6)
        list_frame.pack(fill="both", expand=True)
        self._build_patient_list(list_frame)
 

    def _build_patient_list(self, parent):
        self.text_list = tk.Text(parent, height=8, width=60, state="disabled",
                                 wrap="word")
        self.text_list.pack(fill="both", expand=True)


 
    # --- methods the controller uses ---------------------------------
    def set_handlers(self, on_submit, on_clear):
        self.submit_button.config(command=on_submit)
        self.clear_button.config(command=on_clear)
 
    def get_form_data(self):
        data = {key: var.get() for key, var in self.vars.items()}
        data["reason"] = self.reason_text.get("1.0", "end").strip()
        return data
 
    def clear_form(self):
        for key, var in self.vars.items():
            var.set(False if key == "vaccinated" else "")
        self.reason_text.delete("1.0", "end")
 
    def show_message(self, text, is_error=False):
        self.status_label.config(text=text,
                                 foreground="red" if is_error else "green")

    def refresh_table(self, patients):
        self.text_list.config(state="normal")
        self.text_list.delete("1.0", "end")
        for number, p in enumerate(patients, start=1):
            vax = "vaccinated" if p.vaccinated else "NOT vaccinated"
            self.text_list.insert(
                "end",
                f"{number}. {p.pet_name} the {p.species.lower()} "
                f"(owner: {p.owner_name}) - {p.reason} [{vax}]\n")
        self.text_list.config(state="disabled")


 


# ----------------------------------------------------------------------
# CONTROLLER
# ----------------------------------------------------------------------
class IntakeController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.set_handlers(self.on_submit, self.on_clear)

    def on_submit(self):
        data = self.view.get_form_data()
        try:
            patient = self.model.add_patient(data)
        except ValueError as error:
            self.view.show_message(str(error), is_error=True)
            return
        self.view.refresh_table(self.model.get_patients())
        self.view.clear_form()
        self.view.show_message(f"{patient.pet_name} has been checked in!")

    def on_clear(self):
        self.view.clear_form()
        self.view.show_message("")


# ----------------------------------------------------------------------
# DRIVER
# ----------------------------------------------------------------------
def main():
    root = tk.Tk()
    root.title("Paws & Claws Veterinary - Patient Intake")

    model = IntakeModel()
    view = IntakeView(root, IntakeModel.SPECIES)
    IntakeController(model, view)

    root.mainloop()


if __name__ == "__main__":
    main()