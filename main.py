import random
import pygame
import PySimpleGUI as sg
random.seed()


def Random_start(x, y, percent_of_starting_active_cells):
    universe = []
    temp = []
    # Row filled with zeroes
    for r in range(0, x ):
        temp.append(0)

    # Add rows to 2d list
    for k in range(0, x):
        universe.append(list(temp))

    # Initiate random coordinates, on which cells will become alive.
    for l in range(0, int(((x * y)/100) * percent_of_starting_active_cells)):
        random_coord = (random.randint(0, x -1), random.randint(0, x -1))
        universe[random_coord[0]][random_coord[1]] = 1
    return universe


def Alive_Check(universe, x, y):
    if universe[x][y] == 1:
        return 1
    else:
        return 0


def Generation(universe, cells_x, cells_y, neighbours_to_reproduce, alive_margin):
    to_0 = []
    to_X = []
    for row in range(0, cells_y):
        for column in range(0, cells_x):
            cell = universe[row][column]
            n = 0

            #   Check neighbours, sum up alive ones
            if row == 0:
                if column == 0:
                    n += Alive_Check(universe, row + 1, column)
                    n += Alive_Check(universe, row, column + 1)
                    n += Alive_Check(universe, row + 1, column + 1)

                elif (column == cells_x -1):
                    n += Alive_Check(universe, row + 1, column)
                    n += Alive_Check(universe, row + 1, column -1)
                    n += Alive_Check(universe, row, column-1)

                else:
                    n += Alive_Check(universe, row + 1, column + 1)
                    n += Alive_Check(universe, row + 1, column)
                    n += Alive_Check(universe, row + 1, column -1)
                    n += Alive_Check(universe, row, column + 1)
                    n += Alive_Check(universe, row, column -1)

            elif row == cells_x -1:
                if column == 0:
                    n += Alive_Check(universe, row - 1, column)
                    n += Alive_Check(universe, row - 1, column + 1)
                    n += Alive_Check(universe, row, column + 1)

                elif column == cells_x - 1:
                    n += Alive_Check(universe, row - 1, column)
                    n += Alive_Check(universe, row - 1, column - 1)
                    n += Alive_Check(universe, row, column - 1)

                else:
                    n += Alive_Check(universe, row, column + 1)
                    n += Alive_Check(universe, row, column - 1)
                    n += Alive_Check(universe, row - 1, column)
                    n += Alive_Check(universe, row - 1, column + 1)
                    n += Alive_Check(universe, row - 1, column - 1)
            else:
                if column == 0:
                    n += Alive_Check(universe, row, column + 1)
                    n += Alive_Check(universe, row + 1, column)
                    n += Alive_Check(universe, row + 1, column + 1)
                    n += Alive_Check(universe, row - 1, column)
                    n += Alive_Check(universe, row - 1, column + 1)

                elif column == cells_x - 1:
                    n += Alive_Check(universe, row, column - 1)
                    n += Alive_Check(universe, row + 1, column)
                    n += Alive_Check(universe, row + 1, column - 1)
                    n += Alive_Check(universe, row - 1, column)
                    n += Alive_Check(universe, row - 1, column - 1)

                else:
                    n += Alive_Check(universe, row, column + 1)
                    n += Alive_Check(universe, row, column - 1)
                    n += Alive_Check(universe, row + 1, column)
                    n += Alive_Check(universe, row + 1, column + 1)
                    n += Alive_Check(universe, row + 1, column - 1)
                    n += Alive_Check(universe, row - 1, column)
                    n += Alive_Check(universe, row - 1, column + 1)
                    n += Alive_Check(universe, row - 1, column - 1)

            # If cell would change its state, mark it to be changed.
            n = str(n)
            if cell == 1:
                if n not in list(alive_margin):
                    to_0.append((row, column))
            else:
                if n in list(neighbours_to_reproduce):
                    to_X.append((row,column))

    # Change the states of marked cells
    for coordinate in to_0:
        universe[coordinate[0]][coordinate[1]] = 0

    for coordinate in to_X:
        universe[coordinate[0]][coordinate[1]] = 1

    return universe


def Game(x, y, percent_of_starting_active_cells, neighbours_to_reproduce, alive_margin, disco_mode):
    # Pygame stuff
    pygame.init()
    pygame.display.set_caption("Game of life")
    cell_size = 8
    generation = 1
    screen = pygame.display.set_mode((x * cell_size + 1, y * cell_size + 1))
    font = pygame.font.SysFont("Algerian",15)
    running = True
    grid = Generation(Random_start(x, y, percent_of_starting_active_cells), x, y, neighbours_to_reproduce, alive_margin)
    colours = [(220, 200, 255),(10, 200, 255), (220, 20, 255), (220, 200, 15), (220, 70, 15), (80, 10, 115), (00, 255, 15), (20, 100, 25)]
    amount_of_colours = len(colours)
    current_colour = random.randint(0,len(colours)-1)
    black = (0, 0, 0)

    # main game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        img = font.render(str("Gen: " + str(generation)), True, (255,255,255))
        img.set_alpha(127)
        screen.blit(img, (0, 0))
        column = 0
        grid = Generation(grid, x, y, neighbours_to_reproduce, alive_margin)
        vertical_step = 0

        # Draw cells on screen
        for vertical in range(y):
            horizontal_step = 0
            row = 0
            for horizontal in range(x):
                if grid[column][row] == 1:
                    if disco_mode:
                        if current_colour > amount_of_colours -1:
                            current_colour = 0
                        pygame.draw.rect(screen, colours[current_colour],
                                         pygame.Rect(horizontal_step, vertical_step, cell_size, cell_size))
                        current_colour += 1
                    else:
                        pygame.draw.rect(screen, colours[current_colour],
                                         pygame.Rect(horizontal_step, vertical_step, cell_size, cell_size))
                horizontal_step += cell_size
                row += 1
            column += 1
            vertical_step += cell_size
        generation += 1
        pygame.display.flip()
        pygame.time.wait(50)

        screen.fill(black)  # clear the screen for next generation


sg.theme('LightBrown10')


# UI
def intro():
    layout = [[sg.Text('Welcome to Conway\'s Game of Life!', size=(40, 1))],
              [sg.Text('Choose parameters and watch!:', size=(40, 1))],
              [sg.Text('Neighbours to stay alive:', size=(35, 1)), sg.Button('0', size=(2,1),  key='a0'), sg.Button('1', size=(2,1),  key='a1'),
               sg.Button('2', size=(2,1), key='a2'), sg.Button('3', size=(2,1),  key='a3'),
               sg.Button('4', size=(2,1),  key='a4'), sg.Button('5', size=(2,1),  key='a5')
               ,sg.Button('6', size=(2,1),  key='a6'), sg.Button('7', size=(2,1), key='a7'),
               sg.Button('8', size=(2,1),  key='a8')],
              [sg.Text('Percent of alive cells at the start:', size=(35, 1)),
               sg.Slider((1, 99), key='alive_percent', orientation='h', enable_events=True,
                         disable_number_display=False, default_value=25)],
              [sg.Text('Neighbours to reproduce:', size=(35, 1)), sg.Button('0', size=(2,1),  key='b0'),
               sg.Button('1', size=(2,1),  key='b1'), sg.Button('2', size=(2,1), key='b2'),
               sg.Button('3', size=(2,1),  key='b3'), sg.Button('4', size=(2,1),  key='b4'), sg.Button('5', size=(2,1),  key='b5')
               ,sg.Button('6', size=(2,1),  key='b6'), sg.Button('7', size=(2,1), key='b7'),
               sg.Button('8', size=(2,1),  key='b8')],
              [sg.Button('Run!'), sg.Button('Disco mode!'), sg.Button('Exit')]]
    return sg.Window('Game of Life', layout, location=(600, 300), finalize=True)


# PySimpleGUI loop
def main():
    toggled_dict = {"a0":False, "a1": False, "a2": False, "a3": False, "a4": False,
                    "a5": False, "a6": False, "a7": False, "a8": False,
                    "b0":False, "b1": False, "b2": False, "b3": False, "b4": False,
                    "b5": False, "b6": False, "b7": False, "b8": False, }

    are_toggled = []
    digits1 = []
    digits2 = []
    window1, window2 = intro(), None
    disco_mode = False
    while True:
        window, event, values = sg.read_all_windows()
        if event == sg.WIN_CLOSED or event == 'Exit':
            window.close()
            if window == window2:
                window2 = None
            elif window == window1:
                break
        if event in ['a0', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8',
                     'b0', 'b1',  'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8',]:
            toggled_dict[event] = not(toggled_dict[event])
            for key in toggled_dict:
                if toggled_dict[key]:
                    if key not in are_toggled:
                        are_toggled.append(key)
                else:
                    if key in are_toggled:
                        are_toggled.remove(key)
            window.Element(event).Update(button_color=(('DeepPink4', 'blue4')[toggled_dict[event]]))
        if event == 'Disco mode!':
            disco_mode = not disco_mode
            window.Element('Disco mode!').Update(button_color=(('DeepPink4', 'blue4')[disco_mode]))
        if event == 'Run!':
            for e in are_toggled:
                if e[0] == 'a':
                    digits1.append(e[1])
                else:
                    digits2.append(e[1])
            Game(180, 90, int(values['alive_percent']), digits2, digits1, disco_mode)

    window.close()


if __name__ == "__main__":
    main()
    