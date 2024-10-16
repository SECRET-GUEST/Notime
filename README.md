
```
███╗   ██╗ ██████╗     ████████╗██╗███╗   ███╗███████╗
████╗  ██║██╔═══██╗    ╚══██╔══╝██║████╗ ████║██╔════╝
██╔██╗ ██║██║   ██║       ██║   ██║██╔████╔██║█████╗  
██║╚██╗██║██║   ██║       ██║   ██║██║╚██╔╝██║██╔══╝  
██║ ╚████║╚██████╔╝       ██║   ██║██║ ╚═╝ ██║███████╗
╚═╝  ╚═══╝ ╚═════╝        ╚═╝   ╚═╝╚═╝     ╚═╝╚══════╝
```
![PYTHON](https://img.shields.io/badge/Python-3.10+-blue)
![BETA](https://img.shields.io/badge/VERSION-BETA-orange)
![WINDOWS](https://img.shields.io/badge/Windows-blue)

# Notime ⏰

Notime is a productivity application designed to enhance your focus by managing work and break cycles with synchronized animations and sounds.

---

## 📋 Table of Contents

1. [Features](#-features)
2. [Prerequisites](#-prerequisites)
3. [To Do](#%EF%B8%8F-todo)
4. [News](#news)
5. [Usage](#-usage)
6. [License](#-license)
7. [Support & Questions](#-support--questions)
8. [Recommendations](#-recommendations)
9. [Installation](#-installation)

## 🌟 Features

- **Work & Break Cycles**: Automatically manages 45-minute work sessions followed by alternating 10 and 20-minute breaks.
- **Full-Screen Animations**: Displays engaging animations to signal the start and end of cycles.
- **Audio Notifications**: Plays sounds synchronized with animations to grab your attention.
- **System Tray Icon**: Minimizes to the system tray with a context menu for quick access.
- **Customizable Settings**: Options to disable sounds or animations according to your preference.
- **Background Operation**: Runs silently in the background without interrupting your workflow.

## 🔍 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.10** or higher
- **PySide6** library
- **Windows OS**

## 🛠️ To Do

1. **Multi-language Support**: Implement localization for different languages.
2. **Customizable Timers**: Allow users to set custom durations for work and break periods.
3. **Cross-Platform Compatibility**: Extend support to macOS and Linux systems.
4. **Notification Enhancements**: Add desktop notifications in addition to animations and sounds.
5. **Pause/Resume Functionality**: Enable users to pause or resume the timer as needed.

## News

- 🗞️ **Upcoming Update**: Version 1.0.0 will include customizable timer settings and improved user interface.

## 💡 Usage

- **Launching the Application**: Run `notime.exe` or execute `python notime.py` if running from source.
- **System Tray Menu**:
  - Right-click the Notime icon in the system tray to access options.
  - **Disable Sound**: Toggle audio notifications.
  - **Disable Animation**: Toggle full-screen animations.
  - **Quit**: Exit the application.
- **Cycle Notifications**:
  - **Work Cycle**: Starts with a "counter" animation and sound.
  - **Break Cycle**: Signaled by an "over" animation and sound.
- **Default Cycle Durations**:
  - **Work**: 45 minutes
  - **Breaks**: Alternates between 10 and 20 minutes

## 📜 License

This repository is released under the [MIT License](LICENSE). Please see the `LICENSE` file for more information.

## ❓ Support & Questions

If you have any questions or need support, please feel free to open an issue or start a new discussion. You can also reach out via Twitter.

## 💎 Recommendations

In your quest for more tools to enhance your desktop productivity, these additional repositories are worth a look:

- [Barcraft](https://github.com/SECRET-GUEST/barcraft): Create barcodes/QRCodes using an application free from malware, sourced directly from GitHub.

Looking for more? Discover user-friendly, GUI-free scripts here:

- [Tiny Scripts](https://github.com/SECRET-GUEST/tiny-scripts)

If you're a 3D animator, consider:

- [Animation](https://github.com/SECRET-GUEST/animation)

## 🛠 Installation

```
██   ██  ██████  ██     ██     ████████  ██████      ██████  ██    ██ ███    ██ 
██   ██ ██    ██ ██     ██        ██    ██    ██     ██   ██ ██    ██ ████   ██ 
███████ ██    ██ ██  █  ██        ██    ██    ██     ██████  ██    ██ ██ ██  ██ 
██   ██ ██    ██ ██ ███ ██        ██    ██    ██     ██   ██ ██    ██ ██  ██ ██ 
██   ██  ██████   ███ ███         ██     ██████      ██   ██  ██████  ██   ████ 
```

Here's a tutorial explaining different ways to run the files:

# For **MAC** & **Linux** users:

Since this script is designed for Windows users, you should probably first improve the code.

However, here is the procedure to run the script:

* :computer:: [MAC] - https://macosx-faq.com/how-to-run-python-script/
* :keyboard: [LINUX] - open a terminal, then `cd` to the script's directory and type:

```
python script.pyw

```
(where `script.pyw` is obviously the name of the file you've downloaded)

# :desktop_computer: For **Microsoft** users:

Most of the time you can find an MSI installer in [source forge](https://sourceforge.net/u/secret-guest/profile), or in latest relase here, but if you don't you can still watch this tutorial.

Because this script is made by PyInstaller, it could be detected as malware. (sorry, but I will not spend money to just be approved by "security" software/websites, you have the code, and here are possibilities to help you run it:

## :large_orange_diamond: 1. Run by simple click on `APPLICATION.exe`

The `.exe` file is a portable version created for Microsoft users with PyInstaller, allowing you to download and use this file alone, without any additional files.

If there is no `.exe` file available, it means that the application is stored in a directory, as a portable version is not provided. In this case, simply locate the `APP_NAME.exe` file within the directory and launch it with a single click. You can place the folder anywhere you like and create a shortcut to the executable file for easy access.

## :large_orange_diamond: 2. Run with Python

`Python script` is a directory with the original script for python 3.11.

In case you have a lower version, you may have to download module imported not included with your version. Just read the first lines of the script in Alexandria with a notepad or whatever to find what's missing.

If you would like to run with python **YOU WILL NEED THE IMAGE .png PLACED IN THE SAME DIRECTORY OF THE RUNNING SCRIPT**.

Also, you can add a `w` to the extension (like `script.pyw`). It means `windowed mode`, to launch the python script without the CMD, but it's still a common python file.

## :large_orange_diamond: 3. Compile the script by yourself

### :gear: Instructions :gear: 

To create your own executable from the python file, you will need to install pyinstaller and python.

Here are the steps you should follow:

   :small_red_triangle: Download python 3.11.1 

Don't forget to add it to your path with the installer or in variables environment (so reboot your PC after the installation), here is the link: 

:crossed_flags: https://www.python.org/ftp/python/3.11.1/python-3.11.1-amd64.exe :crossed_flags:

:small_red_triangle: Open your CMD as an administrator and type the following command:

```
python -m pip install pyinstaller
```

:small_red_triangle: You can now run it using a ruby `.spec` file by entering the following command in the project directory:

```bash
pyinstaller YOUR_FILE.spec
```
Normally, I place a blank.spec file in the "script" folder, if there isn't one let's watch over here:

:crossed_flags: [HOW TO MAKE AN EXECUTABLE FAST](https://github.com/SECRET-GUEST/tiny-scripts/tree/ALL/python/INSTALLER) :crossed_flags:

:small_red_triangle: You can also run it directly with your OS, type the following command, replacing the file paths with your own:

```
pyinstaller --onefile --icon="...YOUR PATH.../YOUR ICON.ico" --add-data "...YOUR PATH.../ico;ico" --noconsole test.py
```
#### Here are the explanations of the different options:



- `--onefile`: creates a single executable that includes all dependencies.

- `--icon=icon.ico`: specifies the icon to use for the executable (replace icon.ico with the path to your icon file).

- `--add-data "path/to/file;folder_name"`: adds external files required by the program. The path to the file and the name of the folder in which the file will be extracted should be separated by a semicolon `;`. You can add multiple files by separating them with semicolons.

- `script.py`: specifies the name of your Python script.

- `--noconsole`: hides the console when the executable is run.



Make sure to replace the snipped parts with the names of your files and folders. Also note that the path should be specified based on the operating system you are working on.

After running this command, you should have a single executable that includes all dependencies, external files, and a custom icon, and does not show the console when running.

Alternatively, you can also :

## :large_orange_diamond: 4. Create a batch file to run

- [ ] Create a text file

- [ ] In the text file type and write (and change/complete the path, first is for python, 2nd is for script.py):

```
C:\YOUR PATH TO PYTHON\python.exe" "C:\**YOUR PATH TO THE SCRIPT**\script.pyw"
```


If Python is in the path, you can just:

```
python "C:\**YOUR PATH TO THE SCRIPT**\script.pyw"
```

- [ ] Rename the `new_file.txt` to `script.bat` then just click on it, and it will run the program


```
     _ ._  _ , _ ._            _ ._  _ , _ ._    _ ._  _ , _ ._      _ ._  _ , _ .__  _ , _ ._   ._  _ , _ ._   _ , _ ._   .---.  _ ._   _ , _ .__  _ , _ ._   ._  _ , _ ._      _ ._  _ , _ .__  _ , _ . .---<__. \ _
   (_ ' ( `  )_  .__)        (_ ' ( `  )_  .__ (_ ' ( `  )_  .__)  (_ '    ___   ._( `  )_  .__)  ( `  )_  .__)   )_  .__)/     \(_ ' (    )_  ._( `  )_  .__)  ( `  )_  .__)  (_ ' ( `  )_  ._( `` )_  . `---._  \ \ \
 ( (  (    )   `)  ) _)    ( (  (    )   `)  ) (  (    )   `)  ) _ (  (   (o o) )     )   `)  ) _    )   `)  ) _    `)  ) \.@-@./(  (    )   `)     )   `)  ) _    )   `)  ) _ (  (    )   `)         `) ` ),----`- `.))  
(__ (_   (_ . _) _) ,__)  (__ (_   (_ . _) _) _ (_   (_ . _) _) ,__ (_   (  V  ) _) (_ . _) _) ,_  (_ . _) _) ,_ . _) _) ,/`\_/`\ (_   (  . _) _) (_ . _) _) ,_  (_ . _) _) ,__ (_   (_ . _) _) (__. _) _)/ ,--.   )  |
    `~~`\ ' . /`~~`           `~~`\ ' . /`~~`   `~~`\ ' . /`~~`     `~~`/--m-m- ~~`\ ' . /`~~`   `\ ' . /`~~`  `\ ' . /  //  _  \\ ``\ '  . /`~~`\ ' . /`~~`   `\ ' . /`~~`     `~~`\ ' . /`~~`\ ' . /`~~/_/    >     |
         ;   ;                     ;   ;             ;   ;               ;   ;      ;   ;          ;   ;         ;   ;  | \     )|_   ;    ;      ;   ;          ;   ;               ;   ;      ;   ;    |,\__-'      |
         /   \                     /   \             /   \               /   \      /   \          /   \         /   \ /`\_`>  <_/ \  /    \      /   \          /   \               /   \      /   \     \__         \
________/_ __ \___________________/_ __ \___________/_ __ \______ __ ___/_ __ \____/_ __ \________/_ __ \_______/_ __ \\__/'---'\__/_/_  __ \____/_ __ \________/_ __ \_____ _______/_ __ \____/_ __ \____ __\___      )
```
