##Step1
#pre script
myApp = gui.getWindowsWithTitle("Unreal")[0]
myApp.restore()
time.sleep(1)
myApp.topleft = gui.Point(0,0)
myApp.width = 1920
myApp.height = 1200
#script
loc=[[101,17]]
if self.found_loc==None:
    print("  Image Not Found")
else:
    found = [self.found_loc.left,self.found_loc.top]
    abs_loc = [found[0]+loc[0][0], found[1]+loc[0][1]]
    gui.click(abs_loc[0], abs_loc[1])
    
##Step2    
#pre script

#script
loc=[[58,22]]
if self.found_loc==None:
    print("  Image Not Found")
else:
    found = [self.found_loc.left,self.found_loc.top]
    abs_loc = [found[0]+loc[0][0], found[1]+loc[0][1]]
    time.sleep(0.2)
    gui.click(abs_loc[0], abs_loc[1])
    time.sleep(0.2)
    gui.hotkey('space')
    time.sleep(0.2)
    gui.typewrite('interface')
    
##Step3
#pre script

#script
loc=[[118,30]]
if self.found_loc==None:
    print("  Image Not Found")
else:
    found = [self.found_loc.left,self.found_loc.top]
    abs_loc = [found[0]+loc[0][0], found[1]+loc[0][1]]
    time.sleep(0.2)
    gui.click(abs_loc[0], abs_loc[1])
    time.sleep(0.2)
    gui.typewrite('BPI_EditorTick')
    time.sleep(0.2)
    gui.press('enter')
    
##Step4
#pre script

#script
loc=[[54,57]]
if self.found_loc==None:
    print("  Image Not Found")
else:
    found = [self.found_loc.left,self.found_loc.top]
    abs_loc = [found[0]+loc[0][0], found[1]+loc[0][1]]
    time.sleep(0.2)
    gui.doubleClick(abs_loc[0], abs_loc[1])
    time.sleep(0.2)
    gui.typewrite('EditorTick')
    gui.press('enter')
    
##Step5
#pre script
myApp = gui.getWindowsWithTitle("BPI_EditorTick")[0]
myApp.restore()
time.sleep(0.2)
myApp.topleft = gui.Point(0,0)
myApp.width = 1920
myApp.height = 1200
#script
loc=[[176,20]]
if self.found_loc==None:
    print("  Image Not Found")
else:
    found = [self.found_loc.left,self.found_loc.top]
    abs_loc = [found[0]+loc[0][0], found[1]+loc[0][1]]
    time.sleep(0.2)
    gui.click(abs_loc[0], abs_loc[1])
    time.sleep(0.2)
    gui.hotkey('F7')
    time.sleep(0.2)
    gui.hotkey('alt','F4')
    
##Step6
#pre script

#script
loc=[[58,17]]
if self.found_loc==None:
    print("  Image Not Found")
else:
    found = [self.found_loc.left,self.found_loc.top]
    abs_loc = [found[0]+loc[0][0], found[1]+loc[0][1]]
    time.sleep(0.2)
    gui.click(abs_loc[0], abs_loc[1])
    time.sleep(0.2)
    gui.hotkey('space')
    time.sleep(0.2)
    gui.typewrite('utility')
    
##Step7
#pre script

#script
loc=[[35,28]]
if self.found_loc==None:
    print("  Image Not Found")
else:
    found = [self.found_loc.left,self.found_loc.top]
    abs_loc = [found[0]+loc[0][0], found[1]+loc[0][1]]
    gui.click(abs_loc[0], abs_loc[1])
    time.sleep(1)
    gui.typewrite('editorutilityactor')
    gui.press('down')
    gui.press('down')
    gui.press('enter')
    
##Step8
#pre script

#script
loc=[[67,34]]
if self.found_loc==None:
    print("  Image Not Found")
else:
    found = [self.found_loc.left,self.found_loc.top]
    abs_loc = [found[0]+loc[0][0], found[1]+loc[0][1]]
    gui.click(abs_loc[0], abs_loc[1])
    gui.typewrite('BP_EditorTicker')
    gui.press('enter')
    gui.press('enter')
    
##Step9
#pre script

#script
loc=[[12,180],[272,59],[273,220]]
if self.found_loc==None:
    print("  Image Not Found")
else:
    found = [self.found_loc.left,self.found_loc.top]
    abs_loc1 = [found[0]+loc[0][0], found[1]+loc[0][1]]
    abs_loc2 = [found[0]+loc[1][0], found[1]+loc[1][1]]
    abs_loc3 = [found[0]+loc[2][0], found[1]+loc[2][1]]
    time.sleep(0.2)
    gui.click(abs_loc1[0], abs_loc1[1])
    time.sleep(0.2)
    gui.click(abs_loc2[0], abs_loc2[1])
    time.sleep(0.2)
    gui.click(abs_loc3[0], abs_loc3[1])
    
    
###
#pre script

#script
loc=[[0,0,'python']]
keywords = []
if self.found_loc==None:
    print("-> Image Not Found")
else:
    print("-> Image Found @: "+str(self.found_loc))
    for location in loc:
        abs_location = [self.found_loc.left+location[0], self.found_loc.top+location[1]]
        if location[2] == 'click':
            time.sleep(self.ui_delay)
            gui.click(abs_location[0], abs_location[1])
            print("    -> Clicked @: ["+str(abs_location[0])+","+str(abs_location[1])+"]")
        if location[2] == 'type':
            try:
                text = location[3]
            except:
                text = ""
                
            time.sleep(self.ui_delay)
            gui.click(abs_location[0], abs_location[1])
            time.sleep(self.ui_delay)
            gui.typewrite(text)
            time.sleep(self.ui_delay)
            gui.press('enter')
            print("    -> Typed @: ["+str(abs_location[0])+","+str(abs_location[1])+"]")
            print("    -> "+text)
        if location[2] == 'python':
            #
            # ADD CUSTOM LOGIC HERE
            #
            print("->No logic entered for the current step")
            
            
#pre script

#script
loc=[[0,0,'python']]
keywords = []
if self.found_loc==None:
    print("-> Image Not Found")
else:
    print("-> Image Found @: "+str(self.found_loc))
    for location in loc:
        abs_location = [self.found_loc.left+location[0], self.found_loc.top+location[1]]
        if location[2] == 'click':
            time.sleep(self.ui_delay)
            gui.click(abs_location[0], abs_location[1])
            print("    -> Clicked @: ["+str(abs_location[0])+","+str(abs_location[1])+"]")
        if location[2] == 'type':
            try:
                text = location[3]
            except:
                text = ""
                
            time.sleep(self.ui_delay)
            gui.click(abs_location[0], abs_location[1])
            time.sleep(self.ui_delay)
            gui.typewrite(text)
            time.sleep(self.ui_delay)
            gui.press('enter')
            print("    -> Typed @: ["+str(abs_location[0])+","+str(abs_location[1])+"]")
            print("    -> "+text)
        if location[2] == 'python':
            #
            # ADD CUSTOM LOGIC HERE
            #
            print("    -> No logic entered for the current step")
            
            
    

    
    
    
#pre script

#script
loc=[[105,106,'click'],[354,98,'click'],[621,102,'click']]
keywords = []
if self.found_loc==None:
    print("-> Image Not Found")
else:
    print("-> Image Found @: "+str(self.found_loc))
    for location in loc:
        print(location)
        abs_location = [self.found_loc.left+location[0], self.found_loc.top+location[1]]
        if location[2] == 'click':
            time.sleep(self.ui_delay)
            gui.click(abs_location[0], abs_location[1])
            print("    -> Clicked @: ["+str(abs_location[0])+","+str(abs_location[1])+"]")
        if location[2] == 'type':
            try:
                text = location[3]
            except:
                text = ""
                
            time.sleep(self.ui_delay)
            gui.click(abs_location[0], abs_location[1])
            time.sleep(self.ui_delay)
            gui.typewrite(text)
            time.sleep(self.ui_delay)
            gui.press('enter')
            print("    -> Typed @: ["+str(abs_location[0])+","+str(abs_location[1])+"]")
            print("    -> "+text)
        if location[2] == 'python':
            #
            # ADD CUSTOM LOGIC HERE
            #
            print("    -> No logic entered for the current step")