from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import CreateView
from django.contrib.auth import login, logout
from .models import *
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import speech_recognition as sr
from .forms import *
from pydub import AudioSegment
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
import os
from os import path

#AudioSegment.converter = "C:/Users/Yomi/Documents/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe"
#AudioSegment.ffmpeg = "C:/Users/Yomi/Documents/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe"
#AudioSegment.ffprobe = "C:/Users/Yomi/Documents/ffmpeg-master-latest-win64-gpl/bin/ffprobe.exe"



class UserLoginView(LoginView):
    template_name='home/login.html'
    

@login_required
def logout_user(request):
    logout(request)
    return redirect("/")


class UserSignupView(CreateView):
    model = User
    form_class = UserSignupForm
    template_name = 'home/signup.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')


def index(request):
    user = request.user
    if user.is_authenticated:
        notes = Notes.objects.filter(user = user)
        audios = Audio.objects.filter(user = user)
        return render(request, 'home/home.html', {'notes': notes, 'audios': audios})
    else:
        return render(request, 'home/home.html')
    

def speech_to_text(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return "Error connecting to API: {}".format(e)



def your_view(request):
    transcribed_text = speech_to_text("path/to/audio_file.wav")
    return HttpResponse(transcribed_text)

@login_required
def audio_upload(request):
    if request.method == 'POST':
        #AudioSegment.converter = "C:/Users/Yomi/AppData/Local/Programs/Python/Python39/Lib/site-packages/ffmpeg"
        user = request.user
        form = AudioUploadForm(request.POST, request.FILES)
        if form.is_valid():
            audio_file = request.FILES['audio_file']

            audio = AudioSegment.from_file(audio_file, audio_file.content_type.split('/')[-1])
            wav_filename = 'temp.wav'
            wav_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), wav_filename)
            audio.export(wav_path, format='wav')

            recognizer = sr.Recognizer()
            audio_data = sr.AudioFile(wav_path)
            with audio_data as source:
                audio_text = recognizer.record(source)
            transcript = recognizer.recognize_google(audio_text)
            audio_setup = form.save(commit=False)
            audio_setup.user = user
            audio_setup.name = os.path.splitext(audio_file.name)
            audio_setup.file_text = transcript
            audio_setup.audio_file = audio_file
            audio_setup.save()
            return render(request, 'home/transcript.html', {'transcript': transcript})
    else:
        form = AudioUploadForm()
    return render(request, 'home/audio_upload.html', {'form': form})

@login_required
def note_individual(request, prodid):
    user = request.user
    note = Notes.objects.get(id=prodid)
    audios = Audio.objects.filter(user = user)
    supporting_doc = Supporting_Doc.objects.filter(note=note)

    return render(request, 'home/note.html', {'note': note, 'audios': audios, 'sup': supporting_doc})


@login_required
def note_editor(requset, prodid):
    note = Notes.objects.get(id=prodid)
    supporting_doc = Supporting_Doc.objects.filter(note=note)
    if requset.method == 'POST':
        form = NoteEditorForm(requset.POST, instance=note)
        if form.is_valid():
            form.save()
            return render(requset, 'home/edit.html', {'form': form, 'note_id': note.id, 'note': note})
    else:
        form = NoteEditorForm(instance=note)
        
    return render(requset, 'home/edit.html', {'form': form, 'note_id': note.id, 'note': note, 'sup': supporting_doc})


@login_required
def note_new(request):
    if request.method == 'POST':
        print(request.user.id)
        form = NoteEditorForm(request.POST, request.FILES)
        if form.is_valid():
            new_note = form.save(commit=False)
            new_note.user = request.user
            new_note.save()
            return redirect('/')
    else:
        form = NoteEditorForm()
    return render(request, 'home/edit.html', {'form': form})


@login_required
def add_doc(request, note_id):
    if request.method == 'POST':

        notes = Notes.objects.filter(id=note_id)
        if notes:

            print(request.user.id)
            form = SupportingDocForm(request.POST, request.FILES)
            print(form.is_valid())
            for field in form:
                print("Field Error:", field.name,  field.errors)
            if form.is_valid():
                sup = form.save(commit=False)
                sup.note = notes[0]
                sup.save()
                return redirect('/')
        
    form = SupportingDocForm()
    return render(request, 'home/edit.html', {'form': form})

@login_required
def groups(request):
    groups = Group.objects.all()
    return render(request, 'home/groups.html', {'groups': groups})


class GroupListView(ListView):
    model = Group
    template_name = 'home/group_list.html'
    context_object_name = 'groups'


class GroupCreateView(CreateView):
    model = Group
    template_name = 'home/group_form.html'
    fields = ['name', 'user', 'notes']
    success_url = reverse_lazy('group-list')


class GroupUpdateView(UpdateView):
    model = Group
    template_name = 'home/group_form.html'
    fields = ['name', 'user', 'notes']
    success_url = reverse_lazy('group-list')

@login_required
def delete_note(request, note_id):
    note = Notes.objects.get(id=note_id)
    note.delete()
    messages.success(request, "Note deleted successfully")
    return redirect('/')

@login_required
def delete_audio(request, audio_id):
    audio = Audio.objects.get(id=audio_id)
    audio.delete()
    messages.success(request, "Audio deleted successfully")
    return redirect('/')

@login_required
def delete_supporting_doc(request, sup_id):
    sup = Supporting_Doc.objects.get(id=sup_id)
    sup.delete()
    messages.success(request, "Supporting document deleted successfully")
    return redirect('/')