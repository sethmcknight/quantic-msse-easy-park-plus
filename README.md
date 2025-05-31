# Quantic MSSE - Easy Park Plus

This repository contains the Software Design & Architecture project for Quantic's MSSE program. The project demonstrates comprehensive refactoring of a parking lot management system, implementing multiple design patterns and following domain-driven design principles.

## Project Overview

Easy Park Plus is a parking lot management system that has been extensively refactored to demonstrate:

- **Design Pattern Implementation**: Observer, Factory, Strategy, and Manager patterns
- **Anti-Pattern Removal**: Comprehensive code quality improvements
- **Domain-Driven Design**: Bounded contexts and domain modeling
- **Microservices Architecture**: Scalable system design for future expansion

### Key Features

- **Parking Space Management**: Add, remove, and monitor parking spaces
- **Vehicle Management**: Support for different vehicle types with factory pattern
- **Real-time Notifications**: Observer pattern for parking lot status updates
- **Flexible Search**: Strategy pattern for different search algorithms
- **Clean Architecture**: Separation of concerns with manager pattern
- **Elecric Vehicle Charging Support**: Future-ready architecture for electric vehicle charging stations

## Technologies & Dependencies

- **Python 3** (3.8+ recommended)
- **Tkinter** (Python standard GUI library)

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

1. Open a terminal and navigate to the project root directory:

```sh
cd /Users/sethmcknight/Developer/quantic-msse-easy-park-plus
```

2. Run the application:

```sh
python3 src/ParkingManager.py
```

If you encounter import errors, try running from the project root:

```sh
python3 -m src.ParkingManager
```

The application will launch a graphical user interface (GUI) for managing the parking lot.

## Project Structure

```
src/
├── ParkingManager.py          # Main application entry point
├── business_logic/            # Core business logic
│   ├── ParkingLotManager.py   # Manager pattern implementation
│   └── observers/             # Observer pattern components
├── models/                    # Domain models
│   ├── Vehicle.py             # Vehicle entities and factory
│   ├── ParkingSpace.py        # Parking space model
│   └── strategies/            # Strategy pattern implementations
├── ui/                        # User interface components
│   └── ParkingLotUI.py        # Refactored GUI with improved naming
└── utils/                     # Utility classes and helpers
```

## Design Patterns Implemented

### 1. Observer Pattern

- **Location**: `business_logic/observers/`
- **Purpose**: Real-time notifications for parking lot status changes
- **Benefit**: Loose coupling between UI and business logic

### 2. Factory Pattern

- **Location**: `models/Vehicle.py`
- **Purpose**: Vehicle creation with type-specific behavior
- **Benefit**: Extensible vehicle type system

### 3. Strategy Pattern

- **Location**: `models/strategies/`
- **Purpose**: Pluggable search algorithms for parking spaces
- **Benefit**: Flexible and testable search functionality

### 4. Manager Pattern

- **Location**: `business_logic/ParkingLotManager.py`
- **Purpose**: Centralized business logic coordination
- **Benefit**: Clear separation of concerns and improved maintainability

## Code Quality Improvements

The codebase has been extensively refactored to address anti-patterns:

- ✅ **Improved Variable Naming**: Descriptive, consistent naming throughout
- ✅ **Eliminated Dead Code**: Removed unused methods and variables
- ✅ **Enhanced Error Handling**: Proper exception handling and validation
- ✅ **Code Organization**: Logical structure with clear responsibilities
- ✅ **Documentation**: Comprehensive comments explaining design decisions

## Documentation

The project includes comprehensive documentation:

- **UML Diagrams**: Original and redesigned system architecture
- **Domain Models**: DDD-based entity and aggregate design
- **Microservices Architecture**: Scalable system design for future expansion
- **Pattern Justification**: Detailed explanations of design decisions

## Future Architecture

The system is designed with a microservices architecture to support:

- **Parking Management Service**: Core parking operations
- **EV Charging Service**: Electric vehicle charging station management
- **User Management Service**: Customer and authentication management
- **Payment Service**: Transaction and billing management
- **Notification Service**: Real-time alerts and communications

## Testing

To verify the application functionality:

1. Launch the application as described above
2. Test core features:
   - Add/remove parking spaces
   - Register different vehicle types
   - Search for available spaces
   - Monitor real-time status updates

## Troubleshooting

### Common Issues

**ModuleNotFoundError: No module named '\_tkinter'**

- Follow the Tkinter installation steps above
- Ensure you're using Python 3, not Python 2

**Import Errors**

- Ensure you're running from the correct directory
- Try using `python3 -m src.ParkingManager` instead

**GUI Not Appearing**

- Check if you're running in a headless environment
- Ensure X11 forwarding is enabled if using SSH

**Performance Issues**

- The refactored code should perform better than the original
- If issues persist, check system resources and Python version

## Development

For developers working on this project:

1. Follow the established patterns when adding new features
2. Maintain the separation of concerns established by the manager pattern
3. Use the factory pattern for new vehicle types
4. Implement observer pattern for new notification requirements
5. Consider strategy pattern for new algorithms

## License

This project is for educational purposes as part of the Quantic MSSE program.
