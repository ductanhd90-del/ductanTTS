"""
Audio Utilities - Xử lý âm thanh
"""
import os
import numpy as np
from pydub import AudioSegment
from pydub.utils import mediainfo
import soundfile as sf
import librosa


class AudioUtils:
    """Lớp xử lý âm thanh"""
    
    @staticmethod
    def create_output_directory():
        """Tạo thư mục output nếu chưa có"""
        if not os.path.exists("output"):
            os.makedirs("output")
        if not os.path.exists("models"):
            os.makedirs("models")
        if not os.path.exists("voices"):
            os.makedirs("voices")
    
    @staticmethod
    def save_audio(audio_data, filename, sr=22050, format="mp3"):
        """
        Lưu âm thanh
        
        Args:
            audio_data: numpy array hoặc file path
            filename: tên file output
            sr: sample rate
            format: định dạng file (mp3, wav)
        """
        AudioUtils.create_output_directory()
        
        output_path = f"output/{filename}"
        
        if isinstance(audio_data, str):
            # Nếu là đường dẫn file
            sound = AudioSegment.from_file(audio_data)
            sound.export(output_path, format=format)
        else:
            # Nếu là numpy array
            sf.write(output_path, audio_data, sr)
        
        return output_path
    
    @staticmethod
    def load_audio(file_path, sr=22050):
        """
        Load âm thanh từ file
        
        Args:
            file_path: đường dẫn file
            sr: sample rate
            
        Returns:
            audio_data, sr
        """
        audio_data, sr = librosa.load(file_path, sr=sr)
        return audio_data, sr
    
    @staticmethod
    def get_audio_duration(file_path):
        """Lấy thời lượng file âm thanh (giây)"""
        audio = AudioSegment.from_file(file_path)
        return len(audio) / 1000.0  # convert to seconds
    
    @staticmethod
    def normalize_audio(audio_data):
        """Chuẩn hóa âm thanh (-1 to 1)"""
        max_val = np.max(np.abs(audio_data))
        if max_val > 0:
            return audio_data / max_val
        return audio_data
    
    @staticmethod
    def convert_format(input_file, output_file, format="mp3"):
        """
        Chuyển đổi định dạng âm thanh
        
        Args:
            input_file: file input
            output_file: file output
            format: định dạng mới (mp3, wav, etc)
        """
        audio = AudioSegment.from_file(input_file)
        audio.export(output_file, format=format)
        return output_file
    
    @staticmethod
    def trim_audio(audio_data, start_sec, end_sec, sr=22050):
        """
        Cắt âm thanh từ start_sec đến end_sec
        
        Args:
            audio_data: numpy array
            start_sec: thời điểm bắt đầu (giây)
            end_sec: thời điểm kết thúc (giây)
            sr: sample rate
        """
        start_sample = int(start_sec * sr)
        end_sample = int(end_sec * sr)
        return audio_data[start_sample:end_sample]
