from shortGPT.api.create_reddit_short import RedditShortCreator
import sys

app = RedditShortCreator(number=sys.argv[4], target_google_drive_dir="test", Pexel_token=sys.argv[1], OpenAI_token=sys.argv[2], ElevenLab_token=sys.argv[3])
app.start()
