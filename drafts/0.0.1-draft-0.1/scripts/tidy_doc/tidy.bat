@echo off

where tidy > nul 2>&1
if errorlevel 1 (
    echo Error: 'tidy' could not be found. Please install it and run this script again.
    exit 1
)

tidy -config tidy.config -m ..\..\dcat-eia.html
