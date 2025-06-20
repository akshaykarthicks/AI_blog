from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json,os,assemblyai as aai
from pytube import YouTube
from django.conf import settings
from google import genai
import yt_dlp


# Create your views here.
@login_required
def index(request):
    return render(request,'index.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            return render(request,'login.html',{'error_message':'Invalid username or password'})
    return render(request,'login.html')

def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repeatPassword = request.POST['repeatPassword']
        if password == repeatPassword:
            user = User.objects.create_user(username=username,email=email,password=password)
            user.save()
            return redirect('index')
        else:
            return render(request,'signup.html',{'error_message':'Passwords do not match'})
    return render(request,'signup.html')

@login_required
def logout(request):
    logout(request)
    return redirect('index')

#csrf_exempt decorator is used to bypass csrf protection
@csrf_exempt
def gen_blog(request):
    if request.method == 'POST':
        try :
            data=json.loads(request.body)
            yt_link = data['link']
        except(KeyError,json.decoder.JSONDecodeError):
            return JsonResponse({'error': 'Invalid request'})
        title = yt_title(yt_link)
        
        
        #get the transcription of the audio file in def get_transcript(link)
        
        transcription=get_transcript(yt_link)
        if not transcription:
            return JsonResponse({'error': 'No transcription found'})
        
        #gemini ai 
        blog_content=gen_blog_from_transcript(transcription)
        if not blog_content:
            return JsonResponse({'error': 'No blog content found'})
        
        return JsonResponse({'blog_content':blog_content})
    
    #SAVE BLOG TO DATABASE
    
    
    #return json in the form of {'blog_content':blog_content}
        return JsonResponse({'blog_content':blog_content})
        
    
    else:
        return JsonResponse({'error': 'Invalid request method'})
    
    
def yt_title(link):
    try:
        yt = YouTube(link)
        return yt.title
    except Exception as e:
        print(f"Error fetching YouTube title: {e}")
        return "Unknown Title"

    
def get_transcript(link):
    audio = download_audio(link)
    print(f"Audio file path: {audio}")
    print(f"File exists: {os.path.exists(audio)}")
    print(f"File size: {os.path.getsize(audio) if os.path.exists(audio) else 'N/A'} bytes")
    aai.settings.api_key = os.environ['ASSEMBLYAI_API_KEY']
    if not audio or not os.path.exists(audio):
        print("Audio file does not exist or failed to download.")
        return None
    try:
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio)
        return transcriber.text
    except Exception as e:
        print(f"AssemblyAI transcription error: {e}")
        return None
    

def gen_blog_from_transcript(transcription):
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    prompt =  f"Based on the following transcript from a YouTube video, write a comprehensive blog article, write it based on the transcript, but dont make it look like a youtube video, make it look like a proper blog article:\n\n{transcription}\n\nArticle:"
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    generate_content = response.text.strip()
    return generate_content

# NOTE: Make sure your frontend POSTs to /generate-blog/ (with a trailing slash) to avoid Django APPEND_SLASH errors.

def download_audio(link):
    output_dir = settings.MEDIA_ROOT
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_dir, '%(id)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False,
    }
    try:
        print(f"Attempting to download audio from: {link}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=True)
            filename = os.path.join(output_dir, f"{info['id']}.mp3")
            print(f"Audio downloaded and saved as: {filename}")
            return filename
    except Exception as e:
        print(f"Error downloading audio with yt-dlp: {e}")
        return None
