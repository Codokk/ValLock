import PySimpleGUI as sg
import pyautogui as pag
from PIL import Image
import time
import os
import json

appdata_path = os.environ['APPDATA']
app_folder_path = os.path.join(appdata_path, "valLock")
imageFolder = os.path.join(app_folder_path, "agents/")

print(app_folder_path)
agents = [
    "astra",
    "breach",
    "brimstone",
    "chamber",
    "cypher",
    "deadlock",
    "fade",
    "gekko",
    "harbor",
    "iso",
    "jett",
    "kayo",
    "killjoy",
    "neon",
    "omen",
    "phoenix",
    "raze",
    "reyna",
    "sage",
    "skye",
    "sova",
    "viper",
    "yoru"
]
data = None
window = None
portraitSize = 101
startx = 782
starty = 1070
marginx = 11
marginy = 12

def generate_portraits():
    # Start with screenshot of game
    screenshot = pag.screenshot(imageFolder + "Game.png")
    i = 0
    while i < len(agents):
        new_image = screenshot.crop((startx + (i % 9) * (portraitSize + marginx), starty + (i // 9) * (portraitSize + marginy), startx + (i % 9) * (portraitSize + marginx) + portraitSize, starty + (i // 9) * (portraitSize + marginy) + portraitSize))
        new_image.save(imageFolder + agents[i] + ".png")
        i += 1
    return True
def generate_portraits_from_screenshot():
    existing_image = Image.open(imageFolder + "Game.png")
    i = 0
    while i < len(agents):
        new_image = existing_image.crop((startx + (i % 9) * (portraitSize + marginx), starty + (i // 9) * (portraitSize + marginy), startx + (i % 9) * (portraitSize + marginx) + portraitSize, starty + (i // 9) * (portraitSize + marginy) + portraitSize))
        new_image.save(imageFolder + agents[i] + ".png")
        i += 1
    return True

def load_data(data):
    data_file_path = os.path.join(app_folder_path, "data.json")
    with open(data_file_path, "r") as f:
        data = json.load(f)
    return data
def generateLayout():
    agentsPerRow = 9
    layout = []
    row = []
    layout.append([sg.Text("Choose Your Character")])
    for i in range(len(agents)):
        if i % agentsPerRow == 0 and i != 0:
            layout.append(row)
            row = []
        row.append(sg.Button('',image_filename=imageFolder + agents[i] + ".png", key=agents[i]))
    layout.append(row)
    layout.append([sg.Text("Current Resolution: " + str(pag.size().width) + "x" + str(pag.size().height)), sg.Button("Open Config Folder")])
    layout.append([sg.Button("Generate Portraits"),sg.Button("Update Positions"),sg.Button('Close')])
    return layout

def select_agent(agent, data):
    window.hide()
    time.sleep(1)
    print(data)
    while True:
        loc = pag.locateOnScreen(imageFolder + agent + ".png", confidence=0.8)
        if loc is not None:
            pag.click(loc.left + 40, loc.top + 35)
            pag.moveTo(data['loginBox']['x'], data['loginBox']['y'], 0.1)
            pag.doubleClick(data['loginBox']['x'], data['loginBox']['y']);
            break;
    window.un_hide()
    # Check for agent data

def main():
    # generate the window
    global window
    global data
    data = load_data(data)
    layout = generateLayout()
    window = sg.Window('ValLock', layout)

    while True:
        event, values = window.read()      
        if event == sg.WIN_CLOSED or event == 'Close':
            break
        elif event == 'Update Positions':
            print("Updating Positions")
        elif event == 'Open Config Folder':
            os.startfile(app_folder_path)
        elif event == 'Generate Portraits':
            sg.popup("You will have 5 seconds to tab into Valorant and open the character select screen. Make sure the game is in fullscreen mode and on your primary monitor.")
            time.sleep(5)
            generate_portraits()
            sg.popup("Reopen the app for changes to take effect.")
            exit();
        else:
            select_agent(event, data)

main()
