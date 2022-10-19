import time
import pyautogui as gui
import keyboard
import pyperclip
import os
from PIL import Image, ImageDraw
from PIL.PngImagePlugin import PngInfo
from IPython import display
import ipywidgets as widgets
import io
import dill
import codecs

def find_in_window(imgsrc,bbox=None,tries=10,wait=1,scroll=0,match_q = 0.9):
    """
    returns found image cordinates from desktop
    
    
    # return the co-ordinates of the found image or None
    # ToDo: bbox
    # ToDo: nice break
    # ToDo: move into step obejct?
    
    """
    
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
    
    ToDo: Add default delay on str2stp, remove default dealy for 
          stp2str // make _add_delay, _remove_delay functions and 
          impelemnt them in str2 functionality
    ToDo: Move screencapture to:
          https://python-mss.readthedocs.io/examples.html
          also image detection (cv2)
    ToDo: Create jupyter compatible GUI to edit the markers
          ie. temp.py
          
    TODO: create jupyter object with draw_marker(step, marker), draw_markers(markers)
          [] int,float,str,char -> text input
          [] bool -> checkbox
          [] img -> img
          [] multiselect?
          
    ****  https://github.com/gereleth/jupyter-bbox-widget
    
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
        self.payload = None          # palce to keep the data that is saved in step but can be input/output in the runtime
        self.ui = []
        # main script
        self._script = script
        # image loading
        if type(img) == str:
            self.loadPNG(img)
        else:
            self._img = img          # PIL png data
        self.img_region = (0,0,0,0)  # original image location
            
    def _reset_mark(self):
        self._flags[0] = True
        
    def _reset_recapture(self):
        self._flags[1] = True
        
    def _reset_marker(self):
        self._flags[2] = True
        
    def _reset_quit(self):
        self._flags[3] = True
    
    def display_markers(self):
        count = 0
        for marker in self._markers:
            print(str(count)+": "+str(marker[1]))
            count = count+1
            marker_lib = marker[0]
            for record in marker_lib:
                marker_lib[record].draw()
        
    
        """
        current_marker = self._markers[marker]
        
        # make the image to png file bytearray
        buff = io.BytesIO()
        img = value=current_marker[4]
        img.save(buff, format='png')

        # generate controllers
        loc_x = widgets.Text(value=str(current_marker[0]),description='X:')
        loc_y = widgets.Text(value=str(current_marker[1]),description='Y:')
        if 'no_ctrA' in current_marker[3]:
            chkb1 = widgets.Checkbox(value=False, description="[ctrl]+[a]")
        else:
            chkb1 = widgets.Checkbox(value=True, description="[ctrl]+[a]")
        
        def chkb1_callback(inp):
            if inp.new == True:
                if 'no_ctrA' in self._markers[marker][3]:
                    self._markers[marker][3].remove('no_ctrA')
            else:
                if not('no_ctrA' in self._markers[marker][3]):
                    self._markers[marker][3].append('no_ctrA')
                    
        chkb1.observe(chkb1_callback,names='value')
        
        
        chkb2 = widgets.Checkbox(value=True, description="mouse move")
        if 'no_click' in current_marker[3]:
            chkb3 = widgets.Checkbox(value=False, description="mouse [click]")
        else:
            chkb3 = widgets.Checkbox(value=True, description="mouse [click]")
            
        def chkb3_callback(inp):
            if inp.new == True:
                if 'no_click' in self._markers[marker][3]:
                    self._markers[marker][3].remove('no_click')
            else:
                if not('no_click' in self._markers[marker][3]):
                    self._markers[marker][3].append('no_click')
                    
        chkb3.observe(chkb3_callback,names='value')

        typein = widgets.Text(value='',description='type:')
            
        if 'no_enter' in current_marker[3]:
            chkb4 = widgets.Checkbox(value=False, description="[enter]")
        else:
            chkb4 = widgets.Checkbox(value=True, description="[enter]")
            
        def chkb4_callback(inp):
            if inp.new == True:
                if 'no_enter' in self._markers[marker][3]:
                    self._markers[marker][3].remove('no_enter')
            else:
                if not('no_enter' in self._markers[marker][3]):
                    self._markers[marker][3].append('no_enter')
                    
        chkb4.observe(chkb4_callback,names='value')
        
        image_side = widgets.VBox(children=[widgets.Image(value=buff.getvalue())])
        data_side = widgets.VBox(children=[loc_x,loc_y,chkb1,chkb2,chkb3,typein,chkb4])
        return widgets.HBox(children=[image_side,data_side])
        """

    def copy(self, other):
        self._img = other._img
        self._markers = other._markers
        
    
    def capture(self,draw_ui=True):
        # ToDo: split crosshair drawing into sepparate function
        print("Capture images and (input) positions for step construction")
        print("[alt]  - mark image corner (top left to right bottom)")
        print("[r]    - recapture image with previous location, ie no mouse highlight")
        print("[m]    - add click or input marker, print variable as string")
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
                    self._img = gui.screenshot(region=(prev[0],prev[1],pos.x-prev[0],pos.x-prev[0]))
                    top_right_corner = prev
                    display.display_png(self._img)  
                    
                    #daw UI
                    print("Step properties:")
                    draw_txt_str = "self.w=widgets.Text(value=str(self._val),description=self.name)\ndisplay.display(self.w)\nself.w.observe(self.setval,names='value')"
                    draw_checkbox_str = "self.w=widgets.Checkbox(value=self._val,description=self.name)\ndisplay.display(self.w)\nself.w.observe(self.setval,names='value')"
                    edit_str = "self.w.value = self._val"
                
                    self.props = []
                    self.props.append(prop("x",str(prev[0]),draw=draw_txt_str,on_edit=edit_str))
                    self.props.append(prop("y",str(prev[1]),draw=draw_txt_str,on_edit=edit_str))
                    self.props.append(prop("width",str(pos.x-prev[0]),draw=draw_txt_str,on_edit=edit_str))
                    self.props.append(prop("height",str(pos.x-prev[0]),draw=draw_txt_str,on_edit=edit_str))
                    
                    for p in self.props:
                        p.draw()
                        
                prev=[pos.x,pos.y]   
            
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
                
                # create props (adjustable parameters for markers)
                # x,y,no_ctrA, no_click, no_text, no_enter
                # ToDo: no_mouse, copy, paste, tab
                draw_txt_str = "self.w=widgets.Text(value=str(self._val),description=self.name)\ndisplay.display(self.w)\nself.w.observe(self.setval,names='value')"
                draw_checkbox_str = "self.w=widgets.Checkbox(value=self._val,description=self.name)\ndisplay.display(self.w)\nself.w.observe(self.setval,names='value')"
                edit_str = "self.w.value = self._val"
                
                loc_x = prop("x",str(pos.x-top_right_corner[0]),draw=draw_txt_str,on_edit=edit_str)
                loc_y = prop("y",str(pos.y-top_right_corner[1]),draw=draw_txt_str,on_edit=edit_str)
                loc_ctra = prop("[ctr]+[a]",True,draw=draw_checkbox_str,on_edit=edit_str)
                loc_click = prop("[mouse click]",True,draw=draw_checkbox_str,on_edit=edit_str)
                loc_text = prop("text","",draw=draw_txt_str,on_edit=edit_str)
                loc_enter = prop("[enter]",True,draw=draw_checkbox_str,on_edit=edit_str)
                
                self._markers.append([{'x':loc_x,'y':loc_y,'ctrla':loc_ctra,'click':loc_click,'text':loc_text,'enter':loc_enter},'ui','',preview])
                
                # draw ui
                if draw_ui==True:
                    print("["+str(len(self._markers))+"] Step: ")
                    loc_x.draw()
                    loc_y.draw()
                    loc_ctra.draw()
                    loc_click.draw()
                    loc_text.draw()
                    loc_enter.draw()
                           
            # if [q] is pressed / end capture   
            if self._flags[3]==True:
                self._flags[3]=False
                keyboard.remove_all_hotkeys()
                return
            
            # Be gentele to your CPU ;)
            time.sleep(0.1)
    
    def update_marker(self, marker_nr, xin=0, yin=0, mode='ui', payload=None, img=None):           
        try:
            self._markers[marker_nr][0]['x'].value = xin
            self._markers[marker_nr][0]['y'].value = yin
            self._markers[marker_nr][2] = mode
            self._markers[marker_nr][3] = payload
            self._markers[marker_nr][3] = img
        except Exception as e:
            print(e)
    
    def run(self):
        """
        executes the [pre] script, detects the image, runs [script]
        used for testing an called by [workflow] during execution.
        Exception handeling is done by the [workflow] object
        
        """
        # run pre script
        if not(self._pre_script == None):
            exec(self._pre_script)
        # find image
        self.found_loc = None
        self.found_loc=find_in_window(self._img, tries=self.timeout, scroll=self._scroll)
        
        # if no image is found, maybe move into execution if we want to have custom logic for not found as well
        if self.found_loc==None:
            print("-> Image Not Found")
            return
        
        for location in self._markers:
            abs_location = [self.found_loc.left+int(location[0]['x'].value), self.found_loc.top+int(location[0]['y'].value)]
            # ToDo incorporate the logic into step object and leave only pre and custom logic here
            if location[1] == 'ui':
                # params [0,0,'type', [txt,params]], params: no_ctrA, no_click, no_mouse, no_text, no_enter, copy, paste, tab
                try:
                    text = location[3][0]
                except:
                    text = ""
                
                if location[0]['ctrla'].value==True:
                    time.sleep(self.ui_delay)
                    gui.hotkey('ctrl','a')
                    print("    -> Keystroke: [ctrl]+[a]")
                if location[0]['click'].value==True:
                    # ToDo: no_mouse
                    time.sleep(self.ui_delay)
                    gui.click(abs_location[0], abs_location[1])
                    print("    -> clicked @: ["+str(abs_location[0])+","+str(abs_location[1])+"]")
                if not(location[0]['text'].value==""):    
                    time.sleep(self.ui_delay)
                    gui.typewrite(location[0]['text'].value)
                    print("    -> Typed : "+location[0]['text'].value)
                if location[0]['enter'].value:
                    time.sleep(self.ui_delay)
                    gui.press('enter')
                    print("    -> Keystroke: [enter]")
                """
                if 'copy' in location[3]:
                    time.sleep(self.ui_delay)
                    gui.hotkey('ctrl','c')
                    print("    -> Keystroke: [ctrl]+[c]")
                if 'paste' in location[3]:
                    time.sleep(self.ui_delay)
                    gui.hotkey('ctrl','c')
                    print("    -> Keystroke: [ctrl]+[v]")
                if 'tab' in location[3]:
                    time.sleep(self.ui_delay)
                    gui.hotkey('tab')
                    print("    -> Keystroke: [tab]")
                if 'copy2payload' in location[3]:
                    time.sleep(self.ui_delay)
                    gui.hotkey('ctrl','c')
                    self.payload = pyperclip.paste()
                    print("    -> Keystroke: [ctrl]+[c]")
                    print("    -> clipoard saved as payload")
                if 'paste4pyaload' in location[3]:
                    pyperclip.copy(self.payload)
                    time.sleep(self.ui_delay)
                    gui.hotkey('ctrl','v')
                    print("    -> Keystroke: [ctrl]+[v]")
                    print("    -> clipoard saved as payload")   
                """

            if location[1] == 'python':
                print("    -> running python")
                exec(self._script)               

    
    def savePNG(self,file_name):
        """
        save the [step] object as .png file. The file contains the image 
        to be searched and python logic to recreate the [step] object
              
        """
        if self._img == None:
            print("    Capture image 1st before exporting, nothing to export yet...")
            return
        
        metadata = PngInfo()
        metadata.add_text("EMPpayload", codecs.encode(dill.dumps(self),"base64").decode())
        
        # if file name does not have an extension
        if not(file_name[-4:]=='.png'):
            file_name=file_name+'.png'
            
        self._img.save(file_name, pnginfo=metadata)
    
    def loadPNG(self,file_name):
        target_image = Image.open(file_name)
        payload = target_image.text["EMPpayload"]
        print("    Payload loaded, overwritng self")
        dillobj = dill.loads(codecs.decode(payload.encode(), "base64"))
        self.__dict__ = dillobj.__dict__
    
    def showimg(self):
        self._img.show()

class workflow:
    """
    process->[workflow]->step->action
    workflow is a group of steps to achive one specific goal in the 
    process (ie create a new document and name it properly)
    
    ToDo: TmpFolder - when script is ran, temp folder is generated 
          and once finished if empty deleted
     
    """
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
    
class prop:
    """
    Property
    
    Keep the callbacks as strings, so it would be easy to edit and asjust
    """
    def __init__(self, name, value, kind="text", on_edit = "", on_create = "", on_cancel = "", draw = ""):
        self.name = name
        self._val = value
        self._kind = kind
        self._prev_val = None
        self._on_edit = on_edit
        self._on_create = on_create
        self._on_cancel = on_cancel
        self._draw = draw
        exec(self._on_create)
    
    @property
    def value(self):
        return self._val
    
    @value.setter
    def value(self, val):
        if self._val != val:
            self._prev_val = self._val
            self._val = val
        exec(self._on_edit)
    
    #callback for widget observe
    def setval(self,inp):
        self._val = inp['new']
        
    def cancel(self):
        """
        Flip previous and current value
        """
        tmpval = self._prev_val
        self._prev_val = self._value
        self._value = tmpval
        exec(self._on_cancel)
        
    def draw(self, draw = None, on_edit = None, on_cancel=None):
        """
        Functionality to draw the paramtere editor to gui
        """
        if not(draw==None):
            self._draw = draw
        if not(on_edit==None):
            self._on_edit = on_edit
        if not(on_cancel==None):
            self._on_cancel = on_cancel
            
        exec(self._draw)
        

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