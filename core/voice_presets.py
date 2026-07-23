"""
Voice Presets Manager - Quản lý các giọng nói mặc định
"""
import os
import shutil
from .audio_utils import AudioUtils


class VoicePresetsManager:
    """Quản lý các giọng nói có sẵn (presets)"""
    
    def __init__(self):
        """Khởi tạo Voice Presets Manager"""
        self.audio_utils = AudioUtils()
        self.presets_dir = "voices/presets"
        self.custom_dir = "voices/custom"
        self.create_voice_directories()
        self.presets = self.load_presets()
    
    def create_voice_directories(self):
        """Tạo các thư mục voice nếu chưa có"""
        os.makedirs(self.presets_dir, exist_ok=True)
        os.makedirs(self.custom_dir, exist_ok=True)
    
    def load_presets(self):
        """
        Load danh sách các giọng preset có sẵn
        
        Returns:
            dict - Danh sách giọng preset
        """
        presets = {}
        
        if os.path.exists(self.presets_dir):
            for file in os.listdir(self.presets_dir):
                if file.endswith(('.wav', '.mp3')):
                    voice_name = file.replace('.wav', '').replace('.mp3', '')
                    file_path = os.path.join(self.presets_dir, file)
                    presets[voice_name] = {
                        'type': 'preset',
                        'path': file_path,
                        'file': file
                    }
        
        return presets
    
    def load_custom_voices(self):
        """
        Load danh sách các giọng custom (ghi âm user)
        
        Returns:
            dict - Danh sách giọng custom
        """
        custom = {}
        
        if os.path.exists(self.custom_dir):
            for file in os.listdir(self.custom_dir):
                if file.endswith(('.wav', '.mp3')):
                    voice_name = file.replace('.wav', '').replace('.mp3', '')
                    file_path = os.path.join(self.custom_dir, file)
                    custom[voice_name] = {
                        'type': 'custom',
                        'path': file_path,
                        'file': file
                    }
        
        return custom
    
    def get_all_voices(self):
        """
        Lấy tất cả giọng (Preset + Custom)
        
        Returns:
            dict - Tất cả giọng nói
        """
        all_voices = {}
        
        # Thêm preset voices
        for name, info in self.presets.items():
            all_voices[f"🎙️ {name} (Preset)"] = info
        
        # Thêm custom voices
        custom = self.load_custom_voices()
        for name, info in custom.items():
            all_voices[f"🔊 {name} (Custom)"] = info
        
        return all_voices
    
    def get_preset_voices(self):
        """Lấy danh sách giọng preset"""
        voices = {}
        for name, info in self.presets.items():
            voices[f"🎙️ {name}"] = info
        return voices
    
    def get_custom_voices(self):
        """Lấy danh sách giọng custom"""
        voices = {}
        custom = self.load_custom_voices()
        for name, info in custom.items():
            voices[f"🔊 {name}"] = info
        return voices
    
    def add_custom_voice(self, voice_name, file_path):
        """
        Thêm giọng custom (lưu file ghi âm)
        
        Args:
            voice_name: tên giọng
            file_path: đường dẫn file ghi âm
            
        Returns:
            đường dẫn file đã lưu
        """
        try:
            self.create_voice_directories()
            
            # Lấy phần mở rộng file
            file_ext = os.path.splitext(file_path)[1]
            
            # Tạo đường dẫn đích
            dest_path = os.path.join(self.custom_dir, f"{voice_name}{file_ext}")
            
            # Copy file
            shutil.copy(file_path, dest_path)
            
            print(f"✅ Đã lưu giọng custom: {voice_name}")
            return dest_path
            
        except Exception as e:
            print(f"❌ Lỗi lưu giọng custom: {e}")
            return None
    
    def delete_custom_voice(self, voice_name):
        """
        Xóa giọng custom
        
        Args:
            voice_name: tên giọng
            
        Returns:
            True nếu xóa thành công
        """
        try:
            custom = self.load_custom_voices()
            
            for key, info in custom.items():
                if voice_name in key:
                    os.remove(info['path'])
                    print(f"✅ Đã xóa giọng: {voice_name}")
                    return True
            
            return False
        except Exception as e:
            print(f"❌ Lỗi xóa giọng: {e}")
            return False
    
    def get_voice_path(self, voice_display_name):
        """
        Lấy đường dẫn file giọng từ tên hiển thị
        
        Args:
            voice_display_name: tên giọng hiển thị (ví dụ: "🎙️ Female 1 (Preset)")
            
        Returns:
            đường dẫn file hoặc None
        """
        all_voices = self.get_all_voices()
        
        if voice_display_name in all_voices:
            return all_voices[voice_display_name]['path']
        
        return None
    
    def voice_exists(self, voice_name):
        """Kiểm tra giọng có tồn tại không"""
        all_voices = self.get_all_voices()
        return voice_name in all_voices
