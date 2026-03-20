"""
Data manager for subscribing to ROS topics and managing flight controller and motor data.
"""

import rclpy
from rclpy.node import Node
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
from rclpy.executors import MultiThreadedExecutor

from geometry_msgs.msg import Twist, TwistStamped
from sensor_msgs.msg import NavSatFix, Imu
from mavros_msgs.msg import State, VFR_HUD, RCIn, RCOut
from std_msgs.msg import Float32, Int32
from threading import Lock
from typing import Optional, Callable, Dict, Any


class DataManager(Node):
    """Manages ROS subscriptions and data updates for the GUI."""

    def __init__(self):
        super().__init__('tidebreaker_gui_data_manager')
        
        # Data locks for thread safety
        self._data_lock = Lock()
        
        # Flight controller data
        self._fc_state: Optional[State] = None
        self._fc_vfr_hud: Optional[VFR_HUD] = None
        self._fc_gps: Optional[NavSatFix] = None
        self._fc_imu: Optional[Imu] = None
        self._fc_rc_in: Optional[RCIn] = None
        self._fc_rc_out: Optional[RCOut] = None
        
        # Motor (VESC) data
        self._vesc_state: Dict[str, Any] = {
            'voltage_input': 0.0,
            'temperature_pcb': 0.0,
            'current_motor': 0.0,
            'current_input': 0.0,
            'speed': 0.0,
            'duty_cycle': 0.0,
            'charge_drawn': 0.0,
            'charge_regen': 0.0,
            'energy_drawn': 0.0,
            'energy_regen': 0.0,
            'displacement': 0.0,
            'distance_traveled': 0.0,
            'fault_code': 0,
        }
        
        # Callback registry for UI updates
        self._callbacks: Dict[str, list] = {
            'fc_state': [],
            'fc_vfr_hud': [],
            'fc_gps': [],
            'fc_imu': [],
            'vesc_state': [],
        }
        
        # Create callback group for subscriptions
        callback_group = MutuallyExclusiveCallbackGroup()
        
        # MAVROS subscriptions
        self.create_subscription(
            State,
            '/mavros/state',
            self._fc_state_callback,
            10,
            callback_group=callback_group
        )
        
        self.create_subscription(
            VFR_HUD,
            '/mavros/vfr_hud',
            self._fc_vfr_hud_callback,
            10,
            callback_group=callback_group
        )
        
        self.create_subscription(
            NavSatFix,
            '/mavros/global_position/global',
            self._fc_gps_callback,
            10,
            callback_group=callback_group
        )
        
        self.create_subscription(
            Imu,
            '/mavros/imu/data',
            self._fc_imu_callback,
            10,
            callback_group=callback_group
        )
        
        self.create_subscription(
            RCIn,
            '/mavros/rc/in',
            self._fc_rc_in_callback,
            10,
            callback_group=callback_group
        )
        
        self.create_subscription(
            RCOut,
            '/mavros/rc/out',
            self._fc_rc_out_callback,
            10,
            callback_group=callback_group
        )
        
        # VESC subscription - will need to be connected to the actual VESC ROS node
        # Assuming vesc publishes to /vesc/sensors/core (adjust topic as needed)
        self._vesc_subscription = self.create_subscription(
            # This needs to be updated based on actual VESC message type
            # For now we'll create a placeholder
            Float32,
            '/vesc/sensors/core',
            self._vesc_state_callback,
            10,
            callback_group=callback_group
        )
        
        self.get_logger().info('Data Manager initialized')
    
    def _fc_state_callback(self, msg: State) -> None:
        """Handle flight controller state updates."""
        with self._data_lock:
            self._fc_state = msg
        self._trigger_callbacks('fc_state')
    
    def _fc_vfr_hud_callback(self, msg: VFR_HUD) -> None:
        """Handle flight controller VFR HUD updates."""
        with self._data_lock:
            self._fc_vfr_hud = msg
        self._trigger_callbacks('fc_vfr_hud')
    
    def _fc_gps_callback(self, msg: NavSatFix) -> None:
        """Handle flight controller GPS updates."""
        with self._data_lock:
            self._fc_gps = msg
        self._trigger_callbacks('fc_gps')
    
    def _fc_imu_callback(self, msg: Imu) -> None:
        """Handle flight controller IMU updates."""
        with self._data_lock:
            self._fc_imu = msg
        self._trigger_callbacks('fc_imu')
    
    def _fc_rc_in_callback(self, msg: RCIn) -> None:
        """Handle flight controller RC input updates."""
        with self._data_lock:
            self._fc_rc_in = msg
        self._trigger_callbacks('fc_rc_in')
    
    def _fc_rc_out_callback(self, msg: RCOut) -> None:
        """Handle flight controller RC output updates."""
        with self._data_lock:
            self._fc_rc_out = msg
        self._trigger_callbacks('fc_rc_out')
    
    def _vesc_state_callback(self, msg) -> None:
        """Handle VESC motor state updates."""
        # This callback will be updated once we determine the actual VESC message type
        with self._data_lock:
            pass
        self._trigger_callbacks('vesc_state')
    
    def register_callback(self, event_type: str, callback: Callable) -> None:
        """Register a callback to be triggered on data updates."""
        if event_type not in self._callbacks:
            self._callbacks[event_type] = []
        self._callbacks[event_type].append(callback)
    
    def unregister_callback(self, event_type: str, callback: Callable) -> None:
        """Unregister a callback."""
        if event_type in self._callbacks:
            self._callbacks[event_type] = [
                cb for cb in self._callbacks[event_type] if cb != callback
            ]
    
    def _trigger_callbacks(self, event_type: str) -> None:
        """Trigger all callbacks for a given event type."""
        for callback in self._callbacks.get(event_type, []):
            try:
                callback()
            except Exception as e:
                self.get_logger().error(f'Error in callback for {event_type}: {e}')
    
    # Getter methods for thread-safe data access
    def get_fc_state(self) -> Optional[State]:
        """Get flight controller state."""
        with self._data_lock:
            return self._fc_state
    
    def get_fc_vfr_hud(self) -> Optional[VFR_HUD]:
        """Get flight controller VFR HUD data."""
        with self._data_lock:
            return self._fc_vfr_hud
    
    def get_fc_gps(self) -> Optional[NavSatFix]:
        """Get flight controller GPS data."""
        with self._data_lock:
            return self._fc_gps
    
    def get_fc_imu(self) -> Optional[Imu]:
        """Get flight controller IMU data."""
        with self._data_lock:
            return self._fc_imu
    
    def get_fc_rc_in(self) -> Optional[RCIn]:
        """Get flight controller RC input data."""
        with self._data_lock:
            return self._fc_rc_in
    
    def get_fc_rc_out(self) -> Optional[RCOut]:
        """Get flight controller RC output data."""
        with self._data_lock:
            return self._fc_rc_out
    
    def get_vesc_state(self) -> Dict[str, Any]:
        """Get VESC motor state."""
        with self._data_lock:
            return self._vesc_state.copy()


def get_data_manager() -> DataManager:
    """Factory function to create and return the data manager."""
    if not rclpy.ok():
        rclpy.init()
    return DataManager()
