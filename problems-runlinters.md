The error in the GitHub Actions job logs is due to multiple lines in the typing_extensions.py file that exceed the maximum allowed line length (79 characters). This is causing the linter to fail with error code E501.

How to Fix the Error:
Open typing_extensions.py file located in the virtual environment directory (./venv/lib/python3.12/site-packages/typing_extensions.py).
Modify each line that exceeds 79 characters to either:
Break the line into multiple shorter lines.
Refactor the code to reduce line length.
You can also adjust the linter configuration to allow longer lines if appropriate.