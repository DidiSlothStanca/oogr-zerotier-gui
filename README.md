# OOGR ZeroTier-GUI
OOGR ZeroTier-GUI is a Python-based graphical user interface (GUI) using Tkinter to manage ZeroTier connections on Linux with style and ease.
## ✨ Key Features
- **Multi-Theme System**: Choose your favorite theme (Default, Dark, Light, Pinky, Zombie Green) instantly via the dropdown menu.
- **Smart Join/Unjoin**: Dedicated buttons to join or leave ZeroTier networks easily.
- **Dynamic Status Indicator**: A status dot that turns **Green** when connected and **Red** when disconnected.
- **System Engine Control**: One-click Firewall (UFW) management, ZeroTier service toggle, and service restart.
- **Network Registry**: Save your Network IDs with custom aliases for quick identification.
- **Live Console**: Monitor detailed output from `zerotier-cli` in real-time through the built-in console.

## 🛠️ Prerequisites
Ensure your system has the following installed:
- Python 3
- ZeroTier One (`zerotier-cli`)
- `policykit-1` (required for `pkexec` to handle sudo commands)

## 🚀 How to Use
1. Clone this repository:
   ```bash
   $ git clone [https://github.com/username/oogr-zerotier-gui.git](https://github.com/username/oogr-zerotier-gui.git)
   ```
2. Extract to home
   ```bash
   $ tar -xf oogr-zerotier-gui.tar.gz ~/.
   ```
3. Open folder using terminal
   ```bash
   $ cd ~/oogr-zerotier-gui/
   ```
4. Launch Zerotier-GUI (make sure using sudo)
   ```bash
   $ sudo ./launch.sh
   ```
5. Done! you can manage Zerotier-CLI using GUI Mode
