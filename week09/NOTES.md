# NOTES.md — Week 9: Orchestrated Batch Scoring

**Student ID used with `generate_for_student.py`:**  
142602006

**Seed:**  
4055787547

## notify retry count

The `notify` task took **3 attempts** in my run.

It failed on the first two attempts and succeeded on the third attempt. This happened because `max_retries=2`, which allows a maximum of 3 total attempts.

From `dag_run_summary.json`:

```text
notify: {'status': 'success', 'attempts': 3}
```

## Branch independence

`load` still succeeds because it is an independent branch of the DAG and does not depend on `notify`.

The execution order was:

```text
extract → score → load
                  \
                   → notify
```

The failure of `notify` on its first two attempts did not affect `load` because `load` does not depend on `notify`. This shows that a failure in one branch of a DAG should not automatically stop or affect an unrelated branch. Tasks should only be blocked when one of their required upstream dependencies fails.

In my run, `notify` eventually succeeded after its retries, so all four tasks completed successfully.

## Retry cost under FinOps

If `notify` were a metered API call where every attempt cost money, I would avoid blindly retrying it with the same retry policy as every other task.

I would first determine whether the failure is **transient** or **permanent**. Transient errors such as temporary network failures or rate limits may justify retries, while permanent errors such as invalid credentials or invalid request data should not be repeatedly retried.

I would also use a **limited number of retries with exponential backoff**, so that repeated failures do not create unnecessary API costs. For expensive tasks, I might use fewer retries or disable retries completely when the expected cost is higher than the benefit.

Therefore, "retry every failed task the same way" is risky because different tasks have different failure types, costs, and business importance. A FinOps-aware retry strategy should balance **reliability, recovery, and cost**.