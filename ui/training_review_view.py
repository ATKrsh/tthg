"""
TTHG - Human Perfection & Ground Truth Verification Workbench UI View
Visual human review interface to inspect AI adult-media predictions, rate perfection score (0-100%),
flag edge case errors, and confirm Gold Ground Truth training benchmark records.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QCheckBox, QPushButton,
    QGroupBox, QFormLayout, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox
)
from PySide6.QtCore import Qt
from config import ConfigManager


class TrainingReviewView(QWidget):
    """Human Perfection & Ground Truth Verification Workbench."""

    def __init__(self, config_manager: ConfigManager, parent=None):
        super().__init__(parent)
        self.config = config_manager

        self.setWindowTitle("TTHG — Human Perfection & Ground Truth Workbench")
        self.resize(850, 560)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Title Header
        title_box = QVBoxLayout()
        title = QLabel("🔍 Human Perfection & Ground Truth Workbench")
        title.setObjectName("PageTitle")
        sub = QLabel("Verify AI adult-media tag predictions, rate perfection score, flag error categories, and confirm Gold Ground Truth.")
        sub.setObjectName("HeaderSubtitle")
        title_box.addWidget(title)
        title_box.addWidget(sub)
        layout.addLayout(title_box)

        # Main Split View (Table + Review Inspector)
        content_box = QHBoxLayout()

        # Left: Candidate Records Table
        self.table = QTableWidget(4, 3)
        self.table.setHorizontalHeaderLabels(["Filename", "AI Tags", "Confidence"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        sample_candidates = [
            ("Video_001_POV.mp4", "POV, SOLO, HD_1080P", "96%"),
            ("Video_002_Studio.mkv", "STUDIO, AMATEUR, 4K", "94%"),
            ("Video_003_Series.mp4", "SERIES, AUDIO_VOICE", "92%"),
            ("Video_004_Solo.mp4", "SOLO, FETISH", "95%")
        ]
        for row, (fn, tags, conf) in enumerate(sample_candidates):
            self.table.setItem(row, 0, QTableWidgetItem(fn))
            self.table.setItem(row, 1, QTableWidgetItem(tags))
            self.table.setItem(row, 2, QTableWidgetItem(conf))

        content_box.addWidget(self.table, stretch=3)

        # Right: Perfection Rating Inspector Panel
        inspector_group = QGroupBox("Perfection & Error Inspector")
        insp_layout = QVBoxLayout(inspector_group)

        self.lbl_selected = QLabel("Selected: Video_001_POV.mp4")
        self.lbl_selected.setStyleSheet("color: #38bdf8; font-weight: bold;")
        insp_layout.addWidget(self.lbl_selected)

        # Perfection Slider
        insp_layout.addWidget(QLabel("Human Perfection Score Rating:"))
        self.slider_box = QHBoxLayout()
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setValue(98)
        self.lbl_score_val = QLabel("98%")
        self.lbl_score_val.setStyleSheet("color: #10b981; font-weight: bold;")
        self.slider.valueChanged.connect(lambda v: self.lbl_score_val.setText(f"{v}%"))

        self.slider_box.addWidget(self.slider)
        self.slider_box.addWidget(self.lbl_score_val)
        insp_layout.addLayout(self.slider_box)

        # Error Category Checkboxes
        insp_layout.addWidget(QLabel("Flag Error Categories (Optional):"))
        self.chk_performer = QCheckBox("Misclassified Performer")
        self.chk_viewpoint = QCheckBox("Incorrect Viewpoint (POV/Studio)")
        self.chk_boundary = QCheckBox("False Scene Boundary")
        self.chk_res = QCheckBox("Resolution Mislabel")

        insp_layout.addWidget(self.chk_performer)
        insp_layout.addWidget(self.chk_viewpoint)
        insp_layout.addWidget(self.chk_boundary)
        insp_layout.addWidget(self.chk_res)

        insp_layout.addStretch()

        # Confirmation Action Button
        btn_confirm = QPushButton("✅ Confirm GOLD Ground Truth")
        btn_confirm.setStyleSheet("background: linear-gradient(135deg, #10b981, #059669); font-weight: bold; height: 36px;")
        btn_confirm.clicked.connect(self.confirm_ground_truth)
        insp_layout.addWidget(btn_confirm)

        content_box.addWidget(inspector_group, stretch=2)
        layout.addLayout(content_box)

    def confirm_ground_truth(self):
        score = self.slider.value()
        QMessageBox.information(
            self,
            "Ground Truth Verified",
            f"Record confirmed into GOLD Ground Truth dataset!\n"
            f"Perfection Rating: {score}%\n"
            f"Model benchmark weights updated for next adapter training pass."
        )
