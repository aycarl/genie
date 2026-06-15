# DiaMOND Genie

DiaMOND Genie is a desktop app for estimating how many plates are needed in high-throughput checkerboard DiaMOND assays.

The app takes drug combinations as input, computes key counts used in the assay workflow, and returns a rounded-up plate count.

## Who This Is For

- Lab scientists and research users running checkerboard combination assays
- Team members who need a quick, repeatable plate estimate from a list of combinations

## What The App Does

- Accepts one drug combination per line, for example `A+B` or `A+B+C`
- Calculates:
- Total combinations
- Unique constituent drugs across all combinations
- Number of single-drug entries
- Applies the DiaMOND plate estimate formula and rounds up to a whole number
- Extracts and exports unique drug names from the input list

## What The App Does Not Do

- It does not validate biological plausibility or dose design
- It does not replace assay design review
- It does not persist projects or run batch files automatically

## Quick Scientific Context

In a checkerboard-style combination assay, practical plate planning depends on:

- How many combinations are tested
- How many unique constituent drugs are represented overall
- Whether single-drug conditions are included

DiaMOND Genie converts those counts into a plate estimate using the project formula implemented in code.

## Formula Used

The app calculates:

- `singles`: number of lines containing exactly one drug
- `unique_constituent_drugs`: unique drugs appearing in any line
- `total_combos`: total valid input lines

Then computes:

`raw_result = (unique_constituent_drugs + singles + total_combos) / plates_per_calculation * multiplier`

`final_result = ceil(raw_result)`

Current defaults in the app are:

- `plates_per_calculation = 28`
- `multiplier = 3`

## Installation

### Requirements

- Python 3.9 or newer recommended
- `tkinter` available in your Python installation
- `Pillow` Python package

### Setup (pip + venv)

1. Create and activate a virtual environment.

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

2. Install dependency:

```bash
pip install Pillow
```

## Run The App

From project root:

```bash
python genie.py
```

## Input Format

- Enter one combination per line
- Use `+` to separate drugs in a combination
- Empty lines are ignored
- Values that are blank or equivalent to `nan`, `none`, or `null` are ignored

Examples:

```text
DrugA
DrugA+DrugB
DrugA+DrugC
DrugB+DrugC+DrugD
```

## App Workflow

### 1) Plate Calculator tab

- Paste or type combinations in the Drug Combinations box
- Click Calculate no. of plates
- Review calculated totals in the results dialog

### 2) Constituent Drugs tab

- Paste combinations or import from Plate Calculator tab
- Click Extract Unique Drugs to generate unique drug list
- Click Export List to save as `.txt` or `.csv`

## Worked Example

Input:

```text
A
A+B
A+C
B+C
```

Computed counts:

- singles = 1
- unique_constituent_drugs = 3 (`A`, `B`, `C`)
- total_combos = 4

Formula:

`raw_result = (3 + 1 + 4) / 28 * 3 = 0.8571...`

`final_result = ceil(0.8571...) = 1`

Estimated plates: 1

## Export Output

- CSV export: single-column file with header `Unique_Drugs`
- TXT export: human-readable numbered list with total count

## Troubleshooting

- App fails on launch with tkinter errors:
- Install a Python distribution that includes tkinter
- On macOS, prefer official python.org installers if needed
- `ModuleNotFoundError: PIL`:
- Run `pip install Pillow` in the active virtual environment
- No icon shown:
- The app falls back safely if `genie.ico` is missing or cannot be loaded
- Empty result warnings:
- Ensure input has at least one non-empty valid line

## Documentation Map

- Main guide: this file
- Input details: [docs/input-format.md](docs/input-format.md)
- Formula reference: [docs/formula-reference.md](docs/formula-reference.md)
- Troubleshooting: [docs/troubleshooting.md](docs/troubleshooting.md)
- Documentation maintenance: [docs/documentation-maintenance.md](docs/documentation-maintenance.md)

## Current Scope And Limitations

- GUI-only operation from a local desktop session
- No command-line interface for calculation
- No built-in assay template management

## Contributing To Documentation

If behavior changes in the app, update README and related pages in docs in the same change set.

Start with the checklist in [docs/documentation-maintenance.md](docs/documentation-maintenance.md).
