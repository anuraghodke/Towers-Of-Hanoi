num_disks = 5
peg_height = 150
peg_y = 300
disk_height = 20
initial_disk_width = 5
disk_decrement = 15      
peg_x_positions = [75, 200, 325]  
disk_colors = ['salmon', 'orange', 'gold', 'darkSeaGreen', 'cornflowerBlue']

app.pegs = [[i for i in range(num_disks)], [], []]
app.selected_disk = None       
app.selected_peg = None     
app.move_list = []  # List of moves for solving the game
app.current_move_index = 0  # Index to track current move in the solution
app.auto_solve_mode = False
app.setMaxShapeCount(100000000)

def draw_peg(x, y, height):
    Line(x, y, x, y - height, lineWidth=6, fill='black')

def draw_disk(x, y, width, height, n, highlight=False):
    fill_color = 'whiteSmoke' if highlight else disk_colors[n]
    Rect(x - width / 2, y - height / 2, width, height, fill=fill_color)
    Circle(x - width / 2, y, height / 2, fill=fill_color)
    Circle(x + width / 2, y, height / 2, fill=fill_color)

def draw_tower():
    Rect(0, 0, 400, 400, fill='lavender')
    Label("Towers of Hanoi", 200, 75, size=30, bold=True, font='cinzel')
    Rect(20, 300, 360, 6)
    
    for x in peg_x_positions:
        draw_peg(x, peg_y, peg_height)

    for peg_index, peg in enumerate(app.pegs):
        disk_y = peg_y
        for disk_num in peg:
            disk_width = initial_disk_width + (num_disks - 1 - disk_num) * disk_decrement
            is_highlighted = (disk_num == app.selected_disk)
            draw_disk(peg_x_positions[peg_index], disk_y - disk_height / 2, disk_width, disk_height, disk_num, is_highlighted)
            disk_y -= disk_height

def recursive_hanoi(n, from_peg, to_peg, helper_peg, move_list):
    if n == 1:
        move_list.append((from_peg, to_peg))
    else:
        recursive_hanoi(n - 1, from_peg, helper_peg, to_peg, move_list)
        move_list.append((from_peg, to_peg))
        recursive_hanoi(n - 1, helper_peg, to_peg, from_peg, move_list)

def onMousePress(mouseX, mouseY):
    if not app.auto_solve_mode:  # Allow user interaction only when not auto-solving
        if 35 < mouseX < 115 and 150 < mouseY < 300:
            app.selected_peg = 0
        elif 160 < mouseX < 240 and 150 < mouseY < 300:
            app.selected_peg = 1
        elif 285 < mouseX < 365 and 150 < mouseY < 300:
            app.selected_peg = 2
        else:
            return  

        if app.selected_disk is None: # Selecting a disk
            if app.pegs[app.selected_peg]: # Selected peg is not empty & contains at least one disk
                app.selected_disk = app.pegs[app.selected_peg][-1]
                draw_tower()  
        else: # Placing the disk
            if not app.pegs[app.selected_peg] or app.pegs[app.selected_peg][-1] < app.selected_disk:
                app.pegs = [[item for item in sublist if item != app.selected_disk] for sublist in app.pegs]
                app.pegs[app.selected_peg].append(app.selected_disk)  
                app.selected_disk = None  
                app.selected_peg = None  
                draw_tower()  
            else:
                app.selected_disk = None
                app.selected_peg = None
                draw_tower() 

def autoSolveStep():
    if app.current_move_index < len(app.move_list):
        (from_peg, to_peg) = app.move_list[app.current_move_index]
        app.pegs[to_peg].append(app.pegs[from_peg].pop())
        app.current_move_index += 1
        draw_tower()

def onKeyPress(key):
    if key == 's':  # Start solving the puzzle automatically
        app.auto_solve_mode = True
        app.current_move_index = 0
        app.move_list = []
        app.pegs = [[i for i in range(num_disks)], [], []]
        app.selected_disk = None
        draw_tower()
        recursive_hanoi(num_disks, 0, 2, 1, app.move_list)
    elif key == 'n' and app.auto_solve_mode:  # Proceed to the next move
        autoSolveStep()

def onStep():
    if len(app.pegs[2]) == num_disks:
        Rect(0, 0, 400, 100, fill='lavender')
        Label("You Win!", 200, 75, size=30, bold=True, font='cinzel')
        app.stop()
        
draw_tower()