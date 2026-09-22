# NOTES.md — Week 7: CI/CD Integration Testing

**Student ID used with `generate_for_student.py`:**
142602006

## Why gate integration-test on needs: [lint, unit-test]?

The `integration-test` job is more expensive than the lint and unit-test
jobs because it builds and runs a Docker container and then performs HTTP
requests against the running application.

Using `needs: [lint, unit-test]` ensures that the integration test runs only
after both linting and unit tests have passed. If the code has a linting
error or a unit-test failure, there is no need to spend time building and
starting the Docker container.

This saves CI time and compute resources and gives faster feedback when
there is a basic code or test failure. It also prevents an unnecessary
Docker-based integration test from running when the application has already
failed earlier CI checks.
