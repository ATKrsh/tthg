"""
TTHG - Main Window Application Architecture
Integrates NavigationSidebar and QStackedWidget central container with full Liquid Glass aesthetic.
"""

import sys
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QStackedWidget, QStatusBar, QMessageBox
)
from PySide6.QtCore import Qt

from config import ConfigManager
from ui.styles import TTHG_STYLE
from ui.sidebar import NavigationSidebar
from ui.dashboard_view import DashboardView
from ui.domain_adaptation_view import DomainAdaptationView
from ui.training_review_view import TrainingReviewView
from ui.model_lab_view import ModelLabView
from ui.domain_research_view import DomainResearchView
from ui.settings_dialog import SettingsDialog
from ui.widget import TTHGWidget


class MainWindow(QMainWindow):
    """Primary Application Window for TTHG."""

    def __init__(self, config_manager: ConfigManager):
        super().__init__()
        self.config = config_manager
        self.hud_overlay = None

        self.setWindowTitle("TTHG — Task, Time & Gaming Helper (Liquid Glass Edition)")
        self.resize(1080, 680)
        self.setStyleSheet(TTHG_STYLE)

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. Navigation Sidebar
        self.sidebar = NavigationSidebar(self)
        self.sidebar.page_changed.connect(self.switch_page)
        self.sidebar.toggle_overlay.connect(self.toggle_floating_hud)
        main_layout.addWidget(self.sidebar)

        # 2. Central Stacked Widget
        self.stacked_widget = QStackedWidget()

        # Instantiate Views
        self.view_dashboard = DashboardView(self.config)
        self.view_adapt = DomainAdaptationView(self.config)
        self.view_review = TrainingReviewView(self.config)
        self.view_lab = ModelLabView(self.config)
        self.view_research = DomainResearchView(self.config)
        self.view_settings = SettingsDialog(self.config)

        self.stacked_widget.addWidget(self.view_dashboard)   # 0
        self.stacked_widget.addWidget(self.view_adapt)       # 1
        self.stacked_widget.addWidget(self.view_review)      # 2
        self.stacked_widget.addWidget(self.view_lab)         # 3
        self.stacked_widget.addWidget(self.view_research)    # 4
        self.stacked_widget.addWidget(self.view_settings)    # 5

        main_layout.addWidget(self.stacked_widget)

        # Status Bar
        self.status_bar = QStatusBar()
        self.status_bar.showMessage("TTHG Liquid Glass Engine Ready | 100% Local Inference")
        self.setStatusBar(self.status_bar)

    def switch_page(self, index: int):
        self.stacked_widget.setCurrentIndex(index)

    def toggle_floating_hud(self):
        if not self.hud_overlay:
            self.hud_overlay = TTHGWidget(self.config)

        if self.hud_overlay.isHidden():
            self.hud_overlay.show()
            self.status_bar.showMessage("Floating HUD Enabled")
        else:
            self.hud_overlay.hide()
            self.status_bar.showMessage("Floating HUD Hidden")
