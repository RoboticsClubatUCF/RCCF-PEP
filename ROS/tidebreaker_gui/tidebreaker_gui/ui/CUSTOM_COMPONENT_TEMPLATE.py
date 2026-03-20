"""
Example Custom Component - Template for extending the Tidebreaker GUI

This file demonstrates how to create a new custom data panel for the Tidebreaker GUI.
Copy this template to create your own components.

Usage:
1. Copy this file to tidebreaker_gui/ui/my_custom_panel.py
2. Replace CustomPanel with your component name
3. Add subscriptions to data_manager.py
4. Import and add to sidebar.py
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QLabel, QGroupBox,
    QProgressBar, QScrollArea, QPushButton
)
from PyQt6.QtCore import Qt, pyqtSignal, QObject
from PyQt6.QtGui import QFont, QColor
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..data_manager import DataManager


class DataUpdateSignals(QObject):
    """Signals for data updates (PyQt6 cannot use signals on ROS callback threads)."""
    updated = pyqtSignal()


class CustomPanel(QWidget):
    """
    Custom data panel template.
    
    Replace CustomPanel with your component name and customize as needed.
    """

    def __init__(self, data_manager: 'DataManager'):
        super().__init__()
        self.data_manager = data_manager
        
        # Create signals object for thread-safe updates
        self.signals = DataUpdateSignals()
        self.signals.updated.connect(self.update_display)
        
        # Register callback with data manager
        # (you'll need to add a corresponding subscription in data_manager.py)
        self.data_manager.register_callback('custom_data', self._on_data_update)
        
        # Initialize UI
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Make scrollable for many data points
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        # Panel title
        title = QLabel("My Custom Data")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title.setFont(title_font)
        scroll_layout.addWidget(title)
        
        # Example: Data group 1
        group1 = QGroupBox("Group 1")
        group1_layout = QGridLayout()
        
        self.label_1 = QLabel("Value 1: --")
        self.label_2 = QLabel("Value 2: --")
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        
        group1_layout.addWidget(QLabel("Label 1:"), 0, 0)
        group1_layout.addWidget(self.label_1, 0, 1)
        group1_layout.addWidget(QLabel("Label 2:"), 1, 0)
        group1_layout.addWidget(self.label_2, 1, 1)
        group1_layout.addWidget(QLabel("Progress:"), 2, 0)
        group1_layout.addWidget(self.progress_bar, 2, 1)
        
        group1.setLayout(group1_layout)
        scroll_layout.addWidget(group1)
        
        # Example: Data group 2 with buttons
        group2 = QGroupBox("Group 2")
        group2_layout = QGridLayout()
        
        self.label_3 = QLabel("Status: Idle")
        self.status_button = QPushButton("Update Status")
        self.status_button.clicked.connect(self._on_button_clicked)
        
        group2_layout.addWidget(QLabel("Status:"), 0, 0)
        group2_layout.addWidget(self.label_3, 0, 1)
        group2_layout.addWidget(self.status_button, 1, 0, 1, 2)
        
        group2.setLayout(group2_layout)
        scroll_layout.addWidget(group2)
        
        # Add stretch to push content to top
        scroll_layout.addStretch()
        
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
    
    def _on_data_update(self):
        """
        Called when data is updated in the data manager.
        
        This method is called from a ROS subscription callback thread,
        so we use signals to safely update the GUI.
        """
        self.signals.updated.emit()
    
    def update_display(self):
        """
        Update all display values from the data manager.
        
        This method runs on the Qt main thread and is safe to update GUI.
        Retrieve data from data_manager and update labels/values.
        """
        # Example: Get custom data from data manager
        # (You'll need to add a getter method in data_manager.py)
        # custom_data = self.data_manager.get_custom_data()
        
        # if custom_data:
        #     self.label_1.setText(f"Value 1: {custom_data['value1']:.2f}")
        #     self.label_2.setText(f"Value 2: {custom_data['value2']:.2f}")
        #     self.progress_bar.setValue(int(custom_data['progress']))
        pass
    
    def _on_button_clicked(self):
        """Handle button click events."""
        self.label_3.setText("Status: Updated")


# Steps to integrate this component:
#
# 1. In data_manager.py, add a subscription in __init__:
#    
#    self.create_subscription(
#        MyCustomMessage,          # Your message type
#        '/your/custom/topic',     # Your topic
#        self._custom_callback,
#        10,
#        callback_group=callback_group
#    )
#
# 2. Add callback and getter methods in data_manager.py:
#    
#    def _custom_callback(self, msg):
#        with self._data_lock:
#            self._custom_data = msg
#        self._trigger_callbacks('custom_data')
#    
#    def get_custom_data(self):
#        with self._data_lock:
#            return self._custom_data.copy() if self._custom_data else None
#
# 3. In sidebar.py, import and add the panel:
#    
#    from .custom_panel import CustomPanel  # Add import
#    
#    # In Sidebar._init_ui():
#    custom_panel = CustomPanel(self.data_manager)
#    tabs.addTab(custom_panel, "My Custom Data")
#
# 4. Rebuild and test:
#    
#    colcon build --packages-select tidebreaker_gui
#    source install/setup.bash
#    ros2 run tidebreaker_gui tidebreaker_gui
