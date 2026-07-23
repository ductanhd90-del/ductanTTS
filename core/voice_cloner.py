"""
Voice Cloner - Nhân bản giọng nói
"""
import os
import numpy as np
from .audio_utils import AudioUtils


class VoiceCloner:
    """Lớp nhân bản/clone giọng nói"""
    
    def __init__(self):
        """Khởi tạo Voice Cloner"""
        self.audio_utils = AudioUtils()
        self.audio_utils.create_output_directory()
        self.voice_samples = {}  # Lưu trữ sample giọng
        
    def record_voice(self, duration_seconds=10):
        """
        Ghi âm giọng (cần PyAudio)
        
        Args:
            duration_seconds: thời lượng ghi âm (giây)
            
        Returns:
            đường dẫn file ghi âm
        """
        try:
            import pyaudio
            import wave
            
            CHUNK = 1024
            FORMAT = pyaudio.paFloat32
            CHANNELS = 1
            RATE = 22050
            
            p = pyaudio.PyAudio()
            
            print(f"Đang ghi âm trong {duration_seconds} giây...")
            
            stream = p.open(format=FORMAT,
                          channels=CHANNELS,
                          rate=RATE,
                          input=True,
                          frames_per_buffer=CHUNK)
            
            frames = []
            for _ in range(0, int(RATE / CHUNK * duration_seconds)):
                data = stream.read(CHUNK)
                frames.append(data)
            
            print("Ghi âm xong!")
            
            stream.stop_stream()
            stream.close()
            p.terminate()
            
            # Lưu file
            output_file = "voices/voice_sample.wav"
            self.audio_utils.create_output_directory()
            os.makedirs("voices", exist_ok=True)
            
            with wave.open(output_file, 'wb') as wf:
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(p.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(b''.join(frames))
            
            return output_file
            
        except ImportError:
            print("Lỗi: PyAudio chưa được cài đặt")
            print("Hãy chạy: pip install pyaudio")
            return None
        except Exception as e:
            print(f"Lỗi ghi âm: {e}")
            return None
    
    def load_voice_sample(self, voice_name, file_path):
        """
        Tải mẫu giọng nói
        
        Args:
            voice_name: tên giọng nói
            file_path: đường dẫn file âm thanh
        """
        try:
            audio_data, sr = self.audio_utils.load_audio(file_path)
            self.voice_samples[voice_name] = {
                'audio': audio_data,
                'sr': sr,
                'file_path': file_path
            }
            print(f"Đã tải giọng nói: {voice_name}")
            return True
        except Exception as e:
            print(f"Lỗi tải giọng nói: {e}")
            return False
    
    def get_voice_samples(self):
        """Lấy danh sách các giọng nói đã tải"""
        return list(self.voice_samples.keys())
    
    def clone_voice(self, voice_name, text, output_file):
        """
        Clone giọng nói để đọc text mới
        
        Args:
            voice_name: tên giọng nói để clone
            text: văn bản muốn đọc
            output_file: tên file output
            
        Returns:
            đường dẫn file output
            
        Note:
            Hiện tại là phiên bản đơn giản. 
            Phiên bản nâng cao sẽ dùng RVC (Real-time Voice Conversion)
        """
        try:
            if voice_name not in self.voice_samples:
                print(f"Lỗi: Không tìm thấy giọng nói '{voice_name}'")
                return None
            
            print(f"Đang clone giọng nói '{voice_name}'...")
            
            # Placeholder: Sử dụng gTTS + voice conversion
            # Phiên bản nâng cao sẽ tích hợp RVC
            from .tts_engine import TTSEngine
            
            tts_engine = TTSEngine()
            
            # Tạo text-to-speech thông thường
            output_path = tts_engine.text_to_speech(
                text, 
                output_file, 
                method='gtts'
            )
            
            return output_path
            
        except Exception as e:
            print(f"Lỗi clone giọng nói: {e}")
            return None
    
    def save_voice_profile(self, voice_name, output_name=None):
        """
        Lưu profile giọng nói
        
        Args:
            voice_name: tên giọng nói
            output_name: tên file output (nếu khác)
        """
        try:
            if voice_name not in self.voice_samples:
                print(f"Lỗi: Không tìm thấy giọng nói '{voice_name}'")
                return None
            
            os.makedirs("voices", exist_ok=True)
            
            if output_name is None:
                output_name = voice_name
            
            file_path = f"voices/{output_name}.wav"
            
            sample = self.voice_samples[voice_name]
            self.audio_utils.save_audio(
                sample['audio'],
                f"{output_name}.wav",
                sr=sample['sr'],
                format='wav'
            )
            
            print(f"Đã lưu profile giọng nói: {file_path}")
            return file_path
            
        except Exception as e:
            print(f"Lỗi lưu profile: {e}")
            return None
    
    def list_voice_profiles(self):
        """Liệt kê các profile giọng nói đã lưu"""
        if os.path.exists("voices"):
            return [f for f in os.listdir("voices") if f.endswith('.wav')]
        return []
