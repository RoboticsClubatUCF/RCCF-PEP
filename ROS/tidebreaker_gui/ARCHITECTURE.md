# Tidebreaker GUI - Architecture & Design

## Overview

The Tidebreaker GUI is a modular ROS2-based dashboard application built with PyQt6. It provides real-time monitoring of flight controller (MAVROS) and motor (VESC) data with an extensible architecture for adding new features.

## Design Principles

1. **Modularity**: Each UI component is self-contained and independent
2. **Thread Safety**: All ROS data access is protected with locks
3. **Scalability**: Easy to add new data displays without modifying existing code
4. **Separation of Concerns**: Data management is separate from UI
5. **Signal-Based Updates**: PyQt signals ensure UI updates happen on the main thread

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     PyQt6 Application                        │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────┐      ┌──────────────────────────┐  │
│  │   Main Window        │      │   Sidebar (Left Panel)    │  │
│  │  ┌────────────────┐  │      │  ┌────────────────────┐   │  │
│  │  │  Layout:       │  │      │  │  Tab1: FlightCtl   │   │  │
│  │  │  ┌──────────┐  │  │      │  │  - Status          │   │  │
│  │  │  │ Sidebar  │  │  │      │  │  - Altitude/Speed  │   │  │
│  │  │  ├──────────┤  │  │      │  │  - Position        │   │  │
│  │  │  │ Map      │  │  │      │  │  - Orientation     │   │  │
│  │  │  └──────────┘  │  │      │  │                    │   │  │
│  │  └────────────────┘  │      │  ├────────────────────┤   │  │
│  └──────────────────────┘      │  │  Tab2: Motor/VESC  │   │  │
│                                │  │  - Power (V, I)    │   │  │
│                                │  │  - Performance     │   │  │
│  ┌──────────────────────────┐  │  │  - Temperature     │   │  │
│  │   Map Widget            │  │  │  - Energy          │   │  │
│  │  ┌────────────────────┐  │  │  │  - Status          │   │  │
│  │  │ Folium Map Display │  │  │  └────────────────────┘   │  │
│  │  │ (OpenStreetMap)    │  │  └──────────────────────────┘  │
│  │  └────────────────────┘  │                                │
│  └──────────────────────────┘                                │
└─────────────────────────────────────────────────────────────┘
          │
          │ Uses
          ▼
┌─────────────────────────────────────────────────────────────┐
│              Data Manager (ROS2 Node)                        │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Thread-Safe Data Storage:                                   │
│  ├── FC State (MAVROS)         ← /mavros/state              │
│  ├── FC VFR HUD                ← /mavros/vfr_hud            │
│  ├── FC GPS                    ← /mavros/global_position   │
│  ├── FC IMU                    ← /mavros/imu/data           │
│  ├── FC RC Input               ← /mavros/rc/in              │
│  ├── FC RC Output              ← /mavros/rc/out             │
│  └── VESC State                ← /vesc/sensors/core         │
│                                                               │
│  Callback Registry:                                          │
│  ├── 'fc_state'        → [callbacks]                         │
│  ├── 'fc_vfr_hud'      → [callbacks]                         │
│  ├── 'fc_gps'          → [callbacks]                         │
│  ├── 'fc_imu'          → [callbacks]                         │
│  └── 'vesc_state'      → [callbacks]                         │
└─────────────────────────────────────────────────────────────┘
          │
          │ Subscribes to ROS Topics
          │ (in separate executor thread)
          ▼
┌─────────────────────────────────────────────────────────────┐
│     ROS2 Network (MAVROS, VESC Drivers, Other Nodes)        │
└─────────────────────────────────────────────────────────────┘
```

## Component Hierarchy

```
tidebreaker_gui/
│
├── main.py
│   └── Initializes ROS2, creates DataManager and MainWindow
│       └── Spins ROS2 executor in separate thread
│
├── data_manager.py
│   └── ROS2 Node that subscribes to all topics
│       ├── Thread-safe data storage (with locks)
│       └── Callback registry for event-driven updates
│
└── ui/
    ├── main_window.py
    │   └── Top-level window (QMainWindow)
    │       ├── Sidebar (left)
    │       └── Map Widget (right)
    │
    ├── sidebar.py
    │   └── Tabbed interface container
    │       ├── FlightControllerPanel
    │       └── VescPanel
    │
    ├── flight_controller_panel.py
    │   └── Displays MAVROS telemetry
    │       ├── Status group
    │       ├── Altitude & Speed group
    │       ├── Position group
    │       └── Orientation (IMU) group
    │
    ├── vesc_panel.py
    │   └── Displays VESC motor data
    │       ├── Power group
    │       ├── Performance group
    │       ├── Temperature group
    │       ├── Energy group
    │       ├── Tachometer group
    │       └── Status group
    │
    ├── map_widget.py
    │   └── Displays position map
    │       ├── Folium-based interactive map
    │       └── Real-time position updates
    │
    └── CUSTOM_COMPONENT_TEMPLATE.py
        └── Template for new panels (not used directly)
```

## Data Flow

### ROS → GUI Flow

```
ROS Topic Publication
         │
         ▼
ROS2 Subscription Callback
(in data_manager.py)
         │
         ├─→ Acquire Lock
         ├─→ Update Data
         ├─→ Release Lock
         │
         └─→ Trigger Callback
             (on main thread via signals)
                │
                ▼
            UI Panel Update Slot
            (update_display())
                │
                ├─→ Get Data from Manager
                │   (with lock protection)
                │
                └─→ Update UI Labels/Values
```

### Thread Management

```
Main Thread (Qt Event Loop)
├── UI Rendering
├── User Input Handling
├── Timer-based refresh (1Hz)
└── Callback emission

ROS Executor Thread
├── ROS Subscription Processing
├── ROS Message Callbacks
└── Data Manager Updates
    (via thread-safe locks)

Communication: Qt Signals
(Safe cross-thread communication)
```

## Key Design Patterns

### 1. Observer Pattern (Callbacks)

The DataManager uses a callback registry to notify UI panels of updates:

```python
# Registration
data_manager.register_callback('fc_state', panel.update_display)

# Trigger
data_manager._trigger_callbacks('fc_state')

# Callback executed
panel.update_display()
```

### 2. Thread-Safe Data Access

All shared data uses locks to prevent race conditions:

```python
with self._data_lock:
    self._fc_state = msg  # Write
    
with self._data_lock:
    return self._fc_state.copy()  # Read
```

### 3. Signal-Based UI Updates

PyQt signals ensure UI updates happen on the main thread:

```python
# In Worker Thread
callback()  # Called from ROS thread
  └─> signals.updated.emit()  # Signal crosses thread boundary

# In Main Thread
signals.updated.connect(self.update_display)
  └─> update_display()  # Runs on main thread
```

## Extension Points

### Adding a New Data Panel

1. **Create UI Component**: `tidebreaker_gui/ui/my_panel.py`
   - Inherit from QWidget
   - Implement `__init__()`, `_init_ui()`, `update_display()`
   - Register callbacks with data_manager

2. **Add ROS Subscription**: `tidebreaker_gui/data_manager.py`
   - Add `self.create_subscription()` call
   - Add callback method `_my_callback()`
   - Add getter method `get_my_data()`

3. **Integrate into Sidebar**: `tidebreaker_gui/ui/sidebar.py`
   - Import new panel
   - Create instance and add to tabs

### Adding a New ROS Topic

1. Update `data_manager.py`:
   ```python
   # In __init__
   self.create_subscription(MyMsgType, '/topic', self._callback, 10)
   
   # Add callback and getter
   def _callback(self, msg): ...
   def get_data(self): ...
   ```

2. Update UI panels to call getter and display data

3. Register callbacks for event-driven updates

## Performance Considerations

- **Update Frequency**: 1 Hz (configurable in `main_window.py`)
- **Thread Count**: 2 (Main Qt thread + ROS executor thread)
- **Lock Overhead**: Minimal (only brief locks during updates)
- **Memory**: Depends on ROS message history (typically < 50 MB)
- **CPU**: Typically < 5% on modern systems when idle

## Future Enhancements

1. **Dynamic Topic Configuration**: Load topic names from config file
2. **Waypoint Support**: Click on map to add/edit waypoints
3. **Data Logging**: Record telemetry to CSV/ROS bag
4. **Graph Plotting**: Time-series plots for trend analysis
5. **Alarm System**: Alerts for critical values
6. **Mission Planning**: Integrated mission editor
7. **Custom Themes**: Dark mode, high contrast options

## Testing

### Unit Testing Approach

1. Mock ROS messages in tests
2. Test DataManager isolation from Qt
3. Test UI panels with mock data manager
4. Integration tests with actual ROS topics

### Example Test

```python
def test_fc_panel_updates():
    # Create mock data manager
    mock_manager = MagicMock()
    mock_manager.get_fc_state.return_value = State(
        armed=True, connected=True, mode="GUIDED"
    )
    
    # Create panel
    panel = FlightControllerPanel(mock_manager)
    panel.update_display()
    
    # Assert UI updated
    assert "GUIDED" in panel.flight_mode_label.text()
```

## Deployment

### Package Structure for Distribution

```
tidebreaker_gui-0.0.1/
├── tidebreaker_gui/      # Python package
├── launch/               # ROS launch files
├── config/               # Configuration files
├── CMakeLists.txt
├── package.xml
├── setup.py
├── README.md
├── QUICKSTART.md
└── CHANGELOG.md
```

### Installation Methods

1. **Source Build**: `colcon build`
2. **Binary Package**: `apt install ros-humble-tidebreaker-gui`
3. **Docker Image**: Pre-configured with all dependencies

---

**Author**: Matthew - Tidebreaker Project  
**License**: Apache-2.0  
**Version**: 0.0.1 (Beta)
