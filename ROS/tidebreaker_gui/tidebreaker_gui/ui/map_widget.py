"""
Map Widget - Displays boat position and eventually waypoints.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PyQt6.QtCore import Qt, pyqtSignal, QObject
from PyQt6.QtGui import QFont
from PyQt6.QtWebEngineWidgets import QWebEngineView
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..data_manager import DataManager


class DataUpdateSignals(QObject):
    """Signals for data updates."""
    updated = pyqtSignal()


class MapWidget(QWidget):
    """Widget to display map with boat position."""
    
    def __init__(self, data_manager: 'DataManager', parent=None):
        super().__init__(parent)
        self.data_manager = data_manager
        self.signals = DataUpdateSignals()
        self.signals.updated.connect(self.update_map)
        
        self.current_lat = None
        self.current_lng = None
        self.map_view = None
        
        # Register callback with data manager
        self.data_manager.register_callback('fc_gps', self._on_data_update)
        
        self._init_ui()
        self._init_map()
    
    def _init_ui(self):
        """Initialize the UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Title
        title = QLabel("Position Map")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        layout.addWidget(title)
        
        # Web engine for map display
        self.map_view = QWebEngineView()
        layout.addWidget(self.map_view)
        
        # Status label
        self.status_label = QLabel("Waiting for GPS data...")
        self.status_label.setStyleSheet("color: gray; font-size: 10px;")
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
    
    def _init_map(self):
        """Initialize the map with default position."""
        # Import folium here to avoid issues if not installed
        try:
            import folium
            from io import StringIO
            
            # Default position (San Francisco)
            default_lat = 37.7749
            default_lng = -122.4194
            
            # Create map
            m = folium.Map(
                location=[default_lat, default_lng],
                zoom_start=15,
                tiles='OpenStreetMap'
            )
            
            # Add marker for default position
            folium.Marker(
                location=[default_lat, default_lng],
                popup="Start Position",
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(m)
            
            # Save to HTML
            html_string = m._repr_html_()
            self.map_view.setHtml(html_string)
            
        except ImportError:
            self.status_label.setText("Folium not installed. Install with: pip install folium")
            html = """
            <html>
            <body style="font-family: Arial; padding: 20px;">
                <h2>Map Display</h2>
                <p>To use the map feature, install folium:</p>
                <code>pip install folium</code>
                <p>Map will display GPS position once available.</p>
            </body>
            </html>
            """
            self.map_view.setHtml(html)
    
    def _on_data_update(self):
        """Called when GPS data is updated."""
        self.signals.updated.emit()
    
    def update_map(self):
        """Update map with current GPS position."""
        try:
            import folium
            
            gps = self.data_manager.get_fc_gps()
            if gps and gps.latitude != 0 and gps.longitude != 0:
                self.current_lat = gps.latitude
                self.current_lng = gps.longitude
                
                # Create updated map
                m = folium.Map(
                    location=[self.current_lat, self.current_lng],
                    zoom_start=15,
                    tiles='OpenStreetMap'
                )
                
                # Add marker for current position
                folium.Marker(
                    location=[self.current_lat, self.current_lng],
                    popup=f"Lat: {self.current_lat:.6f}<br>Lng: {self.current_lng:.6f}",
                    icon=folium.Icon(color='red', icon='fa-ship')
                ).add_to(m)
                
                # Update map view
                html_string = m._repr_html_()
                self.map_view.setHtml(html_string)
                
                # Update status
                self.status_label.setText(
                    f"Position: {self.current_lat:.6f}, {self.current_lng:.6f}"
                )
        
        except ImportError:
            pass  # Folium not installed, skip update
        except Exception as e:
            self.status_label.setText(f"Error updating map: {e}")
