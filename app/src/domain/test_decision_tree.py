import unittest
from app.src.domain.decision_tree import Answer, Decision, Scenario

class TestDecisionTree(unittest.TestCase):

    def test_answer(self):
        text = "This is the answer's text"
        a = Answer(text, 100)
        self.assertEqual(a.points, 100)
        self.assertEqual(a.text, text)


    def test_decision(self):
        text_d = "This is the decision's text"
        d = Decision(text_d)
        self.assertEqual(len(d), 0)
        text_a = "This is the answer's text"
        a = Answer(text_a, 100)
        d.add(a)
        self.assertEqual(len(d), 1)
        self.assertEqual(d.answers[0], a)
        a2 = Answer(text_a, 0)
        d.add(a2)
        self.assertEqual(len(d), 2)
        self.assertEqual(d.answers[0], a)

    def test_decision(self):
        d = Decision("")
        d.add_answer("Answer", 100)
        self.assertEqual(d.answers[0], Answer("Answer", 100))

    def test_decision_get_max_points(self):
        d = Decision("")
        d.add_answer("Answer", 0)
        d.add_answer("Answer", 100)
        d.add_answer("Answer", 50)
        self.assertEqual(100, d.get_max_points())

    def test_scenario_is_iterator(self):
        s = Scenario()
        with self.assertRaises(StopIteration):
            next(s)

    def test_scenario_has_next_decisions(self):
        s = Scenario()
        d1 = Decision("1")
        d1.add_answer("Answer", 100)
        s.add(d1)
        d2 = Decision("2")
        d2.add_answer("Answer2", 50)
        s.add(d2)
        self.assertEqual(d1, next(s))
        self.assertEqual(d2, next(s))

    def test_scenario_remove(self):
        s = Scenario()
        self.assertEqual([], s._decisions)
        d1 = Decision("1")
        d1.add_answer("Answer", 100)
        s.add(d1)
        self.assertEqual([d1], s._decisions)
        d2 = Decision("2")
        d2.add_answer("Answer2", 50)
        s.add(d2)
        self.assertEqual([d1, d2], s._decisions)
        s.remove(0)
        self.assertEqual([d2], s._decisions)

    def test_scenario_num_of_desicions(self):
        s = Scenario()
        self.assertEqual(len(s), 0)
        s.add(Decision(""))
        self.assertEqual(len(s), 1)
        s.add(Decision(""))
        self.assertEqual(len(s), 2)
        s.remove(1)
        self.assertEqual(len(s), 1)

    def test_scenario_max_points(self):
        s = Scenario()
        self.assertEqual(0, s.get_max_points())
        d1 = Decision("1")
        d1.add_answer("Answer", 100)
        s.add(d1)
        self.assertEqual(100, s.get_max_points())
        d2 = Decision("2")
        d2.add_answer("Answer2", 50)
        s.add(d2)
        self.assertEqual(150, s.get_max_points())















































if __name__ == '__main__':
    unittest.main()
