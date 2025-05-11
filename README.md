# Quantic MSSE - Easy Park Plus
This repo contains the project for Quantic's MSSE Software Design & Architecture Project.

## Technologies & Dependencies
- Python 3 (latest recommended)
- Tkinter (Python standard GUI library)

## Installing Dependencies

### Python 3
Ensure you have Python 3 installed:
```sh
python3 --version
```
If not, install it from [python.org](https://www.python.org/downloads/) or using Homebrew:
```sh
brew install python
```

### Tkinter
Tkinter is included with most Python installations, but some (like Homebrew Python on macOS) may not include it by default.

#### To check if Tkinter is installed:
```sh
python3 -m tkinter
```
If a small window appears, Tkinter is installed. If you get an error, install it as follows:

#### On macOS (Homebrew Python):
```sh
brew install python-tk
```
Or reinstall Python with Tk support:
```sh
brew reinstall python
```

Alternatively, use the system Python, which usually includes Tkinter:
```sh
/usr/bin/python3 -m tkinter
```

## Running the Application

1. Open a terminal and navigate to the project root directory.
2. Run the following command:
```sh
python3 src/ParkingManager.py
```

If you encounter import errors, try running:
```sh
python3 -m src.ParkingManager
```

The application will launch a graphical user interface (GUI) for managing the parking lot.

## Troubleshooting
- If you see `ModuleNotFoundError: No module named '_tkinter'`, follow the Tkinter installation steps above.
- Ensure you are using Python 3, not Python 2.
