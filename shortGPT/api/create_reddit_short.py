from google.colab import drive 
import shutil 
import os
import random
import traceback

from shortGPT.engine.reddit_short_engine import RedditShortEngine
from gui.asset_components import AssetComponentsUtils
from gui.ui_abstract_component import AbstractComponentUI
from gui.ui_components_html import GradioComponentsHTML
from shortGPT.audio.edge_voice_module import EdgeTTSVoiceModule
from shortGPT.audio.eleven_voice_module import ElevenLabsVoiceModule
from shortGPT.config.api_db import ApiKeyManager
from shortGPT.config.languages import (EDGE_TTS_VOICENAME_MAPPING,
                                       ELEVEN_SUPPORTED_LANGUAGES, Language)
from shortGPT.api_utils.eleven_api import ElevenLabsAPI

class RedditShortCreator:

    def __init__(self, number=1, target_google_drive_dir="", tts_engine = AssetComponentsUtils.ELEVEN_TTS, Pexel_token="", OpenAI_token="", ElevenLab_token=""):
        #define how many shorts need to be created
        self._number = number
        self._target_folder = '/content/drive/MyDrive/{}/'.format(target_google_drive_dir)
        _target_folder = self._target_folder 
        drive.mount('/content/drive', force_remount=True))
        if os.path.exists(_target_folder) and os.path.isdir(_target_folder):        
            print(f"{_target_folder} exists and is a directory.")
        else:
            print("{} does not exist, will create it.".format(_target_folder))
            os.mkdir(_target_folder)
        self._tts_engine = tts_engine
        ApiKeyManager.set_api_key('ELEVEN LABS', ElevenLab_token)
        ApiKeyManager.set_api_key('OPENAI', OpenAI_token)
        ApiKeyManager.set_api_key('PEXELS', Pexel_token)     

    def start(self):
        try:
            voices = list(ElevenLabsAPI(api_key).get_voices().keys())
            voice = random.choice(voices)

            tts_engine = self._tts_engine
            if tts_engine == AssetComponentsUtils.ELEVEN_TTS:
                language = Language("English".lower().capitalize())
                voice_module = ElevenLabsVoiceModule(ApiKeyManager.get_api_key('ELEVEN LABS'), voice, checkElevenCredits=True)
            elif tts_engine == AssetComponentsUtils.EDGE_TTS:
                language = Language("English".lower().capitalize())
                voice_module = EdgeTTSVoiceModule(EDGE_TTS_VOICENAME_MAPPING[language]['male'])

            for i in range(self._number):
                shortEngine = RedditShortEngine(voice_module, background_video_name="Minecraft jumping circuit", background_music_name="Music dj quads", num_images=25, watermark=None, language=language)
                num_steps = shortEngine.get_total_steps()

                for step_num, step_info in shortEngine.makeContent():
                    print(f"Making short {i+1} at step {step_num} - {step_info}")

                video_path = shortEngine.get_video_output_path()
                shutil.copy(video_path, self._target_folder)
        except Exception as e:
            traceback_str = ''.join(traceback.format_tb(e.__traceback__))
            error_name = type(e).__name__.capitalize() + " : " + f"{e.args[0]}"
            print("Error", traceback_str)
            
            