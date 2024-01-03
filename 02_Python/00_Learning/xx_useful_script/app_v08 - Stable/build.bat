pyinstaller --onefile app.py
copy ".\dist\app.exe" "app\"
copy ".\config.json" "app\"
timeout 5