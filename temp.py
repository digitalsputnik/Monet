#pre script

#script
loc=[[0,0,'','']]
keywords = []
if self.found_loc==None:
    print("-> Image Not Found")
else:
    print("-> Image Found @: "+str(self.found_loc))
    for location in loc:
        abs_location = [self.found_loc.left+location[0], self.found_loc.top+location[1]]
        # ToDo incorporate the logic into step object and leave only pre and custom logic here
        if location[2] == 'ui':
            # params [0,0,'type', [txt,params]], params: no_ctrA, no_click, no_mouse, no_text, no_enter, copy, paste, tab
            try:
                text = location[3][0]
            except:
                text = ""
            
            if not('no_ctrA' in location[3][1]):
                time.sleep(self.ui_delay)
                gui.hotkey('ctrl','a')
                print("    -> Keystroke: [ctrl]+[a]")
            if not('no_click' in location[3][1]):
                time.sleep(self.ui_delay)
                gui.click(abs_location[0], abs_location[1])
                print("    -> clicked @: ["+str(abs_location[0])+","+str(abs_location[1])+"]")
            if not('no_text' in location[3][1]):    
                time.sleep(self.ui_delay)
                gui.typewrite(text)
                print("    -> Typed @: ["+str(abs_location[0])+","+str(abs_location[1])+"]")
                print("    -> "+text)
            if not('no_enter' in location[3][1]):
                time.sleep(self.ui_delay)
                gui.press('enter')
            if 'copy' in location[3][1]:
                time.sleep(self.ui_delay)
                gui.hotkey('ctrl','c')
                print("    -> Keystroke: [ctrl]+[c]")
            if 'paste' in location[3][1]:
                time.sleep(self.ui_delay)
                gui.hotkey('ctrl','c')
                print("    -> Keystroke: [ctrl]+[v]")
            if 'tab' in location[3][1]:
                time.sleep(self.ui_delay)
                gui.hotkey('tab')
                print("    -> Keystroke: [tab]")
            
        if location[2] == 'python':
            print("    -> running python")
            time.sleep(self.ui_delay)
            #gui.click(abs_location[0], abs_location[1])
            #print("    --> clicked @: ["+str(abs_location[0])+","+str(abs_location[1])+"]")
            print("    --> no python code entered")
            

#pre script

#script
loc=[[760,398,'python1',''],[-50,400,'python2','']]
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
            gui.hotkey('ctrl','a')
            time.sleep(self.ui_delay)
            gui.click(abs_location[0], abs_location[1])
            time.sleep(self.ui_delay)
            gui.typewrite(text)
            time.sleep(self.ui_delay)
            gui.press('enter')
            print("    -> Typed @: ["+str(abs_location[0])+","+str(abs_location[1])+"]")
            print("    -> "+text)
        if location[2] == 'python1':
            print("    -> running python1")
            time.sleep(self.ui_delay)
            gui.moveTo(abs_location[0], abs_location[1])
            print("    --> moved @: ["+str(abs_location[0])+","+str(abs_location[1])+"]")
            time.sleep(self.ui_delay)
            gui.scroll(-1)
            time.sleep(self.ui_delay)
            gui.scroll(-1)
            time.sleep(self.ui_delay)
            gui.scroll(-1)
            time.sleep(self.ui_delay)
            gui.scroll(-1)
            time.sleep(self.ui_delay)
            gui.scroll(-1)
            print("    --> zoom: -5")
        if location[2] == 'python2':
            print("    -> running python2")
            time.sleep(self.ui_delay)
            gui.click(abs_location[0], abs_location[1])
            print("    --> moved @: ["+str(abs_location[0])+","+str(abs_location[1])+"]")
            with open('darkGrid_mat.txt', 'r') as file:
                content = file.read()
            pyperclip.copy(content)
            time.sleep(self.ui_delay)
            gui.hotkey('ctrl','v')
            print("    --> typed: [ctrl]+[v]")