# Monet

## Installing

1. **First point to the folder containing unreal_artnet and artnet_client from unreal** *(Edit -> Project Settings -> Python -> Additional Paths -> "Folder path here")*
2. **You have to restart unreal engine to apply the changes**

3. **Then import Unreal Blueprints folder contents to your unreal project by copying them to your projects folder**

4. **Start artnet_client by dragging BP_Artnet to your level**

**It is recommended to use unreal_artnet.stop() before closing the project to close network sockets, 
If this is not done the port will be held and the UnrealEditor.exe process has to be closed from the task manager
To start artnet again use unreal_artnet.start(unreal)**

**The default tag for Unreal Artnet is "Desktop"**






## Known issues
- Currently the response to a request is offset by one meaning the response to a command from DSDMpy will be of the previous command sent
