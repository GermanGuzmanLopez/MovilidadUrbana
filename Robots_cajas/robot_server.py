import mesa
from mesa.visualization.UserParam import UserSettableParameter
from robot_model import *

def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "r": 0.5}

    if agent.caja:
        portrayal["Color"] = "brown"
        portrayal["Layer"] = 0
        portrayal["r"] = 0.4
    else:
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 1

    return portrayal

grid = mesa.visualization.CanvasGrid(agent_portrayal, 10, 10, 500, 500)

chart = mesa.visualization.ChartModule([{"Label": "Boxes found and ready",
                      "Color": "Black"}],
                    data_collector_name = 'datacollector')

server = mesa.visualization.ModularServer(robot_model, [grid, chart], "Robot Model",
    {"n": 5,
    "k": UserSettableParameter("slider", "num_cajas", value = 50, max_value = 50, min_value = 1), 
    "width":10, "height":10,  
    "max_step": UserSettableParameter("slider", "Max_steps", value = 100, max_value = 500, min_value = 1)})

server.port = 8521 # The default
server.launch()