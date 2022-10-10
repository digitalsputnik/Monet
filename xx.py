import time
import pyautogui as gui
import keyboard
import pyperclip
import os
from PIL import Image, ImageDraw
from PIL.PngImagePlugin import PngInfo
from IPython import display

def find_in_window(imgsrc,bbox=None,tries=10,wait=1,scroll=0,match_q = 0.9):
    # return the co-ordinates of the found image or None
    # ToDo: bbox
    # ToDo: nice break
    
    for loop in range(tries):
        #if imgsrc is list all items in list will be tested
        if type(imgsrc)==list:
            for image in imgsrc:
                # ToDo add image/total images in step
                print("locating ("+str(loop)+"/"+str(tries)+"): ")
                display.display_png(image)  
        else:
            print("locating ("+str(loop)+"/"+str(tries)+"): ")
            if loop==0:
                # limit display instance to only one time
                display.display_png(imgsrc)  
        #enable scrolling while looking for specific image    
        if not(scroll==0):
            gui.scroll(scroll*-1)
        try:
            out = gui.locateOnScreen(imgsrc, confidence=match_q)
            if out!=None:
                return out
        except Exception as e:
            print(e)
        
        time.sleep(wait)
    # if function times out, no location is found    
    return None

class step:
    """
    process->workflow->[step]->action
    Step is a single unit of logic to find partial image on screen 
    and preform n number of actions realtive to the found location
     
    """
    def __init__(self, img=None, scrollable=False, pre = None, script= None, timeout=10):
        self._scroll = scrollable    # will scroll down between all tries
        self._pre_script = pre       # script to be ran before looking for the image
        self._flags = [False,False,False,False] # Flags for capture keyboartd feedback [mark,recapture,marker,quit]
        self._markers = []           # Action locations realtive to the image        
        self.ui_delay = 0.2          # time for ui to react
        self.found_loc = None        # 1st image found location
        self.timeout = timeout       # How many time to try
        self.match_q = 0.8           # Default search quality
        self.break_flow = False      # If this true if there is an error the workflow will stop and not try next step
        # main script
        if script==None:             # Default script parameter if step instance is just created
            self._script = 'loc=[]\r\nkeywords = []\r\nif self.found_loc==None:\r\n    print("-> Image Not Found")\r\nelse:\r\n    print("-> Image Found @: "+str(self.found_loc))\r\n    for location in loc:\r\n        abs_location = [self.found_loc.left+location[0], self.found_loc.top+location[1]]\r\n        if location[2] == \'click\':\r\n            time.sleep(self.ui_delay)\r\n            gui.click(abs_location[0], abs_location[1])\r\n            print("    -> Clicked @: ["+str(abs_location[0])+","+str(abs_location[1])+"]")\r\n        if location[2] == \'type\':\r\n            try:\r\n                text = location[3]\r\n            except:\r\n                text = ""\r\n            \r\n            time.sleep(self.ui_delay)\r\n            gui.hotkey(\'ctrl\',\'a\')\r\n            time.sleep(self.ui_delay)\r\n            gui.click(abs_location[0], abs_location[1])\r\n            time.sleep(self.ui_delay)\r\n            gui.typewrite(text)\r\n            time.sleep(self.ui_delay)\r\n            gui.press(\'enter\')\r\n            print("    -> Typed @: ["+str(abs_location[0])+","+str(abs_location[1])+"]")\r\n            print("    -> "+text)\r\n        if location[2] == \'python\':\r\n            #\r\n            # ADD CUSTOM LOGIC HERE\r\n            #\r\n            print("    -> No logic entered for the current step")'
        else:
            self._script = script
        # image loading
        if type(img) == str:
            self.loadPNG(img)
        else:
            self._img = img              # PIL png data
            
    def _reset_mark(self):
        self._flags[0] = True
        
    def _reset_recapture(self):
        self._flags[1] = True
        
    def _reset_marker(self):
        self._flags[2] = True
        
    def _reset_quit(self):
        self._flags[3] = True
    
    def capture(self):
        print("Capture images and (input) positions for step construction")
        print("[alt]  - mark image corner (top left to right bottom)")
        print("[r]    - recapture image with previous location, ie no mouse highlight")
        print("[m]    - add click or input marker, print variable as string")
        # ToDo: update marker with multiselect
        print("[q]    - stop capture")
        
        hkey_0 = keyboard.add_hotkey('alt', self._reset_mark)
        hkey_1 = keyboard.add_hotkey('r', self._reset_recapture)
        hkey_2 = keyboard.add_hotkey('m', self._reset_marker)
        hkey_3 = keyboard.add_hotkey('q', self._reset_quit)
        
        prev = False
        last_screenshot = None
        top_right_corner = [0,0]
        
        while True:
            # if [alt] is pressed / mark corner
            if self._flags[0]==True:
                pos = gui.position()
                self._flags[0]=False
                # ignore 1st click for image viewer
                if prev==False:
                    prev = [0,0]
                else:
                    last_screenshot = "gui.screenshot(region=("+str(prev[0])+","+str(prev[1])+","+str(pos.x-prev[0])+","+str(pos.y-prev[1])+"))"
                    print("-> "+last_screenshot)
                    #get_color(pos.x,pos.y)
                    self._img = gui.screenshot(region=(prev[0],prev[1],pos.x-prev[0],pos.y-prev[1]))
                    top_right_corner = prev
                    display.display_png(self._img)  
                prev=[pos.x,pos.y]   
            
            # ToDo:
            # if [r] is pressed / recapture the image from previous location 
            if self._flags[1]==True:
                self._flags[1]=False
                print("-> "+last_screenshot)
                self._img = eval(last_screenshot)
                display.display_png(self._img) 
            
            # if [m] is pressed / add marker 
            if self._flags[2]==True:
                pos = gui.position()
                self._flags[2]=False
                preview = gui.screenshot(region=(pos.x-25,pos.y-25,50,50))
                preview_draw = ImageDraw.Draw(preview)
                preview_draw.line((25,12,25,38),fill='red')
                preview_draw.line((12,25,38,25),fill='red')
                print("-> _markers.append("+str(pos.x-top_right_corner[0])+","+str(pos.y-top_right_corner[1])+",'click',''))")
                display.display_png(preview)
                self._markers.append([pos.x-top_right_corner[0],pos.y-top_right_corner[1],"click"])         
                           
            # if [q] is pressed / end capture   
            if self._flags[3]==True:
                self._flags[3]=False
                keyboard.remove_all_hotkeys()
                self._markers2string()
                self.copy()
                return
            
            # Be gentele to your CPU ;)
            time.sleep(0.1)
    
    def update_marker(self, marker_nr, mode='click', payload=None):
        try:
            self._markers[marker_nr][3] = payload
        except:
            self._markers[marker_nr].append(payload)
            
        try:
            self._markers[marker_nr][2] = mode
            self._markers[marker_nr][3] = payload
            self._markers2string()
        except Exception as e:
            print(e)
    
    def _markers2string(self):
        if self._markers == []:
            self._markers_str = "loc = []"
        else:
            # Convert markers to string
            markers_str = "loc=["
            for marker in self._markers:
                try:
                    markers_str=markers_str+"["+str(marker[0])+","+str(marker[1])+",'"+str(marker[2])+"','"+str(marker[3])+"'],"
                except:
                    # ToDo: Think how this is B.A.D.
                    markers_str=markers_str+"["+str(marker[0])+","+str(marker[1])+",'click',''],"

            self._markers_str = markers_str[:-1]+"]"
        # Update _script
        # Makes an assumption that 1st line is ALWAYS location
        cutpoint = self._script.find('\r')
        self._script = self._markers_str+self._script[cutpoint:]
    
    def run(self):
        # run pre script
        if not(self._pre_script == None):
            exec(self._pre_script)
        # find image
        self.found_loc = None
        self.found_loc=find_in_window(self._img, tries=self.timeout, scroll=self._scroll)
        # run main script
        if not(self._script == None):
            exec(self._script)
    
    def copy(self):
        out = self.step2string()
        pyperclip.copy(out)
        print("    Scripts copied")
        
    def step2string(self):
        # if pre script is used
        if self._pre_script==None:
            pre = ""
        else:
            pre = self._pre_script
            
        out = "#pre script\r\n"+pre+"\r\n#script\r\n"+self._script
        return(out)
    
    def string2step(self,inp):
        # split string into pre and normal script (pre script 1st with starting line [#pre script] and script later staring with [#script] line )
        pre = inp[inp.find('\n'):inp.find('#script')].strip()
        # if pre script is empty
        if pre=='':
            pre=None
            
        scr = inp[inp.find('#script')+9:].strip()
        
        return(pre,scr)
        
    def paste(self):
        in_string = pyperclip.paste()
        pre,src=self.string2step(in_string)
        if pre==None:
            print("No pre script....")
        else:
            print("Pre script:\n\r"+pre)
        print(src)
        question = multiselect([['Keep',0],['Cancel',1]], header='Update scripts?',footer="--")
        selection = question.get()
        if selection[1]==0:
            self._pre_script = pre
            self._script = src
            print("    Scripts updated")
        else:
            print("    Scripts NOT updated")
    
    def savePNG(self,file_name):
        if self._img == None:
            print("    Capture image 1st before exporting, nothing to export yet...")
            return
        
        metadata = PngInfo()
        metadata.add_text("EMPpayload", self.step2string())
        
        # if file name does not have an extension
        if not(file_name[-4:]=='.png'):
            file_name=file_name+'.png'
            
        self._img.save(file_name, pnginfo=metadata)
    
    def loadPNG(self,file_name):
        target_image = Image.open(file_name)
        payload = target_image.text["EMPpayload"]
        #print(payload)
        pre,scr = self.string2step(payload)
        self._pre_script = pre
        self._script = scr
        self._img = target_image
        print("Image sucessfully loaded")
    
    def showimg(self):
        self._img.show()

class workflow:
    """
    process->[workflow]->step->action
    workflow is a group of steps to achive one specific goal in the 
    process (ie create a new document and name it properly)
     
    """
    # automation->workflow->step
    # workflow is a group of steps to achive one specific goal in the process (ie create a new document and name it properly)
    # ToDo: TmpFolder - when script is ran, temp folder is generated and once finished if empty deleted
    # ToDo: Local Stored Parameters???
    def __init__(self):
        self.steps = []
        self._current_step = 0
    
    def load_folder(self, path2folder):
        # Loads all png files in folder as workflow
        #
        # ToDo path2folder
        filelist=os.listdir('.')
        pnglist = []
        for file in filelist:
            if file.endswith(".png"):
                pnglist.append(file)
        
        pnglist = sorted(pnglist)
             
        for png in pnglist:
            self.steps.append(step())
            self.steps[-1].loadPNG(png)
    
    def append(self, file=None):
        if file:
            self.steps.append([step(file),file])
        else:
            self.steps.append([step(),None])
    
    def run(self):
        steps_total = len(self.steps)
        for index in range(steps_total):
            try:
                self.steps[index][0].run()
                self._current_step = index
            except Exception as e:
                print(e)
                # insert break point if the script cannot continue without pervius sucess
    


class multiselect:  
    def __init__(self, items, header=None, footer=None, q='', default_answ=None, width=72):
        if type(items)!=list:
            items = []
        self.items = items
        self.header = header
        self.footer = footer
        self.q = q
        self.default_answ = default_answ
        self.width = width
    
    def _shortcutlist(self):
        """
        Create a list of shortcuts to check item in list
        """
        out_list=[]
        item_nr = 0
        for item in self.items:
            try:
                out_list.append(item[1])
            except Exception as e:
                out_list.append(item_nr)
            item_nr = item_nr+1
            
        return out_list
                
    
    def get(self):
        count = 0
        
        # draw header
        if not(self.header==None):
            label_len=len(self.header)+2
            spacer='-'*int((self.width-label_len)/2)
            print(spacer+" "+self.header+" "+spacer)
        
        for item in self.items:
            try:
                print(str(count)+" ["+str(item[1])+"] "+str(item[0]))
            except Exception as e:
                print(str(count)+" ["+str(count)+"] "+str(item[0]))
            count = count+1
        
        # draw footer
        if not(self.footer==None):
            footer_len=len(self.footer)+2
            spacer='-'*int((self.width-footer_len)/2)
            print(spacer+" "+self.footer+" "+spacer)
            
        # draw answer promt
        default_answ_str = None
        if self.default_answ==None:
            default_answ=len(self.items)-1
        else:
            default_answ=self.default_answ
            
        for item in self.items:
            if str(item[1])==str(default_answ):
                default_answ = item[1]
                default_answ_str = item[0]
                break
        
        ret_val = input(self.q+str(default_answ)+"("+str(default_answ_str)+"): ")
        
        if ret_val=='':
            return default_answ_str, default_answ
        
        else:
            ret_val = ret_val[0]
            
            # try to convert input into int
            try:
                ret_val = int(ret_val)
            except Exception as e:
                pass
                #print(e)
                #print("keeping answer as string")
                
            if ret_val in self._shortcutlist():
                answer = []
                for item in self.items:
                    if str(item[1])==str(ret_val):
                        answer = item
                        break

                return answer[0], answer[1]
            else:
                return None, None

test = step()
w = workflow()