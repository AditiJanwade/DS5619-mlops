# Week 05 — Mini Model Registry

## Overview

This project implements a small local model registry to demonstrate basic ML model governance concepts without requiring an MLflow or Weights & Biases server.

The registry provides four main capabilities:

1. Register trained model versions as artifacts.
2. Generate and validate model cards.
3. Promote models between deployment stages using governance gates.
4. Identify the model currently deployed to Production.

The main implementation is in `src/mini_model_registry.py`, while `src/run_pipeline.py` demonstrates the complete workflow.

---

## Project Structure

```text
week05-model-registry/
│
├── data/
│   ├── candidate_a/
│   │   ├── model.json
│   │   └── metrics.json
│   │
│   └── candidate_b/
│       ├── model.json
│       └── metrics.json
│
├── src/
│   ├── mini_model_registry.py
│   └── run_pipeline.py
│
├── model_card_fields.json
├── generate_for_student.py
├── NOTES.md
├── registry_summary.json
└── README.md
```

---

## Model Registry

The registry stores each model version under:

```text
.model_registry/
└── models/
    └── fraud-detector/
        ├── v1/
        ├── v2/
        └── ...
```

Each registered version contains:

```text
model.json
manifest.json
model_card.json
```

The manifest records information such as:

* Model name
* Version ID
* Metrics
* Current stage
* Creation time
* Promotion history

---

## Governance Rules

A newly registered model starts with:

```text
stage = None
```

A model can be promoted to:

* `Staging`
* `Production`

### Production Gate

A model can reach Production only when **both** conditions are satisfied:

1. A completed `model_card.json` exists.
2. The model's F1 score is at least `0.70`.

The Production threshold is defined as:

```python
PRODUCTION_F1_THRESHOLD = 0.70
```

If either condition fails, a `GovernanceError` is raised.

---

## Model Card

The model card must contain the following required fields:

```text
intended_use
training_data
limitations
ethical_considerations
```

Each field must:

* Exist
* Contain a non-empty string
* Not contain the literal `TODO`

This prevents incomplete model cards from being used to satisfy the Production governance requirement.

---

## Pipeline Workflow

The pipeline performs the following steps:

### 1. Generate Student Data

Run:

```powershell
python generate_for_student.py --student-id 142602006
```

For this submission, the generated seed was:

```text
3394887505
```

The generated model metrics were:

```text
candidate_a: f1 = 0.48
candidate_b: f1 = 0.847
```

### 2. Run the Pipeline

Run:

```powershell
python src/run_pipeline.py
```

The pipeline:

1. Registers candidate A.
2. Registers candidate B.
3. Attempts to promote candidate A without a model card.
4. Blocks candidate A because the model card is missing.
5. Generates a model card for candidate A.
6. Attempts to promote candidate A again.
7. Blocks candidate A because its F1 score is below `0.70`.
8. Generates a model card for candidate B.
9. Promotes candidate B to Production.
10. Writes `registry_summary.json`.

---

## Expected Result

The successful run produced:

```text
Registered candidate_a as v13, candidate_b as v14

[expected] promoting v13 with no card was blocked:
Production promotion blocked: model card is missing for fraud-detector v13.

[expected] promoting v13 with f1 below threshold was blocked:
Production promotion blocked: f1=0.48 is below the required threshold of 0.7.

Promoted v14 to Production.

Wrote registry_summary.json:
production version is v14
```

The version numbers may be different on a clean run because the registry automatically allocates the next available version.

---

## Production Model

After the successful pipeline execution, candidate B is the Production model.

For this run:

```text
Production version: v14
F1 score: 0.847
```

The registry also maintains a promotion history containing:

```json
{
  "from_stage": "None",
  "to_stage": "Production",
  "at": "..."
}
```

If another version is promoted to Production later, the previous Production version is automatically moved to:

```text
Archived
```

This ensures that there is only one Production version of a model at a time.

---

## Output

The pipeline creates:

```text
registry_summary.json
```

The summary contains:

```json
{
  "model_name": "fraud-detector",
  "production_version": "v14",
  "production_metrics": {
    "f1": 0.847
  }
}
```

The exact metrics structure depends on the generated candidate metrics.

---

## Key Concepts Demonstrated

### Artifact Store

Each trained model is stored as an immutable, named version rather than storing many nearly identical training runs.

### Model Card

The model card provides governance information about:

* Intended use
* Training data
* Limitations
* Ethical considerations

### Governance Gate

Production promotion is not simply a stage rename. The registry checks whether the model satisfies the required governance conditions before allowing promotion.

### Audit Trail

Every successful stage change is recorded in the manifest's `history` list.

### Single Production Model

When a new model reaches Production, the previous Production version is archived automatically.

---

## How to Run

From the project root:

```powershell
python generate_for_student.py --student-id 142602006
```

Then:

```powershell
python src/run_pipeline.py
```

Check the generated summary:

```text
registry_summary.json
```

---

## Submission Notes

Student ID:

```text
142602006
```

Generated seed:

```text
3394887505
```

Candidate A F1:

```text
0.48
```

Candidate B F1:

```text
0.847
```

Production threshold:

```text
0.70
```

Final successful Production model in the recorded run:

```text
v14
```

The seed should also be recorded in `NOTES.md` as required by the assignment.
