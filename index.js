const script = document.createElement('script');
script.src = 'https://cdn.jsdelivr.net/npm/hls.js@latest';
script.onload = async () => {
  await playTrack(1572433279);
};
document.head.appendChild(script);

async function playTrack(trackId) {
  const clientId = '';
  const oauth_token = '';

  const response = await fetch(`https://api-v2.soundcloud.com/tracks?ids=${trackId}&client_id=${clientId}&oauth_token=${oauth_token}`);
  console.log('Track data fetched successfully');
  const data = await response.json();
  console.log(data);

  const streamUrl = data[0].media.transcodings.find(t => t.format.mime_type === 'audio/mpeg').url;

  const streamResponse = await fetch(`${streamUrl}?client_id=${clientId}`);
  const streamData = await streamResponse.json();
  console.log('Stream data fetched successfully:', streamData);

  const audio = document.createElement('audio');
  audio.controls = true;

  if (Hls.isSupported()) {
    const hls = new Hls();
    hls.loadSource(streamData.url);
    hls.attachMedia(audio);
    hls.on(Hls.Events.MANIFEST_PARSED, function() {
      audio.play();
    });
  } else if (audio.canPlayType('application/vnd.apple.mpegurl')) {
    audio.src = streamData.url;
    audio.addEventListener('loadedmetadata', function() {
      audio.play();
    });
  }

  document.body.appendChild(audio);
}
