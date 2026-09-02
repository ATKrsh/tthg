"""
TTHG - Frameless Glassmorphism Desktop HUD Widget
Real-time system telemetry gauges (CPU, RAM, Disk, Uptime) and launchers for Domain Adaptation, Model Lab, and Review Workbench.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt, QPoint, QTimer
from config import ConfigManager
from core.system_info import SystemInfoCollector
from ui.settings_dialog import SettingsDialog
from ui.domain_adaptation_view import DomainAdaptationView
from ui.training_review_view import TrainingReviewView
from ui.model_lab_view import ModelLabView
from ui.domain_research_view import DomainResearchView


class TTHGWidget(QWidget):
    def __init__(self, config_manager: ConfigManager):
        super().__init__()
        self.config = config_manager
        self.drag_position = QPoint()

        self._adapt_view = None
        self._review_view = None
        self._lab_view = None
        self._research_view = None

        self.init_flags()
        self.init_ui()

        # Telemetry Timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_telemetry)
        self.timer.start(self.config.get("refresh_interval_ms", 1000))

    def init_flags(self):
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool |
            Qt.SubWindow
        )
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowOpacity(self.config.get("widget_opacity", 0.92))
        self.setObjectName("TTHGWidget")

        pos = self.config.get("widget_position", [150, 150])
        self.move(pos[0], pos[1])

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)

        # Header
        header = QHBoxLayout()
        title = QLabel("⚡ TTHG HUD & Model Lab")
        title.setObjectName("WidgetTitle")

        close_btn = QPushButton("×")
        close_btn.setFixedSize(22, 22)
        close_btn.setStyleSheet("""
            QPushButton {
                background: transparent; color: #94a3b8; font-size: 16px; font-weight: bold; border: none;
            }
            QPushButton:hover { color: #22d3ee; }
        """)
        close_btn.clicked.connect(self.hide)

        header.addWidget(title)
        header.addStretch()
        header.addWidget(close_btn)
        layout.addLayout(header)

        # Telemetry Metrics Layout
        # CPU
        self.cpu_label = QLabel("CPU: 0.0%")
        self.cpu_bar = QProgressBar()
        self.cpu_bar.setRange(0, 100)

        # RAM
        self.ram_label = QLabel("RAM: 0.0 GB / 0.0 GB (0.0%)")
        self.ram_bar = QProgressBar()
        self.ram_bar.setRange(0, 100)

        # Disk
        self.disk_label = QLabel("Disk: 0.0%")
        self.disk_bar = QProgressBar()
        self.disk_bar.setRange(0, 100)

        # Uptime
        self.uptime_label = QLabel("Uptime: 00:00:00")
        self.uptime_label.setStyleSheet("color: #38bdf8; font-weight: bold;")

        layout.addWidget(self.cpu_label)
        layout.addWidget(self.cpu_bar)
        layout.addWidget(self.ram_label)
        layout.addWidget(self.ram_bar)
        layout.addWidget(self.disk_label)
        layout.addWidget(self.disk_bar)
        layout.addWidget(self.uptime_label)

        # Engine Action Launchers Bar 1
        subsystems_box = QHBoxLayout()

        btn_adapt = QPushButton("🎓 Adaptation")
        btn_adapt.setObjectName("ActionBtn")
        btn_adapt.setToolTip("Open Domain Adaptation Engine")
        btn_adapt.clicked.connect(self.open_adaptation)

        btn_review = QPushButton("🔍 Review")
        btn_review.setObjectName("ActionBtn")
        btn_review.setToolTip("Open Human Review Workbench")
        btn_review.clicked.connect(self.open_review)

        btn_lab = QPushButton("🧪 Model Lab")
        btn_lab.setObjectName("ActionBtn")
        btn_lab.setToolTip("Open Continuous Model Improvement Lab")
        btn_lab.clicked.connect(self.open_lab)

        subsystems_box.addWidget(btn_adapt)
        subsystems_box.addWidget(btn_review)
        subsystems_box.addWidget(btn_lab)

        layout.addLayout(subsystems_box)

        # Quick Actions Bar 2
        actions_box = QHBoxLayout()

        btn_research = QPushButton("🌐 Research")
        btn_research.setObjectName("ActionBtn")
        btn_research.clicked.connect(self.open_research)

        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setObjectName("ActionBtn")
        refresh_btn.clicked.connect(self.update_telemetry)

        settings_btn = QPushButton("⚙️ Settings")
        settings_btn.setObjectName("ActionBtn")
        settings_btn.clicked.connect(self.open_settings)

        actions_box.addWidget(btn_research)
        actions_box.addWidget(refresh_btn)
        actions_box.addWidget(settings_btn)

        layout.addLayout(actions_box)

        self.update_telemetry()

    def update_telemetry(self):
        metrics = SystemInfoCollector.get_metrics()

        # CPU
        cpu_val = int(metrics["cpu_pct"])
        self.cpu_bar.setValue(cpu_val)
        self.cpu_label.setText(f"CPU: {metrics['cpu_pct']}%")

        # RAM
        ram_val = int(metrics["ram_pct"])
        self.ram_bar.setValue(ram_val)
        self.ram_label.setText(f"RAM: {metrics['ram_used_gb']} GB / {metrics['ram_total_gb']} GB ({metrics['ram_pct']}%)")

        # Disk
        disk_val = int(metrics["disk_pct"])
        self.disk_bar.setValue(disk_val)
        self.disk_label.setText(f"Disk Usage: {metrics['disk_pct']}%")

        # Uptime
        self.uptime_label.setText(f"System Uptime: {metrics['uptime_str']}")

    def open_adaptation(self):
        if not self._adapt_view:
            self._adapt_view = DomainAdaptationView(self.config)
        self._adapt_view.show()

    def open_review(self):
        if not self._review_view:
            self._review_view = TrainingReviewView(self.config)
        self._review_view.show()

    def open_lab(self):
        if not self._lab_view:
            self._lab_view = ModelLabView(self.config)
        self._lab_view.show()

    def open_research(self):
        if not self._research_view:
            self._research_view = DomainResearchView(self.config)
        self._research_view.show()

    def open_settings(self):
        dlg = SettingsDialog(self.config, self)
        if dlg.exec():
            interval = self.config.get("refresh_interval_ms", 1000)
            self.timer.setInterval(interval)
            self.update_telemetry()

    # --- Mouse Dragging ---
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            new_pos = event.globalPosition().toPoint() - self.drag_position
            self.move(new_pos)
            self.config.set("widget_position", [new_pos.x(), new_pos.y()])
            event.accept()
