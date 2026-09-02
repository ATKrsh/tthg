"""
TTHG - System Telemetry Collector
Retrieves lightweight CPU, Memory, Disk, and System Uptime metrics.
"""

import time
import logging
from typing import Dict, Any

logger = logging.getLogger("TTHG.SystemInfo")

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False


class SystemInfoCollector:
    """Collects real-time system metrics for the TTHG HUD."""

    @staticmethod
    def get_metrics() -> Dict[str, Any]:
        metrics = {
            "cpu_pct": 0.0,
            "ram_pct": 0.0,
            "ram_used_gb": 0.0,
            "ram_total_gb": 0.0,
            "disk_pct": 0.0,
            "uptime_str": "00:00:00"
        }

        if not PSUTIL_AVAILABLE:
            return metrics

        try:
            metrics["cpu_pct"] = round(psutil.cpu_percent(interval=None), 1)

            mem = psutil.virtual_memory()
            metrics["ram_pct"] = round(mem.percent, 1)
            metrics["ram_used_gb"] = round(mem.used / (1024 ** 3), 1)
            metrics["ram_total_gb"] = round(mem.total / (1024 ** 3), 1)

            disk = psutil.disk_usage("/")
            metrics["disk_pct"] = round(disk.percent, 1)

            uptime_sec = time.time() - psutil.boot_time()
            hours = int(uptime_sec // 3600)
            minutes = int((uptime_sec % 3600) // 60)
            seconds = int(uptime_sec % 60)
            metrics["uptime_str"] = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

        except Exception as e:
            logger.error(f"Error collecting system metrics: {e}")

        return metrics
