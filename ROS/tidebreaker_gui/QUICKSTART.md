# Tidebreaker GUI - Quick Start Guide

This guide will help you get the Tidebreaker GUI up and running quickly.

## Prerequisites

- ROS2 installed and sourced
- MAVROS running and publishing flight controller data
- VESC ROS driver running (optional, but recommended)
- Python 3.8 or later

## Step 1: Install Dependencies

```bash
# Install PyQt6 and required packages
pip install PyQt6 PyQtWebEngine PyQtWebEngine

# Install optional map dependencies
pip install folium
```

## Step 2: Build the Package

```bash
# Navigate to your ROS workspace
cd ~/GitHub/RCCF_PEP_ws

# Build the tidebreaker_gui package
colcon build --packages-select tidebreaker_gui

# Source the install setup script
source install/setup.bash
```

## Step 3: Launch the GUI

### Method 1: Using ROS2 Launch File (Recommended)

```bash
# Make sure other ROS2 nodes are running (MAVROS, VESC driver, etc.)

# In a new terminal:
ros2 launch tidebreaker_gui tidebreaker_gui.launch.py
```

### Method 2: Direct Command

```bash
ros2 run tidebreaker_gui tidebreaker_gui
```

## Step 4: Verify Data Display

Once the GUI opens:

1. **Check Flight Controller Tab**:
   - You should see flight mode, armed status, and connection state
   - If connected to MAVROS, altitude/speed/GPS data should appear

2. **Check Motor Tab**:
   - If your VESC driver is running, motor data should display
   - You should see voltage, current, speed, and temperature readings

3. **Check Map Tab**:
   - The map should show your boat's GPS position
   - Default position shown if GPS is not available yet

## Troubleshooting

### GUI shows "Disconnected" for Flight Controller

**Solution**: Ensure MAVROS is running:

```bash
# In a new terminal, run MAVROS
ros2 launch mavros apm.launch.py tgt_system:=1
```

### No motor data showing in VESC tab

**Solution**: Check your VESC ROS driver is running and publishing data:

```bash
# List all ROS topics
ros2 topic list | grep -i vesc

# Check if VESC topics exist (adjust names to match your setup)
# Common topics: /vesc/sensors/core, /vesc/commands/motor/speed, etc.
```

### Map not displaying

**Solution**: Install Folium for map support:

```bash
pip install folium
```

### GUI doesn't respond

**Solution**: Check the terminal for error messages. Common issues:

1. ROS2 not properly sourced
2. PyQt6 not installed
3. ROS2 daemon not running (`ros2 daemon status`)

## Configuration

### Customizing ROS Topics

If your system uses different ROS topic names:

1. Edit `config.yaml` in the `tidebreaker_gui` directory
2. Update topic names to match your system
3. (Note: Dynamic topic configuration coming in future versions)

### Adjusting Display Layout

To modify which data is displayed or change panel layouts:

1. Edit the panel files in `tidebreaker_gui/ui/`:
   - `flight_controller_panel.py` - FC data display
   - `vesc_panel.py` - Motor data display
   - `map_widget.py` - Map display

## Next Steps

### Adding Waypoint Support

1. To add waypoint input to the map, modify `map_widget.py`
2. Add click handlers to create waypoints
3. Publish waypoints to `/boat/waypoints` topic

### Adding More Data

To display additional data:

1. Create a new panel in `tidebreaker_gui/ui/`
2. Add ROS topic subscriptions in `data_manager.py`
3. Add the new panel to the `Sidebar` in `sidebar.py`

See the main README.md for detailed extension examples.

## Support

For issues or questions:

1. Check the README.md for more detailed documentation
2. Verify ROS2 topics with `ros2 topic list` and `ros2 topic echo <topic>`
3. Check node status with `ros2 node info <node_name>`

## Performance Tips

- The GUI updates at 1 Hz by default (adjustable in `main_window.py`)
- For slower computers, increase the timer interval
- Map updates only when GPS data changes (efficient)
- All data access is thread-safe using locks

Enjoy using the Tidebreaker GUI!
