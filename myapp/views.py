from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserRegistrationForm , UserProfileUpdateForm
from .models import User , Comment , Post

def index(request):
    posts = Post.objects.all()
    return render(request, 'index.html', {'posts': posts})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email') 
            request.session['email'] = email 
            messages.success(request, 'Registration successful. You are now logged in.')
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

from .models import User

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if email and password:
            try:
                user = User.objects.get(email=email, password=password)
                request.session['email'] = user.email
                return redirect('dashboard')  # Redirect to dashboard
            except User.DoesNotExist:
                # User with the given email and password does not exist
                messages.error(request, 'Invalid email or password')
        else:
            messages.error(request, 'Email and password are required')
    
    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    request.session.pop('email', None)  # Remove email from session upon logout
    messages.success(request, 'You have been logged out.')
    return redirect('index')


def update_profile(request):
    email = request.session.get('email')
    if not email:
        messages.error(request, 'You need to be logged in to update your profile.')
        return redirect('login')
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('login')

    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            new_password = form.cleaned_data.get('new_password')
            if new_password:
                user.password = new_password  # Ideally, hash the password before saving
            user.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('dashboard')
    else:
        form = UserProfileUpdateForm(instance=user)
    
    return render(request, 'update_profile.html', {'form': form, 'user': user})


def dashboard(request):
    email = request.session.get('email')
    if not email:
        messages.error(request, 'You need to be logged in to view the dashboard.')
        return redirect('login')
    
    user = get_object_or_404(User, email=email)
    posts = Post.objects.all()
    return render(request, 'dashboard.html', {'posts': posts, 'user': user})



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import CommentForm
from .models import Post, Comment, User
import nltk
from nltk.corpus import sentiwordnet as swn
from nltk.corpus import wordnet

nltk.download('sentiwordnet')
nltk.download('wordnet')

def calculate_sentiment(comment_text):
    sentiment_score = 0.0
    sentiment_label = 'neutral'
    words = comment_text.split()

    for word in words:
        synsets = wordnet.synsets(word)
        if not synsets:
            continue
        synset = synsets[0]
        swn_synset = swn.senti_synset(synset.name())
        sentiment_score += swn_synset.pos_score() - swn_synset.neg_score()

    if sentiment_score > 0:
        sentiment_label = 'positive'
    elif sentiment_score < 0:
        sentiment_label = 'negative'

    return sentiment_score, sentiment_label

def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    email = request.session.get('email')
    
    if not email:
        messages.error(request, 'You need to be logged in to add a comment.')
        return redirect('login')
    
    user = get_object_or_404(User, email=email)
    comments = post.comments.all()  # Fetch all comments related to the post
    user_has_commented = comments.filter(user=user).exists()  # Check if user has already commented on the post
    
    if request.method == 'POST' and not user_has_commented:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = user  # Assign the authenticated user instance from your custom User model
            
            # Calculate sentiment
            comment.sentiment_score, comment.sentiment_label = calculate_sentiment(comment.comment_text)
            
            comment.save()
            messages.success(request, 'Your comment has been added.')
            return redirect('add_comment', post_id=post.id)
    else:
        form = CommentForm()
    
    return render(request, 'add_comment.html', {
        'form': form,
        'post': post,
        'comments': comments,
        'user_has_commented': user_has_commented
    })
