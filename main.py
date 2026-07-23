#!/usr/bin/env python3
"""
ductanTTS - Vietnamese Text-to-Speech with Voice Cloning
Main entry point
"""

import sys
import os

# Thêm thư mục hiện tại vào Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.main_window import MainWindow
from PyQt5.QtWidgets import QApplication


def main():
    """Main function"""
    app = QApplication(sys.argv)
    
    # Tạo main window
    window = MainWindow()
    window.show()
    
    # Chạy ứng dụng
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
