# template for "Stopwatch: The Game"
import simplegui

# define global variables
count = 0
sec = 0
min = 0
x = 0
y = 0
num_1 = 0
num_2 = 0

# in tenths of seconds into formatted string A:BC.D
def format(t):
    global count, sec, min
    t = count
    if (t == 10):
        sec = sec + 1
        count = 0
        
    if (sec == 60):
        min = min + 1
        sec = 0
        
# define handlers buttons; "Start", "Stop", "Reset"
def start_timer():
    global num_1
    global num_2
    if ((num_1 - num_2) == 0):
        num_1 = num_1 + 1
        timer.start()

def stop_timer():
    global x
    global y
    global num_1
    global num_2
    if ((num_1 - num_2) == 1):
        num_2 = num_2 + 1
        timer.stop()
        y = y + 1
        if (count == 0):
            x = x + 1
    
def reset_timer():
    global count
    global sec
    global min
    global x
    global y
    timer.stop()
    count = 0
    sec = 0
    min = 0
    x = 0
    y = 0
        
def exit_timer():
    frame.stop()

# define event handler for timer with 0.1 second interval
def timer_handler():
    global count
    count = count + 1
    
def draw_handler(canvas):
    global count
    global sec
    global min
    global x
    global y
    format(count)
    if (sec < 10):
        canvas.draw_text(str(min) + ":" + str(0) +str(sec) + "." + str(count),(70, 110), 60, "White")
    else:
        canvas.draw_text(str(min) + ":" + str(sec) + "." + str(count), (70, 110), 60, "White")
    canvas.draw_text(str(x) + "/" + str(y), (10, 30), 20, "Red")

# create frame
frame = simplegui.create_frame("Stopwatch! The Incredible Game", 250, 200)

# register event handlers
timer = simplegui.create_timer(100, timer_handler)
frame.add_button("Start", start_timer,200)
frame.add_button("Stop", stop_timer,200)
frame.add_button("Reset",reset_timer,200)
frame.set_draw_handler(draw_handler)
frame.add_button("Exit Game", exit_timer,100)

# start timer and frame
frame.start()
