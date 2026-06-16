# Troubleshooting

## App Does Not Start

Symptom:
- Python starts and exits with import or GUI-related errors

Checks:
- Confirm you are in the project virtual environment
- Confirm `Pillow` is installed
- Confirm Python includes `tkinter`

## Missing PIL/Pillow Error

Symptom:
- `ModuleNotFoundError: No module named 'PIL'`

Fix:

```bash
pip install Pillow
```

## Tkinter Not Available

Symptom:
- Import error for `tkinter`

Fix:
- Install a Python distribution that bundles tkinter
- On macOS, python.org installers are typically the easiest path

## No Calculation Result

Symptom:
- Warning appears and no result is shown

Checks:
- Ensure at least one non-empty valid line is entered
- Ensure lines are not all `nan`, `none`, or `null`

## Export Creates Unexpected File Content

Checks:
- CSV export writes one column named `Unique_Drugs`
- TXT export writes a titled numbered list
- Confirm you chose the expected extension in the save dialog

## Icon Not Displayed

Symptom:
- App opens without custom icon

Notes:
- This does not affect calculations
- The app continues if icon loading fails
