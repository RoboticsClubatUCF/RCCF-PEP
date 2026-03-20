"""
VESC Motor Panel - Displays motor controller data.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QLabel, QGroupBox,
    QProgressBar, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal, QObject
from PyQt6.QtGui import QFont, QColor
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..data_manager import DataManager


class DataUpdateSignals(QObject):
    """Signals for data updates."""
    updated = pyqtSignal()


class VescPanel(QWidget):
    """Widget to display VESC motor controller data."""

    # Fault code descriptions
    FAULT_CODES = {
        0: "None",
        1: "Over Voltage",
        2: "Under Voltage",
        3: "DRV8302",
        4: "Abs Over Current",
        5: "Over Temp FET",
        6: "Over Temp Motor",
    }

    def __init__(self, data_manager: 'DataManager'):
        super().__init__()
        self.data_manager = data_manager
        self.signals = DataUpdateSignals()
        self.signals.updated.connect(self.update_display)
        
        # Register callback with data manager
        self.data_manager.register_callback('vesc_state', self._on_data_update)
        
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
        title = QLabel("Motor (VESC)")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title.setFont(title_font)
        scroll_layout.addWidget(title)
        
        # Power Group
        power_group = QGroupBox("Power")
        power_layout = QGridLayout()
        
        self.voltage_label = QLabel("Input Voltage: -- V")
        self.current_motor_label = QLabel("Motor Current: -- A")
        self.current_input_label = QLabel("Input Current: -- A")
        
        power_layout.addWidget(QLabel("Input Voltage:"), 0, 0)
        power_layout.addWidget(self.voltage_label, 0, 1)
        power_layout.addWidget(QLabel("Motor Current:"), 1, 0)
        power_layout.addWidget(self.current_motor_label, 1, 1)
        power_layout.addWidget(QLabel("Input Current:"), 2, 0)
        power_layout.addWidget(self.current_input_label, 2, 1)
        
        power_group.setLayout(power_layout)
        scroll_layout.addWidget(power_group)
        
        # Performance Group
        perf_group = QGroupBox("Performance")
        perf_layout = QGridLayout()
        
        self.speed_label = QLabel("Speed: -- RPM")
        self.duty_cycle_label = QLabel("Duty Cycle: -- %")
        
        perf_layout.addWidget(QLabel("Speed:"), 0, 0)
        perf_layout.addWidget(self.speed_label, 0, 1)
        perf_layout.addWidget(QLabel("Duty Cycle:"), 1, 0)
        perf_layout.addWidget(self.duty_cycle_label, 1, 1)
        
        perf_group.setLayout(perf_layout)
        scroll_layout.addWidget(perf_group)
        
        # Temperature Group
        temp_group = QGroupBox("Temperature")
        temp_layout = QGridLayout()
        
        self.temp_pcb_label = QLabel("PCB Temp: -- °C")
        self.temp_motor_label = QLabel("Motor Temp: -- °C")
        
        temp_layout.addWidget(QLabel("PCB:"), 0, 0)
        temp_layout.addWidget(self.temp_pcb_label, 0, 1)
        temp_layout.addWidget(QLabel("Motor:"), 1, 0)
        temp_layout.addWidget(self.temp_motor_label, 1, 1)
        
        temp_group.setLayout(temp_layout)
        scroll_layout.addWidget(temp_group)
        
        # Energy Group
        energy_group = QGroupBox("Energy")
        energy_layout = QGridLayout()
        
        self.charge_drawn_label = QLabel("Charge Drawn: -- Ah")
        self.charge_regen_label = QLabel("Charge Regen: -- Ah")
        self.energy_drawn_label = QLabel("Energy Drawn: -- Wh")
        self.energy_regen_label = QLabel("Energy Regen: -- Wh")
        
        energy_layout.addWidget(QLabel("Charge Drawn:"), 0, 0)
        energy_layout.addWidget(self.charge_drawn_label, 0, 1)
        energy_layout.addWidget(QLabel("Charge Regen:"), 1, 0)
        energy_layout.addWidget(self.charge_regen_label, 1, 1)
        energy_layout.addWidget(QLabel("Energy Drawn:"), 2, 0)
        energy_layout.addWidget(self.energy_drawn_label, 2, 1)
        energy_layout.addWidget(QLabel("Energy Regen:"), 3, 0)
        energy_layout.addWidget(self.energy_regen_label, 3, 1)
        
        energy_group.setLayout(energy_layout)
        scroll_layout.addWidget(energy_group)
        
        # Tachometer Group
        tach_group = QGroupBox("Tachometer")
        tach_layout = QGridLayout()
        
        self.displacement_label = QLabel("Displacement: -- counts")
        self.distance_traveled_label = QLabel("Distance: -- counts")
        
        tach_layout.addWidget(QLabel("Displacement:"), 0, 0)
        tach_layout.addWidget(self.displacement_label, 0, 1)
        tach_layout.addWidget(QLabel("Distance Traveled:"), 1, 0)
        tach_layout.addWidget(self.distance_traveled_label, 1, 1)
        
        tach_group.setLayout(tach_layout)
        scroll_layout.addWidget(tach_group)
        
        # Status Group
        status_group = QGroupBox("Status")
        status_layout = QGridLayout()
        
        self.fault_code_label = QLabel("Fault Code: None")
        self.fault_code_label.setStyleSheet("color: green; font-weight: bold;")
        
        status_layout.addWidget(QLabel("Fault Code:"), 0, 0)
        status_layout.addWidget(self.fault_code_label, 0, 1)
        
        status_group.setLayout(status_layout)
        scroll_layout.addWidget(status_group)
        
        scroll_layout.addStretch()
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
    
    def _on_data_update(self):
        """Called when data is updated in the data manager."""
        self.signals.updated.emit()
    
    def update_display(self):
        """Update all display values from data manager."""
        vesc_state = self.data_manager.get_vesc_state()
        
        # Power
        self.voltage_label.setText(f"Input Voltage: {vesc_state['voltage_input']:.2f} V")
        self.current_motor_label.setText(f"Motor Current: {vesc_state['current_motor']:.2f} A")
        self.current_input_label.setText(f"Input Current: {vesc_state['current_input']:.2f} A")
        
        # Performance
        self.speed_label.setText(f"Speed: {vesc_state['speed']:.0f} RPM")
        duty_pct = vesc_state['duty_cycle'] * 100
        self.duty_cycle_label.setText(f"Duty Cycle: {duty_pct:.1f} %")
        
        # Temperature
        self.temp_pcb_label.setText(f"PCB Temp: {vesc_state['temperature_pcb']:.1f} °C")
        self.temp_motor_label.setText(f"Motor Temp: -- °C")  # Motor temp not in VescState.msg
        
        # Energy
        self.charge_drawn_label.setText(f"Charge Drawn: {vesc_state['charge_drawn']:.2f} Ah")
        self.charge_regen_label.setText(f"Charge Regen: {vesc_state['charge_regen']:.2f} Ah")
        self.energy_drawn_label.setText(f"Energy Drawn: {vesc_state['energy_drawn']:.2f} Wh")
        self.energy_regen_label.setText(f"Energy Regen: {vesc_state['energy_regen']:.2f} Wh")
        
        # Tachometer
        self.displacement_label.setText(f"Displacement: {vesc_state['displacement']:.0f} counts")
        self.distance_traveled_label.setText(f"Distance: {vesc_state['distance_traveled']:.0f} counts")
        
        # Status
        fault_code = vesc_state['fault_code']
        fault_text = self.FAULT_CODES.get(fault_code, f"Unknown ({fault_code})")
        
        if fault_code == 0:
            self.fault_code_label.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.fault_code_label.setStyleSheet("color: red; font-weight: bold;")
        
        self.fault_code_label.setText(f"Fault Code: {fault_text}")
