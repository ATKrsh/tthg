"""
TTHG - Navigation Sidebar Component
Sleek vertical navigation sidebar for switching main application views.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QFrame
)
from PySide6.QtCore import Signal, Qt


class NavigationSidebar(QWidget):
    """Vertical sidebar for main view switching."""

    page_changed = Signal(int)
    toggle_overlay = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("SidebarWidget")
        self.setFixedWidth(220)
        self.buttons = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 16, 12, 16)
        layout.setSpacing(8)

        # Brand Title
        brand_label = QLabel("⚡ TTHG LABS")
        brand_label.setStyleSheet("color: #38bdf8; font-size: 16px; font-weight: 800; letter-spacing: 1px;")
        sub_label = QLabel("Liquid Glass Edition")
        sub_label.setStyleSheet("color: #94a3b8; font-size: 10px; font-weight: 600; margin-bottom: 12px;")

        layout.addWidget(brand_label)
        layout.addWidget(sub_label)

        # Navigation Items (Index, Label)
        nav_items = [
            (0, "📊 Dashboard"),
            (1, "🎓 Domain Adaptation"),
            (2, "🔍 Review Workbench"),
            (3, "🧪 Model Lab"),
            (4, "🌐 Domain Research"),
            (5, "⚙️ Settings"),
        ]

        for idx, label in nav_items:
            btn = QPushButton(label)
            btn.setObjectName("NavButton")
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda _, i=idx: self.select_page(i))
            self.buttons.append((idx, btn))
            layout.addWidget(btn)

        layout.addStretch()

        # Separator line
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background-color: rgba(56, 189, 248, 0.2); max-height: 1px;")
        layout.addWidget(line)

        # Desktop Overlay Mode Switcher
        hud_btn = QPushButton("🔲 Toggle Floating HUD")
        hud_btn.setObjectName("NavButton")
        hud_btn.setStyleSheet("color: #22d3ee; font-weight: bold;")
        hud_btn.clicked.connect(self.toggle_overlay.emit)
        layout.addWidget(hud_btn)

        self.select_page(0)

    def select_page(self, page_index: int):
        for idx, btn in self.buttons:
            if idx == page_index:
                btn.setObjectName("NavButtonActive")
            else:
                btn.setObjectName("NavButton")
            btn.setStyle(btn.style())

        self.page_changed.emit(page_index)
