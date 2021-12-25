from app.src.domain.task import Task


class TaskQueue:
    
    def __init__(self) -> None:
        self.tasks = set([])
    
    def get(self) -> set:
        return self.tasks

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
