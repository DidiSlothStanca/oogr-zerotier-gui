import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog, ttk
import subprocess
import json
import os

# =======================================================================
# THEME SYSTEM & CONFIG
# =======================================================================
THEMES = {
    "default": {  # Dark Blue - purple (default)
        "name": "Default (Dark Blue)",
        "primary": "#1a1a2e",
        "secondary": "#16213e",
        "accent": "#0f3460",
        "highlight": "#e94560",
        "text": "#ffffff",
        "text_secondary": "#b0b0b0",
        "button_text": "#ffffff",
        "success": "#4CAF50",
        "warning": "#FF9800",
        "danger": "#F44336",
        "card_bg": "#2d3047",
        "border": "#3a3d5c",
        "button_bg": "#0f3460",
        "button_fg": "#ffffff",
        "text_background": "#1e1e35"
    },
    "dark": {  # Classic dark mode
        "name": "Dark",
        "primary": "#121212",
        "secondary": "#1e1e1e",
        "accent": "#2d2d2d",
        "highlight": "#BB86FC",
        "text": "#ffffff",
        "text_secondary": "#aaaaaa",
        "button_text": "#ffffff",
        "success": "#03DAC6",
        "warning": "#FFB74D",
        "danger": "#CF6679",
        "card_bg": "#2d2d2d",
        "border": "#404040",
        "button_bg": "#3700B3",
        "button_fg": "#ffffff",
        "text_background": "#1e1e1e"
    },
    "light": {  # Light mode
        "name": "Light",
        "primary": "#f5f5f5",
        "secondary": "#ffffff",
        "accent": "#e0e0e0",
        "highlight": "#6200EE",
        "text": "#000000",
        "text_secondary": "#666666",
        "button_text": "#ffffff",
        "success": "#00897B",
        "warning": "#FF8F00",
        "danger": "#C62828",
        "card_bg": "#ffffff",
        "border": "#dddddd",
        "button_bg": "#6200EE",
        "button_fg": "#ffffff",
        "text_background": "#ffffff"
    },
    "pinky": {  # Pink theme
        "name": "Pinky",
        "primary": "#2d1b2e",
        "secondary": "#3d2b3f",
        "accent": "#5d3d5f",
        "highlight": "#f06292", 
        "text": "#ffffff",
        "text_secondary": "#e0c3e0",
        "button_text": "#ffffff",
        "success": "#8e24aa",
        "warning": "#ffb6c1",
        "danger": "#d81b60",
        "card_bg": "#4a3b4c",
        "border": "#6d5a6f",
        "button_bg": "#e91e63",
        "button_fg": "#ffffff",
        "text_background": "#3d2b3f"
    },
    "zombie": {  # Zombie Green
        "name": "Zombie Green",
        "primary": "#1b5e20",
        "secondary": "#2e7d32",
        "accent": "#4caf50",
        "highlight": "#c8e6c9", 
        "text": "#ffffff",
        "text_secondary": "#a0d0a0",
        "button_text": "#ffffff", 
        "success": "#32cd32",
        "warning": "#adff2f",
        "danger": "#ff4500",
        "card_bg": "#1e3a1e",
        "border": "#3a5f3a",
        "button_bg": "#66bb6a",
        "button_fg": "#1b5e20",
        "text_background": "#2e7d32"
    }
}

class ZerotierManager:
    def __init__(self, root):
        self.root = root
        self.root.title("OOGR Zerotier-GUI")
        self.root.geometry("750x850")
        
        # Inisialisasi Tema
        self.current_theme_key = "default"
        self.theme = THEMES[self.current_theme_key]
        
        real_user = os.getenv("SUDO_USER") or os.getenv("USER")
        self.config_file = f"/home/{real_user}/.zt_config_v2.json" if real_user != "root" else os.path.expanduser("~/.zt_config_v2.json")
        
        self.saved_data = self.load_data()
        self.setup_ui()
        self.apply_theme() # Terapkan tema saat startup
        self.refresh_status()

    def load_data(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    return data if isinstance(data, dict) else {}
            except: return {}
        return {}

    def save_data(self):
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.saved_data, f)
            real_user = os.getenv("SUDO_USER")
            if real_user:
                subprocess.run(f"chown {real_user}:{real_user} {self.config_file}", shell=True)
        except: pass

    def get_active_networks(self):
        active_ids = []
        try:
            output = subprocess.check_output("zerotier-cli listnetworks", shell=True, text=True)
            for line in output.splitlines():
                parts = line.split()
                if len(parts) > 0 and parts[0] != "200":
                    active_ids.append(parts[0])
        except: pass
        return active_ids

    def run_command(self, cmd, sudo=False):
        if sudo and os.geteuid() != 0:
            cmd = f"pkexec {cmd}"
        try:
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                return stdout.strip() if stdout else "Success"
            else:
                return f"Error: {stderr.strip()}"
        except Exception as e:
            return f"Exception: {str(e)}"

    def change_theme(self, event):
        selected_name = self.theme_combo.get()
        for key, t in THEMES.items():
            if t["name"] == selected_name:
                self.current_theme_key = key
                self.theme = THEMES[key]
                self.apply_theme()
                break

    def apply_theme(self):
        t = self.theme
        self.root.configure(bg=t["primary"])
        self.header_frame.configure(bg=t["highlight"])
        self.header_label.configure(bg=t["highlight"], fg=t["primary"])
        self.main_content.configure(bg=t["primary"])
        self.input_group.configure(bg=t["primary"], fg=t["highlight"])
        self.list_container.configure(bg=t["secondary"])
        self.canvas.configure(bg=t["secondary"])
        self.scrollable_frame.configure(bg=t["secondary"])
        self.control_group.configure(bg=t["primary"], fg=t["highlight"])
        self.status_text.configure(bg=t["text_background"], fg=t["success"])
        self.render_list()

    def setup_ui(self):
        # Header
        self.header_frame = tk.Frame(self.root, height=60)
        self.header_frame.pack(fill=tk.X)
        self.header_label = tk.Label(self.header_frame, text="OOGR ZEROTIER-GUI", font=('Segoe UI', 18, 'bold'))
        self.header_label.pack(side=tk.LEFT, pady=15, padx=25)

        # Dropdown Tema di Pojok Kanan Atas
        theme_names = [t["name"] for t in THEMES.values()]
        self.theme_combo = ttk.Combobox(self.header_frame, values=theme_names, state="readonly", width=18)
        self.theme_combo.set(self.theme["name"])
        self.theme_combo.pack(side=tk.RIGHT, padx=20, pady=20)
        self.theme_combo.bind("<<ComboboxSelected>>", self.change_theme)

        # Main Container
        self.main_content = tk.Frame(self.root, padx=25, pady=20)
        self.main_content.pack(fill=tk.BOTH, expand=True)

        # Input Section
        self.input_group = tk.LabelFrame(self.main_content, text=" Add New Network ", font=('Arial', 10, 'bold'), padx=15, pady=15)
        self.input_group.pack(fill=tk.X, pady=(0, 20))
        
        self.id_entry = tk.Entry(self.input_group, width=25, font=('Monospace', 12), borderwidth=0)
        self.id_entry.pack(side=tk.LEFT, padx=(0, 10), ipady=5)
        
        self.add_btn = tk.Button(self.input_group, text="+ ADD TO LIST", command=self.add_id, font=('Arial', 9, 'bold'), relief=tk.FLAT, padx=15)
        self.add_btn.pack(side=tk.LEFT)

        # List Section
        self.list_container = tk.Frame(self.main_content, bd=0)
        self.list_container.pack(pady=5, fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(self.list_container, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.list_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=650)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # System Controls
        self.control_group = tk.LabelFrame(self.main_content, text=" SYSTEM ENGINE ", font=('Arial', 10, 'bold'), padx=15, pady=15)
        self.control_group.pack(fill=tk.X, pady=20)

        for i in range(3): self.control_group.columnconfigure(i, weight=1)
        self.create_control_buttons()

        # Console Section
        self.status_text = scrolledtext.ScrolledText(self.main_content, height=8, font=('Monospace', 9), borderwidth=0)
        self.status_text.pack(fill=tk.X)

    def create_control_buttons(self):
        for widget in self.control_group.winfo_children():
            widget.destroy()

        t = self.theme
        btns = [
            ("🛡️ FIREWALL ON", lambda: self.toggle_ufw("enable"), t["danger"]),
            ("🔓 FIREWALL OFF", lambda: self.toggle_ufw("disable"), t["danger"]),
            ("🔄 RESTART ZT", self.restart_zt, t["warning"]),
            ("⚡ SERVICE ON", lambda: self.manage_service("start"), t["success"]),
            ("🛑 SERVICE OFF", lambda: self.manage_service("stop"), t["danger"]),
            ("📋 REFRESH", self.refresh_status, t["highlight"])
        ]

        for i, (txt, cmd, clr) in enumerate(btns):
            b = tk.Button(self.control_group, text=txt, command=cmd, bg=clr, fg=t["button_text"], font=('Arial', 8, 'bold'), relief=tk.FLAT, height=2)
            b.grid(row=i//3, column=i%3, sticky="nsew", padx=3, pady=3)

    def render_list(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        active_networks = self.get_active_networks()
        t = self.theme

        for zid, alias in self.saved_data.items():
            is_active = zid in active_networks
            card = tk.Frame(self.scrollable_frame, bg=t["card_bg"], pady=8, padx=10)
            card.pack(fill=tk.X, pady=2, padx=5)
            
            # Status Indicator Dot (Hijau jika aktif, Merah jika tidak)
            dot_color = t["success"] if is_active else t["danger"]
            tk.Label(card, text="●", fg=dot_color, bg=t["card_bg"], font=('Arial', 12)).pack(side=tk.LEFT, padx=(0, 10))
            
            # Network Info
            info_frame = tk.Frame(card, bg=t["card_bg"])
            info_frame.pack(side=tk.LEFT, fill=tk.Y)
            
            tk.Label(info_frame, text=alias if alias else "No Alias", fg=t["text"], bg=t["card_bg"], font=('Arial', 10, 'bold'), anchor='w').pack(fill=tk.X)
            tk.Label(info_frame, text=zid, fg=t["text_secondary"], bg=t["card_bg"], font=('Monospace', 8), anchor='w').pack(fill=tk.X)
            
            # Action Buttons
            btn_opts = {"relief": tk.FLAT, "font": ('Arial', 8, 'bold'), "width": 8, "fg": t["button_text"]}
            
            tk.Button(card, text="DELETE", bg=t["danger"], command=lambda z=zid: self.remove_id(z), **btn_opts).pack(side=tk.RIGHT, padx=2)
            tk.Button(card, text="UNJOIN", bg=t["warning"], command=lambda z=zid: self.action_zt(z, "leave"), **btn_opts).pack(side=tk.RIGHT, padx=2)
            tk.Button(card, text="RENAME", bg=t["accent"], command=lambda z=zid: self.rename_id(z), **btn_opts).pack(side=tk.RIGHT, padx=2)
            
            if not is_active:
                tk.Button(card, text="JOIN", bg=t["success"], command=lambda z=zid: self.action_zt(z, "join"), **btn_opts).pack(side=tk.RIGHT, padx=2)

    def add_id(self):
        zid = self.id_entry.get().strip()
        if len(zid) == 16:
            if zid not in self.saved_data:
                self.saved_data[zid] = ""
                self.save_data()
                self.id_entry.delete(0, tk.END)
                self.refresh_status()
        else:
            messagebox.showerror("Error", "ID must be 16 chars")

    def rename_id(self, zid):
        new_name = simpledialog.askstring("Rename", f"Nama penanda untuk {zid}:", initialvalue=self.saved_data.get(zid, ""))
        if new_name is not None:
            self.saved_data[zid] = new_name
            self.save_data()
            self.render_list()

    def remove_id(self, zid):
        if messagebox.askyesno("Confirm", "Hapus ID ini dari daftar?"):
            del self.saved_data[zid]
            self.save_data()
            self.render_list()

    def action_zt(self, zid, action):
        self.run_command(f"zerotier-cli {action} {zid}", sudo=True)
        self.refresh_status()

    def toggle_ufw(self, action):
        res = self.run_command(f"ufw {action}", sudo=True)
        messagebox.showinfo("UFW Status", res)

    def manage_service(self, action):
        if action == "start":
            self.run_command("systemctl enable zerotier-one", sudo=True)
            self.run_command("systemctl start zerotier-one", sudo=True)
        else:
            self.run_command("systemctl disable zerotier-one", sudo=True)
            self.run_command("systemctl stop zerotier-one", sudo=True)
        self.refresh_status()

    def restart_zt(self):
        self.run_command("systemctl restart zerotier-one", sudo=True)
        self.refresh_status()

    def refresh_status(self):
        self.render_list()
        self.create_control_buttons() # Update warna tombol sistem sesuai tema
        self.status_text.delete('1.0', tk.END)
        srv = self.run_command("systemctl is-active zerotier-one")
        zt_list = self.run_command("zerotier-cli listnetworks")
        ips = self.run_command("hostname -I")
        
        out = f"● SERVICE STATUS: {srv.upper()}\n"
        out += f"● LOCAL IP     : {ips.split()[0] if ips else 'N/A'}\n"
        out += "═" * 50 + "\n"
        out += f"ACTIVE NETWORKS DETAIL:\n{zt_list}"
        self.status_text.insert(tk.END, out)

if __name__ == "__main__":
    root = tk.Tk()
    app = ZerotierManager(root)
    root.mainloop()
