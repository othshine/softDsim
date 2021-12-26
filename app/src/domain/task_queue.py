from app.src.domain.task import Task


class TaskQueue:
    
    def __init__(self, tasks=[]) -> None:
        self.tasks = set([Task(**t) for t in tasks])
    
    def get(self, **kwargs) -> set:
        return {t for t in self.tasks if t.filter(**kwargs)}

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
