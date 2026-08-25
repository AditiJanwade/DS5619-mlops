# NOTES.md — Week 4: Versioning, Feature Store & Lineage

**Student ID used with `generate_for_student.py`:**

142602006
**Seed used:** `155703109`

## v1 vs. v2 manifest comparison

The v1 and v2 feature-group manifests have the same feature-group name, `card_activity`, but they have different version IDs and different raw source version IDs.

- v1 feature group has `feature_group_version_id: v1` and points to raw version `v1`.
- v2 feature group has `feature_group_version_id: v2` and points to raw version `v2`.
- Both record the transformation version and the feature schema.
- The v2 feature group is registered as a new version instead of overwriting v1. This preserves the history and lineage of the previous feature group.
- The `row_count` can also differ because the v1 and v2 source datasets contain different numbers of transactions.



## Why treat amount_minor_units differently from amount?

In v1, the transaction amount is stored directly in the normal currency unit, such as `24.73`.

In v2, the amount is stored as an integer in minor currency units (cents), such as `3972`, which represents `39.72`.

Therefore, `build_features` divides `amount_minor_units` by 100 before calculating the aggregates. This converts the v2 values back to the same unit as the v1 `amount` values.

Without this conversion, the average and maximum amounts from v1 and v2 would not be comparable. For example:

`3972 / 100 = 39.72`

This allows the same feature calculations to be applied consistently across both schema versions.
