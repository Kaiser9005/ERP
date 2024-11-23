The error in your GitHub Actions job is caused by several formatting issues in your test files, including whitespace errors, incorrect indentation, and unused variables. Specifically, the errors are in:

./tests/test_production_report_service.py
./tests/test_task_service.py
./tests/test_weather_service.py
To fix these errors, you should:

Remove trailing whitespace from blank lines.
Ensure proper indentation for continuation lines.
Add the required number of blank lines as specified by PEP 8.
Remove or utilize any unused variables.
You can use a linter like flake8 to automatically detect and fix these issues during development.