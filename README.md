# Monet

// How To

// First point to the folder containing unreal_artnet and artnet_client from unreal
// Edit -> Project Settings -> Python -> Additional Paths -> "Folder path here"

// You have to restart unreal engine to aplly the changes

// Then import Unreal Blueprints folder contents to your unreal project by copying them to your projects folder

// Start artnet_client by dragging BP_Artnet to your level

// It is recommended to use unreal_artnet.stop() before closing the project to close network sockets, 
// If this is not done the port will be held and the UnrealEditor.exe process has to be closed from the task manager
// To start artnet again use unreal_artnet.start(unreal)

// Unreal Python Demos

// Moving actor named Cube
// Create a cube in your level and name it "Cube"
// Send the following lines to unreal using DSDMpy

actors = unreal.EditorLevelLibrary.get_all_level_actors()

for actor in actors:\n    if actor.get_actor_label() == 'Cube':\n        cube = actor

cube.set_actor_location(unreal.Vector(0,0,0), False, False)

// Change Light color
// Create a directional light in your level and name it "Light"

// Send these lines one by one to create the light object in python
actors = unreal.EditorLevelLibrary.get_all_level_actors()

for actor in actors:\n    if actor.get_actor_label() == 'Light':\n        light = actor

light_component = light.get_editor_property('directional_light_component')
light_color = light_component.get_editor_property('light_color')

// This line will now change the color of the lamp previously setup, change the color by changing the 255 values of this command
light_color.set_editor_property('r', 255); light_color.set_editor_property('g', 255); light_color.set_editor_property('b', 255)

// PS! Unreal also has an alpha value which is currently not used in this demo