import pytest

from app.src.domain.team import Member, order_tasks_for_member
from app.src.domain.task import Task, Difficulty



def test_order_tasks_for_junior():
    easy = 23
    medium = 15
    hard = 39
    tasks = {Task(difficulty=t) for t in [*[1]*easy, *[2]*medium, *[3]*hard]}

    m = Member(skill_type='junior')

    tasks = order_tasks_for_member(tasks, m.skill_type)

    for i in range(easy):
        assert tasks[i].difficulty == Difficulty.EASY
    
    for i in range(easy, easy+medium):
        assert tasks[i].difficulty == Difficulty.MEDIUM
    
    for i in range(easy+medium, len(tasks)):
        assert tasks[i].difficulty == Difficulty.HARD
    

def test_order_tasks_for_expert():
    easy = 23
    medium = 15
    hard = 39
    tasks = {Task(difficulty=t) for t in [*[1]*easy, *[2]*medium, *[3]*hard]}

    m = Member(skill_type='expert')

    tasks = order_tasks_for_member(tasks, m.skill_type)

    for i in range(hard):
        assert tasks[i].difficulty == Difficulty.HARD
    
    for i in range(hard, hard+medium):
        assert tasks[i].difficulty == Difficulty.MEDIUM
    
    for i in range(hard+medium, len(tasks)):
        assert tasks[i].difficulty == Difficulty.EASY

def test_order_tasks_for_senior():
    easy = 23
    medium = 15
    hard = 39
    tasks = {Task(difficulty=t) for t in [*[1]*easy, *[2]*medium, *[3]*hard]}

    m = Member(skill_type='senior')

    tasks = order_tasks_for_member(tasks, m.skill_type)

    for i in range(medium):
        assert tasks[i].difficulty == Difficulty.MEDIUM
    
    for i in range(medium, easy+medium+hard):
        assert tasks[i].difficulty == Difficulty.HARD or tasks[i].difficulty == Difficulty.EASY
    