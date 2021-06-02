import pygame
import sys
import time
import numpy as np

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


    def initialize(self):
        self.get_single_cell_size()
        rows,cols,useless = self.grid_values.shape
        for i in range(rows):
            for j in range(cols):
                left_top =j*self.rect_width,i*self.rect_height
                self.all_cells.append(cell(self.rect_width,self.rect_height,left_top,self.screen,self.grid_values[i,j]))

    def draw(self):
        for item in self.all_cells:
            item.draw_me()

    def get_single_cell_size(self):
        rows,cols,useless = self.grid_values.shape
        self.rect_width = self.screen_size[0]/cols
        self.rect_height = self.screen_size[1]/rows
        return self.rect_width,self.rect_height

    


class main_app:
    def __init__(self,initial_state,rule):
        self.state = initial_state
        self.aspect_ratio = initial_state.shape
        self.display = self.state.copy()
        self.piece_display = (0,self.aspect_ratio[0],0,self.aspect_ratio[1])
        self.rule = rule
        self.drag = False
        self.last_mouse = ()
        self.run()

    def run(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.w, self.h = pygame.display.get_surface().get_size()
        black = (0,0,0)
        while True:
            self.handle_events()
            self.screen.fill(black)
            self.update_display()
            my_cells = cells(self.display,self.w,self.h,self.screen)
            my_cells.initialize()
            my_cells.draw()
            pygame.display.flip()
            self.state = self.rule(self.state)            
            time.sleep(0.01)

    def handle_events(self):
        self.aspect_ratio = self.display.shape
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    if event.key == pygame.K_f:
                        #zoom in
                        self.zoom(1)
                    if event.key == pygame.K_g:
                        #zoom out
                        self.zoom(-1)
                    if event.key == pygame.K_LEFT:
                        #pan left
                        self.move_left(1)
                    if event.key == pygame.K_RIGHT:
                        #pan right
                        self.move_left(-1)
                    if event.key == pygame.K_UP:
                        #pan up
                        self.move_up(1)
                    if event.key == pygame.K_DOWN:
                        #pan down
                        self.move_up(-1)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.drag = True
                    self.last_mouse = pygame.mouse.get_rel()

                        
                if event.type == pygame.MOUSEBUTTONUP:
                    self.drag = False

                if event.type == pygame.MOUSEMOTION:
                    if self.drag == True:
                        self.last_mouse = pygame.mouse.get_rel()                      
                        my_cells_size = cells(self.display,self.w,self.h,self.screen).get_single_cell_size()
                        left = round(self.last_mouse[0]/my_cells_size[0])
                        top = round(self.last_mouse[1]/my_cells_size[1])                       
                        self.move_left(left)
                        self.move_up(top)
                        
                if event.type == pygame.MOUSEWHEEL:
                    self.zoom(event.y)
                        

    def move_left(self,unit):
        self.proportion(0,0,-1*unit,1*unit)

    def move_up(self,unit):
        self.proportion(-1*unit,1*unit,0,0)
                        
    def zoom(self,unit):
         scale_rows = round(unit*0.1*(self.aspect_ratio[0]))
         scale_cols = round(unit*0.1*(self.aspect_ratio[1]))
         self.proportion(scale_rows,scale_rows,scale_cols,scale_cols)
         
    def update_display(self):
        self.display = self.state[self.piece_display[0]:self.piece_display[1],self.piece_display[2]:self.piece_display[3]]
        
                
    def proportion(self,up,down,left,right):
        row_top,row_bottom,col_left,col_right = self.piece_display
        rows_s,cols_s,useless = self.state.shape
        
        row_top+=up
        if row_top<0:
            new_arr = np.full((abs(row_top),cols_s,3),255)
            self.state = np.append(new_arr,self.state,axis=0)
            row_bottom+=abs(row_top)
            row_top = 0
            rows_s,cols_s,useless = self.state.shape
        
            
        row_bottom-=down
        if row_bottom >rows_s:
            diff = row_bottom-rows_s
            new_arr = np.full((diff,cols_s,3),255)
            self.state = np.append(self.state,new_arr,axis=0)
            row_bottom = self.state.shape[0]
            rows_s,cols_s,useless = self.state.shape
            
        col_left+=left
        if col_left < 0:
            new_arr = np.full((rows_s,abs(col_left),3),255)
            self.state = np.append(new_arr,self.state,axis=1)
            col_right+=abs(col_left)
            col_left = 0
            rows_s,cols_s,useless = self.state.shape
            
        col_right-=right
        if col_right > cols_s:
            diff = col_right-cols_s
            new_arr = np.full((rows_s,diff,3),255)
            self.state = np.append(self.state,new_arr,axis=1)
            col_right = self.state.shape[1]
            rows_s,cols_s,useless = self.state.shape

        self.piece_display = (row_top,row_bottom,col_left,col_right)

         
         
         
       
        
