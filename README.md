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
   
   # install dependencies including dev dependencies
   pip install .[dev]
   
   # install playwright browsers
   playwright install
   ```
3. Start Django app on http://127.0.0.1:8000
   ```bash
   python manage.py runserver
   ```
4. Use cURL to POST data to local app
   ```bash
   curl -X POST --location "http://localhost:8000/polls/questions" \
    -H "Accept: application/json" \
    -d '[
           {
             "id": 1,
             "question_text": "Who are you?"
           },
           {
             "id": 2,
             "question_text": "Do you prefer cats or dogs?"
           },
           {
             "id": 3,
             "question_text": "What is your favourite sandwich?"
           },
           {
             "id": 4,
             "question_text": "How much wood would a woodchuck chuck?"
           }
       ]'
   ```
4. Run tests
   ```bash
   make test
   ```
5. Run full build
   ```bash
   make verify
   ```
