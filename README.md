# Django minimal

A simple Django setup following from Django tutorial (sort of).

## Setup

To use this project you will need:
- Python 3.12

1. Create virtual environment
   ```bash
   python3.12 -m venv --prompt . .venv
   ```
2. Install project dependencies
   ```bash
   # activate virtual environment
   . .venv/bin/activate
   
   # install dependencies
   pip install -r requirements.txt
   ```
3. Start Django app on http://127.0.0.1:8000
   ```bash
   python manage.py runserver
   ```
4. Run Django tests
   ```bash
   python manage.py test
   ```
