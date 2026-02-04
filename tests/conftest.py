import os
import pytest
import allure
from playwright.sync_api import sync_playwright

# load test.env file variables
from dotenv import load_dotenv

load_dotenv("test.env")
import shutil
from pathlib import Path
from integrations.jira_client import get_or_create_issue
from core.logging_utils import logger_utility


import requests
import os


# pytest run parameters
# in terminal you can run for e.g. 'pytest test_web_framework_api.py --browser_name firefox'
def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="chrome", help="browser selection"
    )

    parser.addoption(
        "--url_start", action="store", default="test", help="starting url"
    )

    parser.addoption(
        "--env", action="store", default="test", help="Environment to run tests against")


@pytest.fixture(scope="session")
def env(request):
    env_name = request.config.getoption("--env")
    # Load the corresponding .env file
    load_dotenv(f"{env_name}.env")
    return env_name


def pytest_sessionstart(session):
    allure_dir = Path("allure-results")
    if allure_dir.exists():
        shutil.rmtree(allure_dir)
    allure_dir.mkdir(parents=True, exist_ok=True)


# Logging skip/xfail reasons yourself (advanced)
# If you want them in your own logs, use a hook.
def pytest_runtest_logreport(report):
    if report.skipped:
        logger_utility().info(f"SKIPPED: {report.nodeid} - {report.longrepr}")
    elif report.outcome == "xfailed":
        logger_utility().info(f"XFAIL: {report.nodeid} - {report.longrepr}")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to handle test failures:
    - attach screenshot & log to Allure
    - create Jira issue if enabled
    """
    outcome = yield
    report = outcome.get_result()

    # --------------------
    # Only act on failures in the test body
    # --------------------
    if report.when != "call":
        return

    if report.outcome != "failed":
        return

    logger_utility().info(f"Test failed: {item.nodeid}")

    # --------------------
    # Attach screenshot if page fixture exists
    # --------------------
    page = item.funcargs.get("page")
    if page:
        try:
            screenshot = page.screenshot()
            allure.attach(
                screenshot,
                name="Failure Screenshot",
                attachment_type=allure.attachment_type.PNG
            )
            logger_utility().info("Attached screenshot to Allure")
        except Exception as e:
            logger_utility().exception(f"Screenshot capture failed: {e}")
            print(f"Screenshot capture failed: {e}")

    # --------------------
    # Create Jira issue if enabled
    # --------------------
    if os.getenv("CREATE_JIRA_ON_FAILURE") == "true":
        #test_name = item.nodeid
        test_name = 'jira test'
        error = str(report.longrepr)
        try:
            issue_key = get_or_create_issue(test_name, error)
            if issue_key:
                logger_utility().info(f"Issue key: {issue_key}")
                print(f"Issue key: {issue_key}")
                # Add Allure link
                allure.dynamic.link(os.environ.get('JIRA_URL') + '/browse/' + issue_key,
                                    name=f"Jira: {issue_key}")

                # Optionally attach the issue key as text too
                allure.attach(f"Jira issue: {issue_key}", name="Jira Issue Key",
                              attachment_type=allure.attachment_type.TEXT)

            else:
                logger_utility().warning("get_or_create_issue returned None")
        except Exception as e:
            logger_utility().exception(f"Failed to create Jira issue: {e}")
            print(f"Failed to create Jira issue: {e}")

    # --------------------
    # Attach logs to Allure
    # --------------------
    log_path = "test_run_logs/test_run.log"
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            allure.attach(
                f.read(),
                name="Execution Log",
                attachment_type=allure.attachment_type.TEXT
            )
        logger_utility().info("Attached execution log to Allure")


@pytest.fixture(scope="session")
def url_start(env):  # env fixture ensures .env is loaded first
    return os.environ.get("BASE_URL")


# A fixture that runs automatically without being requested in the test. autouse=True
@pytest.fixture(autouse=True)
def log_test_start():
    logger_utility().info("Starting test run...")


# Another simple hook: before test run
def pytest_runtest_setup(item):
    print(f"▶ Starting {item.name}")
    logger_utility().info(f"▶ Starting {item.name}")


# A fixture that runs automatically without being requested in the test. autouse=True
# Framework-level concerns → autouse=True
@pytest.fixture(autouse=True)
def check_env(env):
    try:
        assert os.environ.get("BASE_URL"), "BASE_URL not set"
        logger_utility().info(f'BASE_URL is set: {os.environ.get("BASE_URL")}')
    except AssertionError:
        logger_utility().info('BASE_URL is not set')
        raise


@pytest.fixture(scope="function")
def page(request, url_start):
    browser_name = request.config.getoption("browser_name")

    with sync_playwright() as p:
        if browser_name == "chrome":
            browser = p.chromium.launch(headless=False)
        elif browser_name == "firefox":
            browser = p.firefox.launch(headless=False)

        context = browser.new_context()

        page = context.new_page()

        page.goto(url_start)

        try:
            yield page
        finally:
            context.close()
            browser.close()
