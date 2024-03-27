# Libs
import PySimpleGUI as sg
import pyautogui as pag
from PIL import Image
import time
import os
import json

# Dirs
appdata_path = os.environ['APPDATA']
app_folder_path = os.path.join(appdata_path, "valLock")
imageFolder = os.path.join(app_folder_path, "agents/")
if not os.path.exists(app_folder_path):
    os.makedirs(app_folder_path)
if not os.path.exists(imageFolder):
    os.makedirs(imageFolder)
if not os.path.exists(imageFolder + "config.json"):
    with open(imageFolder + "config.json", "w") as f:
        json.dump({}, f)

# Agents
agentsAll = [
    "astra",
    "breach",
    "brimstone",
    "chamber",
    "clove",
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
agentsEnabled = sorted(agentsAll)
agentsPerRow = 9

config = None
#Windows
window = None
agentsWindow = None

# 1440p values
portraitSize = 106
startx = 779
starty = 1069
marginx = 6
marginy = 5
loginBoxX = 1279
loginBoxY = 975

defaultX = 2560
defaultY = 1440

# Adjust these values to match your screen resolution
scaleX = pag.size().width / defaultX
scaleY = pag.size().height / defaultY

portraitSize = int(portraitSize * scaleX)
startx = int(startx * scaleX)
starty = int(starty * scaleY)
marginx = int(marginx * scaleX)
marginy = int(marginy * scaleY)
loginBoxX = int(loginBoxX * scaleX)
loginBoxY = int(loginBoxY * scaleY)

def generate_portraits():
    global agentsEnabled
    # Start with screenshot of game
    screenshot = pag.screenshot(imageFolder + "Game.png")
    i = 0
    while i < len(agentsEnabled):
        new_image = screenshot.crop((startx + (i % 9) * (portraitSize + marginx), starty + (i // 9) * (portraitSize + marginy), startx + (i % 9) * (portraitSize + marginx) + portraitSize, starty + (i // 9) * (portraitSize + marginy) + portraitSize))
        new_image.save(imageFolder + agentsEnabled[i] + ".png")
        i += 1
    return True

# Load the config.json file
def load_config():
    global loginBoxX
    global loginBoxY
    global agentsEnabled
    config_file_path = os.path.join(app_folder_path, "config.json")
    try :
        with open(config_file_path, "r") as f:
            data = json.load(f)
    except:
        data = {
            "loginBox": {
                "x": loginBoxX,
                "y": loginBoxY
            },
            "agents": agentsEnabled
        }
        with open(config_file_path, "w") as f:
            json.dump(data, f)
    return data

def save_config():
    global config
    config_file_path = os.path.join(app_folder_path, "config.json")
    with open(config_file_path, "w") as f:
        json.dump(config, f)
# Geenrate the layout based on the config
def generateLayout():
    global agentsEnabled
    global agentsPerRow
    layout = []
    row = []
    layout.append([sg.Text("Choose Your Character")])
    for i in range(len(agentsEnabled)):
        if i % agentsPerRow == 0 and i != 0:
            layout.append(row)
            row = []
        # if image exists, append image, else append button
        if os.path.exists(imageFolder + agentsEnabled[i] + ".png"):
            row.append(sg.Button("",image_filename=imageFolder + agentsEnabled[i] + ".png", key=agentsEnabled[i]))
        else:
            row.append(sg.Button(agentsEnabled[i], key=agentsEnabled[i]))
    layout.append(row)
    layout.append([sg.Text("Current Resolution: " + str(pag.size().width) + "x" + str(pag.size().height)), sg.Button("Configure Agents")])
    layout.append([sg.Button("Generate Portraits"),sg.Button('Close')])
    return layout

def select_agent(agent, config):
    window.hide()
    time.sleep(1)
    while True:
        loc = pag.locateOnScreen(imageFolder + agent + ".png", confidence=0.8)
        if loc is not None:
            pag.click(loc.left + 40, loc.top + 35)
            pag.moveTo(config['loginBox']['x'], config['loginBox']['y'], 0.1)
            pag.doubleClick(config['loginBox']['x'], config['loginBox']['y'])
            break
    time.sleep(3)
    window.un_hide()
    # Check for agent data

def main():
    # generate the window
    global window
    global config
    global agentsEnabled
    global agentsAll
    global agentsWindow

    config = load_config()
    agentsEnabled = config['agents']
    layout = generateLayout()
    window = sg.Window('ValLock', layout)

    while True:
        event, values = window.read()    
        if event == sg.WIN_CLOSED or event == 'Close':
            break
        elif event == 'Configure Agents':
            agentRows = []
            for agent in agentsAll:
                agentRows.append([sg.Checkbox(agent, default=(True if agent in agentsEnabled else False), key=agent)])

            agentsWindow = sg.Window('ValLock - Configure Agents', [
                [sg.Text("Toggle Agents to Enable/Disable")],
                agentRows,
                [sg.Button('Cancel'), sg.Button('Blacklist')]
            ])
            while True:
                event, values = agentsWindow.read()
                if event == sg.WIN_CLOSED or event == 'Cancel':
                    agentsWindow.close()
                    break
                elif event == 'Blacklist':
                    newAgents = []
                    for agent in agentsAll:
                        if values[agent] == True:
                            newAgents.append(agent)
                    agentsEnabled = newAgents
                    config['agents'] = agentsEnabled
                    save_config()
                    layout = generateLayout()
                    agentsWindow.close()
                    window.close()
                    window = sg.Window('ValLock', layout)
        elif event == 'Generate Portraits':
            sg.popup("You will have 5 seconds to tab into Valorant and open the character select screen. Make sure the game is in fullscreen mode and on your primary monitor.")
            time.sleep(5)
            generate_portraits()
            layout = generateLayout()
            window.close()
            window = sg.Window('ValLock', layout)
            sg.popup("Portraits Generated")
        else:
            select_agent(event, config)

main()
