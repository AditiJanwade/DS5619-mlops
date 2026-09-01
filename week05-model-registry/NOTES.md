# NOTES.md — Week 5: Model Registry Governance

## Student ID used with `generate_for_student.py`

142602006

## Which candidate reached Production, and why?

Candidate B reached Production because it had a completed model card and its F1 score was 0.847, which is above the Production threshold of 0.70. Candidate A was blocked because its F1 score was 0.48, which is below the required threshold. Candidate A was also initially blocked because it did not have a model card.

## Gating stale feature data

To block promotion of a model trained on stale feature data, I would add a feature-data freshness check to the Production gate in `promote_model`. The model manifest could store the feature data timestamp, such as `feature_data_timestamp`. During Production promotion, the code could compare this timestamp with the current time. If the feature data is more than 30 days old, `promote_model` would raise a `GovernanceError` and prevent the model from reaching Production.

For example, the gate could check:

```python
if feature_data_age_days > 30:
    raise GovernanceError(
        "Production promotion blocked: feature data is older than 30 days."
    )
```

## Scaling the gate to 40 candidates

The current design already supports multiple candidates because `register_model` creates a new version for each registered model, and `promote_model` applies the governance checks to the specific model version being promoted. Therefore, the basic gate does not need to change just because there are 40 candidates.

For 40 AutoML/HPO candidates, I would register each candidate as a separate model version with its metrics and model card. Then `promote_model` could apply the same Production gate to every candidate. The main additional need would be an automated selection or ranking step to compare the 40 candidates and identify which candidates should be evaluated for promotion. The governance rules themselves can remain the same and should be applied consistently to every candidate.
