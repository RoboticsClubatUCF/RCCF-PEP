"""
Sidebar Widget - Contains flight controller and VESC panels (similar to Mission Planner layout).
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING

from .flight_controller_panel import FlightControllerPanel
from .vesc_panel import VescPanel

if TYPE_CHECKING:
    from ..data_manager import DataManager


class Sidebar(QWidget):
    """Sidebar widget containing tabbed panels for FC and VESC data."""

    def __init__(self, data_manager: 'DataManager'):
        super().__init__()
        self.data_manager = data_manager
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create tabbed interface
        tabs = QTabWidget()
        
        # Flight Controller Tab
        self.fc_panel = FlightControllerPanel(self.data_manager)
        tabs.addTab(self.fc_panel, "Flight Controller")
        
        # VESC Tab
        self.vesc_panel = VescPanel(self.data_manager)
        tabs.addTab(self.vesc_panel, "Motor (VESC)")
        
        layout.addWidget(tabs)
        self.setLayout(layout)
        
        # Set sidebar width
        self.setMinimumWidth(350)
        self.setMaximumWidth(450)
