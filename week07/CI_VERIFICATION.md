# CI verification

The Week 7 CI pipeline was successfully executed on a real GitHub Actions
runner after pushing the Week 7 implementation to the repository.

## Workflow run

Successful GitHub Actions run:

https://github.com/AditiJanwade/DS5619-mlops/actions/runs/35787456513

## Job summary

All three CI jobs passed successfully:

- `lint`: PASS — 14 seconds
- `unit-test`: PASS — 10 seconds
- `integration-test`: PASS — 20 seconds

## What broke on the way there

During development, the CI workflow initially failed because the workflow
commands were not running from the `week07` working directory. This caused
Flake8 to use the wrong configuration and report lint errors.

The workflow was corrected by setting `working-directory: week07` for the
Week 7 install, lint, unit-test, and integration-test steps. After the fix,
all three GitHub Actions jobs passed successfully.
