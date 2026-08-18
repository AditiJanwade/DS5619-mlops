# NOTES.md — Week 3: ETL and Data Validation

**Student ID used with `generate_for_student.py`:**  
`142602006`

**Generator seed:**  
`3724441359`

## Quarantine count vs. the 7 known injected problems

The pipeline processed **600 rows** and quarantined **6 rows**. There were **8 total validation violations**.

The 6 quarantined rows do not exactly match the 7 known injected problems because the expectation suite does not include a validation check for the country code. Therefore, the invalid country-code row was not detected and was not quarantined.

Some rows also triggered more than one expectation. In particular, rows with a null/empty `amount` failed both `expect_column_not_null` and `expect_column_positive`. This resulted in **8 violations across 6 distinct rows**.

### Results

- Total rows: **600**
- Clean rows: **594**
- Quarantined rows: **6**
- Total violations: **8**
- Known injected problems: **7**
- Undetected injected problem: **invalid country code**, because no country-code expectation is included in the provided suite.

## Validation Results

The pipeline found 8 expectation violations across 6 rows:

- `expect_column_not_null` — 2 violations
- `expect_column_positive` — 3 violations
- `expect_column_in_set` — 1 violation
- `expect_column_unique` — 1 violation

The 8 violations correspond to 6 distinct rows because some rows failed more than one expectation. In particular, the two rows with empty/null `amount` values failed both the `not_null` and `positive` expectations.

## Why 6 Rows Were Quarantined Instead of 7

The generated dataset contains 7 injected problem types/rows, but only **6 rows were quarantined** by this validation suite.

The reason is that the assignment's expectation suite does **not** validate the country code column. Therefore, the injected invalid country-code row is not detected and passes through as a clean row.

The duplicate transaction ID also illustrates how violations are counted: when two rows share the same transaction ID, `expect_column_unique` only flags the **second occurrence**, as required by the expectation specification.

Therefore:

- **7 injected problematic rows**
- **6 rows detected and quarantined**
- **1 invalid-country row not detected because there is no country-code expectation**
- **8 total expectation violations**, because two null-amount rows each trigger two expectations

The quarantine count of **6** is therefore expected given the supplied expectation suite.