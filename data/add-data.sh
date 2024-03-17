#!/usr/bin/env bash

set -e

curl -X POST --location "http://127.0.0.1:8000/polls/questions" \
    -H "Accept: application/json" \
    -H "Authorization: API-key test" \
    -d '[
  {
    "id": 1,
    "question_text": "Who are you?",
    "choices": [
      {"choice_text": "John Smith" },
      {"choice_text": "Roger Moore" },
      {"choice_text": "Zaphod Beeblebrox" }
    ]
  },
  {
    "id": 2,
    "question_text": "Do you prefer cats or dogs?",
    "choices": [
      {"choice_text": "Yes" },
      {"choice_text": "No" }
    ]
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
