from shortGPT.api.create_reddit_short import RedditShortCreator
import sys

'''
Some workarounds:
1, hard code magick path in D:\OneDrive\Work\ShortGPT\ShortGPT\myvenv\Lib\site-packages\moviepy\config.py 
'''

app = RedditShortCreator(number=sys.argv[4], Pexel_token=sys.argv[1], OpenAI_token=sys.argv[2], ElevenLab_token=sys.argv[3])
app.start()
