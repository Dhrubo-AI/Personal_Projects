import pygame
import sys
import csv
import copy
import time

pygame.init()

WIDTH = 800
HEIGHT = 600
COLOR = (0,101,149)


screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Sudoku')
title_font = pygame.font.Font('MachineGunk-nyqg.ttf',80)
path_font = pygame.font.Font('MachineGunk-nyqg.ttf',15)
inp_font = pygame.font.SysFont('calibri',12)

menu_bg = pygame.image.load('bg.jpg')
title = title_font.render('Sudoku',False,COLOR)
path = path_font.render('Enter Puzzle path :',False,COLOR)
inp_txt = ''
inp_field = pygame.Rect(80,280,300,15)
menu_flag = True

def empty(puzzle):
    empties = []
    for i in range(len(puzzle)):
        for j in range(len(puzzle)):
            if puzzle[i][j]=='0':
                empties.append((i,j))
    return empties

def menu():
    inp = inp_font.render(inp_txt, False, 'White')
    screen.blit(menu_bg, (0, 0))
    screen.blit(title, (80, 180))
    screen.blit(path, (80, 260))
    screen.blit(inp, (85, 282.5))
    pygame.draw.rect(screen, 'White', inp_field, 2)

def board(puzzle):
    board_origin = (200,100)
    tile_size = 40

    for i in range(len(puzzle)):
        for j in range(len(puzzle)):
            rect = pygame.Rect(
                board_origin[0] + j*tile_size,
                board_origin[1] + i* tile_size,
                tile_size, tile_size
            )
            pygame.draw.rect(screen,'White',rect,3)
            if puzzle[i][j]!='0':
                cell = path_font.render(puzzle[i][j],True,COLOR)
                cellRect = cell.get_rect()
                cellRect.center = rect.center
                screen.blit(cell,cellRect)

def revise(puzzle):
    maps = {}
    rank = []
    empties = empty(puzzle)
    for cell in empties:
        domain= list(range(1,10))
        maps[cell] = list(range(1,10))
        (i,j) = cell
        vert = [puzzle[a][j] for a in range(len(puzzle))]
        i_start = (i//3)*3
        j_start = (j//3)*3
        grid = [puzzle[c][b] for c in range(i_start,i_start+3) for b in range(j_start,j_start+3)]
        for val in domain:
            if str(val) in puzzle[i]:
                maps[cell].remove(val)
            elif str(val) in vert:
                maps[cell].remove(val)
            elif str(val) in grid:
                maps[cell].remove(val)
        rank_cell = len(maps[cell])
        if rank_cell==0:
            return (maps,False)
        if len(rank)==0:
            rank.append(cell)
        for r in range(len(rank)):
            if len(maps[rank[r]])>rank_cell:
                if cell not in rank:
                    rank = rank[:r]+[cell]+rank[r:]
        if cell not in rank:
            rank.append(cell)

    return (maps,rank)

def backtrack(puzzle,rank,maps):
    domains = copy.deepcopy(maps)
    empties = empty(puzzle)
    if len(empties)==0:
        return puzzle
    cell = rank[0]
    (i,j) = cell
    domain = copy.deepcopy(maps[cell])
    for val in domain:
        maps = copy.deepcopy(domains)
        puzzle[i][j] = str(val)
        out = revise(puzzle)
        if out[-1]==False:
            puzzle[i][j] = '0'
            maps[cell].remove(val)
            continue
        solved = backtrack(puzzle,out[-1],out[0])
        if solved!=False:
            return solved
        puzzle[i][j] = '0'
        maps[cell].remove(val)
    maps = domains
    return False

def solve(puzzle):
    (maps,rank) = revise(puzzle)
    #if rank==False:
    solved = backtrack(puzzle,rank,maps)
    return solved



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                inp_txt = inp_txt[:-1]
            else:
                if len(inp_txt)<=45:
                    inp_txt += event.unicode
        if event.type == pygame.KEYDOWN:
            if event.key == 13:
                try:
                    with open(inp_txt.strip()) as file:
                        f = csv.reader(file)
                        puzzle = []
                        for row in f:
                            puzzle.append(row)
                    menu_flag = False
                except:
                    pass
            if event.key == pygame.K_q:
                menu_flag = True
    if menu_flag:
        menu()
    else:
        screen.fill((35, 31, 32))
        board(puzzle)
        time.sleep(3)
        puzzle = solve(puzzle)

    pygame.display.update()