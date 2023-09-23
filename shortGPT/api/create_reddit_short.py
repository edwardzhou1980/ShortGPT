import shutil 
import os
import random
import traceback
import time

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
from shortGPT.config.asset_db import AssetDatabase

class RedditShortCreator:

    def __init__(self, number=1, target_google_drive_dir="", tts_engine = AssetComponentsUtils.ELEVEN_TTS, Pexel_token="", OpenAI_token="", ElevenLab_token=""):
        #define how many shorts need to be created
        self._number = number
        self._target_folder = '/content/drive/MyDrive/{}/'.format(target_google_drive_dir)
        _target_folder = self._target_folder 
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
            api_key = ApiKeyManager.get_api_key('ELEVEN LABS')
            voices = list(ElevenLabsAPI(api_key).get_voices().keys())
            voice = random.choice(voices)
            numShorts =self._number

            df = AssetDatabase.get_df()
            background_videos = list(df.loc['background video' == df['type']]['name'])
            background_musics = list(df.loc['background music' == df['type']]['name'])

            tts_engine = self._tts_engine
            if tts_engine == AssetComponentsUtils.ELEVEN_TTS:
                language = Language("English".lower().capitalize())
                voice_module = ElevenLabsVoiceModule(ApiKeyManager.get_api_key('ELEVEN LABS'), voice, checkElevenCredits=True)
            elif tts_engine == AssetComponentsUtils.EDGE_TTS:
                language = Language("English".lower().capitalize())
                voice_module = EdgeTTSVoiceModule(EDGE_TTS_VOICENAME_MAPPING[language]['male'])

            for i in range(numShorts):
                start_time = time.time()

                shortEngine = RedditShortEngine(voice_module, 
                    background_video_name=random.choice(background_videos), 
                    background_music_name=random.choice(background_musics), 
                    num_images=25, watermark=None, language=language)
                num_steps = shortEngine.get_total_steps()

                for step_num, step_info in shortEngine.makeContent():
                    print(f"Making short {i+1} at step {step_num} - {step_info}")

                execution_time_seconds = end_time - start_time  # compute the difference in seconds
                execution_time_minutes = execution_time_seconds / 60  # convert the difference to minutes
                print(f"Execution time: {execution_time_minutes:.2f} minutes")

                video_path = shortEngine.get_video_output_path()
                if os.path.exists(video_path):
                    shutil.move(video_path, self._target_folder)
                    if video_path.endswith(".mp4"):
                        metadata_filename = video_path[:-4] + ".txt"
                        if os.path.exists(metadata_filename):
                            shutil.move(metadata_filename, self._target_folder)
                        else:
                            print(f"Youtube meta data file '{metadata_filename}' doesn't exist!")
                else:
                    print(f"Youtube video  file '{video_path}' doesn't exist!")

        except Exception as e:
            traceback_str = ''.join(traceback.format_tb(e.__traceback__))
            error_name = type(e).__name__.capitalize() + " : " + f"{e.args[0]}"
            print(f"Error: {error_name}")
            print("Error Trackback", traceback_str)
            
            