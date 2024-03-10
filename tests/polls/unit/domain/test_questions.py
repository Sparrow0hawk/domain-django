from polls.domain.questions import Question, Choice


class TestQuestions:
    def test_question_create(self) -> None:
        question = Question(id_=1, question_text="What is your favourite sandwich?")

        assert question.id == 1 and question.question_text == "What is your favourite sandwich?"

    def test_question_add_choices(self) -> None:
        question = Question(id_=1, question_text="What is your favourite sandwich?")

        question.add_choices(
            Choice(id_=2, choice_text="Marmite and Cheese"),
            Choice(id_=3, choice_text="Ham and Cheese"),
        )

        assert question.id == 1 and question.question_text == "What is your favourite sandwich?"
        answer1: Choice
        answer2: Choice
        answer1, answer2 = question.choices
        assert (
            answer1.id == 2
            and answer1.choice_text == "Marmite and Cheese"
            and answer2.id == 3
            and answer2.choice_text == "Ham and Cheese"
        )
