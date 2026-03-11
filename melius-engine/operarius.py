import os
import json
import requests
import datetime
from llm_client import LLMClient

class MeliusOperarius:
    def __init__(self):
        self.root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.client = LLMClient(self.root_dir)
        self.pantry_id = os.getenv("PANTRY_ID")
        self.base_url = f"https://getpantry.cloud/apiv1/pantry/{self.pantry_id}/basket"
        self.exclude_dirs = ["melius-engine", ".git", "history", "log", "to-do", "error", ".github", "node_modules"]
        self.target_folder = os.path.join(self.root_dir, "test-website")  # <-- Only modify this folder
        
    def get_pantry_data(self, basket_name):
        if not self.pantry_id:
            return None
        try:
            response = requests.get(f"{self.base_url}/{basket_name}")
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error fetching pantry data ({basket_name}): {e}")
        return None

    def post_pantry_data(self, basket_name, data):
        if not self.pantry_id:
            return
        try:
            requests.post(f"{self.base_url}/{basket_name}", json=data)
        except Exception as e:
            print(f"Error posting pantry data ({basket_name}): {e}")

    def get_all_files(self):
        all_files = []
        file_contents = {}
        for root, dirs, files in os.walk(self.target_folder):  # <-- Walk only test-website
            dirs[:] = [d for d in dirs if d not in self.exclude_dirs]
            for file in files:
                rel_path = os.path.relpath(os.path.join(root, file), self.root_dir)
                all_files.append(rel_path)
                content = self.read_file(rel_path)
                if content:
                    file_contents[rel_path] = content
        return all_files, file_contents

    def read_file(self, file_path):
        full_path = os.path.join(self.root_dir, file_path)
        if os.path.exists(full_path):
            with open(full_path, "r", encoding="utf-8") as f:
                return f.read()
        return None

    def write_file(self, file_path, content):
        ui_extensions = [".tsx", ".css", ".html", ".js", ".ts", ".jsx"]
        # <-- Only write inside test-website
        if not file_path.startswith("test-website/"):
            print(f"Skipped writing outside test-website: {file_path}")
            return False
        if not any(file_path.endswith(ext) for ext in ui_extensions):
            return False
            
        full_path = os.path.join(self.root_dir, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        return True

    def run(self):
        if not self.pantry_id:
            print("PANTRY_ID not found. Melius Operarius requires a Pantry ID.")
            return

        instructions = self.get_pantry_data("melius_instructions")
        if not instructions:
            print("No instructions found in Pantry.")
            return

        all_files, file_contents = self.get_all_files()
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        is_new_year = "01-01" in current_date or "12-31" in current_date
        
        base_prompt = f"""
        You are the Melius Operarius AI Programmer. Your goal is to build and maintain a professional website based on Pantry instructions.
        FILE SYSTEM RULES:
- ALL files MUST be created or edited ONLY inside the folder: test-website/
- Every path MUST start with: test-website/
- Example valid paths:
  test-website/index.html
  test-website/styles.css
  test-website/script.js
- NEVER reference files outside this directory.
        
        CRITICAL SYNC RULE:
        Compare the current website files with the Pantry instructions. If ANY page mentioned in the Pantry is missing, or if the content/theme/strict_text does not match EXACTLY, you MUST set "needs_update": true and provide the full content for those files.
        
        QUALITY & DESIGN:
        - Modern, responsive CSS (Flexbox/Grid).
        - Shared 'styles.css' and 'script.js'.
        - Separate HTML files for each page.
        
        STRICT GUIDELINES:
        - 'strict_text' MUST be used word-for-word. No changes.
        - 'theme' colors must be applied to the CSS.
        - Special tags ({{{{form}}}}, {{{{countdown}}}}, etc.) must be implemented as modular, blank-white components.
        
        FORM HANDLING:
        - If adding a {{{{form}}}}, first check the "forms_registry" provided. If the form_id is missing, request a new bucket via 'request_new_form_bucket'.
        - Once you have the bucket name, link the form to POST data to: https://getpantry.cloud/apiv1/pantry/{self.pantry_id}/basket/[BUCKET_NAME]
        """

        system_prompt = f"""
        {base_prompt}
        
        DATE: {current_date}
        IS NEW YEAR: {is_new_year}
        
        PANTRY INSTRUCTIONS:
        {json.dumps(instructions, indent=2)}
        
        CURRENT WEBSITE FILES:
        {json.dumps(file_contents, indent=2)}

        OUTPUT FORMAT (STRICT JSON ONLY, NO MARKDOWN):
        {{
          "needs_update": true/false,
          "request_new_form_bucket": [
            {{ "form_id": "unique_id", "description": "Form purpose" }}
          ],
          "modifications": [
            {{ "path": "path/to/file", "description": "sync reason", "type": "edit/new", "content": "Full content for new or updated file" }}
          ]
        }}
        """

        try:
            plan = self.client.chat(system_prompt)
        except Exception as e:
            print(f"AI failed to generate plan: {e}")
            return
        
        new_form_requests = plan.get("request_new_form_bucket", [])
        if new_form_requests:
            forms_registry = self.get_pantry_data("melius_forms") or {"forms": []}
            existing_ids = [f["form_id"] for f in forms_registry["forms"]]
            
            new_buckets_created = False
            for req in new_form_requests:
                if req["form_id"] not in existing_ids:
                    bucket_name = f"form_{req['form_id']}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
                    forms_registry["forms"].append({
                        "form_id": req["form_id"],
                        "bucket_name": bucket_name,
                        "created_at": datetime.datetime.now().isoformat()
                    })
                    self.post_pantry_data(bucket_name, {"submissions": []})
                    new_buckets_created = True
            
            if new_buckets_created:
                self.post_pantry_data("melius_forms", forms_registry)
                instructions["forms_registry"] = forms_registry
                system_prompt_retry = system_prompt + f"\n\nUPDATED FORMS REGISTRY: {json.dumps(forms_registry)}"
                try:
                    plan = self.client.chat(system_prompt_retry)
                except Exception as e:
                    print(f"AI failed on retry: {e}")
                    return

        if not plan.get("needs_update", False):
            print("Website is synchronized with Pantry.")
            return

        for mod in plan.get("modifications", []):
            content = mod.get("content")
            if content:
                if self.write_file(mod["path"], content):
                    print(f"Applied {mod['type']}: {mod['path']}")

        print("Melius Operarius sync complete.")
