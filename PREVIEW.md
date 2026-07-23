## 🎨 ductanTTS - Giao Diện Ứng Dụng

Đây là hình ảnh preview giao diện ứng dụng khi chạy trên máy.

---

## 📱 Cửa Sổ Chính

```
╔═══════════════════════════════════════════════════════════════════════════╗
║  ductanTTS - Vietnamese Text-to-Speech with Voice Cloning                 ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                            ║
║  ductanTTS - Chuyển Đổi Văn Bản Thành Âm Thanh                            ║
║                                                                            ║
║  ┌─ 📝 Text to Speech ─ 🎤 Voice Cloning ─ ℹ️ Về Ứng Dụng ────────────┐  ║
║  │                                                                      │  ║
║  │  [Nội dung của các tab sẽ hiển thị ở đây]                           │  ║
║  │                                                                      │  ║
║  └──────────────────────────────────────────────────────────────────────┘  ║
║                                                                            ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

---

## 📝 TAB 1: Text to Speech

```
┌────────────────────────────────────────────────────────────────┐
│ Nhập văn bản tiếng Việt:                                       │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ H��y nhập văn bản bạn muốn chuyển đổi thành âm thanh... │ │
│  │                                                          │ │
│  │ "Xin chào, đây là giọng đọc tự động tiếng Việt"        │ │
│  │                                                          │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
│ Chọn phương thức: [Google TTS (Nhanh) ▼]                     │
│                                                                │
│ Tên file output:                                              │
│  ┌────────────────────┐                                       │
│  │ my_audio.mp3       │                                       │
│  └────────────────────┘                                       │
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ 🔄 Chuyển Đổi                                           │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
│  Progress: [████████████░░░░░] 50%                            │
│                                                                │
│  ✅ Thành công! File đã lưu: output/my_audio.mp3             │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### Chức Năng:
- ✅ Nhập văn bản tiếng Việt
- ✅ Chọn 2 phương thức:
  - **Google TTS** - Nhanh, miễn phí, cần internet
  - **Coqui TTS** - Offline, chất lượng cao
- ✅ Đặt tên file output
- ✅ Hiển thị progress bar
- ✅ Thông báo thành công/lỗi

---

## 🎤 TAB 2: Voice Cloning

```
┌────────────────────────────────────────────────────────────────┐
│ === Bước 1: Ghi Âm Giọng của Bạn ===                          │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  Thời lượng (giây): [10  ▲▼]                                  │
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ 🎤 Bắt Đầu Ghi Âm                                       │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
│ === Bước 2: Lưu & Chọn Giọng ===                              │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  Tên giọng: ┌──────────────┐      ┌──────────────────────┐   │
│             │ my_voice     │      │ 💾 Lưu Giọng        │   │
│             └──────────────┘      └──────────────────────┘   │
│                                                                │
│  Danh sách giọng đã lưu:                                      │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ • my_voice                                              │ │
│  │ • voice_dad                                             │ │
│  │ • voice_mom                                             │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
│ === Bước 3: Tạo Âm Thanh với Giọng Clone ===                 │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  Nhập văn bản:                                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ Nhập văn bản muốn đọc bằng giọng clone...              │ │
│  │                                                          │ │
│  │ "Tôi là một tính năng clone giọng nói"                 │ │
│  │                                                          │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ 🎵 Tạo Âm Thanh Clone                                  │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
│  ✅ Thành công! File: clone_my_voice.mp3                     │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### Chức Năng:
- ✅ **Bước 1:** Ghi âm từ microphone (5-60 giây)
- ✅ **Bước 2:** Lưu profile giọng nói + quản lý danh sách
- ✅ **Bước 3:** Tạo âm thanh với giọng clone

---

## ℹ️ TAB 3: Về Ứng Dụng

```
┌────────────────────────────────────────────────────────────────┐
│                                                                │
│                    ductanTTS v1.0                             │
│                                                                │
│  Ứng dụng chuyển đổi văn bản thành âm thanh với khả năng      │
│  clone giọng nói cá nhân                                       │
│                                                                │
│  📋 Tính Năng:                                                 │
│  ✅ Chuyển text tiếng Việt → âm thanh                         │
│  ✅ Clone/nhân bản giọng nói cá nhân                          │
│  ✅ Hỗ trợ 2 phương thức TTS (Google & Coqui)                │
│  ✅ Ghi âm từ microphone                                      │
│  ✅ Lưu file MP3/WAV                                         │
│                                                                │
│  🛠️ Công Nghệ:                                                │
│  • Python 3.8+                                                │
│  • PyQt5 - Giao diện desktop                                  │
│  • gTTS - Google Text-to-Speech                               │
│  • Coqui TTS - TTS offline                                    │
│  • PyAudio - Ghi âm từ microphone                             │
│                                                                │
│  📖 Hướng Dẫn Nhanh:                                           │
│  1. Text to Speech: Nhập văn bản → Chọn phương thức →        │
│     Click "Chuyển Đổi"                                        │
│  2. Voice Cloning: Ghi âm → Lưu giọng → Tạo âm thanh        │
│     với giọng clone                                           │
│                                                                │
│  📝 License: MIT License - Tự do sử dụng và phát triển       │
│                                                                │
│  👨‍💻 Nhà Phát Triển:                                            │
│  Dựa trên ý tưởng của cộng đồng lập trình Python            │
│                                                                │
│  Cảm ơn bạn đã sử dụng ductanTTS! 🎉                          │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

## 📂 Cấu Trúc Thư Mục:

```
ductanTTS/
├── main.py                    # Entry point
├── requirements.txt           # Dependencies
├── .gitignore                # Git ignore
├── README.md                 # Hướng dẫn
├── PREVIEW.md                # File này
├── core/
│   ├── __init__.py
│   ├── tts_engine.py         # Google TTS + Coqui TTS
│   ├── voice_cloner.py       # Ghi âm + Clone giọng
│   └── audio_utils.py        # Xử lý âm thanh
├── ui/
│   ├── __init__.py
│   └── main_window.py        # PyQt5 GUI
├── output/                   # 📁 File MP3 output
├── voices/                   # 📁 Profile giọng nói
└── models/                   # 📁 Models AI (Coqui TTS)
```

---

## 🎯 Workflow Sử Dụng:

### **Workflow 1: Text to Speech**
```
Nhập text Việt
     ↓
Chọn phương thức TTS
     ↓
Đặt tên file output
     ↓
Click "Chuyển Đổi"
     ↓
✅ File MP3 được lưu trong output/
```

### **Workflow 2: Voice Cloning**
```
Ghi âm giọng (Bước 1)
     ↓
Đặt tên giọng (Bước 2)
     ↓
Lưu profile giọng
     ↓
Chọn giọng từ danh sách
     ↓
Nhập text muốn đọc (Bước 3)
     ↓
Click "Tạo Âm Thanh Clone"
     ↓
✅ File MP3 với giọng clone được tạo
```

---

## 🚀 Để Chạy Thực Tế:

```bash
# Clone repository
git clone https://github.com/ductanhd90-del/ductanTTS.git
cd ductanTTS

# Tạo virtual environment
python -m venv venv
source venv/bin/activate  # Mac/Linux

# Cài đặt dependencies
pip install -r requirements.txt

# Chạy ứng dụng
python main.py
```

---

## 📝 Ghi Chú:

- Lần đầu chạy Coqui TTS sẽ tải model (~500MB)
- Google TTS cần kết nối internet
- PyAudio cần cài riêng cho ghi âm
- File output được lưu trong folder `output/`

---

**Bây giờ bạn có thể xem trước giao diện! Sẵn sàng chạy thử chưa?** 😊
