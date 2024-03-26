from ahk import AHK, Window
from time import sleep, time
import threading
import os
import json

ahk = AHK()

configDefault = {
    "washingMachineMultiplier": 10,
    "clothingDuration": 600
}


class Roblox:
    
    def __init__(self):
        self.window:Window = ahk.find_window(title="Roblox")
        
    def press(self, key:str, duration:int=0):
        """Presses a key for a duration of time. If duration is 0, the key is pressed and released immediately."""
        ahk.send(f"{{{key} down}}")
        sleep(duration)
        ahk.send(f"{{{key} up}}")
        
    def backgroundPress(self, key:str, duration:int=0) -> threading.Thread:
        """Presses a key for a duration of time in a separate thread."""
        thread = threading.Thread(target=self.press, args=(key, duration))
        thread.start()
        return thread
    
    def multiPress(self, keys:list[str], duration:int=0):
        """Presses multiple keys simultaneously for a duration of time."""
        for key in keys:
            ahk.send(f"{{{key} down}}")
        sleep(duration)
        for key in keys:
            ahk.send(f"{{{key} up}}")
            
    def backgroundMultiPress(self, keys:list[str], duration:int=0) -> threading.Thread:
        """Presses multiple keys simultaneously for a duration of time in a separate thread."""
        thread = threading.Thread(target=self.multiPress, args=(keys, duration))
        thread.start()
        return thread
    
    def listPress(self, keys:list[str], duration:int=0):
        """Presses keys in a sequence for a duration of time."""
        for key in keys:
            self.press(key, duration)
        
    def backgroundListPress(self, keys:list[str], duration:int=0) -> threading.Thread:
        """Presses keys in a sequence for a duration of time in a separate thread."""
        thread = threading.Thread(target=self.listPress, args=(keys, duration))
        thread.start()
        return thread
    
    def sequencePress(self, keys:list[tuple[str, int]]):
        """Presses keys in a sequence with a duration of time."""
        for key, duration in keys:
            self.press(key, duration)
        
    def keyDown(self, key:str):
        """Presses a key down."""
        ahk.send(f"{{{key} down}}")
    
    def keyUp(self, key:str):
        """Releases a key up."""
        ahk.send(f"{{{key} up}}")
        
    def mouseMove(self, x:int, y:int):
        """Moves the mouse to a specific position."""
        position = self.window.get_position()
        x_multiplier = position.width / 1920
        y_multiplier = position.height / 1080
        x = x * x_multiplier
        y = y * y_multiplier
        ahk.mouse_move(x, y)
        
    def click(self, x:int, y:int):
        """Clicks at a specific position."""
        self.mouseMove(x, y)
        sleep(0.1)
        ahk.click()
        sleep(0.1)
        
    def zoomOut(self):
        """Zooms out the camera."""
        self.backgroundPress("o", 1)

    def reset(self):
        """Resets the character."""
        self.press("Esc", 0.1)
        self.press("r", 0.1)
        self.press("Enter", 0.1)
        sleep(5.5)
        
    def jump(self):
        """Makes the character jump."""
        self.press("Space", 0.1)
        
        
class Macro:
    config:dict = None
    clothingDuration:int = 0
    washingMachineLoadedAt:int = 0
    timeToGoToWashingMachine:int = 0
    
    
    def __init__(self, roblox:Roblox = None):
        roblox = roblox or Roblox()
        ahk.add_hotkey("f3", callback=self.exitHandler)
        ahk.start_hotkeys()
        roblox.window.activate()
        self.roblox = roblox
        self.config = self.loadConfig()
        self.clothesDuration = self.config["clothingDuration"] / self.config["washingMachineMultiplier"]
        sleep(0.5)
        
    def loadConfig(self):
        path = os.path.join(os.path.dirname(__file__), "config.json")
        if not os.path.exists(path):
            with open(path, "w") as file:
                json.dump(configDefault, file)
        with open(path, "r") as file:
            return json.load(file)
        
    def exitHandler(self):
        print("Exiting...")
        os._exit(0)
        
    def align(self):
        print("Aligning character.")
        roblox = self.roblox
        roblox.zoomOut()
        roblox.press("d", 0.05)
        roblox.multiPress(["s", "a"], 1.5)
        roblox.listPress(["s", "a"], 0.4)
        roblox.press("d", 1.5)
        
    def useSewer(self):
        print("Traveling to the hood.")
        roblox = self.roblox
        roblox.multiPress(["w", "d"], 1)
        roblox.press("w", 0.5)
        roblox.press("e", 0.1)
        roblox.click(1100, 520)
        sleep(0.2)
        
    def useWashingMachine(self):
        print("Using washing machine.")
        roblox.multiPress(["w", "d"], 1)
        roblox.listPress(["d", "s"], 1.5)
        roblox.click(400, 600)
        roblox.click(400, 600)
        
    def sellClothes(self):
        print("Selling clothes.")
        roblox.sequencePress([
            ("w", 0.8),
            ("d", 1.3),
            ("s", 2.1),
            ("e", 0.1)
        ])
        
    def run(self):
        roblox = self.roblox
        roblox.reset()
        while True:
            startedAt = time()
            self.align()
            self.useSewer()
            self.useWashingMachine()
            self.washingMachineLoadedAt = time()
            self.timeToGoToWashingMachine = time() - startedAt
            self.sellClothes()
            roblox.reset()
            sleepDuration = self.clothesDuration - (time() - self.washingMachineLoadedAt)
            sleepDuration -= self.timeToGoToWashingMachine
            sleepDuration += 5
            print("Waiting for", round(sleepDuration), "seconds.")
            sleep(sleepDuration )
        
        
        
if __name__ == "__main__":
    roblox = Roblox()
    macro = Macro(roblox)
    macro.run()