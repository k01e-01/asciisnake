import random
import time
import keyboard

WIDTH    = 10
HEIGHT   = 10
SPEED    = 0.7
QUEUEMAX = 2
FOODS    = 1

data = list[list[int]]

def print_grid(gd: data):
    out = "\x1B[12A   ---\n"

    for row in gd: 
        for val in row:
            if   val == -1:    out += '[]'
            elif val == 0:     out += '..'
            elif val % 2 == 0: out += '&&'
            else:              out += '##'
        out += '\n'
    
    out += "   ---"
    print(out)

def generate_food(gd: data) -> data:
    while True:
        x = random.randint(0, WIDTH -1)
        y = random.randint(0, HEIGHT-1)
        if gd[y][x] == 0:
            gd[y][x] = -1
            return gd

def decrement_snake(gd: data) -> data:
    for j, row in enumerate(gd):
        for i, val in enumerate(row):
            if val > 0: gd[j][i] = val - 1

    return gd

def move_snake(
    gd:   data, 
    vel:  int,
    lnth: int,
    pos:  list[int],
) ->      tuple[data, int, list[int]]:
    
    if vel == 0: pos[0] += 1
    if vel == 1: pos[1] += 1
    if vel == 2: pos[0] -= 1
    if vel == 3: pos[1] -= 1
    # hmmmmmmmmmmmmmm
    
    if gd[pos[1]][pos[0]] == -1: 
        lnth += 1
        gd = generate_food(gd)

    if gd[pos[1]][pos[0]] > 0:
        while True: pass

    gd[pos[1]][pos[0]] = lnth
    return (gd, lnth, pos) 

def get_valid_input(queue: list) -> tuple[list, int]:
    while True:
        try: key = queue.pop(0).name
        except IndexError: 
            return ([], -1)

        if key == 'w': return (queue, 3)
        if key == 'a': return (queue, 2)
        if key == 's': return (queue, 1)
        if key == 'd': return (queue, 0)
        # hmmmmm

def update_vel(new_vel: int, old_vel: int) -> int:
    if new_vel == -1:                 return old_vel
    if (old_vel + new_vel) % 2 == 0:  return old_vel

    return new_vel

def main():
    print("\x1B[2J")

    gd = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
    for _ in range(FOODS):
        gd = generate_food(gd)
    
    snake_len = 3
    snake_vel = 0
    snake_pos = [1, 1]

    keypress_queue = []

    while True:
        keypress_queue, new_vel = get_valid_input(keypress_queue) 
        snake_vel = update_vel(new_vel, snake_vel) 

        gd = decrement_snake(gd)
        gd, snake_len, snake_pos = move_snake(
            gd, 
            snake_vel, 
            snake_len, 
            snake_pos,
        )

        if snake_pos[0] < 0 or snake_pos[1] < 0:
            while True: pass
        
        print_grid(gd)

        keyboard.start_recording()
        time.sleep(SPEED)
        keypress_queue += keyboard.stop_recording()
        while len(keypress_queue) > QUEUEMAX:
            keypress_queue.pop(0)
    

    

if __name__ == "__main__":
    main()
