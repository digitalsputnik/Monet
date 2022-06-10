# Monet

## Installing

1. **First point to the folder containing unreal_artnet and artnet_client from unreal** *(Edit -> Project Settings -> Python -> Additional Paths -> "Folder path here")*
2. **You have to restart unreal engine to apply the changes**

3. **Then import Unreal Blueprints folder contents to your unreal project by copying them to your projects folder**

4. **Start artnet_client by dragging BP_Artnet to your level**

**It is recommended to use unreal_artnet.stop() before closing the project to close network sockets, 
If this is not done the port will be held and the UnrealEditor.exe process has to be closed from the task manager
To start artnet again use unreal_artnet.start(unreal)**


## DSDMpy Demos (Python)

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


## Apollo Controller Demos (Miniscript)

**Setup Artnet Demo Script**
1. Create a directional light in your level and name it "Light"
2. Run this custom script in the controller

```python
// Comments in miniscript are two backslashes, mind the syntax highlighting
// Get a list of all actors in unreal
send_repl("actors = unreal.EditorLevelLibrary.get_all_level_actors()","Desktop")
// Find an actor named Light and set a variable light as the actor
send_repl("for actor in actors:\n    if actor.get_actor_label() == 'Light':\n        light = actor","Desktop")
// Get the light component of the light actor
send_repl("light_component = light.get_editor_property('directional_light_component')","Desktop")
// Get the light color of the light component
send_repl("light_color = light_component.get_editor_property('light_color')","Desktop")
```

**Create Unreal Dummy lamp in controller**
1. Setup Unreal lamp using Setup Artnet Demo Script above
2. Run this custom script in the controller without the # signs

```python
// Comments in miniscript are two backslashes, mind the syntax highlighting
// Create a new dummy lamp in the controller
create_device("UnrealLamp")

// Add a color property to the dummy lamp to see it on the colorwheel
UnrealLamp.properties["color"] = [255,255,255,255,255]

// Create a function that sends out the color as an Unreal Python command
SendUnreal = function(color_in, tag)
    send_repl("light_color.set_editor_property('r', " + color_in[0] + "); light_color.set_editor_property('g', " + color_in[1] + "); light_color.set_editor_property('b', " + color_in[2] + ")", tag)
end function

// Set the previously made function as a callback to when the lamps color has changed
UnrealLamp.send_property_logic = "SendUnreal(__value,""Desktop"")"
```

**Create a lamp in Unreal for each lamp found in controller**
1. Run this custom script in the controller

```python
// Comments in miniscript are two backslashes, mind the syntax highlighting
// Create a function that sends out the color to both an apollo lamp and an unreal lamp
SendWithUnreal = function(color_in, device)
    // Logic that sends the color to unreal as a python command
    send_repl(device.name + "_color.set_editor_property('r', " + color_in[0] + "); " + device.name + "_color.set_editor_property('g', " + color_in[1] + "); " + device.name + "_color.set_editor_property('b', " + color_in[2] + ")", "Desktop")
    // Logic that sends the color to the apollo lamp
    send_repl("color.set_value(" + color_in + ")", device.name)
end function

// Loop though all devices in the controller
for device in device_list
    // Set the previously made function as a callback to when the lamps color has changed
    device.send_property_logic = "SendWithUnreal(__value,__self)"
    // Generate a new DirectionalLight actor in unreal
    send_repl(device.name + " = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.DirectionalLight, unreal.Vector(0,0,0))", "Desktop")
    // Set the DirectionalLight actors name the lamp name
    send_repl(device.name + ".set_actor_label('" + device.name + "')", "Desktop")
    // Get the DirectionalLightComponent of the actor to a variable
    send_repl(device.name + "_component = " + device.name + ".get_editor_property('directional_light_component')","Desktop")
    // Get the color object of the DirectionalLightComponent to a variable
    send_repl(device.name + "_color = " + device.name + "_component.get_editor_property('light_color')","Desktop")
end for
```

**Setup Unreal For Two Lamps**
1. Create two Directional Lights in unreal
2. Run this script in the apollo controller, but change light_one_name and light_two_name to the names of the DirectionalLights in your level

```python
light_one_name = "Light"
light_two_name = "Spotlight"

send_repl("actors = unreal.EditorLevelLibrary.get_all_level_actors()","Desktop")
send_repl("for actor in actors:\n    if actor.get_actor_label() == '" + light_one_name + "':\n        " + light_one_name + " = actor","Desktop")
send_repl("for actor in actors:\n    if actor.get_actor_label() == '" + light_two_name + "':\n        " + light_two_name + " = actor","Desktop")
send_repl(light_one_name + "_component = " + light_one_name + ".get_editor_property('directional_light_component')","Desktop")
send_repl(light_two_name + "_component = " + light_two_name + ".get_editor_property('directional_light_component')","Desktop")
send_repl(light_one_name + "_color = " + light_one_name + "_component.get_editor_property('light_color')","Desktop")
send_repl(light_two_name + "_color = " + light_two_name + "_component.get_editor_property('light_color')","Desktop")

SendWithUnreal = function(color_in, tag)
    send_repl(tag + "_color.set_editor_property('r', " + color_in[0] + "); " + tag + "_color.set_editor_property('g', " + color_in[1] + "); " + tag + "_color.set_editor_property('b', " + color_in[2] + ")", "Desktop")
end function

create_device(light_one_name)
create_device(light_two_name)

exec(light_one_name + ".properties[""color""] = [255,255,255,255,255]")
exec(light_two_name + ".properties[""color""] = [255,255,255,255,255]")

exec(light_one_name + ".send_property_logic = ""SendWithUnreal(__value,""""" + light_one_name + """"")"" ")
exec(light_two_name + ".send_property_logic = ""SendWithUnreal(__value,""""" + light_two_name + """"")"" ")
```

## Known issues
- Currently the response to a request is offset by one meaning the response to a command from DSDMpy will be of the previous command sent
