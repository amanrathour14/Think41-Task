@echo off
echo 🚀 Milestone Commit Tool
echo.

if "%1"=="" (
    echo Usage: commit-milestone.bat [milestone_number] [description]
    echo Example: commit-milestone.bat 2 "Backend Foundation"
    exit /b 1
)

if "%2"=="" (
    echo Usage: commit-milestone.bat [milestone_number] [description]
    echo Example: commit-milestone.bat 2 "Backend Foundation"
    exit /b 1
)

powershell -ExecutionPolicy Bypass -File "commit-milestone.ps1" -MilestoneNumber %1 -Description "%2" 