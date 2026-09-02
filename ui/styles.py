"""
TTHG - Liquid Glass QSS Design System
Vibrant cyan, dark slate, and purple neon glassmorphism aesthetic with soft depth and smooth interaction states.
"""

TTHG_STYLE = """
QMainWindow, QDialog, QWidget {
    background-color: #080c14;
    color: #f1f5f9;
    font-family: 'Segoe UI', Inter, sans-serif;
    font-size: 13px;
}

/* Glassmorphism Card Panels */
#GlassCard {
    background-color: rgba(15, 23, 42, 0.75);
    border: 1px solid rgba(56, 189, 248, 0.25);
    border-radius: 16px;
}

#GlassCardHover:hover {
    border: 1px solid rgba(56, 189, 248, 0.55);
    background-color: rgba(30, 41, 59, 0.85);
}

/* Headings */
#PageTitle {
    color: #38bdf8;
    font-size: 20px;
    font-weight: 800;
    letter-spacing: 0.5px;
}

#HeaderSubtitle {
    color: #94a3b8;
    font-size: 12px;
}

#SectionTitle {
    color: #c084fc;
    font-size: 14px;
    font-weight: 700;
}

/* Sidebar Navigation */
#SidebarWidget {
    background-color: rgba(11, 15, 25, 0.95);
    border-right: 1px solid rgba(56, 189, 248, 0.2);
}

#NavButton {
    background-color: transparent;
    color: #94a3b8;
    border: none;
    border-radius: 10px;
    padding: 10px 14px;
    text-align: left;
    font-weight: 600;
    font-size: 13px;
}

#NavButton:hover {
    background-color: rgba(56, 189, 248, 0.15);
    color: #38bdf8;
}

#NavButtonActive {
    background: linear-gradient(135deg, rgba(2, 132, 199, 0.4) 0%, rgba(37, 99, 235, 0.4) 100%);
    color: #38bdf8;
    border: 1px solid rgba(56, 189, 248, 0.5);
    font-weight: 700;
}

/* Buttons */
QPushButton {
    background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%);
    color: #ffffff;
    border: none;
    border-radius: 9px;
    padding: 8px 16px;
    font-weight: 600;
}

QPushButton:hover {
    background: linear-gradient(135deg, #38bdf8 0%, #60a5fa 100%);
}

QPushButton:pressed {
    background-color: #1d4ed8;
}

QPushButton#AccentBtn {
    background: linear-gradient(135deg, #7c3aed 0%, #c084fc 100%);
}

QPushButton#AccentBtn:hover {
    background: linear-gradient(135deg, #8b5cf6 0%, #d8b4fe 100%);
}

QPushButton#SuccessBtn {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

QPushButton#SuccessBtn:hover {
    background: linear-gradient(135deg, #34d399 0%, #10b981 100%);
}

/* Progress Bars */
QProgressBar {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 6px;
    height: 16px;
    text-align: center;
    color: #f8fafc;
    font-size: 11px;
    font-weight: bold;
}

QProgressBar::chunk {
    background: linear-gradient(90deg, #06b6d4 0%, #3b82f6 100%);
    border-radius: 5px;
}

/* Form Inputs & Tables */
QLineEdit, QSpinBox, QTextEdit, QPlainTextEdit {
    background-color: #0f172a;
    border: 1px solid #334155;
    border-radius: 8px;
    color: #f8fafc;
    padding: 8px 12px;
}

QLineEdit:focus, QTextEdit:focus {
    border: 1px solid #38bdf8;
}

QTableWidget {
    background-color: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 10px;
    gridline-color: #1e293b;
    color: #e2e8f0;
}

QTableWidget::item:selected {
    background-color: rgba(56, 189, 248, 0.25);
    color: #ffffff;
}

QHeaderView::section {
    background-color: #1e293b;
    color: #38bdf8;
    padding: 8px;
    font-weight: bold;
    border: none;
}

QGroupBox {
    background-color: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(56, 189, 248, 0.2);
    border-radius: 12px;
    margin-top: 12px;
    font-weight: bold;
    color: #38bdf8;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
}
"""
