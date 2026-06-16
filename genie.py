# --- Imports: libraries this program needs ---
import tkinter as tk  # tkinter is Python's built-in toolkit for building windows/buttons/etc (the GUI)
from tkinter import messagebox, scrolledtext, filedialog  # popup messages, scrollable text boxes, and "save/open file" dialogs
from tkinter import ttk  # "themed tkinter" - nicer-looking versions of buttons, labels, etc.
import math  # used here for math.ceil(), which rounds a number UP to the next whole number
from typing import List, Dict, Union, Tuple  # these are just labels for what kind of data a function expects/returns (helps readability)
from PIL import Image, ImageTk  # used to load the genie icon image


# This class does the actual MATH. It has no GUI code at all -
# it just takes in drug combination text and works out how many plates are needed.
class PlateCalculator:
    def __init__(self, plates_per_calculation: int = 28, multiplier: int = 3):
        # These are the two "settings" the formula uses. They have default values
        # (28 and 3) but can be changed later from the GUI.
        self.plates_per_calculation = plates_per_calculation
        self.multiplier = multiplier

    # Takes the raw lines of text the user typed (e.g. "DrugA + DrugB")
    # and turns each line into a clean, sorted tuple of drug names, e.g. ("DrugA", "DrugB").
    # Lines that are empty or look like missing data (nan/none/null) are skipped.
    def parse_combos(self, combo_drugs: List[str]) -> List[Tuple[str, ...]]:
        parsed = []
        for combo_str in combo_drugs:
            # Skip blank lines or placeholder "missing value" text
            if not combo_str or combo_str.strip() == "" or str(combo_str).lower() in ['nan', 'none', 'null']:
                continue
            # Split "DrugA + DrugB" into ["DrugA", "DrugB"], trimming extra spaces
            drugs = [drug.strip() for drug in str(combo_str).split("+") if drug.strip()]
            if drugs:
                # Sort the drug names so "A+B" and "B+A" are treated as the same combo
                parsed.append(tuple(sorted(drugs)))
        return parsed

    # This is the main calculation. Given a list of combo lines, it returns a
    # dictionary (like a labeled set of results) describing how many plates are needed.
    def calculate_plates(self, combo_drugs: List[str]) -> Dict[str, Union[int, float]]:
        combos = self.parse_combos(combo_drugs)

        # If nothing valid was entered, return all-zero results plus an error message
        if not combos:
            return {
                "singles": 0,
                "unique_constituent_drugs": 0,
                "total_combos": 0,
                "raw_result": 0.0,
                "final_result": 0,
                "error": "No valid combinations found"
            }

        # Count how many "combos" are actually just a single drug (no "+")
        single_count = sum(1 for combo in combos if len(combo) == 1)

        # Build a list of every distinct drug name that appears anywhere,
        # keeping the order they were first seen in.
        unique_constituent_drugs = []
        seen_drugs = set()  # a "set" is used because checking "have I seen this before?" is fast
        for combo in combos:
            for drug in combo:
                if drug not in seen_drugs:
                    unique_constituent_drugs.append(drug)
                    seen_drugs.add(drug)
        unique_constituent_count = len(unique_constituent_drugs)
        total_combos = len(combos)

        # The actual formula:
        # (unique drugs + single-drug entries + total combos) divided by plates_per_calculation,
        # then multiplied by the multiplier.
        raw_result = (unique_constituent_count + single_count + total_combos) / self.plates_per_calculation * self.multiplier

        # Round UP to the nearest whole plate, since you can't have a fraction of a plate
        final_result = math.ceil(raw_result)

        return {
            "singles": single_count,
            "unique_constituent_drugs": unique_constituent_count,
            "total_combos": total_combos,
            "raw_result": raw_result,
            "final_result": final_result
        }

# ---------- GUI ----------
# This class builds and controls the WINDOW the user sees and interacts with.
# It uses the PlateCalculator class above to do the actual math.
class PlateCalculatorGUI:
    def __init__(self):
        # Create the main application window
        self.root = tk.Tk()
        self.root.title("DiaMOND Genie 🧞‍♀️")
        self.root.geometry("900x750")  # window size: 900px wide, 750px tall

        # Try to load the genie icon for the window's title bar.
        # If anything goes wrong (e.g. file missing), just skip it silently.
        try:
            import os
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "genie.ico")
            genie_icon = Image.open(icon_path)
            genie_image = ImageTk.PhotoImage(genie_icon)
            self.root.iconphoto(True, genie_image)
        except Exception:
            pass

        # color scheme - a dictionary of hex color codes used throughout the UI
        self.colors = {
            'background_main': "#E1D8F4",
            'background_secondary': "#E1D8F4",
            'background_dark': "#943BE8",
            'text_dark': "#943BE8",
            'text_light': "#2E2C2C",
            'accent': "#943BE8",
            'success': "#18C641",
            'error': "#DC143C"
        }
        self.root.configure(background=self.colors['background_main'])

        # ---------- VARIABLES ----------
        # tk.StringVar() creates a value that the GUI can watch/update automatically.
        # These hold the status message and the two formula settings.
        self.calculation_status = tk.StringVar(value="Ready to calculate No. of plates!")
        self.plates_per_calc = tk.StringVar(value="28")
        self.multiplier = tk.StringVar(value="3")

        # ---------- CALCULATOR ----------
        # Create one instance of the math class defined above - this is what
        # actually computes the results when the user clicks "Calculate".
        self.calculator = PlateCalculator()

        # ---------- STYLE ----------
        # Set up the custom look (colors, fonts) for buttons/labels/tabs
        self.style = ttk.Style()
        self.setup_styles()

        # ---------- SETUP UI ----------
        # Build all the tabs, buttons, text boxes, etc.
        self.setup_ui()

    # ---------- STYLE SETUP ----------
    # This defines named "styles" (like CSS classes) that get applied to
    # widgets below, e.g. style="Accent.TButton" on a button.
    def setup_styles(self):
        # General Frame (a "Frame" is an invisible container that holds other widgets)
        self.style.configure("Custom.TFrame", background=self.colors['background_secondary'])

        # Notebook = the tabbed view (the "Plate Calculator" / "Constituent Drugs" tabs)
        self.style.configure("Custom.TNotebook", background=self.colors['background_main'])
        self.style.configure("Custom.TNotebook.Tab", background=self.colors['background_secondary'], foreground=self.colors['text_dark'], font=("San Francisco", 11, "bold"))
        # Buttons - "Accent" is the main purple button style
        self.style.configure("Accent.TButton", background=self.colors['accent'], foreground=self.colors['text_light'], font=("San Francisco", 12, "bold"), padding=5)
        self.style.map("Accent.TButton",
                       foreground=[('active', self.colors['text_light'])],
                       background=[('active', self.colors['background_dark'])])
        # "Success" is the green button style (used for the Import button)
        self.style.configure("Success.TButton", background=self.colors['success'], foreground=self.colors['text_light'], font=("San Francisco", 11, "bold"), padding=5)
        self.style.map("Success.TButton",
                       background=[('active', self.colors['accent'])])
        # Labels (plain text shown on screen)
        self.style.configure("Custom.TLabel", background=self.colors['background_secondary'], foreground=self.colors['text_dark'], font=("San Francisco", 12, "bold"))

    # ---------- UI SETUP ----------
    # Creates the tabbed notebook and adds the two tabs/screens to it.
    def setup_ui(self):
        self.notebook = ttk.Notebook(self.root, style="Custom.TNotebook")
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)

        self.create_manual_tab()
        self.create_unique_drugs_tab()

    # function to clear all entries
    # Resets both tabs back to their starting/empty state.
    def clear_all(self):
        # Clear manual input
        self.manual_text.delete(1.0, tk.END)
        # Clear unique drugs input
        self.unique_drugs_text.delete(1.0, tk.END)
        # Clear unique drugs listbox
        self.unique_drugs_listbox.delete(0, tk.END)
        # Reset count label
        self.unique_count_label.config(text="Total constituent drugs: 0")
        # Reset status
        self.calculation_status.set("Ready to calculate No. of plates!")

    

    # function to creat text section for manually entering drug combinations
    # Builds the FIRST tab: "Plate Calculator" - a big text box where the user
    # types one drug combination per line, plus Calculate/Clear buttons.
    def create_manual_tab(self):
        manual_frame = ttk.Frame(self.notebook, style="Custom.TFrame")
        self.notebook.add(manual_frame, text="Plate Calculator")

        input_frame = ttk.Frame(manual_frame, style="Custom.TFrame")
        input_frame.pack(fill='both', expand=True, padx=10, pady=10)

        label = ttk.Label(input_frame, text="Drug Combinations:", style="Custom.TLabel")
        label.pack(anchor='w', pady=(0,5))

        # The big multi-line text box where the user types/pastes drug combos
        self.manual_text = scrolledtext.ScrolledText(
            input_frame, height=15, wrap=tk.WORD,
            font=("San Francisco", 10), background='white', foreground='black', insertbackground='black'
        )
        self.manual_text.pack(fill='both', expand=True)

        # "command=" links the button to the function that runs when it's clicked
        calc_button = ttk.Button(input_frame, text="Calculate no. of plates", command=self.calculate_manual, style="Accent.TButton")
        calc_button.pack(pady=10)
        clear_button = ttk.Button(input_frame, text="Clear All", command=self.clear_all, style="Accent.TButton")
        clear_button.pack(pady=5)



    # ---------- UNIQUE DRUGS TAB ----------
    # Builds the SECOND tab: "Constituent Drugs" - lets the user paste combos,
    # extract every distinct drug name, view them in a list, and export to a file.
    def create_unique_drugs_tab(self):
        unique_frame = ttk.Frame(self.notebook, style="Custom.TFrame")
        self.notebook.add(unique_frame, text="Constituent Drugs")

        # label secrion
        label = ttk.Label(unique_frame, text="Drug Combinations:", style="Custom.TLabel")
        label.pack(anchor='w', pady=(0,5))

        # Input Section
        input_section = ttk.Frame(unique_frame, style="Custom.TFrame")
        input_section.pack(fill='both', expand=True, padx=10, pady=10)

        # Text box for pasting/typing drug combinations on this tab
        self.unique_drugs_text = scrolledtext.ScrolledText(
            input_section, height=8, wrap=tk.WORD,
            font=("San Francisco", 10), background='white', foreground='black', insertbackground='black'
        )
        self.unique_drugs_text.pack(fill='both', expand=True)

        # Buttons Frame
        buttons_frame = ttk.Frame(input_section, style="Custom.TFrame")
        buttons_frame.pack(fill='x', padx=10, pady=5)

        # "Extract Unique Drugs" reads the text above and finds every distinct drug name
        extract_button = ttk.Button(buttons_frame, text="Extract Unique Drugs", command=self.extract_unique_drugs, style="Accent.TButton")
        extract_button.pack(side='left', padx=(0,5))

        # "Import from Plate Calculator" copies the text from the first tab into this tab
        import_button = ttk.Button(buttons_frame, text="Import from Plate Calculator", command=self.import_from_manual_tab, style="Success.TButton")
        import_button.pack(side='right', padx=(5,0))

         # label secrion
        label = ttk.Label(unique_frame, text="Constiruent Drug List:", style="Custom.TLabel")
        label.pack(anchor='w', pady=(0,5))

        # Results Section
        results_section = ttk.LabelFrame(unique_frame, style="Custom.TFrame")
        results_section.pack(fill='both', expand=True, padx=10, pady=10)


        results_frame = ttk.Frame(results_section, style="Custom.TFrame")
        results_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Listbox = the scrollable list that shows each unique drug found
        self.unique_drugs_listbox = tk.Listbox(results_frame, font=("San Francisco", 10), background='white', foreground='black', height=8)
        self.unique_drugs_listbox.pack(side='left', fill='both', expand=True)

        # Scrollbar attached to the listbox above
        scrollbar = tk.Scrollbar(results_frame, command=self.unique_drugs_listbox.yview)
        scrollbar.pack(side='right', fill='y')
        self.unique_drugs_listbox.config(yscrollcommand=scrollbar.set)

        # Stats + Export
        stats_frame = ttk.Frame(results_section, style="Custom.TFrame")
        stats_frame.pack(fill='x', padx=10, pady=5)

        # Label showing how many unique drugs were found
        self.unique_count_label = ttk.Label(stats_frame, text="Total constituent drugs: 0", style="Custom.TLabel")
        self.unique_count_label.pack(side='left')

        # "Export List" saves the unique drug list to a .txt or .csv file
        export_button = ttk.Button(stats_frame, text="Export List", command=self.export_unique_drugs, style="Accent.TButton")
        export_button.pack(side='right')

    # ---------- FUNCTIONALITY ----------
    # Runs when "Calculate no. of plates" is clicked on the first tab.
    def calculate_manual(self):
        try:
            # Get everything typed in the text box, removing leading/trailing whitespace
            text_content = self.manual_text.get(1.0, tk.END).strip()
            if not text_content:
                messagebox.showwarning("⚠️ Warning", "Please enter some drug combinations!")
                return

            # Update the calculator's settings from the (currently unused) StringVars.
            # NOTE: int(...) will throw a ValueError if the text isn't a whole number.
            self.calculator.plates_per_calculation = int(self.plates_per_calc.get())
            self.calculator.multiplier = int(self.multiplier.get())

            # Turn the text box into a list of lines (one combo per line), skipping blanks
            drug_combos = [line.strip() for line in text_content.split('\n') if line.strip()]

            # Run the math (defined in PlateCalculator above) and show the results popup
            results = self.calculator.calculate_plates(drug_combos)
            self.show_results(results)

        except ValueError:
            messagebox.showerror("❌ Error", "Please enter valid numbers for parameters.")
        except Exception as e:
            messagebox.showerror("❌ Error", f"Calculation failed:\n{str(e)}")

    # Displays the calculation results in a popup dialog.
    def show_results(self, results):
        if 'error' in results:
            messagebox.showerror("❌ Error", results['error'])
            return

        result_message = (
            f"You'll need {results['final_result']} plates for your DiaMOND Assay!\n\n"
            f"• Total number of drug combinations: {results['total_combos']}\n"
            f"• Unique constituent drugs: {results['unique_constituent_drugs']}\n"
            f"• Single drugs: {results['singles']}\n"
        )
        messagebox.showinfo("✅ Calculation Results", result_message)

    # Runs when "Import from Plate Calculator" is clicked.
    # Copies the text from the first tab's text box into this tab's text box.
    def import_from_manual_tab(self):
        manual_content = self.manual_text.get(1.0, tk.END).strip()
        if manual_content:
            self.unique_drugs_text.delete(1.0, tk.END)
            self.unique_drugs_text.insert(1.0, manual_content)
            messagebox.showinfo("✅ Success", "Drugs imported from platw calculator tab!")
        else:
            messagebox.showwarning("⚠️ Warning", "No data found in Manual Input tab!")

    # Runs when "Extract Unique Drugs" is clicked.
    # Reads every line of "DrugA + DrugB" style text and lists each distinct drug name once.
    def extract_unique_drugs(self):
        text_content = self.unique_drugs_text.get(1.0, tk.END).strip()
        if not text_content:
            messagebox.showwarning("⚠️ Warning", "Please enter some drug combinations!")
            return

        # Split the text box into individual non-empty lines
        lines = [line.strip() for line in text_content.split('\n') if line.strip()]
        self.unique_drugs_listbox.delete(0, tk.END)  # clear out any previous results

        seen_drugs = set()           # fast lookup of drugs already added
        unique_drugs_ordered = []    # keeps drugs in the order they were first seen
        for line in lines:
            # Split "DrugA + DrugB" into ["DrugA", "DrugB"]
            drugs_in_combo = [drug.strip() for drug in line.split("+") if drug.strip()]
            for drug in drugs_in_combo:
                if drug and drug not in seen_drugs:
                    unique_drugs_ordered.append(drug)
                    seen_drugs.add(drug)

        # Fill the listbox widget with each unique drug name
        for drug in unique_drugs_ordered:
            self.unique_drugs_listbox.insert(tk.END, drug)

        self.unique_count_label.config(text=f"Total unique drugs: {len(unique_drugs_ordered)}")
        messagebox.showinfo("✅ Success", f"Found {len(unique_drugs_ordered)} unique drugs!")

    # Runs when "Export List" is clicked.
    # Saves the unique drug list to a .txt or .csv file chosen by the user.
    def export_unique_drugs(self):
        if self.unique_drugs_listbox.size() == 0:
            messagebox.showwarning("⚠️ Warning", "No unique drugs to export!")
            return

        # Pull every item out of the listbox into a plain Python list
        drugs_list = [self.unique_drugs_listbox.get(i) for i in range(self.unique_drugs_listbox.size())]

        # Open the OS "Save File" dialog so the user picks a name/location
        filename = filedialog.asksaveasfilename(title="Save Unique Drugs List", defaultextension=".txt",
                                                filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv"), ("All files", "*.*")])
        if filename:
            with open(filename, 'w') as f:
                if filename.endswith('.csv'):
                    # CSV format: one header row, then one drug per row
                    f.write("Unique_Drugs\n")
                    for drug in drugs_list:
                        f.write(f"{drug}\n")
                else:
                    # Plain text format: title, separator line, count, then numbered list
                    f.write("Unique Drugs List\n")
                    f.write("=" * 20 + "\n")
                    f.write(f"Total count: {len(drugs_list)}\n\n")
                    for i, drug in enumerate(drugs_list, 1):
                        f.write(f"{i:2d}. {drug}\n")

            messagebox.showinfo("✅ Success", f"Unique drugs list exported to:\n{filename}")


# ---------- RUN APP ----------
# This is the entry point - it only runs when you execute this file directly
# (e.g. `python genie.py`), not when it's imported by another file.
if __name__ == "__main__":
    app = PlateCalculatorGUI()   # create the window and all its widgets
    app.root.mainloop()          # start the GUI's event loop (keeps the window open and responsive)
