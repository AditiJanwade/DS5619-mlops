# NOTES.md — Week 2: Config-Driven Data Pipelines

**Student ID used with `generate_for_student.py`:**142602006


## What was hardcoded, and what would switching it have required?

<!-- What specifically was hardcoded in the original script, and what would
     have had to happen to change the threshold or switch formats before
     your refactor? -->
The original `pipeline_hardcoded.py` hardcoded the input path (`data/v1/transactions.csv`), high-value threshold (`5000`), and output path (`data/v1/report_hardcoded.json`).
The input format was effectively fixed to CSV because the original implementation used `load_csv()` and `csv.DictReader`.
Changing the threshold required modifying the Python source code and rerunning the script.
Switching from CSV to JSON would have required modifying the data-loading logic because the two formats are parsed differently.
After refactoring, the input path, input format, threshold, and output path are specified through YAML configuration.
I demonstrated this by running the same `pipeline.py` with CSV using threshold `1000` and JSON using threshold `500`.