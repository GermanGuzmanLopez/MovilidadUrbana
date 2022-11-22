import mesa

class robots(mesa.Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.caja = False
        self.companion = None
        self.encaminado = False
        self.trapped = "left"

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=False,
            include_center = False)
        go = True
        # Check for boxes in adjacent tiles

        for i in possible_steps:
            if(i[1] == 0):
                continue
            if(self.encaminado):
                if(i[0] == self.pos[0] - 1):
                    continue
            occupied = self.model.grid.get_cell_list_contents((i))
            if len(occupied) > 0:
                print("--------")
                print("Reviso pos: " + str(i))
                print("--------")
                for j in occupied:
                    if(j in self.model.bschedule.agents):
                        if (j.taken):
                            break
                        self.companion = j
                        self.companion.model.grid.move_agent(self.companion, self.pos)
                        self.companion.taken = True
                        go = False
                        print("--------")
                        print("Agarro Caja" + str(i))
                        print("--------")
                        self.encaminado = True
                        break
            if not go:
                break
        if go: 
            new_position = self.random.choice(possible_steps)
            while(new_position[1] < 1):
                new_position = self.random.choice(possible_steps)
            occupied = self.model.grid.get_cell_list_contents((new_position))
            if len(occupied) > 0:
                for i in occupied:
                    if(i in self.model.schedule.agents):
                        go = False
            if (go): 
                self.model.grid.move_agent(self, new_position)

    def moveBox(self):
        occupied = self.model.grid.get_cell_list_contents((self.pos[0], self.pos[1] -1))
        if self.pos[1] != 1:
            #Move all the way to the right
            # if self.pos[0] != 0:
            #     self.moveLeft()
            #Move to the bottom   
            self.moveDown()

        elif len(occupied) < 5:
            self.companion.descansar()
            self.companion = None
            self.encaminado = False
        else:
            if(self.trapped == "right"):

                if(not self.model.grid.out_of_bounds((self.pos[0] + 1, self.pos[1]))) \
                and (len(self.model.grid.get_cell_list_contents((self.pos[0] + 1, self.pos[1]))) < 1):
                    print("--------")
                    print("Right end move")
                    print("--------")
                    self.model.grid.move_agent(self, (self.pos[0] + 1, self.pos[1]))

                elif(not self.model.grid.out_of_bounds((self.pos[0] - 1, self.pos[1]))) \
                and (len(self.model.grid.get_cell_list_contents((self.pos[0] - 1, self.pos[1]))) < 1):
                    print("--------")
                    print("Left end move")
                    print("--------")
                    self.trapped == "left"
                    self.model.grid.move_agent(self, (self.pos[0] - 1, self.pos[1]))

                elif (len(self.model.grid.get_cell_list_contents((self.pos[0], self.pos[1] + 1))) < 0):
                    print("--------")
                    print("Up end move")
                    print("--------")
                    self.model.grid.move_agent(self, (self.pos[0], self.pos[1] + 1))

            elif(self.trapped == "left"):

                if(not self.model.grid.out_of_bounds((self.pos[0] - 1, self.pos[1]))) \
                and (len(self.model.grid.get_cell_list_contents((self.pos[0] - 1, self.pos[1]))) < 1):
                    print("--------")
                    print("Left end move")
                    print("--------")
                    self.trapped == "left"
                    self.model.grid.move_agent(self, (self.pos[0] - 1, self.pos[1]))

                elif(not self.model.grid.out_of_bounds((self.pos[0] + 1, self.pos[1]))) \
                and (len(self.model.grid.get_cell_list_contents((self.pos[0] + 1, self.pos[1]))) < 1):
                    print("--------")
                    print("Right end move")
                    print("--------")
                    self.trapped == "right"
                    self.model.grid.move_agent(self, (self.pos[0] + 1, self.pos[1]))

                elif (len(self.model.grid.get_cell_list_contents((self.pos[0], self.pos[1] + 1))) < 0):
                    print("--------")
                    print("Up end move")
                    print("--------")
                    self.model.grid.move_agent(self, (self.pos[0], self.pos[1] + 1))
                
    def moveLeft(self):
        possible_box = self.model.grid.get_neighborhood(
            self.pos,
            moore=False,
            include_center = False)
        # Check for boxes in adjacent tiles
        for i in possible_box:
            occupied = self.model.grid.get_cell_list_contents((i))
            if(i[0] == self.pos[0] - 1):
                if len(occupied) == 0:
                    self.model.grid.move_agent(self, i)
                    break

                elif self.model.grid.get_cell_list_contents((self.pos[0], self.pos[1] -1)) == 0:
                    self.model.grid.move_agent(self, (self.pos[0], self.pos[1] - 1))
                    break

            if(i[1] == self.pos[1] - 1):
                self.moveDown()

            elif len(occupied) > 0:
                for j in occupied:
                    if(j in self.model.bschedule.agents):
                        self.companion.model.grid.move_agent(self.companion, i)
                        self.companion.taken = False
                        self.companion = None
                        break

    def moveDown(self):
        possible_box = self.model.grid.get_neighborhood(
            self.pos,
            moore=False,
            include_center = False)
        # Check for boxes in adjacent tiles
        for i in possible_box:
            occupied = self.model.grid.get_cell_list_contents((i))
            if(i[0] == self.pos[0] - 1):
                continue
            elif(i[1] == self.pos[1] - 1):
                if len(occupied) > 0:
                    for j in occupied:
                        if(j in self.model.schedule.agents):
                            new_pos = [possible_box[0], possible_box[-1]]
                            for k in new_pos:
                                if len(self.model.grid.get_cell_list_contents((k))) < 1:
                                    self.model.grid.move_agent(self, k)
                else:
                    self.model.grid.move_agent(self, i)
                    break
            
            elif len(occupied) > 0:
                for j in occupied:
                    if(j in self.model.bschedule.agents):
                        if (j.taken):
                            break
                        if (self.companion != None):
                            self.companion.model.grid.move_agent(self.companion, i)
                            self.companion.taken = False
                            self.companion = None
                            print("--------")
                            print("Dejo encima caja : " + str(i))
                            print("--------")
                            break
            else:
                if (self.companion != None):
                    self.companion.model.grid.move_agent(self.companion, i)
                    self.companion.taken = False
                    self.companion = None
                    print("--------")
                    print("Dejo caja vacio: " + str(i))
                    print("--------")
                    break

    def traerCaja(self):
        if(self.companion != None):
            self.companion.model.grid.move_agent(self.companion, (self.pos))

    # Priority of steps
    def step(self):
        print("--------")
        print("Yo: " + str(self.pos))
        print("--------")

        if(self.companion == None):
            self.move()
        elif(self.companion != None):
            self.moveBox()
            self.traerCaja()

class caja(mesa.Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.caja = True
        self.taken = False

    def descansar(self):
        self.model.grid.move_agent(self, (self.pos[0], 0))
        self.taken = False
        print("--------")
        print("Dejo encima caja : " + str(self.pos))
        print("Cajas apiladas: " + str(len(self.model.grid.get_cell_list_contents((self.pos)))))
        print("--------")

#---------------------------------------------------------- 
  
class robot_model(mesa.Model):
    def __init__(self, n, k, width, height):
        self.num_agents = n
        self.grid = mesa.space.MultiGrid(width, height, False)
        self.schedule = mesa.time.RandomActivation(self)
        self.bschedule = mesa.time.BaseScheduler(self)
        self.current_step = 0
        
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

    def step(self):
        self.schedule.step()
