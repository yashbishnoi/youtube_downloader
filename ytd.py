
import os
from tkinter import filedialog
from tkinter import ttk
from tkinter import *
from pytube import YouTube
import ffmpeg
import time
video_download_path = ""
audio_download_path = ""
# sudo apt-get install python3-tk

# resolution_dict={
# "8K":4320p
#     "4K":2160p,
#     "2K":1440p,
#     "Full HD":1080p,
#     "HD":720p,
#     "Low":480p,
# "BAD": 360p

# }

# adaptive_list=[]
# progressive_list=

adaptive_resolution_dict = {
    "4320p": True,
    "2160p": True,
    "1440p": True,
    "1080p": True,
    "720p": False,
    "480p": True,
    "360p": False,
}
allowed_res=list(adaptive_resolution_dict.keys())
codec_dict = {
    "audio/mp4": {
        "acodec": "aac",
        "ext": ".mp4"
    },
    "audio/webm": {
        "acodec": "libvorbis",
        "ext": ".webm"
    },
    "video/mp4": {
        "ext": ".mp4"
    },
    "video/webm": {
        "ext": ".webm"
    }
}

def filter_allowed_res(res):
    if res in allowed_res:
        return True
    else:
        return False



# file location
def get_available_resolutions():

    url = url_box.get()
    yt = YouTube(url)
    available_video_streams = yt.streams.filter(type="video")
    available_resoltions = list(set([stream.resolution for stream in available_video_streams]))
    print("AVAILABLE RESOLUTIONS ARE :"+available_resoltions)
    available_resoltions = list(filter(filter_allowed_res,available_resoltions))
    return available_resoltions



def open_location():
    global video_download_path
    global audio_download_path
    video_download_path = filedialog.askdirectory()
    if video_download_path:
        locationError.config(text=video_download_path, fg="green")

    else:
        locationError.config(text="Please Choose Folder!!", fg="red")
    audio_download_path = video_download_path+"/audio/"
    video_download_path += "/video/"
    # import ipdb; ipdb.set_trace()
    print(audio_download_path, video_download_path)

# def merge_av():n
#     acodec = audio_codec_dict.get()
#     yt.streams.filter(mime_type="audio/mp4")
#     title = yt.title+".webm"


# donwload video
def download(res):

    # res = choices.get()
    url = url_box.get()

    if url:
        ytdError.config(text="")
        import ipdb;ipdb.set_trace()
        yt = YouTube(url)
        video_stream = None
        count=3
        while video_stream is None:
            count-=1
            try:
                if adaptive_resolution_dict.get(res):
                    video_stream = yt.streams.filter(
                        adaptive=True, res=res).first()
                    print(video_stream)
                    audio_streams = yt.streams.filter(
                        adaptive=True, type="audio")
                    max_audio = str(max([int(a.abr.strip("kbps"))
                                    for a in audio_streams])) + "kbps"
                    audio_stream = audio_streams.filter(
                        abr=max_audio).first()
                   
                    print(audio_stream)
                else:
                    video_stream = yt.streams.filter(
                        progressive=True, res=res).first()
                    audio_stream = None
            except Exception:
                if count<0:
                    ytdError.config(text="Server issue", fg="red")
                    break
                continue

        # ytdError.config(text="Paste Link again!!", fg="red")
        if video_stream:
            video_download=video_stream.download(video_download_path)
            print(video_download)
            if video_download:
                video_mime = video_stream.mime_type
                print(video_mime)
                if audio_stream:
                    audio_mime = audio_stream.mime_type
                    audio_download = audio_stream.download(audio_download_path)
                    codec = codec_dict.get(audio_mime).get("acodec")
                    title = "_".join(yt.title.strip(".").split())
                    # video_extension = video_stream.get()
                    # video_path = video_download_path+title + \
                    #     codec_dict.get(video_mime).get("ext")
                    # audio_path = audio_download_path+title + \
                    #     codec_dict.get(audio_mime).get("ext")
                    # print(video_path)
                    video = ffmpeg.input(video_download)
                    audio = ffmpeg.input(audio_download)
                    merge_path = video_download_path+title+'_' + \
                        res+'_'+codec_dict.get(video_mime).get("ext")
                    print(merge_path)
                    output = ffmpeg.output(
                        video, audio, merge_path, vcodec='copy', acodec=codec, strict='experimental')
                    try:
                        output.run()
                    except Exception as e:
                        print(e)
                    # os.remove(video_path)
                    # os.remove(audio_path)
                    # os.rmdir(audio_download_path)
                    print("########################-------------------COMPLETED-------------------########################")

                    # except Exception:
                    #     continue

                    # merge_av()


root = Tk()
root.title("YTD Downloader")
root.geometry("350x400")  # set window
root.columnconfigure(0, weight=1)  # set all content in center.
res=None
# Ytd Link Label
ytdLabel = Label(root, text="Enter the URL of the Video", font=("jost", 15))
ytdLabel.grid()

# Entry Box
ytdEntryVar = StringVar()
url_box = Entry(root, width=100, textvariable=ytdEntryVar)  # url
url_box.grid()

# Error Msg
ytdError = Label(root, text="Error Msg", fg="red", font=("jost", 10))
ytdError.grid()

# Asking save file label
saveLabel = Label(root, text="Save the Video File", font=("jost", 15, "bold"))
saveLabel.grid()

# btn of save file
saveEntry = Button(root, width=10, bg="red", fg="white",
                   text="Choose Path", command=open_location)
saveEntry.grid()

# Error Msg location
locationError = Label(root, text="Error Msg of Path",
                      fg="red", font=("jost", 10))
locationError.grid()

# Download Quality
ytdQuality = Label(root, text="Select Quality", font=("jost", 15))
ytdQuality.grid()

# combobox
# choices = ["2160p", "1080p", "720p"]
# choices = ttk.Combobox(root, values=choices)
# choices.grid()

# res=get_available_resolutions()
# if res:
#     i=3
#     for j in range(res):
#         e = Button(root, text=j) 
#         e.grid(row=i, column=j) 




# donwload btn
download2160btn = Button(root, text="2160p", width=10,
                     bg="red", fg="white", command=lambda :download('2160p'))
download2160btn.grid()

download1080btn = Button(root, text="1080p", width=10,
                     bg="red", fg="white", command=lambda :download('1080p'))
download1080btn.grid()

download720btn = Button(root, text="720p", width=10,
                     bg="red", fg="white", command=lambda :download('720p'))
download720btn.grid()

# # developer Label
# developerlabel = Label(root, text="Dream Developers", font=("jost", 15))
# developerlabel.grid()
root.mainloop()
