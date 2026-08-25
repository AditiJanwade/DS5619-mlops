# Lab 4 — Versioning, Feature Store & Lineage

**Track A (tabular fraud-detection) · Week 4 · DS5619 Machine Learning Systems Operations**

## Overview

This lab implements a small, local, dependency-free feature store that demonstrates:

1. **Raw data versioning** using content hashes.
2. **Feature group versioning** with lineage back to the exact raw data version.
3. **Schema evolution** from transaction schema v1 to v2 without overwriting history.
4. **Lineage lookup** from a feature group version back to its source raw version.

All registry information is stored as readable JSON files under `.feature_store/`.

## Student Data

The transaction data was generated using:

```bash
python generate_for_student.py --student-id 142602006
```

- **Student ID:** `142602006`
- **Generated seed:** `155703109`
- **v1 records:** 500
- **v2 records:** 125

The generated files are:

```text
data/
├── v1/
│   └── transactions.csv
└── v2/
    └── transactions.csv
```

## Project Structure

```text
week04-versioning-feature-store/
├── data/
│   ├── v1/
│   │   └── transactions.csv
│   └── v2/
│       └── transactions.csv
├── src/
│   ├── mini_feature_store.py
│   └── run_pipeline.py
├── tests/
├── .feature_store/
├── lineage_report.json
├── NOTES.md
├── generate_for_student.py
├── requirements.txt
└── README.md
```

## Implementation

### Part 1 — Raw Data Versioning

`snapshot_raw_version()` stores a raw dataset version using the SHA-256 content hash of the input file.

The same file content always produces the same hash. Therefore, if the same data is registered again, the existing version ID is returned instead of creating a duplicate.

Raw versions are stored as:

```text
.feature_store/
└── raw_versions/
    ├── v1/
    │   └── manifest.json
    └── v2/
        └── manifest.json
```

Each raw manifest records:

- `version_id`
- `source_path`
- `content_hash`
- `columns`
- `row_count`
- `created_at`

### Part 2 — Feature Engineering

`build_features()` creates one feature row per `card_id`.

The generated features are:

| Feature | Description |
|---|---|
| `card_id` | Card identifier |
| `txn_count` | Number of transactions for the card |
| `avg_amount` | Average transaction amount |
| `max_amount` | Maximum transaction amount |
| `pct_card_present` | Fraction of transactions where the card was present |
| `event_time` | Latest transaction timestamp |

The function handles both transaction schemas.

#### v1 Schema

v1 contains:

```text
amount
country
timestamp
```

#### v2 Schema

v2 contains:

```text
amount_minor_units
country_code
device_fingerprint
timestamp
```

For v2, `amount_minor_units` is divided by 100 before aggregation so that amounts are comparable with v1.

For example:

```text
3972 / 100 = 39.72
```

The input column is `timestamp`, which is stored in the generated feature as `event_time`.

### Part 3 — Feature Group Registration

`register_feature_group()` creates a new immutable version each time it is called.

The feature groups are stored as:

```text
.feature_store/
└── feature_groups/
    └── card_activity/
        ├── v1/
        │   ├── features.json
        │   └── manifest.json
        └── v2/
            ├── features.json
            └── manifest.json
```

The feature-group manifest records:

- `feature_group_version_id`
- `name`
- `source_raw_version_id`
- `transform_version`
- `schema`
- `row_count`
- `created_at`

The v2 feature group is therefore a new version rather than an overwrite of v1.

### Part 4 — Lineage

`get_lineage()` reads the feature-group manifest and follows its `source_raw_version_id` to the corresponding raw-data manifest.

The resulting lineage has the form:

```text
Feature Group
     │
     │ source_raw_version_id
     ▼
Raw Data Version
```

The combined lineage information is written to:

```text
lineage_report.json
```

## Running the Pipeline

Run:

```bash
python src/run_pipeline.py
```

The successful run produced:

```text
v1 raw version: v1 -> feature group version: v1
v2 raw version: v2 -> feature group version: v2
idempotency check ok: re-snapshotting v1 returned v1
Wrote .../lineage_report.json
```

The idempotency check confirms that registering the same v1 data again returns the existing `v1` raw version.

## Self-Check

Run the provided tests with:

```bash
pytest tests/ -q
```

## Deliverables

The completed submission contains:

- `src/mini_feature_store.py`
- `.feature_store/`
- `lineage_report.json`
- `NOTES.md`
- `README.md`
- Student-specific `data/v1/transactions.csv`
- Student-specific `data/v2/transactions.csv`

## Key Concepts Demonstrated

This lab demonstrates three important machine-learning systems concepts:

### Data Versioning

Raw datasets are identified by content hashes and stored as immutable versions.

### Feature Store

Features are generated from raw data and stored in versioned feature groups.

### Data Lineage

Each feature group records exactly which raw-data version was used to produce it.

This allows changes in upstream schemas to be handled without silently changing or destroying historical data.
