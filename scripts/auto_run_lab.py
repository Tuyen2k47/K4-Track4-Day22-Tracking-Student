#!/usr/bin/env python
"""Tự động chạy toàn bộ quy trình tracking cho 5 video theo cấu hình tối ưu.

Chạy script này sau khi đã có thư mục dữ liệu ``lab_data``:
    python scripts/auto_run_lab.py --lab-data-root "$LAB_DATA"
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict


def get_recommended_configs() -> Dict[str, Dict[str, Any]]:
    """Trả về cấu hình tracker và ngưỡng detector được tối ưu cho từng video.

    Returns:
        Dict chứa tên tracker, conf, iou và lý do chọn cho video_1 đến video_5.
    """
    return {
        "video_1": {
            "tracker": "bytetrack",
            "conf": 0.3,
            "iou": 0.5,
            "reason": "Quảng trường tĩnh, chuyển động đều, ByteTrack giữ ID mượt và tốc độ cao",
        },
        "video_2": {
            "tracker": "strongsort",
            "conf": 0.25,
            "iou": 0.5,
            "reason": "Phố đêm rất đông, che khuất nhiều; Re-ID của StrongSORT giúp tránh nhảy ID",
        },
        "video_3": {
            "tracker": "ocsort",
            "conf": 0.25,
            "iou": 0.45,
            "reason": "Camera di động, fps chậm; OCSORT khắc phục quán tính và mất dấu tốt",
        },
        "video_4": {
            "tracker": "botsort",
            "conf": 0.35,
            "iou": 0.5,
            "reason": "Trong nhà có phản chiếu kính; conf cao lọc phản chiếu, BoT-SORT có CMC bù camera",
        },
        "video_5": {
            "tracker": "botsort",
            "conf": 0.3,
            "iou": 0.5,
            "reason": "Xe bus rung lắc, giao lộ đông; BoT-SORT hỗ trợ CMC bù rung lắc kết hợp Re-ID",
        },
    }


def run_all(lab_data_root: Path, out_dir: Path, device: str = "cpu", max_frames: int = 0) -> None:
    """Chạy lần lượt cả 5 video với cấu hình tối ưu.

    Args:
        lab_data_root: Thư mục dữ liệu chứa video_1 đến video_5.
        out_dir: Thư mục xuất kết quả (ví dụ runs/nop_bai).
        device: Thiết bị tính toán ('cpu' hoặc 'cuda:0').
        max_frames: Giới hạn frame (0 để chạy toàn bộ).

    Raises:
        FileNotFoundError: Nếu thiếu thư mục ảnh của bất kỳ video nào.
    """
    configs = get_recommended_configs()
    out_dir.mkdir(parents=True, exist_ok=True)

    for seq_name, cfg in configs.items():
        src = lab_data_root / seq_name / "img1"
        if not src.exists():
            raise FileNotFoundError(f"Không tìm thấy thư mục ảnh: {src}")

        cmd = [
            sys.executable,
            "scripts/run_tracking.py",
            "--source", str(src),
            "--seq-name", seq_name,
            "--tracker", cfg["tracker"],
            "--conf", str(cfg["conf"]),
            "--iou", str(cfg["iou"]),
            "--out", str(out_dir),
            "--device", device,
            "--save-video",
        ]
        if max_frames > 0:
            cmd.extend(["--max-frames", str(max_frames)])

        print(f"\n>>> Đang chạy {seq_name} ({cfg['tracker']}, conf={cfg['conf']}, iou={cfg['iou']})...")
        subprocess.run(cmd, check=True)


def parse_args() -> argparse.Namespace:
    """Khai báo tham số dòng lệnh.

    Returns:
        Namespace chứa các tham số đã parse.
    """
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--lab-data-root", required=True, type=Path, help="Đường dẫn thư mục lab_data")
    parser.add_argument("--out", default=Path("runs/nop_bai"), type=Path, help="Thư mục xuất kết quả")
    parser.add_argument("--device", default="cpu", help="'cpu' hoặc 'cuda:0'")
    parser.add_argument("--max-frames", type=int, default=0, help="Giới hạn số frame (0 = chạy hết)")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run_all(args.lab_data_root, args.out, device=args.device, max_frames=args.max_frames)
