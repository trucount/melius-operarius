import os
import json

class SoleManager:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.event_file = os.path.join(self.root_dir, "event.json")

    def get_event(self):
        """
        Reads the event from event.json.
        event.json format: {"event": "christmas"} or {"event": ""}
        """
        if os.path.exists(self.event_file):
            try:
                with open(self.event_file, "r") as f:
                    data = json.load(f)
                    return data.get("event", "").strip()
            except:
                return ""
        return ""

if __name__ == "__main__":
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    manager = SoleManager(root)
    print(f"Current Event: {manager.get_event()}")
