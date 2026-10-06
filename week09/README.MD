# Week 9 — Orchestrated Batch Scoring

## Overview

This assignment implements a small local DAG orchestrator to demonstrate two important workflow orchestration concepts:

1. **DAG-based task execution** — tasks are executed according to their dependencies using topological ordering.
2. **Task-level retries** — individual tasks can be retried when they fail transiently, similar to Airflow's per-task `retries` configuration.

The implementation does not require Apache Airflow or any external scheduler. A lightweight Python-based DAG orchestrator is used instead.

---

## Student Information

**Student ID:** `142602006`

**Generated Seed:** `4055787547`

The synthetic input data was generated using:

```bash
python generate_for_student.py --student-id 142602006
```

The generator created:

- 40 images
- 2 camera profiles
- 171 annotations
- COCO-format annotation file

---

## Project Structure

```text
week09-orchestrated-batch-scoring/
│
├── data/
│   └── fixtures/
│       ├── images/
│       └── _annotations.coco.json
│
├── src/
│   ├── dag.py
│   └── run_pipeline.py
│
├── generate_for_student.py
├── dag_run_summary.json
├── NOTES.md
└── README.md
```

> The exact file structure may vary depending on the starter repository provided for the assignment.

---

## DAG Workflow

The pipeline consists of four tasks:

```text
        extract
           |
         score
           |
          load
           |
         notify
```

The execution order observed in the run was:

```text
extract → score → load → notify
```

The orchestrator determines this order from task dependencies rather than simply following the order in which tasks appear in the Python file.

---

## Part 1 — Topological Ordering

The `topological_order()` function implements **Kahn's algorithm**.

The algorithm:

1. Calculates the in-degree of every task.
2. Finds tasks with zero dependencies.
3. Executes/removes those tasks from the dependency graph.
4. Decreases the in-degree of their dependent tasks.
5. Continues until all tasks are ordered.
6. Raises `ValueError` if:
   - A dependency does not exist.
   - A dependency cycle is detected.

For example:

```text
extract → score → load
```

must produce an order where:

```text
extract comes before score
score comes before load
```

Multiple valid orders are possible when independent tasks exist.

---

## Part 2 — Task Retry

The `run_task_with_retry()` function provides per-task retry behavior.

The `Task` dataclass contains:

```python
max_retries: int = 0
retry_delay_seconds: float = 0.0
```

If:

```python
max_retries = 2
```

the task can run up to **3 total attempts**:

```text
Attempt 1
   ↓
Failure
   ↓
Attempt 2
   ↓
Failure
   ↓
Attempt 3
   ↓
Success
```

The retry delay is implemented using:

```python
time.sleep(task.retry_delay_seconds)
```

If all attempts fail, the final exception is propagated.

---

## Part 3 — DAG Execution

The `run_dag()` function:

1. Calculates the topological order.
2. Executes each task using the same `context` dictionary.
3. Calls `run_task_with_retry()` for each task.
4. Records the task status and number of attempts.
5. Stops execution if a task ultimately fails.

A successful task is recorded as:

```python
{
    "status": "success",
    "attempts": 1
}
```

A failed task is recorded as:

```python
{
    "status": "failed",
    "attempts": 3,
    "error": "..."
}
```

---

## Running the Assignment

### Step 1 — Generate the fixtures

From the project root:

```bash
python generate_for_student.py --student-id 142602006
```

Expected output includes:

```text
student_id: 142602006
seed: 4055787547
Wrote 40 images across 2 camera profiles
Wrote 171 annotations
```

---

### Step 2 — Run the pipeline

Run:

```bash
python src/run_pipeline.py
```

The pipeline should display the execution order and task results.

My run produced:

```text
Execution order: ['extract', 'score', 'load', 'notify']

extract: {'status': 'success', 'attempts': 1}
score: {'status': 'success', 'attempts': 1}
load: {'status': 'success', 'attempts': 1}
notify: {'status': 'success', 'attempts': 3}
```

The pipeline also generated:

```text
dag_run_summary.json
```

---

## Execution Result

### Execution Order

```text
extract → score → load → notify
```

### Task Results

| Task | Status | Attempts |
|---|---|---:|
| extract | Success | 1 |
| score | Success | 1 |
| load | Success | 1 |
| notify | Success | 3 |

The `notify` task required three attempts because it failed transiently during its first two attempts and succeeded on the third attempt.

---

## Branch Independence

The DAG demonstrates that tasks in separate branches should not unnecessarily affect each other.

For example, if the DAG contains:

```text
       extract
          |
        score
       /     \
    load     notify
```

then `load` and `notify` are sibling tasks.

A failure in `notify` should not automatically cause `load` to fail because `load` does not depend on `notify`.

This demonstrates an important DAG property:

> A task should be affected by failures in its upstream dependencies, not by unrelated branches of the workflow.

---

## FinOps — Retry Cost

Retries improve reliability, but retries can also increase operational cost.

If `notify` were a metered API call where every attempt incurred a cost, blindly retrying every failure could become expensive.

For example:

```text
1 API call  →  ₹X
3 attempts  →  3 × ₹X
```

Therefore, retry strategies should consider:

- API cost per request
- Type of failure
- Maximum retry count
- Retry delay
- Rate limits
- Importance of the task
- Whether the failure is transient or permanent

A better strategy would be to retry transient failures such as temporary network errors while avoiding retries for permanent errors such as invalid credentials or malformed requests.

For expensive APIs, **exponential backoff** and a limited retry count can reduce unnecessary costs.

Therefore, the same retry policy should not necessarily be applied to every task. Retry behavior should balance:

```text
Reliability + Recovery + Cost
```

---

## Key Learnings

### 1. DAGs represent dependencies

A DAG is not simply a list of tasks. The execution order is determined by dependencies between tasks.

### 2. Topological sorting

Kahn's algorithm can be used to find an execution order that respects all dependencies.

### 3. Per-task retries

Retries can be configured at the individual task level instead of restarting the entire pipeline.

### 4. Shared context

The same context dictionary can be passed between tasks, allowing downstream tasks to use results generated by upstream tasks.

### 5. Branch independence

A failure in one branch should not unnecessarily affect unrelated branches.

### 6. FinOps-aware orchestration

Retries improve reliability but may increase costs, especially when tasks call metered external APIs.

---

## Conclusion

This Week 9 assignment demonstrates the basic principles behind workflow orchestration systems such as Airflow using a lightweight local implementation.

The pipeline successfully demonstrated:

- Dependency-aware DAG execution
- Topological ordering
- Per-task retry handling
- Shared task context
- Failure handling
- Branch independence
- Cost-aware retry considerations

The final pipeline completed successfully, with the `notify` task requiring **3 attempts** before succeeding.