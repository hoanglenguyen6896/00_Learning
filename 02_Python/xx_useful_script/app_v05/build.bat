pyinstaller --onefile app.py
copy ".\dist\app.exe" "app\"
copy config.json ".\dist\"
timeout 5