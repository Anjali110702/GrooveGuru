import pickle
from django.shortcuts import render,redirect
from .forms import AudioFileForm
from .models import AudioFile
import librosa
import numpy as np


# Load the models and scaler
models = pickle.load(open('C:/Desktop/MiniProject/audiogenre/predictions/models.p', 'rb'))

# Verify the keys to match the saved model
print(models.keys())  # Ensure this outputs 'norma', 'svmp', and 'lgn'

scaler = models.get('norma')
knn_best = models.get('svmp')
svm_best = models.get('svmp')  # Assuming 'svmp' is also used for SVM in your case
lookup_genre_name = models.get('lgn')
def index(request):
    return render(request, 'home.html')

def get_metadata(file_path):
    y, sr = librosa.load(file_path, sr=None)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=27)
    mfccs_mean = np.mean(mfccs.T, axis=0)
    return mfccs_mean
from django.shortcuts import render, redirect
from django.urls import reverse

def upload_audio(request):
    if request.method == 'POST':
        form = AudioFileForm(request.POST, request.FILES)
        if form.is_valid():
            audio_file = form.save()
            audio_features = get_metadata(audio_file.file.path)
            
            if scaler is None:
                return render(request, 'genre_output.html', {'form': form, 'error': 'Scaler model is not loaded correctly.'})
            
            audio_features_scaled = scaler.transform([audio_features])

            genre_prediction_knn = knn_best.predict(audio_features_scaled)
            genre_prediction_svm = svm_best.predict(audio_features_scaled)

            genre = lookup_genre_name[genre_prediction_svm[0]]  # Assuming you want to use SVM prediction

            # Render the genre result page with the prediction and genre
            context = {'svm_prediction': genre, 'redirect_url': reverse('recommend_songs', args=[genre])}
            return render(request, 'genre_output.html', context)
    else:
        form = AudioFileForm()
    return render(request, 'genre_output.html', {'form': form})


def home(request):
    return render(request, 'home.html')

def genre_classification(request):
    return render(request, 'genre_classification.html')

def genre_recommendation(request):
    return render(request, 'genre_recommendation.html')

def about(request):
    return render(request, 'about.html')

def statistics(request):
    return render(request,'statistics.html')

def get_started(request):
    return render(request, 'get_started.html')
# views.py
from django.shortcuts import render
from .models import AudioFile, SongRecommendation  # Assuming you have a model for recommendations

# Add the existing functions and imports

def recommend_songs(request, genre):
    # Fetch the recommended songs for the given genre
    recommended_songs = SongRecommendation.objects.filter(genre=genre)[:5]
    
    context = {
        'recommended_songs': recommended_songs
    }
    return render(request, 'song_recommendations.html', context)

