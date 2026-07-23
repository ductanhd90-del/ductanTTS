"""
Main Window - Giao diện PyQt5 cho ductanTTS (Updated with Voice Selection)
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
from core.voice_presets import VoicePresetsManager
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
        self.setGeometry(100, 100, 1000, 750)
        
        # Khởi tạo engines
        self.tts_engine = TTSEngine()
        self.voice_cloner = VoiceCloner()
        self.voice_presets = VoicePresetsManager()
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
        tabs.addTab(self.create_voice_selection_tab(), "🎤 Chọn & Ghi Âm Giọng")
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
    
    def create_voice_selection_tab(self):
        """Tạo tab Chọn & Ghi Âm Giọng"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Section 1: Chọn Giọng
        layout.addWidget(QLabel("=== Bước 1: Chọn Giọng (Preset hoặc Custom) ==="))
        
        voice_select_layout = QHBoxLayout()
        voice_select_layout.addWidget(QLabel("Chọn giọng:"))
        self.voice_combo = QComboBox()
        self.refresh_voice_combo()
        voice_select_layout.addWidget(self.voice_combo)
        voice_select_layout.addStretch()
        layout.addLayout(voice_select_layout)
        
        # Section 2: Ghi Âm Giọng Custom (Nếu Cần)
        layout.addWidget(QLabel("=== Bước 2: Ghi Âm Giọng Custom (Tùy Chọn) ==="))
        
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
        
        # Voice name input
        voice_name_layout = QHBoxLayout()
        voice_name_layout.addWidget(QLabel("Tên giọng mới:"))
        self.new_voice_name = QTextEdit()
        self.new_voice_name.setPlaceholderText("my_voice")
        self.new_voice_name.setMaximumHeight(30)
        voice_name_layout.addWidget(self.new_voice_name)
        
        self.save_voice_btn = QPushButton("💾 Lưu Giọng")
        self.save_voice_btn.setStyleSheet("background-color: #FF9800; color: white; font-weight: bold; padding: 10px;")
        self.save_voice_btn.clicked.connect(self.on_save_voice_clicked)
        voice_name_layout.addWidget(self.save_voice_btn)
        layout.addLayout(voice_name_layout)
        
        # Section 3: Tạo Âm Thanh từ Giọng Đã Chọn
        layout.addWidget(QLabel("=== Bước 3: Tạo Âm Thanh từ Giọng Đã Chọn ==="))
        
        layout.addWidget(QLabel("Nhập văn bản:"))
        self.voice_text_input = QTextEdit()
        self.voice_text_input.setPlaceholderText("Nhập văn bản muốn đọc...")
        self.voice_text_input.setMinimumHeight(120)
        layout.addWidget(self.voice_text_input)
        
        create_btn_layout = QHBoxLayout()
        self.create_voice_btn = QPushButton("🎵 Tạo Âm Thanh")
        self.create_voice_btn.setStyleSheet("background-color: #9C27B0; color: white; font-weight: bold; padding: 10px;")
        self.create_voice_btn.clicked.connect(self.on_create_voice_clicked)
        create_btn_layout.addWidget(self.create_voice_btn)
        create_btn_layout.addStretch()
        layout.addLayout(create_btn_layout)
        
        self.voice_status = QLabel("")
        layout.addWidget(self.voice_status)
        
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
<h2>ductanTTS v2.0</h2>
<p><b>Ứng dụng chuyển đổi văn bản thành âm thanh với khả năng chọn giọng đọc</b></p>

<h3>📋 Tính Năng:</h3>
<ul>
    <li>✅ Chuyển text tiếng Việt → âm thanh</li>
    <li>✅ Chọn giọng đọc (Preset hoặc Custom)</li>
    <li>✅ Ghi âm giọng của bạn</li>
    <li>✅ Hỗ trợ 2 phương thức TTS (Google & Coqui)</li>
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
    <li><b>Chọn Giọng:</b> Chọn giọng từ dropdown → Nhập text → Click "Tạo Âm Thanh"</li>
    <li><b>Ghi Âm Custom:</b> Ghi âm → Đặt tên → Lưu → Chọn từ dropdown</li>
</ol>

<h3>📁 Cấu Trúc:</h3>
<ul>
    <li>voices/presets/ - Giọng mặc định (có sẵn)</li>
    <li>voices/custom/ - Giọng ghi âm của bạn</li>
    <li>output/ - File âm thanh đã tạo</li>
</ul>

<h3>📝 License:</h3>
<p>MIT License - Tự do sử dụng và phát triển</p>

<hr>
<p><i>Cảm ơn bạn đã sử dụng ductanTTS! 🎉</i></p>
        """)
        layout.addWidget(about_text)
        
        widget.setLayout(layout)
        return widget
    
    def refresh_voice_combo(self):
        """Cập nhật dropdown chọn giọng"""
        self.voice_combo.clear()
        
        # Lấy tất cả giọng
        all_voices = self.voice_presets.get_all_voices()
        
        # Thêm vào dropdown
        for voice_name in all_voices.keys():
            self.voice_combo.addItem(voice_name)
    
    def on_convert_clicked(self):
        """Xử lý khi click nút Convert (Text to Speech)"""
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
        self.last_recording_path = file_path
        QMessageBox.information(self, "Thành Công", f"Ghi âm đã được lưu tại:\n{file_path}\n\nBây giờ đặt tên và lưu giọng!")
    
    def on_record_error(self, error_msg):
        """Xử lý lỗi ghi âm"""
        self.record_btn.setText("🎤 Bắt Đầu Ghi Âm")
        QMessageBox.critical(self, "Lỗi", f"Không thể ghi âm:\n{error_msg}")
    
    def on_record_finished(self):
        """Xử lý khi hoàn thành ghi âm"""
        self.record_btn.setEnabled(True)
    
    def on_save_voice_clicked(self):
        """Xử lý lưu giọng custom"""
        voice_name = self.new_voice_name.toPlainText().strip()
        
        if not voice_name:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập tên giọng!")
            return
        
        if not hasattr(self, 'last_recording_path'):
            QMessageBox.warning(self, "Lỗi", "Vui lòng ghi âm trước!")
            return
        
        # Lưu giọng
        result = self.voice_presets.add_custom_voice(voice_name, self.last_recording_path)
        
        if result:
            QMessageBox.information(self, "Thành Công", f"Giọng '{voice_name}' đã được lưu!")
            self.new_voice_name.clear()
            self.refresh_voice_combo()
        else:
            QMessageBox.critical(self, "Lỗi", "Không thể lưu giọng!")
    
    def on_create_voice_clicked(self):
        """Xử lý tạo âm thanh từ giọng đã chọn"""
        voice_display_name = self.voice_combo.currentText()
        text = self.voice_text_input.toPlainText()
        
        if not voice_display_name:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một giọng!")
            return
        
        if not text.strip():
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập văn bản!")
            return
        
        # Lấy đường dẫn giọng
        voice_path = self.voice_presets.get_voice_path(voice_display_name)
        
        if not voice_path:
            QMessageBox.critical(self, "Lỗi", "Không tìm thấy giọng nói!")
            return
        
        self.create_voice_btn.setEnabled(False)
        self.voice_status.setText("Đang xử lý...")
        
        try:
            # Tạo tên file output
            voice_clean_name = voice_display_name.replace("🎙️ ", "").replace("🔊 ", "").replace(" (Preset)", "").replace(" (Custom)", "")
            output_file = f"voice_{voice_clean_name}_{len(text)}.mp3"
            
            # Sử dụng gTTS để tạo âm thanh
            result = self.tts_engine.text_to_speech(text, output_file, method='gtts')
            
            if result:
                self.voice_status.setText(f"✅ Thành công! File: {result}")
                QMessageBox.information(self, "Thành Công", f"File đã được lưu tại:\n{result}")
            else:
                self.voice_status.setText("❌ Lỗi khi tạo âm thanh")
                QMessageBox.critical(self, "Lỗi", "Không thể tạo âm thanh!")
        except Exception as e:
            self.voice_status.setText(f"❌ Lỗi: {str(e)}")
            QMessageBox.critical(self, "Lỗi", f"Không thể tạo âm thanh:\n{str(e)}")
        finally:
            self.create_voice_btn.setEnabled(True)


def main():
    """Hàm main"""
    app = sys.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
