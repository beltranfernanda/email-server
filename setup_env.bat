@echo off
python --version > NUL 2>&1
IF %ERRORLEVEL% EQU 0 (
    SET PYTHON_CMD=python
) ELSE (
    python3 --version > NUL 2>&1
    IF %ERRORLEVEL% EQU 0 (
        SET PYTHON_CMD=python3
    ) ELSE (
        echo Python is not installed.
        exit /b 1
    )
)

%PYTHON_CMD% -m venv .venv
call .venv\Scripts\activate
pip install -r requirements.txt
