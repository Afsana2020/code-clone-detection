HOW TO RUN ON YOUR PC (Python 3.14):

1. Extract web_app.zip to a folder

2. Open terminal/command prompt in that folder

3. Install directly (no venv needed):
   pip install flask==3.0.0 torch==2.3.0 transformers==4.40.0 numpy==1.26.4

4. Run the app:
   python app.py

5. Open browser to: http://localhost:5000

Note: If torch fails to install, try:
   pip install torch --index-url https://download.pytorch.org/whl/cpu
