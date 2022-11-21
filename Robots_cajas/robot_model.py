import mesa
from robot_agents import *

class robot_model(mesa.Model):
    
    def __init__(self, n, k, width, height, max_step):
        self.num_agents = n
        self.width = width
        self.grid = mesa.space.MultiGrid(width, height, False)
        self.schedule = mesa.time.RandomActivation(self)
        self.bschedule = mesa.time.BaseScheduler(self)
        self.current_step = 2
        self.max_step = max_step
        
        for i in range(n):
            a = robots(i, self)

            #Add the agent to a random cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(1, self.grid.height)

            cellmates = self.grid.get_cell_list_contents((x, y))
            while len(cellmates) > 0:
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                
                cellmates = self.grid.get_cell_list_contents((x, y))
            self.schedule.add(a)
            self.grid.place_agent(a, (x, y))

        for i in range(k):
            a = caja(i, self)

            #Add the agent to a random cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)

            cellmates = self.grid.get_cell_list_contents((x, y))
            while len(cellmates) > 0:
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                cellmates = self.grid.get_cell_list_contents((x, y))
                
            self.bschedule.add(a)
            self.grid.place_agent(a, (x, y))

            self.datacollector = mesa.DataCollector(
                model_reporters = {"Boxes found and ready": len_cajas_listas}
            )

    def step(self) -> None:
        self.running = (self.current_step < self.max_step)
        self.schedule.step()
        self.datacollector.collect(self)
        self.current_step += 1