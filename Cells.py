import pygame
import sys
import time

class cell:
    def __init__(self,w,h,left_top,screen,color):
        self.rect = pygame.Rect(left_top[0],left_top[1],w,h)
        self.screen = screen
        self.color = color


    def draw_me(self):
        pygame.draw.rect(self.screen,self.color,self.rect)
        #draw border on the rectangles
        pygame.draw.rect(self.screen,(40,40,40),self.rect,1)


class cells:
    def __init__(self,array_of_values,screen_width,screen_height,screen):
        self.grid_values = array_of_values
        self.screen = screen
        self.screen_size = screen_width,screen_height
        self.all_cells = []
        self.initialize()


    def initialize(self):
        rows,cols,useless = self.grid_values.shape
        rect_width = self.screen_size[0]/cols
        rect_height = self.screen_size[1]/rows


        for i in range(rows):
            for j in range(cols):
                left_top =j*rect_width,i*rect_height
                self.all_cells.append(cell(rect_width,rect_height,left_top,self.screen,self.grid_values[i,j]))

    def draw(self):
        for item in self.all_cells:
            item.draw_me()


class main_app:
    def __init__(self,initial_state,rule):
        self.state = initial_state        
        self.rule = rule
        self.run()

    def run(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        w, h = pygame.display.get_surface().get_size()
        black = (0,0,0)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()

            self.screen.fill(black)
            my_cells = cells(self.state,w,h,self.screen)
            my_cells.draw()
            pygame.display.flip()
            self.state = self.rule(self.state)
            time.sleep(1)

            
        
