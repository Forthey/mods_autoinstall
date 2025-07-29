# Minecraft Mod Installer

A utility for automatically installing mods in Minecraft using Google Sheets.

---

## Features

- Downloading mods from **Modrinth** and **CurseForge**
- Support for both client and server mods
- Flexible configuration via `config.txt`
- Easy integration with Google Sheets

---

## Preparing the Google Sheet

Create a sheet with mods containing the following columns:

- `client-name` — name of the client mod  
- `client-url` — link to the client mod (Modrinth or CurseForge)  
- `server-name` — name of the server mod  
- `server-url` — link to the server mod  

> Additional columns are allowed but not required.

Your sheet should look something like this:

| client-name      | client-url                            | server-name      | server-url                            |
|------------------|---------------------------------------|------------------|---------------------------------------|
| mode1            | https://modrinth.com/mode1            | mode1            | https://modrinth.com/mode1            |
| client-side-mode | https://modrinth.com/client-side-mode | server-side-mode | https://modrinth.com/server-side-mode |

---

## Configuration

In the `config.txt` file, specify the values of the environment variables:

| Variable               | Description                                   |
|------------------------|-----------------------------------------------|
| `SHEET_ID`             | ID of your Google Sheet                       |
| `CURSEFORGE_API_KEY`   | API key for accessing CurseForge              |
| `MINECRAFT_VERSION`    | Minecraft version                             |
| `MINECRAFT_MOD_LOADER` | Mod loader (e.g., `forge` or `fabric`)        |
| `DOWNLOAD_PATH`        | Path to the folder for downloading mods       |
| `DOWNLOAD_CLIENT`      | Download client mods (`true` / `false`)       |
| `DOWNLOAD_SERVER`      | Download server mods (`true` / `false`)       |

---

## Running

1. Ensure that `config.txt` is filled out correctly.
2. Run the program.
3. Mods will be downloaded to the folders:  
   - `DOWNLOAD_PATH/client`  
   - `DOWNLOAD_PATH/server`
4. In case of an error, rerun the program — it will process the missing mods again.

---

## Building the Project

### Classic Run

```shell
py -m venv venv
venv/Scripts/activate
pip install -r requirements.txt
py source/main.py
```

### Building into an Executable (.exe)

```shell
pyinstaller --onefile source/main.py --add-data config.txt:. --name install_mods --icon icon.ico
```

---

