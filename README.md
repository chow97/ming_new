python3 -m venv ming_venv
deactivate
source ming_venv/bin/activate
pip install -r requirements.txt
pyinstaller --onefile --windowed your_app.py

