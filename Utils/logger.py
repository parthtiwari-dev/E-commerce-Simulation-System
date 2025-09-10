"""
Logger Utility Module

Purpose:
    Provides a centralized logging utility for the e-commerce system.
    Supports logging of informational messages, warnings, errors,
    and optionally to different outputs (stdout, file, etc.) with timestamps.

Key Responsibilities:
    - Standardize log message formats across all modules.
    - Include timestamps and log levels for each entry.
    - (Optional) Save to log files for persistent audit trails.
    - Make debugging and error tracking easier during development and stress tests.

Example Methods:
    info(msg):     Log a general system action or event.
    warning(msg):  Log a warning condition.
    error(msg):    Log an error, exception, or failure scenario.
    debug(msg):    (Optional) Log detailed trace/debug info for developers.

Notes:
    All services and models should import and use this logger for consistency.
"""
