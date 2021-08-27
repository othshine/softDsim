import pytest

from app.src.domain.scenario import Scenario


@pytest.mark.django_db
def test_answer_can_be_saved():
    answer = Answer("Waterfall", 100, result_text="OK")

    repo = repository.DjangoRepository()
    repo.add(answer)

    [saved_answer] = django_models.Answers.objects.all()
    assert saved_answer.text == answer.text
    assert saved_answer.points == answer.points
    assert saved_answer.result_text == answer.result_text

