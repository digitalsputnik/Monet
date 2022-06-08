# Monet - How to use

1. **First point to the folder containing unreal_artnet and artnet_client from unreal** *(Edit -> Project Settings -> Python -> Additional Paths -> "Folder path here")*
2. **You have to restart unreal engine to apply the changes**

3. **Then import Unreal Blueprints folder contents to your unreal project by copying them to your projects folder**

4. **Start artnet_client by dragging BP_Artnet to your level**

**It is recommended to use unreal_artnet.stop() before closing the project to close network sockets, 
If this is not done the port will be held and the UnrealEditor.exe process has to be closed from the task manager
To start artnet again use unreal_artnet.start(unreal)**


# Unreal Python Demos

## DSDMpy Demos

**Moving actor named Cube**
1. Create a cube in your level and name it "Cube"
2. Send the following lines to unreal using DSDMpy

```python
# Get all actors in level
actors = unreal.EditorLevelLibrary.get_all_level_actors()
```
```python
# Find actor named Cube
# You might need to use \n newlines to send it as one line
for actor in actors:
    if actor.get_actor_label() == 'Cube':
        cube = actor
```
```python
# Set cube position to (0,0,0)
cube.set_actor_location(unreal.Vector(0,0,0), False, False)
```

**Change Light color**
1. Create a directional light in your level and name it "Light"
2. Send these lines one by one to create the light object in python

```python
# Get all actors in level
actors = unreal.EditorLevelLibrary.get_all_level_actors()
```
```python
# Find actor named Light
# You might need to use \n newlines to send it as one line
for actor in actors:
    if actor.get_actor_label() == 'Light':
        light = actor
```
```python
# Get the Directional Light Component of the actor Light
light_component = light.get_editor_property('directional_light_component')
```
```python
# Get the Color component of the Directional Light Component
light_color = light_component.get_editor_property('light_color')
```

3. The next command will now change the color of the lamp previously setup, change the color by changing the 255 values of this command

```python
# Set lamp color to (255,255,255)
light_color.set_editor_property('r', 255); light_color.set_editor_property('g', 255); light_color.set_editor_property('b', 255)
```

###### PS! Light Color also has an alpha value which is currently not used in this demo

## Apollo Controller Demos

**Setup Artnet Demo Script**
1. Create a directional light in your level and name it "Light"
2. Run this custom script in the controller

```python
send_repl("actors = unreal.EditorLevelLibrary.get_all_level_actors()","Desktop")
send_repl("for actor in actors:\n    if actor.get_actor_label() == 'Light':\n        light = actor","Desktop")
send_repl("light_component = light.get_editor_property('directional_light_component')","Desktop")
send_repl("light_color = light_component.get_editor_property('light_color')","Desktop")
```

**Create Unreal Dummy lamp in controller**
1. Setup Unreal lamp using Setup Artnet Demo Script above
2. Run this custom script in the controller

```python
create_device("UnrealLamp")

UnrealLamp.properties["color"] = [255,255,255,255,255]

SendUnreal = function(color_in, tag)
    send_repl("light_color.set_editor_property('r', " + color_in[0] + "); light_color.set_editor_property('g', " + color_in[1] + "); light_color.set_editor_property('b', " + color_in[2] + ")", tag)
end function

UnrealLamp.send_property_logic = "SendUnreal(__value,""Desktop"")"
```

## Known issues
- Currently the response to a request is offset by one meaning the response to a command from DSDMpy will be of the previous command sent
