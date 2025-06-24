# Desktop Overlay

## Overview

**Desktop Overlay** is a modular, open-source overlay for your desktop, built with Python and PySide6. It lets you extend your desktop with custom mods, such as a web browser, Spotify integration, and a notes widget. The project is designed for easy extensibility—create and add your own mods with minimal effort.

**Alpha version highlights:**
- Persistent GUI overlay with mod dock and settings panel
- Built-in web browser mod
- Spotify now-playing mod
- Notes mod

---

## Installation

### Prerequisites

- Python 3.9+
- [pip](https://pip.pypa.io/en/stable/)
- [poetry](https://python-poetry.org/)

### Getting Started

1. **Clone the repository:**
    ```sh
    git clone https://github.com/Kyloof/desktop_overlay
    cd desktop_overlay
    ```
2. **Install dependencies:**
- On Linux and MacOS:
    - From Script
        ```
        pip install -e .
        ```
    - From Binary
        ```
        ./build.sh
        ```

3. **Run the application:**
- From Script    
    ```sh
    desktop-overlay
    ```
- From Binary
    ```sh
    ./dist/main/main
    ```

### Spotify Integration

To enable Spotify features, create a `.env` file in the project root with your Spotify API credentials:
```env
CLIENT_ID="<your_spotify_client_id>"
CLIENT_SECRET="<your_spotify_client_secret>"
REDIRECT_URI="<your_redirect_uri>"
```
Replace the placeholders with values from your [Spotify developer dashboard](https://developer.spotify.com/dashboard).



## Usage

- The overlay stays on top of your desktop and can be toggled with a customizable hotkey (default: `Ctrl + 0`).
- Use the settings menu (left panel) to change the overlay shortcut or select the display.
- Mods appear in the bottom dock; click an icon to open a mod window.
- The system tray icon lets you open or quit the overlay.

## Project Structure

```text
desktop_overlay/
├── src/
│   └── desktop_overlay/
│       ├── core/         # Core logic: mod manager, hotkey manager, settings manager
│       ├── mods/         # Built-in mods (web, spotify, notes)
│       ├── ui/           # UI components and themes
│       ├── definitions.py
│       ├── main.py       # Entry point
│       └── ...
├── tests/                # Unit tests
├── pyproject.toml
├── README.md
└── .env                  # Spotify credentials (not tracked by git)
```

## Creating Your Own Mod

1. Create a new folder in `src/desktop_overlay/mods/your_mod_name_mod/`.
2. Implement a class that inherits from [`BaseMod`](src/desktop_overlay/core/base_mod.py).
3. Add your assets (icons, images) in your mod's `assets/` folder.
4. Restart the overlay; your mod will be auto-detected and available.

## Running Tests

```sh
pytest
```

## Authors

- Jan Kubów
- Dawid Wyskwarski