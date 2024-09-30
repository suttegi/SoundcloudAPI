import requests

CLIENT_ID = ''
TRACK_ID = 1572433279

track_url = f'https://api-v2.soundcloud.com/tracks?ids={TRACK_ID}&client_id={CLIENT_ID}'
response = requests.get(track_url)
if response.status_code != 200:
    raise Exception('Не удалось получить информацию о треке')
track_data = response.json()

stream_url = None
for transcoding in track_data[0]['media']['transcodings']:
    if transcoding['format']['protocol'] == 'hls':
        stream_url = transcoding['url']
        break

if not stream_url:
    raise Exception('Не удалось найти HLS поток')

stream_response = requests.get(f'{stream_url}?client_id={CLIENT_ID}')
if stream_response.status_code != 200:
    raise Exception('Не удалось получить ссылку на поток')
stream_data = stream_response.text

segments = []
for line in stream_data.splitlines():
    if line and not line.startswith('#'):
        segments.append(line.strip())

output_file = f'track_{TRACK_ID}.mp3'
with open(output_file, 'wb') as f:
    for segment in segments:
        if isinstance(segment, dict) and 'url' in segment:
            segment_url = segment['url']
        else:
            segment_url = segment

        segment_response = requests.get(segment_url, stream=True)
        if segment_response.status_code != 200:
            raise Exception('Не удалось скачать аудио сегмент')
        for chunk in segment_response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

print(f'Аудио успешно сохранено как {output_file}')
