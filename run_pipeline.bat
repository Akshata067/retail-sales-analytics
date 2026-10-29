@echo off
title Global Retail Analytics Pipeline Runner
echo ===============================================================================
echo Starting Retail Sales Data Analytics Master Pipeline...
echo ===============================================================================
C:\ProgramData\anaconda3\python.exe run_pipeline.py
if %ERRORLEVEL% NEQ 0 (
    echo [X] Pipeline failed with error code %ERRORLEVEL%.
) else (
    echo [V] Pipeline executed successfully!
)
echo ===============================================================================
pause
