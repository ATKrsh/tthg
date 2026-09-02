"""
TTHG - Main Application Entry Point & System Tray Manager
Launches Liquid Glass MainWindow with System Tray overlay options and exception crash handler.
"""

import sys
import os
import traceback
import logging
from pathlib import Path

# ── PyInstaller frozen-exe path resolution ──────────────────────────────────
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys._MEIPASS)
    APP_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).parent.resolve()
    APP_DIR = BASE_DIR

sys.path.insert(0, str(BASE_DIR))

# Directories
DATA_DIR = APP_DIR / "data"
LOGS_DIR = APP_DIR / "logs"
DATA_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# File Logging Setup
log_file = LOGS_DIR / "tthg.log"
logging.basicConfig(
    filename=log_file,
    filemode="a",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("TTHG.App")

from PySide6.QtWidgets import (
    QApplication, QSystemTrayIcon, QMenu, QMessageBox
)
from PySide6.QtGui import QIcon, QAction, QPixmap, QPainter, QColor
from PySide6.QtCore import Qt

from config import ConfigManager
from ui.styles import TTHG_STYLE
from ui.main_window import MainWindow


def _write_crash(exc: Exception) -> None:
    """Write crash report to tthg/logs/crash.log and attempt Qt notification."""
    crash_path = LOGS_DIR / "crash.log"
    with open(crash_path, "a", encoding="utf-8") as f:
        f.write("\n=== TTHG Crash Report ===\n")
        traceback.print_exc(file=f)
    logger.error(f"Uncaught exception: {exc}")


def create_tray_icon_pixmap() -> QPixmap:
    """Generate a high-DPI programmatic icon for the tray."""
    pix = QPixmap(64, 64)
    pix.fill(Qt.transparent)
    painter = QPainter(pix)
    painter.setRenderHint(QPainter.Antialiasing)

    painter.setBrush(QColor("#06b6d4"))
    painter.setPen(Qt.NoPen)
    painter.drawRoundedRect(4, 4, 56, 56, 16, 16)

    painter.setBrush(QColor("#ffffff"))
    painter.drawEllipse(20, 20, 24, 24)

    painter.end()
    return pix


def main():
    logger.info("Starting TTHG Liquid Glass Application...")
    try:
        app = QApplication(sys.argv)
        app.setQuitOnLastWindowClosed(True)
        app.setStyleSheet(TTHG_STYLE)

        config_manager = ConfigManager()

        # Launch Main Window
        main_win = MainWindow(config_manager)
        main_win.show()

        # System Tray Icon Setup
        tray_icon = QSystemTrayIcon(QIcon(create_tray_icon_pixmap()), app)
        tray_icon.setToolTip("TTHG — Liquid Glass Engine")

        tray_menu = QMenu()

        show_win_action = QAction("Open Main Window", app)
        show_win_action.triggered.connect(lambda: main_win.show() if main_win.isHidden() else main_win.raise_())

        toggle_hud_action = QAction("🔲 Toggle Floating HUD", app)
        toggle_hud_action.triggered.connect(main_win.toggle_floating_hud)

        quit_action = QAction("Exit TTHG", app)
        quit_action.triggered.connect(app.quit)

        tray_menu.addAction(show_win_action)
        tray_menu.addAction(toggle_hud_action)
        tray_menu.addSeparator()
        tray_menu.addAction(quit_action)

        tray_icon.setContextMenu(tray_menu)
        tray_icon.show()

        ret = app.exec()
        logger.info("TTHG Application exiting cleanly.")
        sys.exit(ret)

    except Exception as exc:
        _write_crash(exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
