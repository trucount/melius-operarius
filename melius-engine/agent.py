import os
import json
import glob
import shutil
from operarius import MeliusOperarius
from sole import SoleManager

class MeliusEngine:
    def __init__(self):
        self.root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.operarius = MeliusOperarius()
        self.sole_manager = SoleManager(self.root_dir)

    def run(self):
        print("Starting Melius Operarius Engine...")
        
        # 1. Check for reset command in event.json
        event = self.sole_manager.get_event()
        if event.lower() == "no change":
            print("Resetting system as requested...")
            for d in ["log", "error", "to-do", "history"]:
                dir_path = os.path.join(self.root_dir, d)
                if os.path.exists(dir_path):
                    shutil.rmtree(dir_path)
                os.makedirs(dir_path, exist_ok=True)
            return

        # 2. Run the main Operarius logic (Pantry-based)
        # This replaces the old event.json logic for website management
        self.operarius.run()
        
        print("Melius Engine run complete.")

if __name__ == "__main__":
    engine = MeliusEngine()
    engine.run()
