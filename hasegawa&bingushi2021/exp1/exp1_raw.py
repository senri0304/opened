# -*- coding: utf-8 -*-
import sys, os, pyglet, time, datetime
from pyglet.gl import *
from collections import deque
import pandas as pd
import numpy as np

# Get display informations
platform = pyglet.window.get_platform()
display = platform.get_default_display()      
screens = display.get_screens()
win = pyglet.window.Window(style=pyglet.window.Window.WINDOW_STYLE_BORDERLESS)
win.set_fullscreen(fullscreen = True, screen = screens[1]) # Present secondary display
#win.set_exclusive_mouse() # Exclude mouse pointer
key = pyglet.window.key

#------------------------------------------------------------------------
rc = 1 # right stimuli color, red = 1, black = 0
lc = 0 # left stimuli color
rept = 3 # Input repeat counts
data = pd.read_csv("cross.csv") # Load the condition file
test_x = -1 # presentation test stimuli on right when positive number
#------------------------------------------------------------------------

# Load variable conditions
header = data.columns # Store variance name
ind = data.shape[0] # Store number of csv file's index
dat = pd.DataFrame()
list_a = [] # Create null list to store experimental variance
#list_b = []
blank = 6.8
deg1 = 42.8 # 1 deg = 43 pix at LEDCinemaDisplay made by Apple
am42 = 30.0 # 42 arcmin = 30 pix 
cntx = screens[1].width/2 #Store center of screen about x positon
cnty = screens[1].height/8 #Store center of screen about y position
draw_objects = [] # 描画対象リスト
end_routine = False # Routine status to be exitable or not
tc = 0 # Count transients
tcs = [] # Store transients per trials
trial_starts = [] # Store time when trial starts
kud_list = [] # Store durations of key pressed
cdt = [] #Store sum(kud), cumulative reaction time on a trial.

# Load sound resource
p_sound = pyglet.resource.media("button57.mp3", streaming = False)
beep_sound = pyglet.resource.media("p01.mp3", streaming = False)

#----------- Core program following ---------------------------- 

# A drawing polygon function
class DrawStim():
    def __init__(self, width, height, xpos, ypos, R, G, B):
        self.width = width
        self.height = height
        self.xpos = xpos
        self.ypos = ypos
        self.angle = 0
        self.size = 1
        self.R = R
        self.G = G
        self.B = B
    def draw(self):
        glPushMatrix()
        glTranslatef(self.xpos, self.ypos, 0)
        glRotatef(self.angle, 0, 0, 1)
        glScalef(self.size, self.size, self.size)
        glColor3f(self.R, self.G, self.B)
    
        # 頂点リストを用意する
        x = self.width / 2
        y = self.height / 2
        vlist = pyglet.graphics.vertex_list(4, ('v2f',[-x, -y, x, -y, -x, y, x, y]), ('t2f', [0,0, 1,0, 0,1, 1,1]))
        # 描画する
        vlist.draw(GL_TRIANGLE_STRIP)
        glPopMatrix()

# A getting key response function
class key_resp(object):
    def on_key_press(self, symbol, modifiers):
        global tc, end_routine
        if end_routine == False and symbol == key.SPACE:
            kd.append(time.time())
            tc = tc + 1
        if end_routine == True and symbol == key.B:
            end_routine = False
            p_sound.play()
            pyglet.app.exit()
        if symbol == key.ESCAPE:
            win.close()
            pyglet.app.exit()
    def on_key_release(self, symbol, modifiers):
        global tc
        if end_routine == False and symbol == key.SPACE:
            ku.append(time.time())
            tc = tc + 1
resp_handler = key_resp()

# Set up polygons for presentation area
bsl = DrawStim(deg1*5, deg1*5, cntx - deg1*blank, cnty, 1, 1, 1)
bsr = DrawStim(deg1*5, deg1*5, cntx + deg1*blank, cnty, 1, 1, 1)
lfixv = DrawStim(5, 15, cntx - deg1*blank + deg1*0.7071068, cnty - deg1*0.7071068, 0,0,1)
lfixw = DrawStim(15,5, cntx - deg1*blank + deg1*0.7071068, cnty - deg1*0.7071068, 0,0,1)
rfixv = DrawStim(5, 15, cntx + deg1*blank + deg1*0.7071068, cnty - deg1*0.7071068, 0,0,1)
rfixw = DrawStim(15, 5, cntx + deg1*blank + deg1*0.7071068, cnty - deg1*0.7071068, 0,0,1)

# A end routine function
def end_rou(dt):
    global end_routine
    end_routine = True
    beep_sound.play()
    # Display fixation
    draw_objects.append(bsl)
    draw_objects.append(bsr)
    draw_objects.append(lfixv)
    draw_objects.append(lfixw)
    draw_objects.append(rfixv)
    draw_objects.append(rfixw)    

# Store the start time
start = time.time()

# Store objects into draw_objects
draw_objects.append(bsl)
draw_objects.append(bsr)
draw_objects.append(lfixv)
draw_objects.append(lfixw)
draw_objects.append(rfixv)
draw_objects.append(rfixw)

#----------------- start loop -----------------------------
# Get variables per trial from csv
for j in range(rept):
    camp = data.take(np.random.permutation(ind))
    dat = pd.concat([dat, camp], axis=0, ignore_index=True)
dat = dat.values
dl = dat.shape[0]
for i in range(dl):
    tc = 0 #Count transients
    ku = deque([]) #Store unix time when key up
    kd = deque([]) #Store unix time when key down
    kud = [] # Differences between kd and ku
    da = dat[i]
    cola = da[0] # Store variance of index [i], column 0
#    colb = da[1] # Store variance of index [i], column 1
    list_a.append(cola)
#    list_b.append(colb)
    
    # Set up polygon for stimulus
    cntrstm = DrawStim(5, am42, cntx + deg1*blank*test_x, cnty, 0, 0, 0)
    updot = DrawStim(5, 5, cntx + deg1*blank*-test_x - cola, cnty + am42/2 - 2.5 + 7.5, 0, 0, 0)
    downdot = DrawStim(5, 5, cntx + deg1*blank*-test_x - cola, cnty - am42/2 + 2.5 - 7.5, 0, 0, 0)
    
    # Add stimulus onto dispaly
    def replace(dt):
        draw_objects.append(cntrstm)
        draw_objects.append(updot)
        draw_objects.append(downdot)
    
    @win.event
    def on_draw():
        # Refresh window
        win.clear()
        
        # 描画対象のオブジェクトを描画する
        for draw_object in draw_objects:
            draw_object.draw()
    
    # Event handler handlers
    def set_handler(dt):
        win.push_handlers(resp_handler)
    def remove_handler(dt):
        win.remove_handlers(resp_handler)
    
    # Remove stimulus
    def delete(dt):
        del draw_objects[:]
        p_sound.play()
        # Check the experiment continue or break
        if i == dl - 1:
            pyglet.app.exit()
    
    # Scheduling flow
    pyglet.clock.schedule_once(remove_handler, 0.0)
    pyglet.clock.schedule_once(replace, 1.0)
    pyglet.clock.schedule_once(set_handler, 1.0)
    pyglet.clock.schedule_once(remove_handler, 31.0)
    pyglet.clock.schedule_once(delete, 31.0)
    pyglet.clock.schedule_once(end_rou, 61.0)
    pyglet.clock.schedule_once(set_handler, 61.0)
    
    trial_start = time.time()
    
    pyglet.app.run()
    
    trial_end = time.time()
    
    # Get results
    ku.append(trial_start + 31.0)
    while len(kd) > 0:
        kud.append(ku.popleft() - kd.popleft() + 0) # list up key_press_duration
    kud_list.append(str(kud))
    cdt.append(sum(kud))
    tcs.append(tc)
    trial_starts.append(trial_start)
    print("--------------------------------------------------")
    print("start: " + str(trial_start))
    print("end: " + str(trial_end))
    print("key_pressed: " + str(kud))
    print("transient counts: " + str(tc))
    print("cdt: " + str(sum(kud)))
    print("condition" + str(da))
    print("--------------------------------------------------")
#-------------- End loop -------------------------------

win.close()

# Store the end time
end_time = time.time()
daten = datetime.datetime.now()

# Write results onto csv
results = pd.DataFrame({header[0]:list_a, # Store variance_A conditions
#                        header.base[1]:list_b, # Store variance_B conditions
                        "transient_counts":tcs, # Store transient_counts
                        "cdt":cdt, # Store cdt(target values) and input number of trials
                        "traial_start":trial_starts,
                        "key_press_list":kud_list}) # Store the key_press_duration list
#index = range(ind*rept)
results.to_csv(path_or_buf="./data3/" + str(daten) + ".csv", index=False) # Output experimental data

# Output following to shell, check this experiment
print(u"開始日時: " + str(start))
print(u"終了日時: " + str(end_time))  
print(u"経過時間: " + str(end_time - start))
