from datetime import date, timedelta

from fca.quiz_engine import Question, accuracy, build_session, check_answer
from fca.srs import SRSState, is_due, leitner_due, mastery, review


def test_sm2_success_intervals_and_ease():
    today = date(2026, 1, 1); s1 = review(SRSState(due=today), 5, today); s2 = review(s1, 5, today)
    assert s1.interval == 1 and s2.interval == 6
    assert s2.box == 3 and s2.ease >= 2.5


def test_sm2_failure_resets_and_never_drops_below_minimum():
    state = SRSState(4, 30, 1.31, date.today(), 4); failed = review(state, 0)
    assert failed.repetitions == 0 and failed.interval == 1 and failed.box == 3 and failed.ease >= 1.3


def test_due_mastery_and_leitner_rules():
    assert is_due(SRSState(due=date.today()))
    assert mastery(9, 1, 4) > mastery(5, 5, 2)
    assert leitner_due(3, date.today() - timedelta(days=4))


def test_quiz_strict_spelling_and_scoring():
    q = Question("type_in", "school", "école", [])
    assert check_answer(q, "école") and not check_answer(q, "ecole")
    assert accuracy([True, False, True, True]) == 75.0


def test_session_generation():
    words = [{"target": "maison", "tr": "ev"}, {"target": "livre", "tr": "kitap"},
             {"target": "porte", "tr": "kapı"}, {"target": "train", "tr": "tren"}]
    session = build_session(words, 4)
    assert len(session) == 4 and all(q.answer in q.options for q in session)
