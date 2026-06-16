# Documentation Maintenance

Use this checklist whenever behavior changes in the app.

## Update Triggers

- Formula or count logic changes
- Input parsing behavior changes
- Tab labels or user-facing messages change
- Export format changes
- Setup/runtime dependency changes

## Required Updates

1. Update root README sections affected by the change
2. Update the corresponding guide in docs
3. Verify internal links still resolve
4. Verify at least one worked example still matches app output

## Quality Checklist

- New user can install and run from README only
- Formula examples are mathematically correct
- Terminology is consistent across pages
- Troubleshooting covers newly introduced failure modes

## Suggested Ownership

- Feature author updates docs in the same pull request
- Reviewer checks docs as a required review item
