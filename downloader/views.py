from django.shortcuts import render, redirect
from .models import Request
from .forms import LinkForm
import youtube_dl


def home_view(request):
    form = LinkForm()
    if request.method == 'POST':
        form = LinkForm(request.POST)
        if form.is_valid():
            youtube_url = form.cleaned_data.get('url')
            url = Request(url=youtube_url)
            url.save()
            options = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]}

            with youtube_dl.YoutubeDL(options) as ydl:
                info = ydl.extract_info(youtube_url, download=False)
                video_url = info['formats'][0]['url']
                return redirect(video_url)
    return render(request, 'home.html', {'form': form})
