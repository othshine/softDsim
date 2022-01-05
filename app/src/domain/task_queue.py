from app.src.domain.task import Task


class TaskQueue:
    
    def __init__(self, tasks=[]) -> None:
        self.tasks = set([Task(**t) for t in tasks])
    
    def __str__(self):
        txt =   "=== Task Queue ===\n"
        txt += f"Size:        {len(self.tasks)}\n"
        txt += f"Done:        {len(self.get(done=True))}\n"
        txt += f"Unit Tested: {len(self.get(unit_tested=True))}\n"
        txt += f"Int. Tested: {len(self.get(integration_tested=True))}\n"
        txt += f"Bug:         {len(self.get(bug=True))}\n"
        txt += f"Spec. T/F:   {len(self.get(correct_specification=True))}/{len(self.get(correct_specification=False))}\n"
        return txt 
    
    def get(self, n=None, **kwargs) -> set[Task]:
        filtered =  {t for t in self.tasks if t.filter(**kwargs)}
        if not n is None and n < len(filtered):
            filtered = set(list(filtered)[:n])
        return filtered
    
    def size(self, **kwargs) -> int:
        """Returns the len of the TQ with all given filters applied."""
        return len({t for t in self.tasks if t.filter(**kwargs)})


    def add(self, t) -> None:
        """Adds a task or multiple tasks to the queue.

        Args:
            t (Tasks or List[Task] or Set[Task]): Task Object(s) to be added.

        Raises:
            TypeError: If t is neither a Task or list/set of tasks.
        """
        if t is None:
            return
        if isinstance(t, Task):
            self.tasks.add(t)
        elif isinstance(t, set) or isinstance(t, list):
            for task in t: 
                self.add(task)
        else:
            raise TypeError(f"t must be of type Task or must be a set/list of objects of type Task not {type(t)}")
    
    @property
    def json(self):
        return {'tasks': [t.json for t in self.tasks]}
    
    @property
    def quality_score(self):
        k = 8
        return int(((len(self.tasks) - (len(self.get(bug=True)) + len(self.get(done=False)))) * 1/len(self.tasks))**k * 100)
    
    def reset_cascade(self, task: Task):
        tasks_to_reset = set()
        tasks_to_reset.add(task)

        d = True
        while d:
            d = False
            for t in self.tasks:
                if t.pred in {ta.id for ta in tasks_to_reset} and t not in tasks_to_reset:
                    tasks_to_reset.add(t)
                    d = True
        for task in tasks_to_reset:
            task.reset()

    def false_spec(self) -> int:
        return (len(self.get(correct_specification=False)))
    
    def bugs(self) -> int:
        return (len(self.get(bug=True)))
    
    def deploy(self) -> int:
        return (len(self.get(done=True, unit_tested=True, integration_tested=True, bug=False, correct_specification=True)))

    def total(self) -> int:
        return len(self.tasks)
    
    def not_done(self) -> int:
        return len(self.get(done=False))

    