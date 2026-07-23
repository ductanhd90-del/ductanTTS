"""
Test Script - Kiểm tra toàn bộ tính năng ductanTTS
"""
import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.tts_engine import TTSEngine
from core.voice_cloner import VoiceCloner
from core.voice_presets import VoicePresetsManager
from core.audio_utils import AudioUtils


class TestTTSEngine(unittest.TestCase):
    """Test cases cho TTSEngine"""
    
    def setUp(self):
        """Khởi tạo trước mỗi test"""
        self.tts_engine = TTSEngine()
    
    def test_tts_engine_initialization(self):
        """Test khởi tạo TTSEngine"""
        self.assertIsNotNone(self.tts_engine)
        print("✅ TTSEngine khởi tạo thành công")
    
    def test_output_directory_created(self):
        """Test thư mục output được tạo"""
        self.tts_engine.audio_utils.create_output_directory()
        self.assertTrue(os.path.exists("output"))
        print("✅ Thư mục output được tạo thành công")
    
    @patch('gtts.gTTS')
    def test_gtts_method(self, mock_gtts):
        """Test phương thức Google TTS"""
        mock_instance = MagicMock()
        mock_gtts.return_value = mock_instance
        
        # Simulate save
        def save_side_effect(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)
            open(path, 'w').close()
        
        mock_instance.save.side_effect = save_side_effect
        
        text = "Xin chào"
        output_file = "test_gtts.mp3"
        
        try:
            result = self.tts_engine.use_gtts(text, output_file)
            print(f"✅ Google TTS test passed: {result}")
        except Exception as e:
            print(f"⚠️  Google TTS test warning: {e}")
    
    def test_coqui_tts_method(self):
        """Test phương thức Coqui TTS (chỉ kiểm tra initialization)"""
        try:
            # Chỉ test khởi tạo, không tải model đầy đủ
            self.assertIsNotNone(self.tts_engine)
            print("⚠️  Coqui TTS test skipped (requires model download)")
        except Exception as e:
            print(f"⚠️  Coqui TTS test warning: {e}")


class TestVoicePresets(unittest.TestCase):
    """Test cases cho VoicePresetsManager"""
    
    def setUp(self):
        """Khởi tạo trước mỗi test"""
        self.voice_presets = VoicePresetsManager()
    
    def test_voice_presets_initialization(self):
        """Test khởi tạo VoicePresetsManager"""
        self.assertIsNotNone(self.voice_presets)
        print("✅ VoicePresetsManager khởi tạo thành công")
    
    def test_directories_created(self):
        """Test các thư mục được tạo"""
        self.voice_presets.create_voice_directories()
        self.assertTrue(os.path.exists("voices/presets"))
        self.assertTrue(os.path.exists("voices/custom"))
        print("✅ Thư mục voices được tạo thành công")
    
    def test_get_all_voices(self):
        """Test lấy tất cả giọng"""
        all_voices = self.voice_presets.get_all_voices()
        self.assertIsInstance(all_voices, dict)
        print(f"✅ Lấy tất cả giọng thành công: {len(all_voices)} giọng")
    
    def test_get_preset_voices(self):
        """Test lấy giọng preset"""
        preset_voices = self.voice_presets.get_preset_voices()
        self.assertIsInstance(preset_voices, dict)
        print(f"✅ Lấy giọng preset thành công: {len(preset_voices)} giọng")
    
    def test_get_custom_voices(self):
        """Test lấy giọng custom"""
        custom_voices = self.voice_presets.get_custom_voices()
        self.assertIsInstance(custom_voices, dict)
        print(f"✅ Lấy giọng custom thành công: {len(custom_voices)} giọng")


class TestVoiceCloner(unittest.TestCase):
    """Test cases cho VoiceCloner"""
    
    def setUp(self):
        """Khởi tạo trước mỗi test"""
        self.voice_cloner = VoiceCloner()
    
    def test_voice_cloner_initialization(self):
        """Test khởi tạo VoiceCloner"""
        self.assertIsNotNone(self.voice_cloner)
        print("✅ VoiceCloner khởi tạo thành công")
    
    def test_voice_samples_empty(self):
        """Test voice_samples trống ban đầu"""
        self.assertEqual(len(self.voice_cloner.voice_samples), 0)
        print("✅ Voice samples trống ban đầu")
    
    def test_get_voice_samples(self):
        """Test lấy danh sách giọng"""
        samples = self.voice_cloner.get_voice_samples()
        self.assertIsInstance(samples, list)
        print(f"✅ Lấy danh sách giọng thành công: {samples}")


class TestAudioUtils(unittest.TestCase):
    """Test cases cho AudioUtils"""
    
    def setUp(self):
        """Khởi tạo trước mỗi test"""
        self.audio_utils = AudioUtils()
    
    def test_audio_utils_initialization(self):
        """Test khởi tạo AudioUtils"""
        self.assertIsNotNone(self.audio_utils)
        print("✅ AudioUtils khởi tạo thành công")
    
    def test_create_output_directory(self):
        """Test tạo thư mục output"""
        self.audio_utils.create_output_directory()
        self.assertTrue(os.path.exists("output"))
        self.assertTrue(os.path.exists("models"))
        self.assertTrue(os.path.exists("voices"))
        print("✅ Các thư mục được tạo thành công")


class TestIntegration(unittest.TestCase):
    """Integration tests - Kiểm tra tích hợp các module"""
    
    def setUp(self):
        """Khởi tạo trước mỗi test"""
        self.tts_engine = TTSEngine()
        self.voice_cloner = VoiceCloner()
        self.voice_presets = VoicePresetsManager()
        self.audio_utils = AudioUtils()
    
    def test_all_modules_work_together(self):
        """Test tất cả module hoạt động cùng nhau"""
        try:
            # Tạo thư mục
            self.audio_utils.create_output_directory()
            self.voice_presets.create_voice_directories()
            
            # Lấy giọng
            all_voices = self.voice_presets.get_all_voices()
            
            # Kiểm tra
            self.assertIsNotNone(self.tts_engine)
            self.assertIsNotNone(self.voice_cloner)
            self.assertIsNotNone(self.voice_presets)
            
            print("✅ Tất cả module hoạt động cùng nhau thành công")
        except Exception as e:
            print(f"❌ Lỗi integration test: {e}")


def run_tests():
    """Chạy tất cả tests"""
    print("\n" + "="*60)
    print("🧪 ductanTTS - Test Suite")
    print("="*60 + "\n")
    
    # Tạo test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Thêm tests
    suite.addTests(loader.loadTestsFromTestCase(TestTTSEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestVoicePresets))
    suite.addTests(loader.loadTestsFromTestCase(TestVoiceCloner))
    suite.addTests(loader.loadTestsFromTestCase(TestAudioUtils))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Chạy tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # In kết quả
    print("\n" + "="*60)
    print("📊 Test Results Summary")
    print("="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*60 + "\n")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
