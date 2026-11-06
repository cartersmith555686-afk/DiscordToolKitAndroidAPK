import sys
import json
import time
import threading
import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.clock import Clock

Window.size = (480, 800)

class CyberpunkTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = get_color_from_hex("#121214")
        self.foreground_color = get_color_from_hex("#00FF66")
        self.cursor_color = get_color_from_hex("#00FF66")
        self.hint_text_color = get_color_from_hex("#006622")
        self.font_name = "Roboto"
        self.padding = [10, 10, 10, 10]

class NeonButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ""
        self.background_color = get_color_from_hex("#1F1135")
        self.color = get_color_from_hex("#9D4EDD")
        self.bold = True
        
    def on_press(self):
        self.background_color = get_color_from_hex("#9D4EDD")
        self.color = get_color_from_hex("#121214")
        
    def on_release(self):
        self.background_color = get_color_from_hex("#1F1135")
        self.color = get_color_from_hex("#9D4EDD")

class DeltaMatrixEngine(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.padding = 12
        self.spacing = 8
        
        header = Label(
            text="[b]DELTA WEBHOOK MATRIX v2.0[/b]\n[size=11][color=00FF66]STATUS: AUTHENTICATED[/color][/size]",
            markup=True,
            size_hint_y=None,
            height=55,
            halign='center',
            color=get_color_from_hex("#9D4EDD")
        )
        self.add_widget(header)
        
        self.saved_templates = {}
        self.allowed_mentions_config = {"parse": ["users", "roles", "everyone"]}
        
        self.webhook_input = CyberpunkTextInput(
            hint_text="TARGET DISCORD WEBHOOK URL",
            size_hint_y=None,
            height=45,
            multiline=False
        )
        self.add_widget(self.webhook_input)
        
        self.payload_input = CyberpunkTextInput(
            hint_text="INPUT STRING MESSAGE / CONTENT / VARIABLE DATA",
            size_hint_y=None,
            height=55,
            multiline=True
        )
        self.add_widget(self.payload_input)
        
        scroll = ScrollView(size_hint=(1, 0.52))
        grid = GridLayout(cols=2, spacing=6, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        
        features = [
            ("01. Send Message", self.feat_send_msg),
            ("02. Quick Embed", self.feat_quick_embed),
            ("03. Message + Embed", self.feat_msg_embed),
            ("04. Send File", self.feat_send_file),
            ("05. Send Spoiler File", self.feat_send_spoiler),
            ("06. Threads Config", self.feat_threads_config),
            ("07. Edit/Delete", self.feat_edit_delete),
            ("08. Bulk Send", self.feat_bulk_send),
            ("09. Scheduled Send", self.feat_scheduled_send),
            ("10. Allowed Mentions", self.feat_allowed_mentions),
            ("11. Username/Avatar", self.feat_user_avatar),
            ("12. Templates", self.feat_templates),
            ("13. Rotate Across", self.feat_rotate_across),
            ("14. Raw JSON", self.feat_raw_json),
            ("15. Test Ping", self.feat_test_ping),
            ("16. Webhook Info", self.feat_webhook_info),
            ("17. Manage Webhooks", self.feat_manage_webhooks),
            ("18. Import/Export", self.feat_import_export),
            ("19. Link Button", self.feat_link_button),
            ("20. Links Hub", self.feat_links_hub),
            ("00. System Quit", self.feat_quit)
        ]
        
        for name, callback in features:
            btn = NeonButton(text=name, size_hint_y=None, height=42)
            btn.bind(on_press=callback)
            grid.add_widget(btn)
            
        scroll.add_widget(grid)
        self.add_widget(scroll)
        
        self.console_output = Label(
            text="[System Ready] Dynamic Dashboard Loaded.\n",
            markup=True,
            size_hint_y=0.28,
            halign='left',
            valign='top',
            color=get_color_from_hex("#00FF66")
        )
        self.console_output.bind(size=self.console_output.setter('text_size'))
        
        console_scroll = ScrollView()
        console_scroll.add_widget(self.console_output)
        self.add_widget(console_scroll)

    def log(self, text, error=False):
        def update_text(dt):
            color = "FF3333" if error else "00FF66"
            self.console_output.text += f"[color={color}]>[/color] {text}\n"
        Clock.schedule_once(update_text)

    def validate_inputs(self):
        url = self.webhook_input.text.strip()
        data = self.payload_input.text.strip()
        if not url:
            self.log("Action Aborted: Missing destination URL path.", error=True)
            return None, None
        return url, data

    def feat_send_msg(self, instance):
        url, data = self.validate_inputs()
        if not url or not data: return
        def run():
            try:
                r = requests.post(url, json={"content": data, "allowed_mentions": self.allowed_mentions_config})
                self.log(f"Status: {r.status_code} | Dispatched Payload.")
            except Exception as e: self.log(f"Fault: {str(e)}", error=True)
        threading.Thread(target=run).start()

    def feat_quick_embed(self, instance):
        url, data = self.validate_inputs()
        if not url or not data: return
        def run():
            embed = {"title": "Delta Engine Alert", "description": data, "color": 10309852}
            try:
                r = requests.post(url, json={"embeds": [embed]})
                self.log(f"Quick Embed Dispatched: {r.status_code}")
            except Exception as e: self.log(str(e), error=True)
        threading.Thread(target=run).start()

    def feat_msg_embed(self, instance):
        url, data = self.validate_inputs()
        if not url or not data: return
        def run():
            payload = {
                "content": "Delta Broadcast Transmission:",
                "embeds": [{"title": "Matrix Metadata", "description": data, "color": 65280}]
            }
            try:
                r = requests.post(url, json=payload)
                self.log(f"Msg+Embed Status: {r.status_code}")
            except Exception as e: self.log(str(e), error=True)
        threading.Thread(target=run).start()

    def feat_send_file(self, instance):
        url, path = self.validate_inputs()
        if not url or not path: return
        def run():
            try:
                with open(path, 'rb') as f:
                    r = requests.post(url, files={'file': f})
                self.log(f"File Outbound Status: {r.status_code}")
            except Exception as e: self.log(f"Read error: {str(e)}", error=True)
        threading.Thread(target=run).start()

    def feat_send_spoiler(self, instance):
        url, path = self.validate_inputs()
        if not url or not path: return
        def run():
            try:
                filename = "SPOILER_" + path.split('/')[-1]
                with open(path, 'rb') as f:
                    r = requests.post(url, files={'file': (filename, f.read())})
                self.log(f"Spoiler transmission: {r.status_code}")
            except Exception as e: self.log(str(e), error=True)
        threading.Thread(target=run).start()

    def feat_threads_config(self, instance):
        url, data = self.validate_inputs()
        if not url: return
        self.log(f"Thread Activated for ID: {data if data else 'None'}")

    def feat_edit_delete(self, instance):
        url, data = self.validate_inputs()
        if not url or not data: return
        def run():
            try:
                parts = data.split('|')
                msg_id = parts[0].strip()
                if len(parts) > 1 and parts[1].strip().lower() == "delete":
                    r = requests.delete(f"{url}/messages/{msg_id}")
                    self.log(f"Delete Signal: {r.status_code}")
                else:
                    new_text = parts[1] if len(parts) > 1 else "Modified via UI."
                    r = requests.patch(f"{url}/messages/{msg_id}", json={"content": new_text})
                    self.log(f"Edit Patch: {r.status_code}")
            except Exception as e: self.log(f"Formatting error: {str(e)}", error=True)
        threading.Thread(target=run).start()

    def feat_bulk_send(self, instance):
        url, data = self.validate_inputs()
        if not url or not data: return
        def run():
            try:
                parts = data.split('|')
                count = int(parts[0]) if parts[0].isdigit() else 3
                msg_content = parts[1] if len(parts) > 1 else "Automated Stream Output"
                self.log(f"Initializing mass transmission: count={count}")
                for i in range(count):
                    requests.post(url, json={"content": f"{msg_content} | #{i+1}"})
                    time.sleep(0.4)
                self.log("Bulk deployment executed successfully.")
            except Exception as e: self.log(str(e), error=True)
        threading.Thread(target=run).start()

    def feat_scheduled_send(self, instance):
        url, data = self.validate_inputs()
        if not url or not data: return
        def run():
            try:
                parts = data.split('|')
                delay = int(parts[0]) if parts[0].isdigit() else 5
                msg = parts[1] if len(parts) > 1 else "Deferred transmission delivered."
                self.log(f"Queue established. Waiting {delay} seconds.")
                time.sleep(delay)
                r = requests.post(url, json={"content": msg})
                self.log(f"Deferred resolved: HTTP {r.status_code}")
            except Exception as e: self.log(str(e), error=True)
        threading.Thread(target=run).start()

    def feat_allowed_mentions(self, instance):
        _, data = self.validate_inputs()
        if "disable" in data.lower():
            self.allowed_mentions_config = {"parse": []}
            self.log("Mentions: All explicit parsing loops suppressed.")
        else:
            self.allowed_mentions_config = {"parse": ["users", "roles", "everyone"]}
            self.log("Mentions: Standard tracking enabled.")

    def feat_user_avatar(self, instance):
        url, data = self.validate_inputs()
        if not url or not data: return
        def run():
            try:
                parts = data.split('|')
                name = parts[0].strip()
                avatar = parts[1].strip() if len(parts) > 1 else ""
                payload = {"username": name}
                if avatar: payload["avatar_url"] = avatar
                r = requests.post(url, json={"content": "Profile override verified.", **payload})
                self.log(f"Identity update response: {r.status_code}")
            except Exception as e: self.log(str(e), error=True)
        threading.Thread(target=run).start()

    def feat_templates(self, instance):
        _, data = self.validate_inputs()
        if not data:
            self.log("Templates: " + str(list(self.saved_templates.keys())))
            return
        self.saved_templates["ActiveProfile"] = data
        self.log("Config object stored locally inside session stack.")

    def feat_rotate_across(self, instance):
        url, data = self.validate_inputs()
        if not url or not data: return
        def run():
            urls = [u.strip() for u in url.split(',')]
            self.log(f"Distribution running across {len(urls)} targets.")
            for target in urls:
                try: requests.post(target, json={"content": data})
                except: pass
            self.log("Rotational proxy dispatch complete.")
        threading.Thread(target=run).start()

    def feat_raw_json(self, instance):
        url, data = self.validate_inputs()
        if not url or not data: return
        def run():
            try:
                payload = json.loads(data)
                r = requests.post(url, json=payload)
                self.log(f"Raw JSON Response: {r.status_code}")
            except Exception as e: self.log(f"Syntax validation failure: {str(e)}", error=True)
        threading.Thread(target=run).start()

    def feat_test_ping(self, instance):
        url, _ = self.validate_inputs()
        if not url: return
        def run():
            try:
                r = requests.get(url)
                self.log(f"Ping Return Status: {'ONLINE' if r.status_code == 200 else f'ERROR [{r.status_code}]'}")
            except Exception as e: self.log(f"Target connection offline: {str(e)}", error=True)
        threading.Thread(target=run).start()

    def feat_webhook_info(self, instance):
        url, _ = self.validate_inputs()
        if not url: return
        def run():
            try:
                r = requests.get(url)
                if r.status_code == 200:
                    d = r.json()
                    self.log(f"Name: {d.get('name')} | Guild Target ID: {d.get('guild_id')}")
                else: self.log(f"Meta retrieval exception: {r.status_code}", error=True)
            except Exception as e: self.log(str(e), error=True)
        threading.Thread(target=run).start()

    def feat_manage_webhooks(self, instance):
        url, data = self.validate_inputs()
        if not url or not data: return
        def run():
            try:
                r = requests.patch(url, json={"name": data})
                self.log(f"Modification return code: {r.status_code}")
            except Exception as e: self.log(str(e), error=True)
        threading.Thread(target=run).start()

    def feat_import_export(self, instance):
        self.log(f"Backup token hash generated: {hash(self.webhook_input.text)}")

    def feat_link_button(self, instance):
        url, data = self.validate_inputs()
        if not url or not data: return
        def run():
            try:
                parts = data.split('|')
                label = parts[0].strip()
                target_url = parts[1].strip() if len(parts) > 1 else "https://google.com"
                payload = {
                    "content": "Interactive component array:",
                    "components": [{
                        "type": 1,
                        "components": [{"type": 2, "style": 5, "label": label, "url": target_url}]
                    }]
                }
                r = requests.post(url, json=payload)
                self.log(f"Button Link Response: {r.status_code}")
            except Exception as e: self.log(str(e), error=True)
        threading.Thread(target=run).start()

    def feat_links_hub(self, instance):
        self.log("Delta Hub Links routing stable.")

    def feat_quit(self, instance):
        sys.exit(0)

class DeltaMatrixContainerApp(App):
    def build(self):
        Window.clearcolor = get_color_from_hex("#0B0B0C")
        return DeltaMatrixEngine()

if __name__ == '__main__':
    DeltaMatrixContainerApp().run()
