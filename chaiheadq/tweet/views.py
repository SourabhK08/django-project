from django.shortcuts import render
from .models import Tweet
from .forms import TweetForm
from django.shortcuts import get_object_or_404,redirect
# Create your views here.

def index(request):
    return render(request,'index.html')

# LIST ALL THE TWEETS ON A PAGE

def tweet_list(request):
    tweets = Tweet.objects.all()
    for tweet in tweets:
        if not tweet.photo:
            tweet.photo = None  # Handle the missing photo as needed
    return render(request, 'tweet_list.html', {'tweets': tweets})


# CREATING A TWEET 

def tweet_create(request):
    
    #CASE 1 WHEN USER HAS AN EMPTY FORM   
    
    # if:
    #     pass
    # else:
    #     form = TweetForm()
    # return render(request, 'tweet_form.html',{'form' : form})

    # CASE 2 WHEN  USER HAS FILLED THE FORM
    
    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES)
        
        # HANDLING SECURITY MEASURES
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
        
    else:
        form = TweetForm()
    return render(request, 'tweet_form.html',{'form' : form})


# HOW TO EDIT THE TWEET 

def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user = request.user)
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES,instance=tweet)
        
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list') 
    else:
        form = TweetForm(instance=tweet) 
    return render(request, 'tweet_form.html',{'form' : form})


# DELETING THE TWEET

def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user = request.user)
    if request.method == 'POST':
        tweet.delete()
        return redirect('tweet_list')
    return render(request, 'tweet_confirm_delete.html',{'tweet' : tweet})
    
