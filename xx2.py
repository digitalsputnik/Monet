import platform
from PIL import Image, ImageDraw
from PIL.PngImagePlugin import PngInfo
import pyautogui as gui
from IPython import display
from IPython.display import clear_output
import ipywidgets as widgets
from pynput import keyboard, mouse
import time
import dill
import codecs
import uuid
import shutil
import os
import copy
import pyperclip

# Widget usage, need to make it somehow an addon, ie install once and use
# ToDo: Create an object that will return the necessary init strings
create_txt_str = "self._w=widgets.Text(value=str(self._value),description=self.name)"
create_checkbox_str = "self._w=widgets.Checkbox(value=self._value,description=self.name)"
create_dropdown_str = "self._w=widgets.Dropdown(options=['move', 'click', 'right-click','double-click'],value=self._value,description=self.name)"
draw_str = "display.display(self._w)\nself._w.observe(self.setval,names=\"value\")"
edit_str = "self._w.value = self._value"
close_output_btn_str = "self._w=widgets.Button(description='close')\noutput = widgets.Output()\ndisplay(self._w, output)\nself._w.on_click(close_cell)"

i_text = {'init':create_txt_str,'edit':edit_str,'draw':draw_str}
i_dropdown = {'init':create_dropdown_str,'edit':edit_str,'draw':draw_str}
i_checkbox = {'init':create_checkbox_str,'edit':edit_str,'draw':draw_str}

def os_ctrl(short=False):
    if platform.system() == 'Darwin':
        if short:
            return 'cmd'
        else:
            return 'command'
    else:
        return 'ctrl'
    
def find_in_window(imgsrc, bbox=None, tries=10, wait=1, scroll=0, match_q = 0.9):
    """
    returns found image cordinates from desktop
    
    
    # return the co-ordinates of the found image or None
    # ToDo: bbox
    # ToDo: nice break
    # ToDo: move into step obejct?
    
    """
    #scale compensation from mouse co-ordinates to desktop bitmap
    scale = 2.0
    
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
                outn = []
                outn.append(int(out.left/scale))
                outn.append(int(out.top/scale))
                outn.append(int(out.width/scale))
                outn.append(int(out.height/scale))
                print("found @: "+str(outn))
                return outn
        except Exception as e:
            print(e)
        
        time.sleep(wait)
    # if function times out, no location is found    
    return None

class prop():
    """
    Simple object to hold any python value, with string based callbacks
    for init and edit. Main use is to allow bi-directional communication
    with the different python GUI elements
    
    if any interactive textblock is visible in the workbook it should show
    most up to date info, if the field is editabale, editing it would cause
    other fields to update sutomagicaly
    """
    
    def __init__(self, name, value, call_on_edit=False, init_script=None):
        self.name = name
        self._value = value 
        
        if type(init_script)==dict:
            #print("creating prop '"+name+"' with init script:")
            
            try:
                self._init_str = init_script['init']
            except:
                self._init_str = ''
                
            try:
                self._edit_str = init_script['edit']
            except:
                self._edit_str = ''
                
            try:
                self._draw_str = init_script['draw']
            except:
                self._draw_str = ''
                
        else:
            print("[!] Init script should dict with following keywords")
            print("    ['init','edit','draw']")
            self._init_str = ''
            self._edit_str = ''
            self._draw_str = ''
            
        if not(self._init_str ==''):
            exec(self._init_str)
        
        # if need to use the on edit while we initing the value
        if call_on_edit:
            self.value = value
    
    def __repr__(self):
        if (self._init_str != '') or (self._edit_str != ''): 
            return "'"+str(self.name)+"':'"+str(self._value)+"' (custom callbacks)"
        else:
            return "'"+str(self.name)+"':'"+str(self._value)+"'"
    
    # compatibilty for some UI libraries that do not support @property
    def setval(self, val):
        self._value = val['new']
    
    # recreate to support loading pickeled object
    def regen(self):
        exec(self._init_str)
    
    # draw the widget into UI and register appropriate callbacks
    def draw(self):
        exec(self._draw_str)
    
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self,val_in):
        self._value = val_in
        exec(self._edit_str)

class step():
    """
    process->workflow->[step]->action
    Step is a single unit of logic to find partial image on screen 
    and preform action realtive to the found location
    
    ToDo: Move screencapture to:
          https://python-mss.readthedocs.io/examples.html
          also image detection (cv2)
          
    ****  https://github.com/gereleth/jupyter-bbox-widget
    
    """
    
    def __init__(self, name=None, folder_in=None, workflow = None, timeout=30, wait=1, ui_delay = 0.1, scroll=False):
        self.workflow = workflow    # if step is attached to workflow
        self.timeout = timeout      # how many times to try before giving up on finding the image
        self.wait = wait            # how long to wait between tries to locate image after failure
        self.scroll = scroll        # mouse scroll when tring to find the image from desktop
        self.ui_delay = ui_delay    # small delay after pre script to allow some time to open menu
        self.pre_script_str = ""    # holds the script to run before looking for an image
        self.payload_str = ""       # if the step needs to hold on to some important data it is in here
        self._properties = []       # holds all the properties of the step, use 'add_prop' and 'get_prop' to manipulate
        self._action_img = None     # holds action loaction png preview
        
        if name==None:
            self.name = str(uuid.uuid4()) # if user does not provide name for the step UUID is assigned (same name for png)
            self._img = None          # holds the image to be searched on screen
        else:
            self.name = name
            tmpobj = self.loadPNG(folder=folder_in) # if name is provided, will try to load the image from disk
    
    def add_prop(self,name,val,init_script=None):
        """
        Repeating names NOT ALLOWED, if new variable is with the same name
        as the previous the existing prop is overwiritten and warning is printed
        """
        new_prop = prop(name,val,init_script=init_script)
        found_prop = self.get_prop(name)
        if found_prop:
            print(" -> overwriting "+new_prop.name)
            found_prop.__dict__ = new_prop.__dict__
        else:
            self._properties.append(new_prop)
    
    def get_prop(self,prop_name):
        """
        return property by name
        if name is not found False is returned
        """
        for p in self._properties:
            if p.name == prop_name:
                return p
            
        return False
    
    def _points2area(self, list_of_points):
        """
        return top, left corner location and with and height in list format
        """
        x1 = min(list_of_points[0][0], list_of_points[1][0])
        y1 = min(list_of_points[0][1], list_of_points[1][1])
        
        x2 = max(list_of_points[0][0], list_of_points[1][0])
        y2 = max(list_of_points[0][1], list_of_points[1][1])
        
        width = x2-x1
        height = y2-y1
        
        return [x1,y1,width,height]
    
    def _capture_pointer(self):
        """
        capture mouse pointer location on the screen
        print a message and return 2 co-ordinates
        """
        pointer = mouse.Controller()
        x = int(pointer.position[0])
        y = int(pointer.position[1])
        print(" -> saved location on screen: "+str(x)+" , "+str(y))
        return x,y
    
    def recapture_region(self):
        """
        re-capture the image if chaning the properties or moving mouse will change
        the appareance
        """
        
        # hardcoded osx scale
        scale = 2
        
        try:
            area = []
            area.append(int(self.get_prop("x").value))
            area.append(int(self.get_prop("y").value))
            area.append(int(self.get_prop("width").value))
            area.append(int(self.get_prop("height").value))
            self._img = gui.screenshot(region=(area[0]*scale,area[1]*scale,area[2]*scale,area[3]*scale))
            display.display_png(self._img)
        except:
            print(" -> no properties found, capture again")
            self.capture_region()
    
    def capture_region(self):
        print("Capture images and (input) positions for step construction")
        print("["+os_ctrl()+"]  - mark image corner (top left to right bottom)")  
        print("[esc]  - stop capture")
        print("")
        
        # hardcoded osx scale
        scale = 2
        
        # get the actual key obj on different platforms
        exec("marker_key = keyboard.Key."+os_ctrl(short=True),globals())
        
        points = []
        
        def on_release(key):
            if key == marker_key:
                x, y = self._capture_pointer()
                points.append([x,y])
                if len(points) == 2:
                    print(" -> captured: ")
                    area = self._points2area(points)
                    self._img = gui.screenshot(region=(area[0]*scale,area[1]*scale,area[2]*scale,area[3]*scale))
                    # set props
                    # ToDo: global init scripts
                    self.add_prop("x",str(area[0]),init_script=i_text)
                    self.add_prop("y",str(area[1]),init_script=i_text)
                    self.add_prop("width",str(area[2]),init_script=i_text)
                    self.add_prop("height",str(area[3]),init_script=i_text)
                    self.add_prop("break if not found",True,init_script=i_checkbox)
                    
                    display.display_png(self._img)
                    return False
                
            if key == keyboard.Key.esc:
                return False

        # Collect events until released
        with keyboard.Listener(on_release=on_release) as listener:
            listener.join()
        # show prop editor for step
    
    def capture_action_marker(self):
        if self._img == None:
            print("[!] Capture image 1st before assiging a marker")
            self.capture_region()
            self.capture_action_marker()
            return
        
        loc = find_in_window(self._img)
        print("Image found @: "+str(loc[0])+", "+str(loc[1]))
        print("["+os_ctrl()+"]  - mark action location")  
        print("[esc]  - stop capture")
        print("")
 
        # hardcoded osx scale
        scale = 2

        # get the actual key obj on different platforms
        exec("marker_key = keyboard.Key."+os_ctrl(short=True),globals())

        def on_release(key):
            if key == marker_key:
                x, y = self._capture_pointer()
                offset_x = x-loc[0]
                offset_y = y-loc[1]
                print(" -> captured action marker @: "+str(offset_x)+", "+str(offset_y))
                self._action_img = gui.screenshot(region=((x-25)*scale,(y-25)*scale,50*scale,50*scale))
                # set props
                # ToDo: global init scripts
                self.add_prop("offset_x",str(offset_x),init_script=i_text)
                self.add_prop("offset_y",str(offset_y),init_script=i_text)
                self.add_prop("mouse",'click',init_script=i_dropdown)
                self.add_prop("ctrla",False,init_script=i_checkbox)
                self.add_prop("text","",init_script=i_text)
                self.add_prop("enter",False,init_script=i_checkbox)
                self.add_prop("break if not found",False,init_script=i_checkbox)
                self.add_prop("allfound",False,init_script=i_checkbox)
                    
                #display.display_png(self._img)
                return False
                
            if key == keyboard.Key.esc:
                return False
        
        # Collect events until released
        with keyboard.Listener(on_release=on_release) as listener:
            listener.join()
            
        # find image 1st, if not found excpetion
        # show prop editor for marker
        
    def edit(self):
        """
        print all properties with active editing widgets
        ToDo: create ._w if it is not esisting allready
        """
        for p in self._properties:
            p.draw()

        print("[!] clear output before sving the step")
        # ToDo: add button to the end to close the output
        
        #def close_cell(inp):
            #print("test")
            #clear_output()    
        #exec(close_output_btn_str)
        
    def run(self):
        """
        if the step is finished then it is used inside workflow as run()
        all the step variables are self. and workflow variables self.workflow
        
        ToDo: self.workflow
        """
        # pre script
        if not(self.pre_script_str==""):
            exec(self.pre_script_str)
            
        if self._img==None:
            print(" -> No image in step, skipping the rest of the logic...")
            return True
            
        # find image
        self.found_loc = None
        self.found_loc = find_in_window(self._img, tries=self.timeout, wait=self.wait, scroll=self.scroll)
        
        # if no image is found, maybe move into execution if we want to have custom logic for not found as well
        if self.found_loc==None:
            print(" -> Image not found")
            for i in self._properties:
                if i.name=='break if not found':
                    if i.value==True:
                        return False
            return True
        
        # get actual screen space mouse co-ordinates
        offset_x = self.get_prop("offset_x")
        offset_y = self.get_prop("offset_y")
        if offset_x==False or offset_y==False:
            print(" -> Offsets not found")
            for i in self._properties:
                if i.name=='break if not found':
                    if i.value==True:
                        return False
            return True
        
        display.display_png(self._action_img)
        offset_x = int(offset_x.value)
        offset_y = int(offset_y.value)
        abs_location = [self.found_loc[0]+offset_x, self.found_loc[1]+offset_y]
        
        # filter through found props
        mouse = self.get_prop('mouse')
        if mouse.value == 'move':
            time.sleep(self.ui_delay)
            gui.gui.moveTo(abs_location[0], abs_location[1])
            print(" -> moved to: ["+str(abs_location[0])+","+str(abs_location[1])+"]")
            
        if mouse.value == 'click':
            time.sleep(self.ui_delay)
            gui.click(abs_location[0], abs_location[1])
            print(" -> clicked @: ["+str(abs_location[0])+","+str(abs_location[1])+"]")
            
        if mouse.value == 'right-click':
            time.sleep(self.ui_delay)
            gui.click(abs_location[0], abs_location[1], button='right')
            print(" -> right-clicked @: ["+str(abs_location[0])+","+str(abs_location[1])+"]")
            
        if mouse.value == 'double-click':
            time.sleep(self.ui_delay)
            gui.click(abs_location[0], abs_location[1], clicks=2)
            print(" -> double-clicked @: ["+str(abs_location[0])+","+str(abs_location[1])+"]")
            
        # ctrl a 
        ctrla = self.get_prop('ctrla')
        if ctrla.value==True:
            time.sleep(self.ui_delay)
            gui.hotkey(os_ctrl(),'a')
            print(" -> Keystroke: [ctrl]+[a]")
            
        # text entry
        text = self.get_prop('text')
        if not(text.value == ''):
            time.sleep(self.ui_delay)
            
            exec("out1="+text.value,globals())
            current_txt = out1
            
            pyperclip.copy(out1)
            gui.hotkey(os_ctrl(),'v')
            print(" -> Pasted : "+current_txt)
        
        # enter
        enter = self.get_prop('enter')
        if enter.value==True:
            time.sleep(self.ui_delay)
            gui.press('enter')
            print(" -> Keystroke: [enter]")
            
        # loop through all found objects
        allfound = self.get_prop('allfound')
        if allfound.value == True:
            self.workflow._current_step = self.workflow._current_step - 1
        
        
        return True
            
    def savePNG(self,folder=None):
        """
        save the [step] object as .png file. The file contains the image 
        to be searched and python logic to recreate the [step] object
              
        """
        
        if self._img == None:
            # ToDo
            print("[!] Capture image 1st before exporting, nothing to export yet...")
            return
        
        #close UI
        self.pre_dill()
        
        metadata = PngInfo()
        payload = codecs.encode(dill.dumps(self),"base64").decode()
        metadata.add_text("EMPpayload", payload)
        
        # create file name
        if folder==None:
            file_name = self.name
        else:
            file_name = folder+"/"+self.name
        
        print("load step: step = xx2.step(name=\""+file_name+"\")")
        self._img.save(file_name+'.png', pnginfo=metadata)
        
    def loadPNG(self, folder=None):
        # create file name
        if folder==None:
            file_name = self.name+'.png'
        else:
            file_name = folder+"/"+self.name+'.png'
        
        target_image = Image.open(file_name)
        payload = target_image.text["EMPpayload"]
        print(" -> Payload loaded, overwritng self")
        pickleobj = dill.loads(codecs.decode(payload.encode(), "base64"))
        self.__dict__ = pickleobj.__dict__
        
        # reactivate step props
        self.post_dill()
            
    def pre_dill(self):
        for p in self._properties:
            try:
                p._w.close()
                del(p._w)
            except:
                pass
            
    def post_dill(self):
        for p in self._properties:
            p.regen()
        
class workflow:
    """
    process->[workflow]->step->action
    workflow is a group of steps to achive one specific goal in the 
    process (ie create a new document and name it properly)
    
    ToDo: TmpFolder - when script is ran, temp folder is generated 
          and once finished if empty deleted
     
    """
    def __init__(self, name):
        self.name = name
        self.steps = []
        self._current_step = 0
    
    def run(self):
        """
        if run breaks due to an exception or timeout, calling run again 
        will continue from the failure paint
        """
        steps_total = len(self.steps)
        while True:
            if self._current_step == steps_total:
                self._current_step = 0
                break
            else:
                try:
                    if not(self.steps[self._current_step].run()):
                        raise Exception("Last step failed to locate image")
                except Exception as e:
                    print(e)
                    return
                    # insert break point if the script cannot continue without pervius sucess
                self._current_step = self._current_step+1
    
    def show_steps(self):
        index = 0
        for s in self.steps:
            print("Step["+str(index)+"]")
            display.display_png(s._img)
            print(" - mouse: ")
            display.display_png(s._action_img)
            index = index +1
    
    def add_step(self, requested_name=None):
        """
        create and add new step into workflow end
        if you want define custom name use name=...
        """
        self.steps.append(step(name=requested_name, folder_in=self.name, workflow=self))
            
    def last_step(self):
        """
        returns last step object
        ToDo: If empty
        """
        return self.steps[len(self.steps)-1]
    
    def copy_step(self, src_index=None):
        """
        copy last step and assign new name
        if using custom index any existing step in the workflo can be used
        """
        if src_index==None:
            src = self.steps[len(self.steps)-1]
        else:
            src = self.steps[src_index]
            
        self.steps.append(step())
        current_step = self.last_step()
        for p in src._properties:
            current_step._properties.append(copy.copy(p))
            
        current_step._img = copy.copy(src._img)
    
    def save(self):
        """
        save workflow as a seppareate folder with name
        the step order is staored is sepparate file in the folder as .pickle file 
        with same name as the folder
        """
        
        #check if workflow folder exists, if so delete it
        try:
            shutil.rmtree(self.name)
        except:
            pass
        
        #create new workflow folder
        os.makedirs(self.name)
        
        #save the list of step names
        file_list= []
        for f in self.steps:
            #save all steps
            f.savePNG(folder=self.name)
            
            file_list.append(f.name)
            content = codecs.encode(dill.dumps(file_list),"base64").decode()
            
            file = open(self.name+"/"+self.name+".pickle", "w")
            file.write(content)
            file.close()
                  
    def load(self):
        #load the workflow pickle
        with open(self.name+"/"+self.name+".pickle", "r") as file:
            data = file.read()
        
        self.file_list = dill.loads(codecs.decode(data.encode(), "base64"))
        #load in the steps?
        for file in self.file_list:
            self.add_step(requested_name=file)
                
test = step()