# -*- coding: utf-8 -*-
import pyglet, time, datetime
from pyglet.gl import *
from collections import deque
import pandas as pd
import numpy as np
from mod import DrawStim

#------------------------------------------------------------------------
use_scr = 0
rc = 0 # test stimuli color, red = 1, black = 0
lc = 0 # left stimuli color
rept = 9 # Input repeat counts
data = pd.read_csv("pare.csv") # Load the condition file
test_x = -1 # presentation test stimuli on right when positive number
disparity = -9 # Horizon disparity between test and control stimulus 
#------------------------------------------------------------------------

# Get display informations
platform = pyglet.window.get_platform()
display = platform.get_default_display()      
screens = display.get_screens()
win = pyglet.window.Window(style=pyglet.window.Window.WINDOW_STYLE_BORDERLESS)
win.set_fullscreen(fullscreen = True, screen = screens[use_scr]) # Present secondary display
#win.set_exclusive_mouse() # Exclude mouse pointer
key = pyglet.window.key

# Load variable conditions
header = data.columns # Store variance name
ind = data.shape[0] # Store number of csv file's index
dat = pd.DataFrame()
list_a = [] # Create null list to store experimental variance
list_b = []
iso = 6.8
deg1 = 42.8 # 1 deg = 43 pix at LEDCinemaDisplay made by Apple
am42 = 30.0 # 42 arcmin = 30 pix
cntx = screens[use_scr].width/2 #Store center of screen about x positon
cnty = screens[use_scr].height/8 #Store center of screen about y position
draw_objects = [] # 描画対象リスト
end_routine = False # Routine status to be exitable or not
tc = 0 # Count transients
tcs = [] # Store transients per trials
trial_starts = [] # Store time when trial starts
kud_list = [] # Store durations of key pressed
cdt = [] #Store sum(kud), cumulative reaction time on a trial.
mdt = []
dtstd = []
exitance = True
n = 0

print(dat)# Load sound resource
p_sound = pyglet.resource.media("button57.mp3", streaming = False)
beep_sound = pyglet.resource.media("p01.mp3", streaming = False)

#----------- Core program following ---------------------------- 

# A getting key response function
class key_resp(object):
    def on_key_press(self, symbol, modifiers):
        global tc, exitance, trial_start
        if exitance == False and symbol == key.SPACE:
            kd.append(time.time())
            tc = tc + 1
        if exitance == True and symbol == key.B:
            p_sound.play()
            exitance = False
            pyglet.clock.schedule_once(delete, 30.0)
            replace()
            trial_start = time.time()
        if symbol == key.ESCAPE:
            win.close()
            pyglet.app.exit()
    def on_key_release(self, symbol, modifiers):
        global tc
        if exitance == False and symbol == key.SPACE:
            ku.append(time.time())
            tc = tc + 1
resp_handler = key_resp()

# Set up polygons for presentation area
bsl = DrawStim.Quad(deg1 * 5, deg1 * 5, cntx - deg1 * iso, cnty, 1, 1, 1)
bsr = DrawStim.Quad(deg1 * 5, deg1 * 5, cntx + deg1 * iso, cnty, 1, 1, 1)
lfixv = DrawStim.Quad(5, 15, cntx - deg1 * iso + deg1 * 0.7071068, cnty - deg1 * 0.7071068, 0, 0, 1)
lfixw = DrawStim.Quad(15, 5, cntx - deg1 * iso + deg1 * 0.7071068, cnty - deg1 * 0.7071068, 0, 0, 1)
rfixv = DrawStim.Quad(5, 15, cntx + deg1 * iso + deg1 * 0.7071068, cnty - deg1 * 0.7071068, 0, 0, 1)
rfixw = DrawStim.Quad(15, 5, cntx + deg1 * iso + deg1 * 0.7071068, cnty - deg1 * 0.7071068, 0, 0, 1)

test = DrawStim.Quad(5, am42, cntx + deg1 * iso * test_x, cnty, 0, 0, 0)
control = DrawStim.Quad(5, am42, cntx + deg1 * iso * -test_x + disparity, cnty, 0, 0, 0)

# Store objects into draw_objects
def fixer():
    draw_objects.append(bsl)
    draw_objects.append(bsr)
    draw_objects.append(lfixv)
    draw_objects.append(lfixw)
    draw_objects.append(rfixv)
    draw_objects.append(rfixw)
    draw_objects.append(test)
    draw_objects.append(control)

# A end routine function
def exit_routine(dt):
    global exitance, n, dat, rightdot, leftdot
    exitance = True
    beep_sound.play()
    rightdot = DrawStim.Quad(5, 5, cntx + deg1 * iso * -test_x + dat[n + 1, 0] + 15, cnty, 0, 0, 0)
    leftdot = DrawStim.Quad(5, 5, cntx + deg1 * iso * -test_x + dat[n + 1, 0] - 15, cnty, 0, 0, 0)
    fixer()
    pyglet.app.exit()

@win.event
def on_draw():
    # Refresh window
    win.clear()
    # 描画対象のオブジェクトを描画する
    for draw_object in draw_objects:
        draw_object.draw()

# Remove stimulus
def delete(dt):
    global n, dl
    del draw_objects[:]
    p_sound.play()
    pyglet.clock.schedule_once(exit_routine, 30.0)
    # Check the experiment continue or break
    if n + 1 == dl:
        pyglet.app.exit()

# Add stimulus onto dispaly
def replace():
    draw_objects.append(rightdot)
    draw_objects.append(leftdot)

##def schedule(): # Scheduling flow
#    pyglet.clock.schedule_once(delete, 30.0)

# Store the start time
start = time.time()
win.push_handlers(resp_handler)

#----------------- start loop -----------------------------
# Get variables per trial from csv
for j in range(rept):
    camp = data.take(np.random.permutation(ind))
    dat = pd.concat([dat, camp], axis=0, ignore_index=True)
dat = dat.values
dl = dat.shape[0]
# Set up polygon for stimulus
rightdot = DrawStim.Quad(5, 5, cntx + deg1 * iso * -test_x + dat[0, 0] + 15, cnty, 0, 0, 0)
leftdot = DrawStim.Quad(5, 5, cntx + deg1 * iso * -test_x + dat[0, 0] - 15, cnty, 0, 0, 0)
for i in range(dl):
    tc = 0 #Count transients
    ku = deque([]) #Store unix time when key up
    kd = deque([]) #Store unix time when key down
    kud = [] # Differences between kd and ku
    da = dat[i]
    cola = da[0] # Store variance of index [i], column 0
    colb = da[1] # Store variance of index [i], column 1
    list_a.append(cola)
    list_b.append(colb)
    
    fixer()
    
    pyglet.app.run()
    
    trial_end = time.time()
    
    # Get results
    ku.append(trial_start + 31.0)
    while len(kd) > 0:
        kud.append(ku.popleft() - kd.popleft() + 0) # list up key_press_duration
    kud_list.append(str(kud))
    c = sum(kud)
    cdt.append(c)
    tcs.append(tc)
    if kud == []:
        kud.append(0)
    m = np.mean(kud)
    d = np.std(kud)
    mdt.append(m)
    dtstd.append(d)
    print("--------------------------------------------------")
    print("start: " + str(trial_start))
    print("end: " + str(trial_end))
    print("key_pressed: " + str(kud))
    print("transient counts: " + str(tc))
    print("cdt: " + str(c))
    print("mdt: " + str(m))
    print("dtstd "+ str(d))
    print("condition" + str(da))
    print("--------------------------------------------------")
    n += 1
#-------------- End loop -------------------------------

win.close()

# Store the end time
end_time = time.time()
daten = datetime.datetime.now()

# Write results onto csv
results = pd.DataFrame({header[0]:list_a, # Store variance_A conditions
                        header[1]:list_b, # Store variance_B conditions
                        "transient_counts":tcs, # Store transient_counts
                        "cdt":cdt, # Store cdt(target values) and input number of trials
                        "mdt":mdt,
                        "dtstd":dtstd,
                        "key_press_list":kud_list}) # Store the key_press_duration list
#index = range(ind*rept)
results.to_csv(path_or_buf="./data/" + str(daten) + ".csv", index=False) # Output experimental data

# Output following to shell, check this experiment
print(u"開始日時: " + str(start))
print(u"終了日時: " + str(end_time))  
print(u"経過時間: " + str(end_time - start))
