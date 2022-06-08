# Monet


## How To

1. **First point to the folder containing unreal_artnet and artnet_client from unreal** *(Edit -> Project Settings -> Python -> Additional Paths -> "Folder path here")*
2. **You have to restart unreal engine to apply the changes**

3. **Then import Unreal Blueprints folder contents to your unreal project by copying them to your projects folder**

4. **Start artnet_client by dragging BP_Artnet to your level**

**It is recommended to use unreal_artnet.stop() before closing the project to close network sockets, 
If this is not done the port will be held and the UnrealEditor.exe process has to be closed from the task manager
To start artnet again use unreal_artnet.start(unreal)**


## Unreal Python Demos

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
