
# Week 7 — CI/CD Integration Testing

## Overview

This week focuses on integrating automated testing into a CI/CD pipeline using
GitHub Actions.

The project contains a Flask-based vehicle detection API, unit tests for the
API, a lightweight mock detector, and a Docker-based integration test.

The CI pipeline contains three jobs:

1. **lint** — checks the Python source code using Flake8.
2. **unit-test** — runs the Flask unit tests using pytest.
3. **integration-test** — builds and runs the Docker application and verifies
   the API using the integration test script.

The integration test runs only after both linting and unit tests pass.

---

## Project Structure

```text
week07/
├── .github/
│   └── workflows/
│       └── ci.yml
├── _shared/
│   ├── generate_synthetic_fixtures.py
│   └── student_seed.py
├── data/
│   └── fixtures/
│       ├── _annotations.coco.json
│       ├── camera_A_daylight/
│       └── camera_B_lowlight/
├── scripts/
│   └── integration_test.sh
├── src/
│   ├── app.py
│   └── mock_detector.py
├── tests/
│   ├── test_app.py
│   └── test_ci_config.py
├── CI_VERIFICATION.md
├── Dockerfile
├── NOTES.md
├── requirements.txt
├── setup.cfg
└── generate_for_student.py
```

---

## Application

The project contains a Flask inference API that exposes two endpoints.

### Health Check

```text
GET /health
```

Returns:

```json
{
  "status": "ok"
}
```

### Vehicle Detection

```text
POST /detect
```

The endpoint accepts an uploaded image using the form field:

```text
image
```

and returns detection results in JSON format.

The current implementation uses a lightweight mock detector so that the CI
pipeline can run without requiring a GPU or a large machine-learning model.

---

## Local Setup

### 1. Create a virtual environment

From the `week07` directory:

```bash
python3 -m venv .venv
```

Activate it on Linux/WSL:

```bash
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## Running Tests Locally

### Run all tests

```bash
pytest tests/ -q
```

The Week 7 test suite passes successfully.

Expected result:

```text
12 passed
```

### Run Flake8

```bash
flake8 src/
```

The Flake8 configuration is defined in:

```text
setup.cfg
```

---

## Docker

The application can also be containerized using the provided `Dockerfile`.

### Build the Docker image

From the `week07` directory:

```bash
docker build -t week07-detector .
```

### Run the container

```bash
docker run --rm -p 8080:8080 week07-detector
```

The Flask API will be available at:

```text
http://localhost:8080
```

### Test the health endpoint

```bash
curl http://localhost:8080/health
```

Expected response:

```json
{
  "status": "ok"
}
```

---

## Integration Test

The integration test is located at:

```text
scripts/integration_test.sh
```

It performs the following steps:

1. Builds the Docker image.
2. Starts the container.
3. Waits for the application to become available.
4. Sends a request to the `/health` endpoint.
5. Sends an image to the `/detect` endpoint.
6. Verifies the API response.
7. Stops and removes the container.

Run it with:

```bash
chmod +x scripts/integration_test.sh
./scripts/integration_test.sh
```

---

# GitHub Actions CI/CD

The CI workflow is located at:

```text
.github/workflows/ci.yml
```

The workflow is triggered on:

- Pushes to `main`
- Pull requests targeting `main`

The pipeline contains three jobs.

## 1. Lint

The `lint` job:

- Sets up Python 3.11.
- Installs dependencies.
- Runs Flake8 against `src/`.

```yaml
- name: Lint
  working-directory: week07
  run: flake8 src/
```

---

## 2. Unit Test

The `unit-test` job:

- Sets up Python 3.11.
- Installs dependencies.
- Runs the pytest test suite.

```yaml
- name: Run unit tests
  working-directory: week07
  run: pytest tests/
```

---

## 3. Integration Test

The `integration-test` job:

- Runs after both `lint` and `unit-test`.
- Builds and runs the Docker application.
- Executes the integration test script.

The dependency is configured using:

```yaml
needs: ["lint", "unit-test"]
```

This prevents the more expensive Docker-based integration test from running
when basic linting or unit tests have already failed.

---

## CI Pipeline

The workflow can be represented as:

```text
             Git Push / Pull Request
                      |
          +-----------+-----------+
          |                       |
          v                       v
        lint                  unit-test
          |                       |
          +-----------+-----------+
                      |
                      v
             integration-test
                      |
                      v
                Docker + API
```

The `integration-test` job starts only when both `lint` and `unit-test`
complete successfully.

---

## CI Verification

The successful GitHub Actions run is documented in:

```text
CI_VERIFICATION.md
```

Successful workflow:

```text
https://github.com/AditiJanwade/DS5619-mlops/actions/runs/35787456513
```

The successful run completed all three jobs:

```text
lint               PASS
unit-test          PASS
integration-test   PASS
```

---

## Why CI/CD Is Useful

Continuous Integration helps detect problems automatically whenever code is
pushed to the repository or submitted through a pull request.

This Week 7 pipeline checks the project at three levels:

- **Linting** catches code-quality issues.
- **Unit testing** verifies application behavior.
- **Integration testing** verifies that the application works correctly when
  packaged and executed inside Docker.

Running these checks automatically provides faster feedback and reduces the
chance of merging code that breaks the application or its deployment
environment.

---


