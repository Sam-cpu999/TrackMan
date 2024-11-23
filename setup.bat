@echo off
setlocal
color 0A
set SOURCE_DIR=%~dp0packages
set DEST_DIR=C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\Lib\site-packages
set REQ_FILE=%~dp0requirements.txt
for /d %%i in ("%SOURCE_DIR%\*") do (
    echo Copying "%%i" to "%DEST_DIR%"
    xcopy "%%i" "%DEST_DIR%\%%~nxi" /E /I /H /Y
)
echo local packages are installed, now installing pip dependencies...
if exist "%REQ_FILE%" (
    echo Installing requirements from requirements.txt...
    pip install -r "%REQ_FILE%"
) else (
    echo requirements.txt not found.
)
color
pause
echo press any key to exit...
