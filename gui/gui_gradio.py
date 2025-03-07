import gradio as gr

from gui.content_automation_ui import GradioContentAutomationUI
from gui.ui_abstract_base import AbstractBaseUI
from gui.ui_components_html import GradioComponentsHTML
from gui.ui_tab_asset_library import AssetLibrary
from gui.ui_tab_config import ConfigUI
from shortGPT.utils.cli import CLI
from shortGPT.config.api_db import ApiKeyManager

class ShortGptUI(AbstractBaseUI):
    '''Class for the GUI. This class is responsible for creating the UI and launching the server.'''

    def __init__(self, colab=False, Pexel_token="", OpenAI_token="", ElevenLab_token=""):
        super().__init__(ui_name='gradio_shortgpt')        
        self.colab = colab
        ApiKeyManager.set_api_key('ELEVEN LABS', ElevenLab_token)
        ApiKeyManager.set_api_key('OPENAI', OpenAI_token)
        ApiKeyManager.set_api_key('PEXELS', Pexel_token)        
        CLI.display_header()

    def create_interface(self):
        '''Create Gradio interface'''
        with gr.Blocks(css="footer {visibility: hidden}", title="ShortGPT Demo") as shortGptUI:
            with gr.Row(variant='compact'):
                gr.HTML(GradioComponentsHTML.get_html_header())

            self.content_automation = GradioContentAutomationUI(shortGptUI).create_ui()
            self.asset_library_ui = AssetLibrary().create_ui()
            self.config_ui = ConfigUI().create_ui()
        return shortGptUI

    def launch(self):
        '''Launch the server'''
        shortGptUI = self.create_interface()
        shortGptUI.queue(concurrency_count=5, max_size=20).launch(server_port=31415, height=1000, share=self.colab, server_name="0.0.0.0")


if __name__ == "__main__":
    app = ShortGptUI()
    app.launch()

