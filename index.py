from youtube_transcript_api import YouTubeTranscriptApi
import sys
from requests_html import HTMLSession
session = HTMLSession()

data = sys.argv[1]
phrase = sys.argv[2:]


def is_phrase_in_transcript(phrase, transcript):
    transcript_text = ' '.join([x['text'] for x in transcript])
    if ' '.join(phrase) in transcript_text:
        return True
    else:
        return False

def extract_id_channel_and_title_from_yt5_url(url):
    res = session.get(url)
    if len(url.split('&')) > 1: # regular url
        channel = url.split('&')[1].split('=')[1]
        v_id = url.split('=')[1].split('&')[0]
    else:
        if len(url.split('=')) > 1: # yt url no ab channel
            v_id = url.split('=')[1]
            channel_html = res.html.find('body')
            if "channelId" in channel_html[0].text:
                channel = channel_html[0].text.split('channelId')[1].strip().split('author')[1].strip().split(':')[1].strip().split(',')[0].strip().replace('"', '')
        else: # yt share shortlink
            v_id = url.split('be/')[1]
            channel_html = res.html.find('body')
            if "channelId" in channel_html[0].text:
                channel = channel_html[0].text.split('channelId')[1].strip().split('author')[1].strip().split(':')[1].strip().split(',')[0].strip().replace('"', '')
    
    title = res.html.xpath('.//title')[0].text
    channel = channel.replace(' ', '_')

    return v_id, title, channel

if data:
    yt_url = data
else:
    yt_url = input('Enter the youtube url: ')
    if len(yt_url) == 0 or len(yt_url) > 150:
        raise Exception('Please enter a valid youtube url')


# print('Extracting video information...')
v_id, title, channel = extract_id_channel_and_title_from_yt5_url(yt_url)
transcript = YouTubeTranscriptApi.get_transcript(v_id)
print(is_phrase_in_transcript(phrase, transcript))
