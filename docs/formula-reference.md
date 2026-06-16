# Formula Reference

DiaMOND Genie computes plate requirements from three counts derived from your input list.

## Counting Terms

- `singles`: combinations that contain exactly one drug
- `unique_constituent_drugs`: unique drug names observed across all valid lines
- `total_combos`: total number of valid combination lines

## Formula

`raw_result = (unique_constituent_drugs + singles + total_combos) / plates_per_calculation * multiplier`

`final_result = ceil(raw_result)`

## Default Parameters

- `plates_per_calculation = 28`
- `multiplier = 3`

## Example Walkthrough

Input lines:

```text
A
A+B
A+C
B+C
```

Counts:

- `singles = 1`
- `unique_constituent_drugs = 3`
- `total_combos = 4`

Compute:

`raw_result = (3 + 1 + 4) / 28 * 3 = 0.8571...`

`final_result = ceil(0.8571...) = 1`

Result: 1 plate.

## Interpretation Notes

- Result is always rounded up to the next whole plate
- If no valid combinations are detected, the app returns an error condition
