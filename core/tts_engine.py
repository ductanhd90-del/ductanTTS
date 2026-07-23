"""
TTS Engine - Chuyển đổi Text to Speech
"""
import os
from gtts import gTTS
from TTS.api import TTS
from .audio_utils import AudioUtils


class TTSEngine:
    """Engine chuyển đổi text thành âm thanh"""
    
    def __init__(self):
        """Khởi tạo TTS Engine"""
        self.audio_utils = AudioUtils()
        self.audio_utils.create_output_directory()
        
        # Coqui TTS models
        self.tts_model = None
        self.model_name = "tts_models/vi_VN/cv/glow-tts"  # Vietnamese model
        
    def use_gtts(self, text, output_file, language='vi'):
        """
        Sử dụng Google Text-to-Speech (đơn giản, miễn phí)
        
        Args:
            text: văn bản muốn chuyển đổi
            output_file: tên file output
            language: mã ngôn ngữ (vi=Vietnamese)
            
        Returns:
            đường dẫn file output
        """
        try:
            # Tạo object gTTS
            tts = gTTS(text=text, lang=language, slow=False)
            
            # Lưu file
            output_path = f"output/{output_file}"
            self.audio_utils.create_output_directory()
            tts.save(output_path)
            
            return output_path
        except Exception as e:
            print(f"Lỗi gTTS: {e}")
            return None
    
    def use_coqui_tts(self, text, output_file, speaker=None):
        """
        Sử dụng Coqui TTS (offline, chất lượng cao)
        
        Args:
            text: văn bản
            output_file: tên file output
            speaker: lựa chọn giọng nói
            
        Returns:
            đường dẫn file output
        """
        try:
            # Load model nếu chưa load
            if self.tts_model is None:
                print("Đang tải Coqui TTS model... (lần đầu sẽ mất vài phút)")
                self.tts_model = TTS(model_name=self.model_name, gpu=True)
            
            # Tạo âm thanh
            wav = self.tts_model.tts(text=text, speaker=speaker)
            
            # Lưu file
            output_path = f"output/{output_file}"
            self.audio_utils.create_output_directory()
            self.tts_model.save_wav(wav, output_path)
            
            return output_path
        except Exception as e:
            print(f"Lỗi Coqui TTS: {e}")
            return None
    
    def get_available_speakers(self):
        """Lấy danh sách giọng nói có sẵn"""
        try:
            if self.tts_model is None:
                self.tts_model = TTS(model_name=self.model_name, gpu=True)
            
            return self.tts_model.speakers
        except Exception as e:
            print(f"Lỗi lấy danh sách giọng: {e}")
            return []
    
    def text_to_speech(self, text, output_file, method='gtts', speaker=None):
        """
        Chuyển đổi text thành âm thanh (phương thức chọn)
        
        Args:
            text: văn bản
            output_file: tên file output
            method: 'gtts' hoặc 'coqui'
            speaker: giọng nói (cho Coqui)
            
        Returns:
            đường dẫn file output hoặc None nếu lỗi
        """
        if not text or text.strip() == "":
            print("Lỗi: Văn bản không được để trống")
            return None
        
        if method == 'gtts':
            return self.use_gtts(text, output_file)
        elif method == 'coqui':
            return self.use_coqui_tts(text, output_file, speaker)
        else:
            print(f"Phương thức '{method}' không được hỗ trợ")
            return None
