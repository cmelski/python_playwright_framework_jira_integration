🧪 Python Playwright Test Automation Framework

A modern Python + Playwright test automation framework built with scalability, maintainability, and real-world QA practices in mind.
The framework integrates Allure reporting and Jira defect creation to provide full test failure visibility from execution to defect tracking.

🚀 Key Features

Page Object Model (POM) using composition

Pytest-based test execution

Automatic Jira issue creation on test failure

Allure reporting with screenshots, logs, and Jira links

Environment-based configuration

Designed for real-world CI/CD usage

🏗️ Framework Architecture

```text
allure-report/                     
allure-results/                  
core/
├── logging_utils.py 
integrations/ 
├── jira_client.py          calls to JIRA REST API         
page_objects/             
screenshots/                
test_run_logs/               
tests/                    
├── conftest.py   
├── test_scenarios.py    
pytest.ini
requirements.txt
test.env
```




📐 Design Patterns & Practices
Page Object Model (Composition-Based)

Page objects compose reusable components instead of inheriting large base classes

Improves flexibility and avoids deep inheritance chains

Encourages clean separation of concerns

Pytest Features Used

Fixtures (conftest.py)

Browser & page lifecycle management

Environment variable loading

Session and function-scoped fixtures

Markers

@pytest.mark.xfail for known issues

@pytest.mark.skip for conditional test execution

Custom markers for test grouping

Parameterization

Multiple test data sets for the same test logic

Keeps tests concise and expressive

🪝 Pytest Hooks
Failure Handling via pytest_runtest_makereport

On test failure, the framework automatically:

📸 Captures a Playwright screenshot

📄 Attaches execution logs

🐞 Searches for an existing Jira issue

➕ Creates a new Jira Bug if none exists

🔗 Adds the Jira issue link directly to the Allure report

This ensures zero silent failures and full traceability.

📊 Allure Reporting

Allure reports include:

Test execution status

Failure screenshots

Execution logs

Clickable Jira issue links

Jira issue key attached as test metadata

Generate Report
pytest --alluredir=allure-results
allure serve allure-results

🐞 Jira Integration
Features

Uses Jira Cloud REST API v3

JQL-based search to prevent duplicate defects

Automatically creates Bug issues on test failure

Uses Atlassian Document Format (ADF) for descriptions

Environment Variables Required:

JIRA_URL=https://your-domain.atlassian.net
JIRA_EMAIL=your-email@example.com
JIRA_API_TOKEN=your_api_token
JIRA_PROJECT=PROJECT_KEY
CREATE_JIRA_ON_FAILURE=true

🔐 Configuration Management

All sensitive values are injected via environment variables

No secrets are stored in code

Ready for CI tools like GitHub Actions, GitLab CI, Jenkins

▶️ Running Tests
pytest -m login --alluredir=allure-results


With logging enabled:

pytest -rA --log-cli-level=INFO --alluredir=allure-results

🧠 Why This Framework?

This project demonstrates:

Production-grade test automation design

Strong understanding of pytest internals

Real-world defect lifecycle automation

Clean architecture and maintainable code

Tooling that scales beyond toy examples

🛠️ Tech Stack

Python

Playwright

Pytest

Allure

Jira REST API (v3)