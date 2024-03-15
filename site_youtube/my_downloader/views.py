from django.shortcuts import render
from pytube import YouTube
from django.http import HttpResponse
from wsgiref.util import FileWrapper
import os



def index_view(request):


    return render(request, 'my_downloader/index.html')


def download_view (request):
    global url
    url = request.GET.get('url')

    #print (f' this is my url: {url}')

    yt = YouTube(url)
    global global_streams
    global_streams = yt.streams

    res = []
    ores = []
    
    for item in global_streams:
        onlyres = item.resolution

        string = str(item.resolution) + ' ' + str(item.filesize_approx) + 'Mb' 

        res.append(string)
        ores.append(onlyres)
    ores = list(dict.fromkeys(ores))



    title = yt.title
    author = yt.author
    thumbnail = yt.thumbnail_url

    return render (
        request,
        'my_downloader/download.html',
        {
                'global_streams': global_streams,
                'title': title,
                'author': author,
                'thumbnail': thumbnail,
                'onlyres' : ores,
                'res': res,
        }
    )

def success (request, res):
    global url

    homedir = os.path.expanduser("~")
    dirs = homedir + '/Downloads/'

    yt = YouTube(url)
    title = yt.title
    print(f' the file title is: {title}')

    print(f' tmy resolutions: {res}')

    #res, b = res.split() # unpacking
    size = global_streams.filter(res=res).first().filesize // 1048576
    print(f' the file size is: {size}')

    if request.method == 'POST' and size < 900:

        global_streams.filter(res=res).first().download(output_path = dirs, filename = 'video.mp4')
        file = FileWrapper(open(f'{dirs}/video.mp4', 'rb'))
        response = HttpResponse(file, content_type='application/vnd.mp4')
        response['Content-Disposition'] = 'attachment; filename = "video.mp4"'
        os.remove(f'{dirs}/video.mp4')
        return response
    else:
        return render (request, 'error.html') 

    


  





 
