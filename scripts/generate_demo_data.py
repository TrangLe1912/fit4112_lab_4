"""Sinh dữ liệu PM2.5 giả lập reproducible cho FIT4112 Lab 4."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.lab4 import generate_demo

if __name__ == "__main__":
    path = generate_demo(ROOT / "data/raw/demo_pm25_hourly.csv")
    print(f"Generated synthetic data: {path}")
