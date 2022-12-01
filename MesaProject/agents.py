from mesa import Agent


class Car(Agent):
    def __init__(self, unique_id, model, destiny_id):
        super().__init__(unique_id, model)
        self.direction = ""
        self.possible_direction = ""
        self.destino = destiny_id.pos
        self.decision = True

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
        #print(self.destino)
        self.prevstep = False
#################################################################
    def closer(self):
        """"🎶 No juzgue los nombres profe, son las 3 de la mañana (es la 1:30 xd)
         y estoy en tu ventana buscandote amor escucha porfavor 🎶 """
        x,y = self.pos[0],self.pos[1]
        if self.direction == "Left":
            dirpos = (x - 1, y)
        elif self.direction == "Right":
            dirpos = (x + 1,y)
        elif self.direction == "Up":
            dirpos = (x, y + 1)
        elif self.direction == "Down":
            dirpos = (x, y - 1)
        else:
            dirpos = (0,0)

        if self.possible_direction == "Left":
            posdirpos = (x - 1, y)
        elif self.possible_direction == "Down":
            posdirpos = (x, y - 1)
        elif self.possible_direction == "Up":
            posdirpos = (x, y + 1)
        elif self.possible_direction == "Right":
            posdirpos = (x + 1, y)
        else:
            posdirpos = (0,0)
        
        
        pospos = (abs(self.destcalle[0] - x), abs(self.destcalle[1] - y))
        dirpospos = (abs(self.destcalle[0] - dirpos[0]), abs(self.destcalle[1] - dirpos[1]))
        posdirpospos = (abs(self.destcalle[0] - posdirpos[0]), abs(self.destcalle[1] - posdirpos[1])) #A donde te lleva la calle

        #print("En camino actual " + str(dirpospos) + " Possible camino " + str(posdirpospos))
        #print("Movimiento rerctilinio uniforme en un espacio de tiempo anterior al nuestro: " + str(self.prevstep))
        
        if ((sum(list(pospos)) < sum(list(dirpospos))) and (sum(list(pospos)) < sum(list(posdirpospos)))):
            return False

        if (sum(list(dirpospos)) > sum(list(posdirpospos))):
            self.prevstep = False
            return True

        elif (sum(list(dirpospos)) == sum(list(posdirpospos))):
            if (self.pos in self.repetir):
                i = self.repetir.index(self.pos)

                if self.prevstep:
                    return self.repetir[i+1]

                self.prevstep = not self.prevstep

                self.repetir[i+1] = not(self.repetir[i+1])
                return self.repetir[i+1]
            else:
                self.prevstep = not self.prevstep
                self.repetir.append(self.pos)
                self.repetir.append(True)
                return True
        else: 
            self.prevstep = False
            return False
#################################################################
    def move(self, alli):
        go = True
        x = self.pos[0]
        y = self.pos[1]

        if len(self.buffer) > 0:
            self.Bdirection = alli
            alli = self.buffer.pop(0)
        
        if alli == "Right":
            occupied = self.model.grid.get_cell_list_contents((x + 1, y))
            for j in occupied:
                if j in self.model.schedule.agents:
                    go = False
                    break
                elif j in self.model.Eschedule.agents:
                    self.buffer.clear()
                    self.move(self.Bdirection)
                    go = False  
                elif j in self.model.Tschedule.agents:
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
                    self.move(self.Bdirection)
                    go = False  
                elif j in self.model.Tschedule.agents:
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
                    self.move(self.Bdirection)
                    go = False
                elif j in self.model.Tschedule.agents:
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
                    self.move(self.Bdirection)
                    go = False
                    break
                elif j in self.model.Tschedule.agents:
                    if not j.state:
                        go = False
                        break
            if go: self.model.grid.move_agent(self, (x, y - 1))

#################################################################
    def decidir(self):
        #print(self.destino)
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
            self.prevstep = False
            self.move(self.direction)
           
        else:
            self.move(self.direction) 
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
                        self.buffer.append("Up")
                        break

            elif self.possible_direction == "Down":
                occupied = self.model.grid.get_cell_list_contents((x, y - 1))
                for j in occupied:
                    if j in self.model.schedule.agents:
                        break
                    else:
                        self.buffer.append("Down")
                        self.buffer.append("Down")
                        break
#################################################################   
    def checate(self, i):
        x = self.pos[0]
        y = self.pos[1]
        
        if self.direction == "Right":
            checate = [(x + i, y + 2), (x + i, y + 1), (x + i, y), (x + i, y - 1), (x + i, y - 2), (x,y+1), (x,y-1), (x,y+2), (x,y-2)]
        elif self.direction == "Left":
            checate = [(x - i, y - 2), (x - i, y - 1), (x - i, y), (x - i, y + 1), (x - i, y + 2), (x,y+1), (x,y-1), (x,y+2), (x,y-2)]
        elif self.direction == "Up":
            checate = [(x - 2, y + i), (x - 1, y + i), (x, y + i), (x + 1, y + i), (x + 2, y + i), (x-1,y),(x+1,y),(x-2,y),(x+2,y)]
        elif self.direction == "Down":
            checate = [(x + 2, y - i), (x + 1, y - i), (x, y - i), (x - 1, y - i), (x - 2, y - i), (x-1,y),(x+1,y),(x-2,y),(x+2,y)]

        return checate
#################################################################
    def get_direction(self, checate):
        directoL = False
        directoR = False
        directol = False
        director = False    
        for i in range(1, len(checate) + 1):
            if i == len(checate):
                i = 0
            if(not self.model.grid.out_of_bounds(checate[i])):
                occupied = self.model.grid.get_cell_list_contents(checate[i])
                for j in occupied:
                    if j in self.model.Rschedule.agents:
                        if (i == 1):
                                directoL = True
                        if (i == 3):
                                directoR = True
                        if (i == 5):
                            director = True
                        if (i == 6):
                            directol = True

                        
                        if(self.direction != j.direction):
                            if(self.direction == "Left" and j.direction == "Right") or (self.direction == "Right" and j.direction == "Left"):
                                if (i == 0):
                                    #print("pass con i 0")
                                    pass
                                elif (i == len(checate)-1):
                                    #print("pass con i 1")
                                    pass
                            elif(i == 0) and directoL:
                                #print("Directo Left: " + j.direction)
                                return j.direction
                            elif (i == 3) and (self.direction == j.direction):
                                return j.direction
                            elif(i == 4) and directoR:
                                #print("Directo Right: " + j.direction)
                                return j.direction
                            elif (i == 7) and director:
                                return j.direction
                            elif (i == 8) and directol:
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
            self.decidir()
#-----------------------------------------------------------------
class Traffic_Light(Agent):
    def __init__(self, unique_id, model, state = False):
        super().__init__(unique_id, model)
        self.first = True
        self.horizontal = False
        self.companion = None
        self.corner = None
        self.state = state

        self.solo = 0
        self.conjunto = 0
        self.timer = 0
        self.maxtimer = 7
        self.viendo = ""
#################################################################   
    def get_pc(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=False,
            include_center=False)
        
        for i in possible_steps:
            occupied = self.model.grid.get_cell_list_contents(i)
            for j in occupied:
                
                if j in self.model.Tschedule.agents:
                    self.companion = j
                    self.horizontal = (lambda mypos, partnerpos: 
                    (mypos == partnerpos+1 or mypos == partnerpos-1))(self.pos[0], j.pos[0])
                    break

        x = self.pos[0]
        y = self.pos[1]

        possible_steps = [(x - 1, y + 1),(x - 1, y - 1),(x + 1, y + 1),(x + 1, y - 1)]

        for i in possible_steps:
            if not self.model.grid.out_of_bounds(i):
                occupied = self.model.grid.get_cell_list_contents(i)
                for j in occupied:
                    if j in self.model.Tschedule.agents:
                        self.companion.corner = j
                        self.corner = j
                        break
 
        self.first = False
#################################################################   
    def get_direccion(self):
        x = self.pos[0]
        y = self.pos[1]

        if self.horizontal:
            possible_steps = [(x, y - 1),(x, y +1)]
            for i in possible_steps:
                occupied = self.model.grid.get_cell_list_contents(i)
                for j in occupied:
                    if j in self.model.Rschedule.agents:
                        if (j.direction == "Left") or (j.direction == "Right"):
                            break
                        else:
                            return j.direction
                
        else:
            possible_steps = [(x - 1, y), (x + 1, y)]
            for i in possible_steps:
                occupied = self.model.grid.get_cell_list_contents(i)
                for j in occupied:
                    if j in self.model.Rschedule.agents:
                        if (j.direction == "Up") or (j.direction == "Down"):
                            break
                        else:
                            return j.direction
        
#################################################################   
    def administrar(self):
        a,c,k,z = 0,0,0,0
        
        x = self.pos[0]
        y = self.pos[1]
        if self.viendo == "Left":
            a = 1
            z = 1
        elif self.viendo == "Right":
            a = -1
            z = -1
        elif self.viendo == "Up":
            c = -1
            k = -1
        elif self.viendo == "Down":
            c = 1
            k = 1
        for i in range(3):
            casilla = (x + a, y + c)
            occupied = self.model.grid.get_cell_list_contents(casilla)
            for j in occupied:
                if j in self.model.schedule.agents:
                    self.solo += 1
            a += z
            c += k
        
        self.conjunto = self.solo + self.companion.solo
        if (self.corner != None) and (self.corner.companion != None):
            if (self.conjunto > self.corner.conjunto):
                self.state = True
                self.companion.state = True
                self.corner.state = False
                self.corner.companion.state = False
            elif(self.conjunto == self.corner.conjunto):
                pass
            else:
                self.state = False
                self.companion.state = False
                self.corner.state = True
                self.corner.companion.state = True
        
#################################################################

    def step(self):
        if self.first:
            self.get_pc()
            self.viendo = self.get_direccion()
        self.administrar()
        self.solo = 0
        self.timer += 1
            
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
