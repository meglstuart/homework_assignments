from intake_interface import IntakeModel, IntakeController, IntakeView
import tkinter as tk
from tkinter import ttk

class TextListIntakeView(IntakeView):
    """Alternate view: same form and same public methods, but the patient
    list is a plain read-only text box with one line per patient.
 
    Only two things change: how the list is built, and how it is refreshed.
    The model and controller cannot tell the difference."""
 
    def _build_patient_list(self, parent):
        """Default look: a table (Treeview) with one column per field."""
        columns = ("pet", "species", "owner", "reason", "vax")
        self.table = ttk.Treeview(parent, columns=columns,
                                  show="headings", height=6)
        headings = {"pet": "Pet", "species": "Species", "owner": "Owner",
                    "reason": "Reason", "vax": "Vaccinated"}
        widths = {"pet": 90, "species": 70, "owner": 110,
                  "reason": 160, "vax": 80}
        for col in columns:
            self.table.heading(col, text=headings[col])
            self.table.column(col, width=widths[col])
        self.table.pack(fill="both", expand=True)
 
    def refresh_table(self, patients):
        self.table.delete(*self.table.get_children())
        for p in patients:
            self.table.insert("", "end", values=(
                p.pet_name, p.species, p.owner_name, p.reason,
                "Yes" if p.vaccinated else "No"))




# ----------------------------------------------------------------------
# DRIVER
# ----------------------------------------------------------------------
def main():
    root = tk.Tk()
    root.title("Paws & Claws Veterinary - Patient Intake")

    model = IntakeModel()
    view = TextListIntakeView(root, IntakeModel.SPECIES)
    IntakeController(model, view)

    root.mainloop()


if __name__ == "__main__":
    main()