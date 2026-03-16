"""Conftest for HomeMatic tests — registers --run-live CLI flag."""


def pytest_addoption(parser):
    parser.addoption(
        "--run-live",
        action="store_true",
        default=False,
        help="Run live tests against a real CCU (requires CCU_URL + CCU_PASSWORD env vars)",
    )
