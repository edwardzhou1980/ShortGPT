from gui.gui_gradio import ShortGptUI

Pexel_token = sys.argv[1]
OpenAI_token = sys.argv[2]
ElevenLab_token = sys.argv[3]

app = ShortGptUI(colab=True, Pexel_token, OpenAI_token, ElevenLab_token)
app.launch()
