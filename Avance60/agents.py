from mesa import Agent

class Car(Agent):
    def __init__(self, unique_id, model, destiny_id):
        super().__init__(unique_id, model)
        self.direction = ""
        self.possible_direction = ""
        self.destino = destiny_id.pos
        print(self.destino)

    def closer(self):
        if self.direction == "Left":
            pos = self.pos[0] - 1
        elif self.direction == "Right":
            pos = self.pos[0] + 1
        elif self.direction == "Up":
            pos = self.pos[1] + 1
        elif self.direction == "Down":
            pos = self.pos[1] - 1

        if self.possible_direction == "Left":
            return (lambda possible,pos,dest : (possible + dest) < (pos + dest)) (self.pos[0] - 1 , pos, self.destino[0])
            
        elif self.possible_direction == "Down":
            return (lambda possible,pos,dest : (possible + dest) < (pos + dest)) (self.pos[1] - 1 , pos,  self.destino[1])
            
        elif self.possible_direction == "Up":
            return (lambda possible,pos,dest : (possible + dest) > (pos + dest)) (self.pos[1] + 1 , pos,  self.destino[1])

        elif self.possible_direction == "Right":
            return (lambda possible,pos,dest : (possible + dest) > (pos + dest)) (self.pos[0] + 1 , pos,  self.destino[0])
        else:
            return False

    def decidir(self):
        x = self.pos[0]
        y = self.pos[1]

        if self.direction == "Right":
            occupied = self.model.grid.get_cell_list_contents((x + 1, y))
            for j in occupied:
                if j in self.model.schedule.agents:
                    break
                else:
                    self.model.grid.move_agent(self, (x + 1, y))
                    print("---------")
                    print("Move right")
                    print("---------")
                    break
        elif self.direction == "Left":
            occupied = self.model.grid.get_cell_list_contents((x - 1, y))
            for j in occupied:
                if j in self.model.schedule.agents:
                    break
                else:
                    self.model.grid.move_agent(self, (x - 1, y))
                    print("---------")
                    print("Move left")
                    print("---------")
                    break
        elif self.direction == "Up":
            occupied = self.model.grid.get_cell_list_contents((x, y + 1))
            for j in occupied:
                if j in self.model.schedule.agents:
                    break
                else:
                    self.model.grid.move_agent(self, (x, y + 1))
                    print("---------")
                    print("Move up")
                    print("---------")
                    break
        elif self.direction == "Down":
            occupied = self.model.grid.get_cell_list_contents((x, y - 1))
            for j in occupied:
                if j in self.model.schedule.agents:
                    break
                else:
                    self.model.grid.move_agent(self, (x, y - 1))
                    print("---------")
                    print("Move down")
                    print("---------")
                    break

    def move(self):
        occupied = self.model.grid.get_cell_list_contents(self.pos)
        for i in occupied:
            if i in self.model.Rschedule.agents:
                self.direction = i.direction
                break
        self.possible_direction = ""
                
        x = self.pos[0]
        y = self.pos[1]

        if self.direction == "Right":
            checate = [(x + 1, y - 1), (x  + 1, y ), (x  + 1, y  + 1)]
        elif self.direction == "Left":
            checate = [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1)]
        elif self.direction == "Up":
            checate = [(x - 1, y + 1), (x , y + 1), (x  + 1, y  + 1)]
        elif self.direction == "Down":
            checate = [(x - 1, y - 1), (x , y - 1), (x + 1, y - 1)]

        for i in checate:
            if(not self.model.grid.out_of_bounds(i)):
                occupied = self.model.grid.get_cell_list_contents(i)
                for j in occupied:
                    if j in self.model.Rschedule.agents:
                        if(self.direction != j.direction):
                            self.possible_direction = j.direction

        if not self.closer():
            self.decidir()
        else:
            self.decidir()
            print(self.closer())
            x = self.pos[0]
            y = self.pos[1]
            if self.possible_direction == "Right":
                occupied = self.model.grid.get_cell_list_contents((x + 1, y))
                for j in occupied:
                    if j in self.model.schedule.agents:
                        break
                    else:
                        self.model.grid.move_agent(self, (x + 1, y))
                        print("---------")
                        print("Closer right")
                        print(self.direction)
                        print("---------")
                        break
            elif self.possible_direction == "Left":
                occupied = self.model.grid.get_cell_list_contents((x - 1, y))
                for j in occupied:
                    if j in self.model.schedule.agents:
                        break
                    else:
                        self.model.grid.move_agent(self, (x - 1, y))
                        print("---------")
                        print("Closer left")
                        print(self.direction)
                        print("---------")
                        break
            elif self.possible_direction == "Up":
                occupied = self.model.grid.get_cell_list_contents((x, y + 1))
                for j in occupied:
                    if j in self.model.schedule.agents:
                        break
                    else:
                        self.model.grid.move_agent(self, (x, y + 1))
                        print("---------")
                        print("Closer up")
                        print(self.direction)
                        print("---------")
                        break
            elif self.possible_direction == "Down":
                occupied = self.model.grid.get_cell_list_contents((x, y - 1))
                for j in occupied:
                    if j in self.model.schedule.agents:
                        break
                    else:
                        self.model.grid.move_agent(self, (x, y - 1))
                        print("---------")
                        print("Closer down")
                        print(self.direction)
                        print("---------")
                        break
            

        
                    
       
            
            

    def step(self):
        self.move()

class Traffic_Light(Agent):

    def __init__(self, unique_id, model, state = False):
        super().__init__(unique_id, model)
        self.cars = 0
        self.timer = 3

        self.state = state

    def check_cars(self):
        neighbors = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center = False)
                     


    def step(self):
        # if self.model.schedule.steps % self.timeToChange == 0:
        #     self.state = not self.state
        pass

class Destination(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

class Obstacle(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

class Road(Agent):
    def __init__(self, unique_id, model, direction = "Left"):
        super().__init__(unique_id, model)
        self.direction = direction

    def step(self):
        pass
