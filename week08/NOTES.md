# NOTES.md — Week 8: Drift and Observability Monitoring

## Student ID used with `generate_for_student.py`

142602006

## Seed

1438761046

## Drift level vs. expectation

The drift report showed a **PSI of 0.1057**, which corresponds to a **moderate** drift level.

This matches the expectation because `camera_A_daylight` and `camera_B_lowlight` were deliberately generated with different visual conditions. Therefore, a difference in the confidence-score distributions between the two cameras is expected.

## What confidence-score-only monitoring misses

If ground-truth labels were available a day later, I would additionally monitor the detector's actual performance, such as **detection accuracy and mAP**.

Confidence-score monitoring detects changes in the distribution of model confidence scores, but it cannot determine whether the predictions are correct. Therefore, confidence-score-only monitoring can miss **performance/concept drift** that affects the relationship between the input data and the correct detection outcome.