"""
Main Window - Top-level window for the Tidebreaker GUI application.
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
    QStatusBar, QMenuBar, QMenu
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon, QAction
from typing import TYPE_CHECKING

from .sidebar import Sidebar
from .map_widget import MapWidget

if TYPE_CHECKING:
    from ..data_manager import DataManager


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self, data_manager: 'DataManager'):
        super().__init__()
        self.data_manager = data_manager
        
        self.setWindowTitle("Tidebreaker - Autonomous Boat Dashboard")
        self.setWindowGeometry(100, 100, 1400, 900)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create sidebar
        self.sidebar = Sidebar(self.data_manager)
        main_layout.addWidget(self.sidebar)
        
        # Add vertical separator
        separator = QWidget()
        separator.setFixedWidth(1)
        separator.setStyleSheet("background-color: #cccccc;")
        main_layout.addWidget(separator)
        
        # Create map widget
        map_container = QWidget()
        map_layout = QVBoxLayout(map_container)
        map_layout.setContentsMargins(5, 5, 5, 5)
        
        self.map_widget = MapWidget(self.data_manager)
        map_layout.addWidget(self.map_widget)
        map_container.setLayout(map_layout)
        
        main_layout.addWidget(map_container, 1)
        
        # Create menu bar
        self._create_menu_bar()
        
        # Create status bar
        self.statusBar().showMessage("Ready")
        
        # Set up update timer for UI refresh
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._update_ui)
        self.update_timer.start(1000)  # Update every 1 second
    
    def _create_menu_bar(self):
        """Create the menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu("&View")
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("&About", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
    
    def _show_about(self):
        """Show about dialog."""
        from PyQt6.QtWidgets import QMessageBox
        
        QMessageBox.about(
            self,
            "About Tidebreaker GUI",
            "Tidebreaker - Autonomous Boat Dashboard\n\n"
            "Version 0.0.1\n\n"
            "A ROS2-based GUI for monitoring and controlling "
            "autonomous boats equipped with ArduPilot flight controllers "
            "and VESC motor controllers.\n\n"
            "© 2026 Tidebreaker Project"
        )
    
    def _update_ui(self):
        """Periodic UI update."""
        # This can be used to check connection status, etc.
        state = self.data_manager.get_fc_state()
        if state:
            connected_status = "Connected" if state.connected else "Disconnected"
            self.statusBar().showMessage(f"Flight Controller: {connected_status}")
    
    def closeEvent(self, event):
        """Handle window close event."""
        self.update_timer.stop()
        event.accept()
