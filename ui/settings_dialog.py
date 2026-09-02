"""
TTHG - Settings Configuration Dialog
Allows configuring hotkeys, refresh rate, widget opacity, and display options.
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QSpinBox,
    QPushButton, QCheckBox, QGroupBox, QFormLayout, QMessageBox
)
from config import ConfigManager


class SettingsDialog(QDialog):
    def __init__(self, config_manager: ConfigManager, parent=None):
        super().__init__(parent)
        self.config = config_manager
        self.setWindowTitle("TTHG — Settings")
        self.resize(440, 360)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        group_gen = QGroupBox("HUD Display & Telemetry Options")
        form_gen = QFormLayout(group_gen)

        self.hotkey_input = QLineEdit(self.config.get("hotkey_toggle", "Ctrl+Alt+T"))
        form_gen.addRow("Toggle HUD Hotkey:", self.hotkey_input)

        self.refresh_spin = QSpinBox()
        self.refresh_spin.setRange(200, 5000)
        self.refresh_spin.setSingleStep(100)
        self.refresh_spin.setValue(self.config.get("refresh_interval_ms", 1000))
        form_gen.addRow("Refresh Interval (ms):", self.refresh_spin)

        self.check_cpu = QCheckBox("Show CPU Usage")
        self.check_cpu.setChecked(self.config.get("show_cpu", True))
        form_gen.addRow("", self.check_cpu)

        self.check_ram = QCheckBox("Show RAM Usage")
        self.check_ram.setChecked(self.config.get("show_ram", True))
        form_gen.addRow("", self.check_ram)

        self.check_disk = QCheckBox("Show Disk Usage")
        self.check_disk.setChecked(self.config.get("show_disk", True))
        form_gen.addRow("", self.check_disk)

        layout.addWidget(group_gen)

        # Action Buttons
        btn_box = QHBoxLayout()
        btn_cancel = QPushButton("Cancel")
        btn_cancel.clicked.connect(self.reject)
        btn_save = QPushButton("Save Settings")
        btn_save.clicked.connect(self.save_settings)

        btn_box.addStretch()
        btn_box.addWidget(btn_cancel)
        btn_box.addWidget(btn_save)

        layout.addLayout(btn_box)

    def save_settings(self):
        self.config.set("hotkey_toggle", self.hotkey_input.text().strip())
        self.config.set("refresh_interval_ms", self.refresh_spin.value())
        self.config.set("show_cpu", self.check_cpu.isChecked())
        self.config.set("show_ram", self.check_ram.isChecked())
        self.config.set("show_disk", self.check_disk.isChecked())

        QMessageBox.information(self, "TTHG", "Settings saved successfully!")
        self.accept()
