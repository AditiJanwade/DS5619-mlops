# Week 8 — Drift and Observability Monitoring

**Course:** DS5619 — Machine Learning Systems Operations  
**Track:** BMD-45 Vehicle Detection  
**Student ID:** 142602006

## 1. Objective

This lab implements feature drift monitoring for a vehicle detector using **confidence scores** as the monitored feature.

The Population Stability Index (PSI) is used to compare the confidence-score distribution of a reference camera with the distribution observed from a live camera.

The lab uses two synthetic camera conditions:

- `camera_A_daylight` — reference distribution
- `camera_B_lowlight` — live distribution

These two camera profiles represent different visual conditions and are used as a synthetic example of domain shift.

## 2. Project Structure

```text
week08/
├── src/
│   ├── drift_monitor.py
│   ├── mock_detector.py
│   └── run_pipeline.py
│
├── data/
│   └── fixtures/
│       ├── camera_A_daylight/
│       ├── camera_B_lowlight/
│       └── _annotations.coco.json
│
├── tests/
│
├── generate_for_student.py
├── requirements.txt
├── NOTES.md
├── README.md
└── drift_report.json
```

## 3. Environment Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
```

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

### Linux / WSL

```bash
source .venv/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## 4. Generate the Dataset

The synthetic CCTV images are generated using the student ID:

```bash
python generate_for_student.py --student-id 142602006
```

The generated dataset contains two camera profiles with different visual conditions.

The generator produced:

```text
40 images
157 annotations
```

The generated seed was:

```text
1438761046
```

This seed is recorded in `NOTES.md`.

## 5. Drift Monitoring

Run the monitoring pipeline:

```bash
python src/run_pipeline.py
```

The pipeline:

1. Loads images from both camera directories.
2. Runs the provided mock detector.
3. Extracts confidence scores from the detections.
4. Treats `camera_A_daylight` as the reference distribution.
5. Treats `camera_B_lowlight` as the live distribution.
6. Computes the Population Stability Index (PSI).
7. Classifies the drift level.
8. Writes the results to `drift_report.json`.

## 6. PSI Interpretation

The following thresholds are used:

| PSI | Drift Level |
|---|---|
| `< 0.10` | None |
| `0.10 – < 0.25` | Moderate |
| `>= 0.25` | Significant |

## 7. Results

The pipeline produced the following results:

### Reference — `camera_A_daylight`

| Statistic | Value |
|---|---:|
| Count | 89 |
| Mean | 0.9732 |
| Standard deviation | 0.0415 |
| Minimum | 0.6270 |
| Maximum | 0.9800 |

### Live — `camera_B_lowlight`

| Statistic | Value |
|---|---:|
| Count | 78 |
| Mean | 0.9800 |
| Standard deviation | 0.0000 |
| Minimum | 0.9800 |
| Maximum | 0.9800 |

### Drift Result

```text
PSI = 0.1057
Drift level = moderate
```

The moderate drift is consistent with the fact that the two synthetic camera profiles were deliberately created with different visual statistics.

## 8. Implemented Functions

The following functions were implemented in `src/drift_monitor.py`:

### `extract_confidence_scores(camera_dir)`

Runs the detector on each `.jpg` image and collects the confidence score of every detection.

### `compute_psi(reference_scores, live_scores, n_bins)`

Calculates the Population Stability Index by:

- Dividing the confidence-score range `[0, 1]` into equal-width bins.
- Calculating reference and live proportions.
- Applying a minimum proportion of `1e-4`.
- Computing the PSI across all bins.

### `classify_drift(psi)`

Converts the PSI value into:

- `none`
- `moderate`
- `significant`

### `summarize_scores(scores)`

Calculates:

- Count
- Mean
- Standard deviation
- Minimum
- Maximum

The single-value case is handled with a standard deviation of `0.0`.

## 9. Limitations of Confidence-Score Monitoring

Confidence-score monitoring can identify changes in the distribution of model predictions, but it does not directly determine whether the predictions are correct.

If ground-truth labels become available later, additional model-performance metrics such as **detection accuracy and mAP** should be monitored.

This can reveal performance or concept drift that confidence-score-only monitoring may miss.

## 10. Testing

Run the test suite with:

```bash
pytest tests/ -q
```

The lab provides this as a self-check for the implementation.

## 11. Submission

The required deliverables are:

- `src/drift_monitor.py`
- `drift_report.json`
- `NOTES.md`
- `README.md`

Create the submission commit and tag:

```bash
git add -A
git commit -m "Week 8: drift and observability monitoring"
git tag week08-submit
git push origin main --tags
```

The `week08-submit` tag is the submission tag specified by the lab instructions.

## 12. Conclusion

This lab demonstrates univariate drift monitoring using detector confidence scores and the Population Stability Index. The comparison between the daylight reference camera and low-light live camera produced a PSI of **0.1057**, corresponding to **moderate drift**.