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
agentBlacklist = []
agentsperrow = 9
removeMode = False
data = None
window = None

portraitSize = 106
startx = 779
starty = 1069
marginx = 6
marginy = 5

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
    try :
        with open(data_file_path, "r") as f:
            data = json.load(f)
    except:
        data = {
            "loginBox": {
                "x": 1279,
                "y": 975
            }
        }
        if not os.path.exists(app_folder_path):
            os.makedirs(app_folder_path)
        with open(data_file_path, "w") as f:
            json.dump(data, f)
    with open(data_file_path, "r") as f:
        data = json.load(f)
    return data
def generateLayout():
    agentsPerRow = 9
    enabledAgents = []
    for agent in agents:
        if agent not in agentBlacklist:
            enabledAgents.append(agent)
    layout = []
    row = []
    layout.append([sg.Text("Choose Your Character")])
    for i in range(len(enabledAgents)):
        if i % agentsPerRow == 0 and i != 0:
            layout.append(row)
            row = []
        # if image exists, append image, else append button
        if os.path.exists(imageFolder + enabledAgents[i] + ".png"):
            row.append(sg.Button(enabledAgents[i],image_filename=imageFolder + enabledAgents[i] + ".png", key=enabledAgents[i]))
        else:
            row.append(sg.Button(enabledAgents[i], key=enabledAgents[i]))
    layout.append(row)
    layout.append([sg.Text("Current Resolution: " + str(pag.size().width) + "x" + str(pag.size().height)), sg.Button("Remove Mode")])
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
    time.sleep(3)
    window.un_hide()
    # Check for agent data

def main():
    print("Starting ValLock...")
    # Create the app and image folderes
    if not os.path.exists(app_folder_path):
        os.makedirs(app_folder_path)
    if not os.path.exists(imageFolder):
        os.makedirs(imageFolder)
    # generate the window
    global window
    global data
    data = load_data(data)
    layout = generateLayout()
    window = sg.Window('ValLock', layout)

    while True:
        event, values = window.read()    
        print(event)  
        if event == sg.WIN_CLOSED or event == 'Close':
            break
        elif event == 'Update Positions':
            print("Updating Positions")
        elif event == 'Remove Mode':
            global removeMode
            removeMode = not removeMode
            if removeMode:
                sg.popup("Remove Mode Enabled")
            else:
                sg.popup("Remove Mode Disabled")
        elif event == 'Generate Portraits':
            sg.popup("You will have 5 seconds to tab into Valorant and open the character select screen. Make sure the game is in fullscreen mode and on your primary monitor.")
            time.sleep(5)
            generate_portraits()
            layout = generateLayout()
            window.close()
            window = sg.Window('ValLock', layout)
            sg.popup("Portraits Generated")
        else:
            if removeMode:
                agentBlacklist.append(event)
                sg.popup("Agent " + event + " added to blacklist")
                layout = generateLayout()
                window.close()
                window = sg.Window('ValLock', layout)
            else:
                select_agent(event, data)

main()
