from mesa import Agent

class Car(Agent):
    def __init__(self, unique_id, model, destiny_id):
        super().__init__(unique_id, model)
        self.direction = ""
        self.possible_direction = ""
        self.destino = destiny_id.pos
        
        possible_steps = model.grid.get_neighborhood(
            self.destino,
            moore=False,
            include_center=False)
            
        for i in possible_steps:
            occupied = model.grid.get_cell_list_contents(i)
            for j in occupied:
                if j in model.Rschedule.agents:
                    self.destcalle = j.pos
                    break
        
        self.buffer = []
        self.repetir = []
        self.arrived = False
        self.Bdirection = ""
        print(self.destino)
#################################################################
    def closer(self):
        """"🎶 No juzgue los nombres profe, son las 3 de la mañana (es la 1:30 xd)
         y estoy en tu ventana buscandote amor escucha porfavor 🎶 """
        if self.direction == "Left":
            dirpos = (self.pos[0] - 1, self.pos[1])
        elif self.direction == "Right":
            dirpos = (self.pos[0] + 1, self.pos[1])
        elif self.direction == "Up":
            dirpos = (self.pos[0], self.pos[1] + 1)
        elif self.direction == "Down":
            dirpos = (self.pos[0], self.pos[1] - 1)
        else:
            dirpos = (0,0)

        if self.possible_direction == "Left":
            posdirpos = (self.pos[0] - 1, self.pos[1])
        elif self.possible_direction == "Down":
            posdirpos = (self.pos[0], self.pos[1] - 1)
        elif self.possible_direction == "Up":
            posdirpos = (self.pos[0], self.pos[1] + 1)
        elif self.possible_direction == "Right":
            posdirpos = (self.pos[0] + 1, self.pos[1])
        else:
            posdirpos = (0,0)

        dirpospos = (abs(self.destcalle[0] - dirpos[0]), abs(self.destcalle[1] - dirpos[1]))
        posdirpospos = (abs(self.destcalle[0] - posdirpos[0]), abs(self.destcalle[1] - posdirpos[1]))
        

        #print("Suma dirpospos:" + str(sum(list(dirpospos))))
        #print("Suma posdirpospos:" + str(sum(list(posdirpospos))))

        if (sum(list(dirpospos)) > sum(list(posdirpospos))):
            
            return True

        elif (sum(list(dirpospos)) == sum(list(posdirpospos))):
            if (self.pos in self.repetir):
                print("Deja Vu")
                return False
                
            else:
                self.repetir.append(self.pos)
                print("------")
                print("Repetir: " + str(self.pos))
                print("------")
                return True
        else: return False
#################################################################
    def decidir(self, alli):
        go = True

        x = self.pos[0]
        y = self.pos[1]

        print(str(x)+ "-" + str(y))

        print("Buffereado del smash: " + str(self.buffer))

        if len(self.buffer) > 0:
            self.Bdirection = alli
            alli = self.buffer.pop(0)

        print(self.direction)
        
        if alli == "Right":
            occupied = self.model.grid.get_cell_list_contents((x + 1, y))
            for j in occupied:
                if j in self.model.schedule.agents:
                    go = False
                    break
                elif j in self.model.Eschedule.agents:
                    self.buffer.clear()
                    self.decidir(self.Bdirection)
                    go = False
                    
                elif j in self.model.Tschedule.agents:
                    print("Semaforo en: "+ str(j.state))
                    if not j.state:
                        go = False
                        break
                                          
            
            if go: self.model.grid.move_agent(self, (x + 1, y))
                
        elif alli == "Left":
            occupied = self.model.grid.get_cell_list_contents((x - 1, y))
            for j in occupied:
                if j in self.model.schedule.agents:
                    go = False
                    break
                elif j in self.model.Eschedule.agents:
                    self.buffer.clear()
                    self.decidir(self.Bdirection)
                    go = False
                    
                elif j in self.model.Tschedule.agents:
                    print("Semaforo en: "+ str(j.state))
                    if not j.state:
                        go = False
                        break
            
            if go: self.model.grid.move_agent(self, (x - 1, y))

                
        elif alli == "Up":
            occupied = self.model.grid.get_cell_list_contents((x, y + 1))
            for j in occupied:
                if j in self.model.schedule.agents:
                    go = False
                    break
                elif j in self.model.Eschedule.agents:
                    self.buffer.clear()
                    self.decidir(self.Bdirection)
                    go = False
                elif j in self.model.Tschedule.agents:
                    print("Semaforo en: "+ str(j.state))
                    if not j.state:
                        go = False
                        break  

            if go: self.model.grid.move_agent(self, (x, y + 1))


        elif alli == "Down":
            occupied = self.model.grid.get_cell_list_contents((x, y - 1))
            for j in occupied:
                if j in self.model.schedule.agents:
                    go = False
                    break
                elif j in self.model.Eschedule.agents:
                    self.buffer.clear()
                    self.decidir(self.Bdirection)
                    go = False
                    break
                elif j in self.model.Tschedule.agents:
                    print("Semaforo en: "+ str(j.state))
                    if not j.state:
                        go = False
                        break
            print(go)           
            if go: self.model.grid.move_agent(self, (x, y - 1))

#################################################################
    def move(self):
        print(self.pos)
        possible_steps = self.model.grid.get_neighborhood(
            self.destcalle,
            moore=False,
            include_center=False)

        if self.pos in possible_steps:
            self.model.grid.move_agent(self, self.destcalle)
            return
        elif self.pos == self.destcalle:
            self.model.grid.move_agent(self, self.destino)
            self.arrived = True
            return

        occupied = self.model.grid.get_cell_list_contents(self.pos)
        for i in occupied:
            if i in self.model.Rschedule.agents:
                self.direction = i.direction
                break
        self.possible_direction = ""

        checate = self.checate(1)

        self.possible_direction = self.get_direction(checate)

        if not self.closer():
            self.decidir(self.direction)
        else:
            self.decidir(self.direction)
            print(self.closer())
            x = self.pos[0]
            y = self.pos[1]

            if self.possible_direction == "Right":
                occupied = self.model.grid.get_cell_list_contents((x + 1, y))
                for j in occupied:
                    if j in self.model.schedule.agents:
                        break
                    else:
                        self.buffer.append("Right")
                        break

            elif self.possible_direction == "Left":
                occupied = self.model.grid.get_cell_list_contents((x - 1, y))
                for j in occupied:
                    if j in self.model.schedule.agents:
                        break
                    else:
                        self.buffer.append("Left")
                        break

            elif self.possible_direction == "Up":
                occupied = self.model.grid.get_cell_list_contents((x, y + 1))
                for j in occupied:
                    if j in self.model.schedule.agents:
                        break
                    else:
                        self.buffer.append("Up")
                        break

            elif self.possible_direction == "Down":
                occupied = self.model.grid.get_cell_list_contents((x, y - 1))
                for j in occupied:
                    if j in self.model.schedule.agents:
                        break
                    else:
                        self.buffer.append("Down")
                        break
#################################################################   
    def checate(self, i):
        x = self.pos[0]
        y = self.pos[1]
        
        if self.direction == "Right":
            checate = [(x + i, y + 2), (x + i, y + 1), (x + i, y), (x + i, y - 1), (x + i, y - 2)]
        elif self.direction == "Left":
            checate = [(x - i, y - 2), (x - i, y - 1), (x - i, y), (x - i, y + 1), (x - i, y + 2)]
        elif self.direction == "Up":
            checate = [(x - 2, y + i), (x - 1, y + i), (x, y + i), (x + 1, y + i), (x + 2, y + i)]
        elif self.direction == "Down":
            checate = [(x + 2, y - i), (x + 1, y - i), (x, y - i), (x - 1, y - i), (x - 2, y - i)]

        return checate
#################################################################
    def get_direction(self, checate):
        directoL = False
        directoR = False
        for i in range(1, len(checate) + 1):
            if i == len(checate):
                i = 0
            if(not self.model.grid.out_of_bounds(checate[i])):
                occupied = self.model.grid.get_cell_list_contents(checate[i])
                print(i, len(checate) - 1, directoL, directoR)
                for j in occupied:
                    if j in self.model.Rschedule.agents:
                        if (i == 1):
                             #if not (self.direction != j.direction):
                                directoL = True
                        if (i == 3):
                             #if not (self.direction != j.direction):
                                directoR = True
                        if(self.direction != j.direction):
                            if(self.direction == "Left" and j.direction == "Right" or self.direction == "Right" and j.direction == "Left"):
                                if (i == 0):
                                    pass
                                elif (i == len(checate)-1):
                                    pass
                            elif(i == 0) and directoL:
                                print("Directo Left: " + j.direction)
                                return j.direction
                            elif(i == len(checate) - 1) and directoR:
                                print("Directo Right: " + j.direction)
                                return j.direction
                        

                                

            elif(self.model.grid.out_of_bounds(checate[i])):
                if(i == 1):
                    self.model.grid.move_agent(self, (checate[3][0], checate[3][1]))
                    return True
                elif(i == 3):
                    self.model.grid.move_agent(self, (checate[1][0], checate[1][1]))
                    return True
#################################################################   
    def step(self):
        if not self.arrived:
            self.move()

class Traffic_Light(Agent):

    def __init__(self, unique_id, model, state = False):
        super().__init__(unique_id, model)
        self.cars = 0
        self.timer = 1

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
