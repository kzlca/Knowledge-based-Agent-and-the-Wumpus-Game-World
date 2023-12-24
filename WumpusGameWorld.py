import pygame
import random
import sys
import time

GRID_SIZE = 4
CELL_SIZE = 100
MARGIN = 6
SCREEN_SIZE = ((GRID_SIZE * CELL_SIZE) + 5 * MARGIN , (GRID_SIZE * CELL_SIZE) + 5 * MARGIN)
agent_pos = (0,0)
knowledge_base = {
    "visited": set(),
    "stench": set(),
    "breeze": set(),
    "glitter": set(),
}

class WumpusWorld:
    def __init__(self):
        self.grid = [[None] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.stench = [[None] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.breeze = [[None] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.glitter = [[False] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.wumpus_alive = True
        self.place_objects()

    def place_objects(self):
        self.place_object("Wumpus", 1)
        self.place_object("Gold", 1)
        self.place_object("Pit", 1)

    def place_object(self, obj_type, max):
        for num in range(random.randint(1, max)):
            x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
            while (
                self.grid[y][x] is not None
                or (x, y) == (0, 0)
                or (x, y) == (1, 0)
                or (x, y) == (0, 1)
                or (x, y) == (1, 1)
            ):
                x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
            self.grid[y][x] = obj_type

            if obj_type == "Wumpus":
                self.set_stench(x, y, True)
            elif obj_type == "Pit":
                self.set_breeze(x, y)
            elif obj_type == "Gold":
                self.set_glitter(x, y)

    def set_stench(self, x, y, state):
        if y > 0:
            self.stench[y - 1][x] = state
        if y < GRID_SIZE - 1:
            self.stench[y + 1][x] = state
        if x > 0:
            self.stench[y][x - 1] = state
        if x < GRID_SIZE - 1:
            self.stench[y][x + 1] = state

    def set_breeze(self, x, y):
        if y > 0:
            self.breeze[y - 1][x] = True
        if y < GRID_SIZE - 1:
            self.breeze[y + 1][x] = True
        if x > 0:
            self.breeze[y][x - 1] = True
        if x < GRID_SIZE - 1:
            self.breeze[y][x + 1] = True

    def set_glitter(self, x, y):
        self.glitter[y][x] = True

    def draw(self, screen):
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                pygame.draw.rect(screen, (0, 0, 0), ( (CELL_SIZE + MARGIN) * x + MARGIN, (CELL_SIZE + MARGIN) * y + MARGIN , CELL_SIZE, CELL_SIZE), 4)
                #drawing objects
                if self.grid[y][x] is not None:
                    self.draw_object(screen, x, y, self.grid[y][x])

                if self.breeze[y][x]:
                     pygame.draw.rect(screen, (0, 0, 0), ( (CELL_SIZE + MARGIN) * x + MARGIN, (CELL_SIZE + MARGIN) * y + MARGIN , CELL_SIZE, CELL_SIZE), 10)
                
                if self.stench[y][x]:
                    center_x = x * (CELL_SIZE + MARGIN) + MARGIN + CELL_SIZE // 2
                    center_y = y * (CELL_SIZE + MARGIN) + MARGIN + CELL_SIZE // 2
                    line_length = CELL_SIZE // 4
                    pygame.draw.line(screen, (255, 0, 0), (center_x - line_length, center_y), (center_x + line_length, center_y), 2)
                    pygame.draw.line(screen, (255, 0, 0), (center_x, center_y - line_length), (center_x, center_y + line_length), 2)

                if self.glitter[y][x]:
                    pygame.draw.rect(screen, (255, 255, 0), ( (CELL_SIZE + MARGIN) * x + MARGIN, (CELL_SIZE + MARGIN) * y + MARGIN , CELL_SIZE, CELL_SIZE), 4)

    def draw_object(self, screen, x, y, obj_type):
        colors = {"Wumpus": (255, 0, 0), "Gold": (255, 255, 0), "Pit": (0, 0, 0)}
        pygame.draw.circle(screen, colors[obj_type], (x * (CELL_SIZE + MARGIN) + MARGIN + CELL_SIZE // 2, y * (CELL_SIZE + MARGIN) + MARGIN + CELL_SIZE // 2), CELL_SIZE // 3)


class Agent:
    def __init__(self, grid_size):
        self.x, self.y = 0, 0
        self.grid = [[None] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.previous_move = ""
        self.wumpus_location = ""

    def draw(self, screen):
        pygame.draw.circle(screen, (0, 255, 0), ((CELL_SIZE + MARGIN) * self.x + MARGIN + CELL_SIZE // 2, (CELL_SIZE + MARGIN) * self.y + MARGIN + CELL_SIZE // 3), CELL_SIZE // 8)
        body_size = CELL_SIZE // 4
        pygame.draw.line(screen, (0, 255, 0), ((CELL_SIZE + MARGIN) * self.x + MARGIN + CELL_SIZE // 2 - body_size // 2, (CELL_SIZE + MARGIN) * self.y + MARGIN + CELL_SIZE // 2),
                         ((CELL_SIZE + MARGIN) * self.x + MARGIN + CELL_SIZE // 2 + body_size // 2, (CELL_SIZE + MARGIN) * self.y + MARGIN + CELL_SIZE // 2), 4)
        pygame.draw.line(screen, (0, 255, 0), ((CELL_SIZE + MARGIN) * self.x + MARGIN + CELL_SIZE // 2, (CELL_SIZE + MARGIN) * self.y + MARGIN + CELL_SIZE // 2 - body_size // 2),
                         ((CELL_SIZE + MARGIN) * self.x + MARGIN + CELL_SIZE // 2, (CELL_SIZE + MARGIN) * self.y + MARGIN + CELL_SIZE // 2 + body_size // 2), 4)

    def check_win(self, wumpus_world):
        return wumpus_world.grid[self.y][self.x] == "Gold"
    
    def check_loss(self, wumpus_world):
        return wumpus_world.grid[self.y][self.x] in ["Pit", "Wumpus"]
    
    def sense_environment(self, wumpus_world):
        stench = breeze = glitter = False

        if wumpus_world.stench[self.y][self.x]:
            stench = True
        elif wumpus_world.breeze[self.y][self.x]:
            breeze = True
        elif wumpus_world.glitter[self.y][self.x]:
            glitter = True
        
        return stench, breeze, glitter
    
    def update_knowledge(self):
        agent_pos = (self.x,self.y)
        knowledge_base["visited"].add(agent_pos)

        stench, breeze, glitter = self.sense_environment(wumpus_world)

        if stench:
            knowledge_base["stench"].add(agent_pos)
        if breeze:
            knowledge_base["breeze"].add(agent_pos)
        if glitter:
            knowledge_base["glitter"].add(agent_pos)

    def is_safe_move(self, new_pos):
        return (
            new_pos not in knowledge_base["visited"]
            and new_pos not in knowledge_base["stench"]
            and new_pos not in knowledge_base["breeze"]
        )
    def is_hazzard(self, new_pos):
        return (
        new_pos in knowledge_base["stench"]
        or new_pos in knowledge_base["breeze"]
        )
    def decide(self):
        possible_moves = []

        #killing wumpus
        if len(knowledge_base["stench"]) > 1 and wumpus_world.wumpus_alive:
            if list(knowledge_base["stench"])[0][1] > list(knowledge_base["stench"])[1][1] and list(knowledge_base["stench"])[0][0] < list(knowledge_base["stench"])[1][0]:
                x = list(knowledge_base["stench"])[1][0]
                y = list(knowledge_base["stench"])[0][1]
            if list(knowledge_base["stench"])[0][1] > list(knowledge_base["stench"])[1][1] and list(knowledge_base["stench"])[0][0] > list(knowledge_base["stench"])[1][0]:
                y = list(knowledge_base["stench"])[1][1]
                x = list(knowledge_base["stench"])[0][0]
            if list(knowledge_base["stench"])[1][1] > list(knowledge_base["stench"])[0][1] and list(knowledge_base["stench"])[1][0] < list(knowledge_base["stench"])[0][0]:
                x = list(knowledge_base["stench"])[0][0]
                y = list(knowledge_base["stench"])[1][1]
            if list(knowledge_base["stench"])[1][1] > list(knowledge_base["stench"])[0][1] and list(knowledge_base["stench"])[1][0] > list(knowledge_base["stench"])[0][0]:
                y = list(knowledge_base["stench"])[1][1]
                x = list(knowledge_base["stench"])[0][0]
            
            
            self.wumpus_location = (x,y)
            print("Shooting AT : " + str(self.wumpus_location))
            wumpus_world.wumpus_alive = False
            return "SHOOT"

        if self.is_hazzard((self.x , self.y)):
            if self.previous_move == "RIGHT":
               possible_moves.append("LEFT") 
            elif self.previous_move == "LEFT":
               possible_moves.append("RIGHT")
            elif self.previous_move == "UP":
               possible_moves.append("DOWN") 
            elif self.previous_move == "DOWN":
               possible_moves.append("UP") 
            
            if possible_moves:
                action = random.choice(possible_moves)

        else:
            should_restart = True
            while should_restart:    
                if self.x > 0 and self.is_safe_move((self.x  - 1, self.y)):
                    possible_moves.append("LEFT")
                if self.x  < GRID_SIZE - 1 and self.is_safe_move((self.x  + 1, self.y)):
                    possible_moves.append("RIGHT")
                if self.y  > 0 and self.is_safe_move((self.x, self.y - 1)):
                    possible_moves.append("UP")
                if self.y < GRID_SIZE - 1 and self.is_safe_move((self.x, self.y + 1)):
                    possible_moves.append("DOWN")

                if possible_moves:
                    action = random.choice(possible_moves)
                    self.previous_move = action
                    should_restart = False   
                if not possible_moves:
                    knowledge_base["visited"].clear()
        return action
    
    def act(self, action, wumpus_world):
        agent_pos = (self.x,self.y)
        new_pos = agent_pos
        if action == "LEFT" and agent_pos[0] > 0:
            new_pos = (agent_pos[0] - 1, agent_pos[1])
        elif action == "RIGHT" and agent_pos[0] < GRID_SIZE - 1:
            new_pos = (agent_pos[0] + 1, agent_pos[1])
        elif action == "UP" and agent_pos[1] > 0:
            new_pos = (agent_pos[0], agent_pos[1] - 1)
        elif action == "DOWN" and agent_pos[1] < GRID_SIZE - 1:
            new_pos = (agent_pos[0], agent_pos[1] + 1)
        elif action == "SHOOT":
            wumpus_world.grid[self.wumpus_location[1]][self.wumpus_location[0]] = None
            knowledge_base['stench'].clear()
            print("shooting x at :" + str(self.wumpus_location[0]) + "and y = " + str(self.wumpus_location[1]))
            wumpus_world.set_stench(self.wumpus_location[0],self.wumpus_location[1],False)

        self.x = new_pos[0]
        self.y = new_pos[1]

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Wumpus World")

wumpus_world = WumpusWorld()
agent = Agent(GRID_SIZE)

screen.fill((255, 255, 255))
wumpus_world.draw(screen)
agent.draw(screen)
pygame.display.flip()
pygame.time.Clock().tick(1)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    screen.fill((255, 255, 255))
    wumpus_world.draw(screen)


    agent.update_knowledge()
    action = agent.decide()
    agent.act(action, wumpus_world)

    agent.draw(screen)
    
    pygame.display.flip()
    pygame.time.Clock().tick(1)

    if agent.check_loss(wumpus_world):
        print("You lost!")
        time.sleep(2)
        pygame.quit()
        sys.exit()

    if agent.check_win(wumpus_world):
        print("You won!")
        time.sleep(2)
        pygame.quit()
        sys.exit()

    