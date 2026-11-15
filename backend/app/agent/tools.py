from app.simulation.water import simulate
from app.models.schemas import Scenario

def scenario_summary(s:Scenario):
    return simulate(s)['summary']
