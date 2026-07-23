# ductanTTS - Vietnamese Text-to-Speech with Voice Cloning

**ductanTTS** là một ứng dụng desktop chuyên biệt cho việc chuyển đổi văn bản tiếng Việt thành file âm thanh với khả năng nhân bản giọng nói cá nhân.

## 🎯 Tính Năng

- ✅ **Chuyển text → âm thanh** hỗ trợ tiếng Việt
- ✅ **Clone/Nhân bản giọng nói** - Ghi âm giọng của bạn rồi dùng cho văn bản khác
- ✅ **Giao diện desktop** dễ sử dụng
- ✅ **Lưu file âm thanh** (MP3, WAV)
- ✅ **Hoàn toàn miễn phí** và offline

## 🚀 Cài Đặt

### Yêu cầu
- Python 3.8+
- pip (package manager)

### Bước 1: Clone repository
```bash
git clone https://github.com/ductanhd90-del/ductanTTS.git
cd ductanTTS
```

### Bước 2: Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### Bước 3: Chạy ứng dụng
```bash
python main.py
```

## 📖 Hướng Dẫn Sử Dụng

### 1. Chuyển Text Thành Âm Thanh
1. Mở ứng dụng
2. Chọn tab **"Text to Speech"**
3. Nhập văn bản tiếng Việt
4. Chọn giọng đọc yêu thích
5. Click **"Chuyển Đổi"** → File sẽ được lưu trong thư mục `output/`

### 2. Clone Giọng Nói
1. Chọn tab **"Voice Cloning"**
2. Click **"Ghi Âm Giọng"** → Ghi âm giọng của bạn (10-30 giây)
3. Click **"Lưu Giọng"** 
4. Nhập văn bản muốn đọc bằng giọng clone của bạn
5. Click **"Tạo Âm Thanh"** → File output sẽ có giọng của bạn

## 🛠️ Cấu Trúc Dự Án

```
ductanTTS/
├── README.md                 # Hướng dẫn này
├── requirements.txt          # Danh sách thư viện
├── main.py                   # Entry point
├── ui/
│   └── main_window.py        # Giao diện PyQt5
├── core/
│   ├── tts_engine.py         # Engine TTS
│   ├── voice_cloner.py       # Voice cloning
│   └── audio_utils.py        # Xử lý âm thanh
├── models/                   # Lưu models AI
└── output/                   # Lưu file âm thanh output
```

## 📝 Công Nghệ Sử Dụng

- **PyQt5** - Giao diện desktop
- **gTTS** - Google Text-to-Speech (miễn phí)
- **Coqui TTS** - TTS offline, chất lượng cao
- **RVC (Real-time Voice Conversion)** - Clone giọng nói
- **pydub** - Xử lý âm thanh

## 🤝 Góp Ý & Phát Triển

Nếu bạn có ý tưởng mới hoặc phát hiện lỗi, vui lòng:
1. Tạo issue mới
2. Hoặc pull request với cải tiến

## 📄 License

MIT License - Bạn tự do sử dụng và phát triển

---

**Bắt đầu sử dụng ngay!** 🎉
