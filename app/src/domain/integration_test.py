from app.src.domain.scenario import TaskQueue

def integration_test(tq: TaskQueue):
    n = 0
    pt = {'easy': tq.easy.unit_tested, 'medium': tq.easy.unit_tested, 'hard': tq.easy.unit_tested}
    

