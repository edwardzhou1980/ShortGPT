from gui.gui_gradio import ShortGptUI

app = ShortGptUI(colab=True, Pexel_token="", OpenAI_token="", ElevenLab_token="")
app.launch()
