# Tidebreaker GUI - Autonomous Boat Dashboard

A modular ROS2-based GUI dashboard for monitoring and controlling autonomous boats equipped with ArduPilot flight controllers and VESC motor controllers.

## Features

- **Flight Controller Dashboard**: Displays MAVROS telemetry including:
  - Flight mode, armed status, and connection state
  - Altitude, speed, and climb rate
  - GPS position, heading, and fix quality
  - Orientation (roll, pitch, yaw) from IMU data

- **Motor (VESC) Dashboard**: Displays motor controller data including:
  - Input/output voltage and current
  - Motor speed and duty cycle
  - Temperature readings
  - Energy consumption and regeneration
  - Tachometer (displacement and distance)
  - Fault code status

- **Position Map**: 
  - Interactive map showing current boat position
  - OpenStreetMap-based display with Folium
  - Foundation for future waypoint input

- **Modular Architecture**:
  - Separate UI components for easy extension
  - Data manager for centralized ROS subscriptions
  - Thread-safe data access with callback system

## Package Structure

```
tidebreaker_gui/
├── CMakeLists.txt              # ROS2 build configuration
├── package.xml                 # ROS2 package metadata
├── setup.py                    # Python package setup
├── setup.cfg                   # Python setup configuration
├── resource/
│   └── tidebreaker_gui        # Package resource marker
└── tidebreaker_gui/           # Python package
    ├── __init__.py
    ├── main.py                # Application entry point
    ├── data_manager.py        # ROS2 node for subscriptions
    └── ui/                    # UI components
        ├── __init__.py
        ├── main_window.py     # Main application window
        ├── sidebar.py         # Left sidebar with tabs
        ├── flight_controller_panel.py  # FC data display
        ├── vesc_panel.py      # VESC motor data display
        └── map_widget.py      # Map display with position
```

## Dependencies

### ROS2 Dependencies
- `rclpy` - ROS2 Python client library
- `geometry_msgs` - Geometry message types
- `sensor_msgs` - Sensor message types
- `nav_msgs` - Navigation message types
- `mavros_msgs` - MAVROS message types

### Python Dependencies
- `PyQt6` (>= 6.0) - GUI framework
- `PyQtWebEngine` - Web view for maps
- `folium` (Optional) - Map visualization

## Installation

### Build the package

```bash
cd ~/GitHub/RCCF_PEP_ws
colcon build --packages-select tidebreaker_gui
source install/setup.bash
```

### Install optional dependencies

```bash
# For map functionality (Folium)
pip install folium

# PyQt6 (usually installed as exec_depend in package.xml)
pip install PyQt6 PyQtWebEngine
```

## Running the GUI

### Option 1: Using ROS2 launch (recommended)

Create a launch file or run the node directly:

```bash
ros2 run tidebreaker_gui tidebreaker_gui
```

### Option 2: Direct Python execution

```bash
ros2 run tidebreaker_gui tidebreaker_gui
# or
python3 -m tidebreaker_gui.main
```

## ROS Topics

The GUI subscribes to the following topics:

### Flight Controller (MAVROS)
- `/mavros/state` - Flight mode, armed status, connected status
- `/mavros/vfr_hud` - Altitude, speed, climb rate, heading, throttle
- `/mavros/global_position/global` - GPS position and fix quality
- `/mavros/imu/data` - Orientation (IMU quaternion)
- `/mavros/rc/in` - RC input channels
- `/mavros/rc/out` - RC output channels

### Motor (VESC)
- `/vesc/sensors/core` - Motor state (will be configured to match your VESC ROS driver)

**Note**: Topic names may need adjustment based on your specific MAVROS and VESC configuration.

## Extending the GUI

### Adding a New Data Panel

1. Create a new widget class in `ui/` (e.g., `battery_panel.py`):

```python
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import pyqtSignal, QObject

class DataUpdateSignals(QObject):
    updated = pyqtSignal()

class BatteryPanel(QWidget):
    def __init__(self, data_manager):
        super().__init__()
        self.data_manager = data_manager
        self.signals = DataUpdateSignals()
        self.signals.updated.connect(self.update_display)
        
        # Register callback
        self.data_manager.register_callback('battery_data', self._on_data_update)
        
        self._init_ui()
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        # Add your widgets here
    
    def _on_data_update(self):
        self.signals.updated.emit()
    
    def update_display(self):
        # Update UI with latest data
        pass
```

2. Add the new panel to the `Sidebar` class in `ui/sidebar.py`:

```python
from .battery_panel import BatteryPanel

# In Sidebar._init_ui():
battery_panel = BatteryPanel(self.data_manager)
tabs.addTab(battery_panel, "Battery")
```

3. Update the `DataManager` class in `data_manager.py` to subscribe to new ROS topics:

```python
# Add in __init__
self.create_subscription(
    BatteryState,  # Your message type
    '/battery/state',  # Your topic
    self._battery_callback,
    10,
    callback_group=callback_group
)

# Add callback method
def _battery_callback(self, msg):
    with self._data_lock:
        self._battery_state = msg
    self._trigger_callbacks('battery_data')

# Add getter method
def get_battery_state(self):
    with self._data_lock:
        return self._battery_state
```

### Modifying Existing Panels

All panels are self-contained in their own files, making them easy to modify without affecting other components. Update the `_init_ui()` method to add/remove widgets and the `update_display()` method to change how data is presented.

## Contributing

When adding new features:

1. Keep components modular and self-contained
2. Use the `DataManager` callback system for updates
3. Follow the existing UI patterns for consistency
4. Add docstrings to all public methods
5. Test with actual MAVROS and VESC topics

## Troubleshooting

### GUI doesn't start
- Ensure ROS2 is properly sourced: `source /opt/ros/<distro>/setup.bash`
- Check that the GUI package is built: `colcon build --packages-select tidebreaker_gui`

### No data being displayed
- Verify MAVROS/VESC nodes are running and publishing data
- Check topic names match your configuration (use `ros2 topic list`)
- Check GUI node can subscribe (use `ros2 node info /tidebreaker_gui_data_manager`)

### Map not displaying
- Install folium: `pip install folium`
- Check internet connection (map uses OpenStreetMap)

## License

Apache-2.0

## Author

Matthew - Tidebreaker Project
