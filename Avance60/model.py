import mesa
from agents import *
import json
from random import choice

class RandomModel(mesa.Model):
    """ 
    Creates a new model with random agents.
    Args:
        N: Number of agents in the simulation
    """
    def __init__(self, N):

        dataDictionary = json.load(open("/Users/USER/code/python/MovilidadUrbana/mapDictionary.json"))

        self.traffic_lights = []
        self.destinos = []

        with open('/Users/USER/code/python/MovilidadUrbana/BaseMap.txt') as baseFile:
            lines = baseFile.readlines()
            self.width = len(lines[0])-1
            self.height = len(lines)


            self.grid = mesa.space.MultiGrid(self.width, self.height, torus = False) 
            self.schedule = mesa.time.RandomActivation(self)
            self.Tschedule = mesa.time.RandomActivation(self)
            self.Rschedule = mesa.time.BaseScheduler(self)

            for r, row in enumerate(lines):
                for c, col in enumerate(row):
                    if col in ["v", "^", ">", "<"]:
                        agent = Road(f"r_{r*self.width+c}", self, dataDictionary[col])
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.Rschedule.add(agent)

                    elif col in ["S", "s"]:
                        agent = Traffic_Light(f"tl_{r*self.width+c}", self, False if col == "S" else True)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.Tschedule.add(agent)
                        self.traffic_lights.append(agent)

                    elif col == "#":
                        agent = Obstacle(f"ob_{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))

                    elif col == "D":
                        agent = Destination(f"d_{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.destinos.append(agent)


            for i in range(N):
                a = Car(i, self, choice(self.destinos))
                notfound = True
                while notfound:
                    agente = choice(self.Rschedule.agents)
                    cellmates = self.grid.get_cell_list_contents((agente.pos))
                    
                    for i in cellmates:
                        if i in self.schedule.agents:
                            continue
                        else:
                            notfound = False
            
                self.schedule.add(a)
                self.grid.place_agent(a, (agente.pos))

        self.running = True

    def step(self):
        '''Advance the model by one step.'''
        if self.Tschedule.steps % 10 == 0:
            for agent in self.traffic_lights:
                agent.state = not agent.state
        self.Tschedule.step()
        self.schedule.step()
