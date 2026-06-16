# Input Format

This page defines valid and invalid input patterns for DiaMOND Genie.

## Accepted Structure

- One combination per line
- Drug names separated by `+`
- Leading and trailing spaces are ignored

Examples:

```text
DrugA
DrugA+DrugB
DrugA+DrugB+DrugC
```

## Ignored Entries

The parser skips lines that are:

- Empty after trimming spaces
- String equivalents of missing values:
- `nan`
- `none`
- `null`

Case is ignored for these missing-value tokens.

## Normalization Behavior

- Drugs inside each line are trimmed
- Empty tokens produced by repeated separators are dropped
- A line with at least one valid token is kept

Example:

```text
DrugA +  DrugB +
```

Is treated as:

```text
DrugA+DrugB
```

## Practical Guidance

- Use consistent spelling for each drug name to avoid accidental duplicates
- Keep naming conventions stable across experiments
- If you use aliases, normalize names before pasting input
