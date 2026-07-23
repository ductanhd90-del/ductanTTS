"""
Main Window - Giao diện PyQt5 cho ductanTTS
"""
import sys
import os
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QLabel, QTextEdit, QPushButton, QComboBox, QSpinBox, 
    QFileDialog, QMessageBox, QProgressBar, QListWidget, QListWidgetItem
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QIcon
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.tts_engine import TTSEngine
from core.voice_cloner import VoiceCloner
from core.audio_utils import AudioUtils


class TTSWorker(QThread):
    """Worker thread cho TTS"""
    finished = pyqtSignal()
    error = pyqtSignal(str)
    success = pyqtSignal(str)
    
    def __init__(self, text, output_file, method='gtts'):
        super().__init__()
        self.text = text
        self.output_file = output_file
        self.method = method
        self.tts_engine = TTSEngine()
    
    def run(self):
        try:
            result = self.tts_engine.text_to_speech(
                self.text,
                self.output_file,
                method=self.method
            )
            if result:
                self.success.emit(result)
            else:
                self.error.emit("Không thể tạo âm thanh")
        except Exception as e:
            self.error.emit(str(e))
        finally:
            self.finished.emit()


class VoiceRecorderWorker(QThread):
    """Worker thread cho ghi âm"""
    finished = pyqtSignal()
    error = pyqtSignal(str)
    success = pyqtSignal(str)
    
    def __init__(self, duration):
        super().__init__()
        self.duration = duration
        self.voice_cloner = VoiceCloner()
    
    def run(self):
        try:
            result = self.voice_cloner.record_voice(self.duration)
            if result:
                self.success.emit(result)
            else:
                self.error.emit("Không thể ghi âm")
        except Exception as e:
            self.error.emit(str(e))
        finally:
            self.finished.emit()


class MainWindow(QMainWindow):
    """Main Window của ứng dụng"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ductanTTS - Vietnamese Text-to-Speech with Voice Cloning")
        self.setGeometry(100, 100, 1000, 700)
        
        # Khởi tạo engines
        self.tts_engine = TTSEngine()
        self.voice_cloner = VoiceCloner()
        self.audio_utils = AudioUtils()
        
        # Setup UI
        self.setup_ui()
    
    def setup_ui(self):
        """Thiết lập giao diện"""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        
        # Title
        title = QLabel("ductanTTS - Chuyển Đổi Văn Bản Thành Âm Thanh")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        main_layout.addWidget(title)
        
        # Tab widget
        tabs = QTabWidget()
        tabs.addTab(self.create_tts_tab(), "📝 Text to Speech")
        tabs.addTab(self.create_voice_clone_tab(), "🎤 Voice Cloning")
        tabs.addTab(self.create_about_tab(), "ℹ️ Về Ứng Dụng")
        
        main_layout.addWidget(tabs)
        central_widget.setLayout(main_layout)
    
    def create_tts_tab(self):
        """Tạo tab Text to Speech"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Input text
        layout.addWidget(QLabel("Nhập văn bản tiếng Việt:"))
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Hãy nhập văn bản bạn muốn chuyển đổi thành âm thanh...")
        self.text_input.setMinimumHeight(150)
        layout.addWidget(self.text_input)
        
        # Method selection
        method_layout = QHBoxLayout()
        method_layout.addWidget(QLabel("Chọn phương thức:"))
        self.method_combo = QComboBox()
        self.method_combo.addItems(["Google TTS (Nhanh)", "Coqui TTS (Chất lượng cao)"])
        method_layout.addWidget(self.method_combo)
        method_layout.addStretch()
        layout.addLayout(method_layout)
        
        # Output file name
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("Tên file output:"))
        self.output_name = QTextEdit()
        self.output_name.setPlaceholderText("my_audio.mp3")
        self.output_name.setMaximumHeight(30)
        output_layout.addWidget(self.output_name)
        layout.addLayout(output_layout)
        
        # Convert button
        self.convert_btn = QPushButton("🔄 Chuyển Đổi")
        self.convert_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 10px;")
        self.convert_btn.clicked.connect(self.on_convert_clicked)
        layout.addWidget(self.convert_btn)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Status
        self.status_label = QLabel("")
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_voice_clone_tab(self):
        """Tạo tab Voice Cloning"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Recording section
        layout.addWidget(QLabel("=== Bước 1: Ghi Âm Giọng của Bạn ==="))
        
        record_layout = QHBoxLayout()
        record_layout.addWidget(QLabel("Thời lượng (giây):"))
        self.record_duration = QSpinBox()
        self.record_duration.setValue(10)
        self.record_duration.setMinimum(5)
        self.record_duration.setMaximum(60)
        record_layout.addWidget(self.record_duration)
        record_layout.addStretch()
        layout.addLayout(record_layout)
        
        self.record_btn = QPushButton("🎤 Bắt Đầu Ghi Âm")
        self.record_btn.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold; padding: 10px;")
        self.record_btn.clicked.connect(self.on_record_clicked)
        layout.addWidget(self.record_btn)
        
        # Voice selection
        layout.addWidget(QLabel("=== Bước 2: Lưu & Chọn Giọng ==="))
        
        voice_layout = QHBoxLayout()
        voice_layout.addWidget(QLabel("Tên giọng:"))
        self.voice_name = QTextEdit()
        self.voice_name.setPlaceholderText("my_voice")
        self.voice_name.setMaximumHeight(30)
        voice_layout.addWidget(self.voice_name)
        
        self.save_voice_btn = QPushButton("💾 Lưu Giọng")
        self.save_voice_btn.setStyleSheet("background-color: #FF9800; color: white; font-weight: bold; padding: 10px;")
        self.save_voice_btn.clicked.connect(self.on_save_voice_clicked)
        voice_layout.addWidget(self.save_voice_btn)
        layout.addLayout(voice_layout)
        
        # Voice list
        layout.addWidget(QLabel("Danh sách giọng đã lưu:"))
        self.voice_list = QListWidget()
        self.refresh_voice_list()
        layout.addWidget(self.voice_list)
        
        # Clone section
        layout.addWidget(QLabel("=== Bước 3: Tạo Âm Thanh với Giọng Clone ==="))
        
        layout.addWidget(QLabel("Nhập văn bản:"))
        self.clone_text_input = QTextEdit()
        self.clone_text_input.setPlaceholderText("Nhập văn bản muốn đọc bằng giọng clone...")
        self.clone_text_input.setMinimumHeight(100)
        layout.addWidget(self.clone_text_input)
        
        clone_btn_layout = QHBoxLayout()
        self.clone_btn = QPushButton("🎵 Tạo Âm Thanh Clone")
        self.clone_btn.setStyleSheet("background-color: #9C27B0; color: white; font-weight: bold; padding: 10px;")
        self.clone_btn.clicked.connect(self.on_clone_clicked)
        clone_btn_layout.addWidget(self.clone_btn)
        clone_btn_layout.addStretch()
        layout.addLayout(clone_btn_layout)
        
        self.clone_status = QLabel("")
        layout.addWidget(self.clone_status)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_about_tab(self):
        """Tạo tab Về Ứng Dụng"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        about_text = QTextEdit()
        about_text.setReadOnly(True)
        about_text.setText("""
<h2>ductanTTS v1.0</h2>
<p><b>Ứng dụng chuyển đổi văn bản thành âm thanh với khả năng clone giọng nói</b></p>

<h3>📋 Tính Năng:</h3>
<ul>
    <li>✅ Chuyển text tiếng Việt → âm thanh</li>
    <li>✅ Clone/nhân bản giọng nói cá nhân</li>
    <li>✅ Hỗ trợ 2 phương thức TTS (Google & Coqui)</li>
    <li>✅ Ghi âm từ microphone</li>
    <li>✅ Lưu file MP3/WAV</li>
</ul>

<h3>🛠️ Công Nghệ:</h3>
<ul>
    <li>Python 3.8+</li>
    <li>PyQt5 - Giao diện desktop</li>
    <li>gTTS - Google Text-to-Speech</li>
    <li>Coqui TTS - TTS offline</li>
    <li>PyAudio - Ghi âm từ microphone</li>
</ul>

<h3>📖 Hướng Dẫn Nhanh:</h3>
<ol>
    <li><b>Text to Speech:</b> Nhập văn bản → Chọn phương thức → Click "Chuyển Đổi"</li>
    <li><b>Voice Cloning:</b> Ghi âm → Lưu giọng → Tạo âm thanh với giọng clone</li>
</ol>

<h3>📝 License:</h3>
<p>MIT License - Tự do sử dụng và phát triển</p>

<h3>👨‍💻 Nhà Phát Triển:</h3>
<p>Dựa trên ý tưởng của cộng đồng lập trình Python</p>

<hr>
<p><i>Cảm ơn bạn đã sử dụng ductanTTS! 🎉</i></p>
        """)
        layout.addWidget(about_text)
        
        widget.setLayout(layout)
        return widget
    
    def on_convert_clicked(self):
        """Xử lý khi click nút Convert"""
        text = self.text_input.toPlainText()
        output_name = self.output_name.toPlainText().strip()
        
        if not text.strip():
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập văn bản!")
            return
        
        if not output_name:
            output_name = "output.mp3"
        
        if not output_name.endswith(('.mp3', '.wav')):
            output_name += '.mp3'
        
        method = 'coqui' if self.method_combo.currentIndex() == 1 else 'gtts'
        
        # Disable button
        self.convert_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(50)
        
        # Start worker
        self.worker = TTSWorker(text, output_name, method)
        self.worker.success.connect(self.on_convert_success)
        self.worker.error.connect(self.on_convert_error)
        self.worker.finished.connect(self.on_convert_finished)
        self.worker.start()
        
        self.status_label.setText("Đang xử lý...")
    
    def on_convert_success(self, file_path):
        """Xử lý khi chuyển đổi thành công"""
        self.progress_bar.setValue(100)
        self.status_label.setText(f"✅ Thành công! File đã lưu: {file_path}")
        QMessageBox.information(self, "Thành Công", f"File âm thanh đã được lưu tại:\n{file_path}")
    
    def on_convert_error(self, error_msg):
        """Xử lý lỗi chuyển đổi"""
        self.status_label.setText(f"❌ Lỗi: {error_msg}")
        QMessageBox.critical(self, "Lỗi", f"Không thể chuyển đổi:\n{error_msg}")
    
    def on_convert_finished(self):
        """Xử lý khi hoàn thành"""
        self.convert_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
    
    def on_record_clicked(self):
        """Xử lý khi click nút ghi âm"""
        self.record_btn.setEnabled(False)
        self.record_btn.setText("⏹️ Đang ghi âm...")
        
        duration = self.record_duration.value()
        
        self.recorder = VoiceRecorderWorker(duration)
        self.recorder.success.connect(self.on_record_success)
        self.recorder.error.connect(self.on_record_error)
        self.recorder.finished.connect(self.on_record_finished)
        self.recorder.start()
    
    def on_record_success(self, file_path):
        """Xử lý khi ghi âm thành công"""
        self.record_btn.setText("🎤 Bắt Đầu Ghi Âm")
        QMessageBox.information(self, "Thành Công", f"Ghi âm đã được lưu tại:\n{file_path}")
        self.voice_cloner.load_voice_sample("current_recording", file_path)
    
    def on_record_error(self, error_msg):
        """Xử lý lỗi ghi âm"""
        self.record_btn.setText("🎤 Bắt Đầu Ghi Âm")
        QMessageBox.critical(self, "Lỗi", f"Không thể ghi âm:\n{error_msg}")
    
    def on_record_finished(self):
        """Xử lý khi hoàn thành ghi âm"""
        self.record_btn.setEnabled(True)
    
    def on_save_voice_clicked(self):
        """Xử lý lưu giọng nói"""
        voice_name = self.voice_name.toPlainText().strip()
        
        if not voice_name:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập tên giọng!")
            return
        
        if "current_recording" not in self.voice_cloner.voice_samples:
            QMessageBox.warning(self, "Lỗi", "Vui lòng ghi âm trước!")
            return
        
        # Lưu voice sample
        self.voice_cloner.voice_samples[voice_name] = self.voice_cloner.voice_samples["current_recording"]
        self.voice_cloner.save_voice_profile(voice_name)
        
        QMessageBox.information(self, "Thành Công", f"Giọng nói '{voice_name}' đã được lưu!")
        self.voice_name.clear()
        self.refresh_voice_list()
    
    def on_clone_clicked(self):
        """Xử lý tạo âm thanh clone"""
        selected_items = self.voice_list.selectedItems()
        
        if not selected_items:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một giọng nói!")
            return
        
        voice_name = selected_items[0].text()
        text = self.clone_text_input.toPlainText()
        
        if not text.strip():
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập văn bản!")
            return
        
        self.clone_btn.setEnabled(False)
        self.clone_status.setText("Đang xử lý...")
        
        # Clone voice
        output_file = f"clone_{voice_name}.mp3"
        result = self.voice_cloner.clone_voice(voice_name, text, output_file)
        
        if result:
            self.clone_status.setText(f"✅ Thành công! File: {result}")
            QMessageBox.information(self, "Thành Công", f"File đã được lưu tại:\n{result}")
        else:
            self.clone_status.setText("❌ Lỗi khi tạo âm thanh")
            QMessageBox.critical(self, "Lỗi", "Không thể tạo âm thanh clone!")
        
        self.clone_btn.setEnabled(True)
    
    def refresh_voice_list(self):
        """Cập nhật danh sách giọng nói"""
        self.voice_list.clear()
        voices = self.voice_cloner.get_voice_samples()
        for voice in voices:
            self.voice_list.addItem(QListWidgetItem(voice))


def main():
    """Hàm main"""
    app = sys.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
