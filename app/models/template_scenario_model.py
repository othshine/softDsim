from djongo import models

from app.models.decision_models.decision_model import Decision

from app.models.management_goal_model import ManagementGoal
from app.models.simulation_models.simulation_model import Simulation


class TemplateScenario(models.Model):
    """
    A `TemplateScenario` is a predefined 'Story' that users go through.
    When a user starts a scenario, a UserScenario is created.

    :param management_goal: ManagementGoal with budget, duration, tasks
    :tpe management_GOAL: `ManagementGoal`

    :param decisions: List of decisions
    :type decisions: List[Descision]

    :param simulation:
    :type simulation: `Simulation`
    """

    id = models.ObjectIdField()
    management_goal = models.OneToOneField(ManagementGoal, on_delete=models.CASCADE)
    decisions = models.ArrayField(Decision)
    simulation = models.OneToOneField(Simulation, on_delete=models.CASCADE)
