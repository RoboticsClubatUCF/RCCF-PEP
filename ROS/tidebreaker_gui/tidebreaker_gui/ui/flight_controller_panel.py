"""
Flight Controller Data Panel - Displays MAVROS flight controller information.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QLabel, QGroupBox,
    QProgressBar, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal, QObject
from PyQt6.QtGui import QFont, QColor
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..data_manager import DataManager


class DataUpdateSignals(QObject):
    """Signals for data updates (since we can't use signals in the data manager)."""
    updated = pyqtSignal()


class FlightControllerPanel(QWidget):
    """Widget to display flight controller data from MAVROS."""

    def __init__(self, data_manager: 'DataManager'):
        super().__init__()
        self.data_manager = data_manager
        self.signals = DataUpdateSignals()
        self.signals.updated.connect(self.update_display)
        
        # Register callback with data manager
        self.data_manager.register_callback('fc_state', self._on_data_update)
        self.data_manager.register_callback('fc_vfr_hud', self._on_data_update)
        self.data_manager.register_callback('fc_gps', self._on_data_update)
        self.data_manager.register_callback('fc_imu', self._on_data_update)
        
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        # Title
        title = QLabel("Flight Controller")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title.setFont(title_font)
        scroll_layout.addWidget(title)
        
        # Flight Mode & Status Group
        status_group = QGroupBox("Status")
        status_layout = QGridLayout()
        
        self.flight_mode_label = QLabel("Flight Mode: --")
        self.armed_label = QLabel("Armed: --")
        self.connected_label = QLabel("Connected: --")
        
        status_layout.addWidget(QLabel("Mode:"), 0, 0)
        status_layout.addWidget(self.flight_mode_label, 0, 1)
        status_layout.addWidget(QLabel("Armed:"), 1, 0)
        status_layout.addWidget(self.armed_label, 1, 1)
        status_layout.addWidget(QLabel("Connected:"), 2, 0)
        status_layout.addWidget(self.connected_label, 2, 1)
        
        status_group.setLayout(status_layout)
        scroll_layout.addWidget(status_group)
        
        # Altitude & Speed Group
        alt_speed_group = QGroupBox("Altitude & Speed")
        alt_speed_layout = QGridLayout()
        
        self.altitude_label = QLabel("Altitude: -- m")
        self.groundspeed_label = QLabel("Ground Speed: -- m/s")
        self.airspeed_label = QLabel("Air Speed: -- m/s")
        self.climb_rate_label = QLabel("Climb Rate: -- m/s")
        
        alt_speed_layout.addWidget(QLabel("Altitude:"), 0, 0)
        alt_speed_layout.addWidget(self.altitude_label, 0, 1)
        alt_speed_layout.addWidget(QLabel("Ground Speed:"), 1, 0)
        alt_speed_layout.addWidget(self.groundspeed_label, 1, 1)
        alt_speed_layout.addWidget(QLabel("Air Speed:"), 2, 0)
        alt_speed_layout.addWidget(self.airspeed_label, 2, 1)
        alt_speed_layout.addWidget(QLabel("Climb Rate:"), 3, 0)
        alt_speed_layout.addWidget(self.climb_rate_label, 3, 1)
        
        alt_speed_group.setLayout(alt_speed_layout)
        scroll_layout.addWidget(alt_speed_group)
        
        # Position Group
        pos_group = QGroupBox("Position")
        pos_layout = QGridLayout()
        
        self.latitude_label = QLabel("Latitude: --")
        self.longitude_label = QLabel("Longitude: --")
        self.heading_label = QLabel("Heading: --°")
        self.gps_hdop_label = QLabel("HDOP: --")
        self.gps_fix_label = QLabel("GPS Fix: --")
        
        pos_layout.addWidget(QLabel("Latitude:"), 0, 0)
        pos_layout.addWidget(self.latitude_label, 0, 1)
        pos_layout.addWidget(QLabel("Longitude:"), 1, 0)
        pos_layout.addWidget(self.longitude_label, 1, 1)
        pos_layout.addWidget(QLabel("Heading:"), 2, 0)
        pos_layout.addWidget(self.heading_label, 2, 1)
        pos_layout.addWidget(QLabel("HDOP:"), 3, 0)
        pos_layout.addWidget(self.gps_hdop_label, 3, 1)
        pos_layout.addWidget(QLabel("GPS Fix:"), 4, 0)
        pos_layout.addWidget(self.gps_fix_label, 4, 1)
        
        pos_group.setLayout(pos_layout)
        scroll_layout.addWidget(pos_group)
        
        # Orientation Group (IMU)
        imu_group = QGroupBox("Orientation (IMU)")
        imu_layout = QGridLayout()
        
        self.roll_label = QLabel("Roll: -- °")
        self.pitch_label = QLabel("Pitch: -- °")
        self.yaw_label = QLabel("Yaw: -- °")
        
        imu_layout.addWidget(QLabel("Roll:"), 0, 0)
        imu_layout.addWidget(self.roll_label, 0, 1)
        imu_layout.addWidget(QLabel("Pitch:"), 1, 0)
        imu_layout.addWidget(self.pitch_label, 1, 1)
        imu_layout.addWidget(QLabel("Yaw:"), 2, 0)
        imu_layout.addWidget(self.yaw_label, 2, 1)
        
        imu_group.setLayout(imu_layout)
        scroll_layout.addWidget(imu_group)
        
        scroll_layout.addStretch()
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
    
    def _on_data_update(self):
        """Called when data is updated in the data manager."""
        self.signals.updated.emit()
    
    def update_display(self):
        """Update all display values from data manager."""
        # Update FC state
        fc_state = self.data_manager.get_fc_state()
        if fc_state:
            self.armed_label.setText(f"Armed: {'Yes' if fc_state.armed else 'No'}")
            self.connected_label.setText(f"Connected: {'Yes' if fc_state.connected else 'No'}")
            self.flight_mode_label.setText(f"Flight Mode: {fc_state.mode}")
        
        # Update VFR HUD
        vfr_hud = self.data_manager.get_fc_vfr_hud()
        if vfr_hud:
            self.altitude_label.setText(f"Altitude: {vfr_hud.altitude:.1f} m")
            self.groundspeed_label.setText(f"Ground Speed: {vfr_hud.groundspeed:.1f} m/s")
            self.airspeed_label.setText(f"Air Speed: {vfr_hud.airspeed:.1f} m/s")
            self.climb_rate_label.setText(f"Climb Rate: {vfr_hud.climb:.1f} m/s")
            self.heading_label.setText(f"Heading: {int(vfr_hud.heading)}°")
            self.throttle_label = QLabel(f"Throttle: {vfr_hud.throttle}%")
        
        # Update GPS
        gps = self.data_manager.get_fc_gps()
        if gps:
            self.latitude_label.setText(f"Latitude: {gps.latitude:.6f}")
            self.longitude_label.setText(f"Longitude: {gps.longitude:.6f}")
            
            # GPS fix type
            fix_types = ['No Fix', '2D Fix', '3D Fix', 'DGPS Fix', 'RTK Fixed', 'RTK Float']
            fix_type = fix_types[gps.status.status] if gps.status.status < len(fix_types) else 'Unknown'
            self.gps_fix_label.setText(f"GPS Fix: {fix_type}")
            
            # HDOP
            if len(gps.position_covariance) > 0:
                self.gps_hdop_label.setText(f"HDOP: {gps.position_covariance[0]:.2f}")
        
        # Update IMU
        imu = self.data_manager.get_fc_imu()
        if imu:
            # Extract roll, pitch, yaw from orientation quaternion
            q = imu.orientation
            import math
            
            # Convert quaternion to Euler angles (simplified)
            roll = math.atan2(2*(q.w*q.x + q.y*q.z), 1 - 2*(q.x**2 + q.y**2))
            pitch = math.asin(2*(q.w*q.y - q.z*q.x))
            yaw = math.atan2(2*(q.w*q.z + q.x*q.y), 1 - 2*(q.y**2 + q.z**2))
            
            # Convert to degrees
            roll_deg = math.degrees(roll)
            pitch_deg = math.degrees(pitch)
            yaw_deg = math.degrees(yaw)
            
            self.roll_label.setText(f"Roll: {roll_deg:.1f}°")
            self.pitch_label.setText(f"Pitch: {pitch_deg:.1f}°")
            self.yaw_label.setText(f"Yaw: {yaw_deg:.1f}°")
