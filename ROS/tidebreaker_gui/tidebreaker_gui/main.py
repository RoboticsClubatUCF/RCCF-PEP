"""
Main entry point for the Tidebreaker GUI application.

This module initializes ROS2 and the PyQt6 application, setting up
the data manager and main window.
"""

import sys
import rclpy
from rclpy.executors import MultiThreadedExecutor
from threading import Thread

from PyQt6.QtWidgets import QApplication, QMessageBox

from .data_manager import DataManager
from .ui.main_window import MainWindow


def main():
    """Main entry point for the GUI application."""
    
    # Initialize Qt application
    qt_app = QApplication(sys.argv)
    
    # Initialize ROS2
    try:
        if not rclpy.ok():
            rclpy.init()
    except Exception as e:
        QMessageBox.critical(
            None,
            "ROS2 Initialization Error",
            f"Failed to initialize ROS2:\n{str(e)}\n\n"
            "Make sure ROS2 is properly installed and sourced."
        )
        return 1
    
    # Create data manager node
    try:
        data_manager = DataManager()
    except Exception as e:
        QMessageBox.critical(
            None,
            "Data Manager Error",
            f"Failed to create data manager:\n{str(e)}"
        )
        return 1
    
    # Create ROS2 executor in separate thread
    executor = MultiThreadedExecutor()
    executor.add_node(data_manager)
    
    ros_thread = Thread(target=executor.spin, daemon=True)
    ros_thread.start()
    
    # Create and show main window
    try:
        window = MainWindow(data_manager)
        window.show()
    except Exception as e:
        QMessageBox.critical(
            None,
            "GUI Error",
            f"Failed to create main window:\n{str(e)}"
        )
        return 1
    
    # Run Qt application
    exit_code = qt_app.exec()
    
    # Cleanup
    executor.shutdown()
    rclpy.shutdown()
    
    return exit_code


if __name__ == '__main__':
    sys.exit(main())
