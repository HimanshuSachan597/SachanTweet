from django.shortcuts import render
from .forms import TweetForms, UserRegistrationForm
from .models import Tweet
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login


# Create your views here.
def index (request):
     return render(request, 'index.html')

# def tweet_list(request): # this method define the list of tweet (ham all tweet ko ak list form me le rhe hai)
#      tweets = Tweet.objects.all().order_by('-create_at')  # hmesa model ke sath object ka use krte hai 
#      return render (request,'tweet_list.html', {'tweets':tweets}) # object dena jaruri hota hai

def tweet_list(request):
    # .distinct() har duplicate row hata dega
    tweets = Tweet.objects.order_by('-create_at').distinct()
    return render(request, 'tweet_list.html', {'tweets': tweets})
     ###################################################################
     # for tweet creation
     
@login_required     
def tweet_create(request):
     # if:
     #      pass
     # else:~
     #      form = TweetForms()
          
     # return render (request,'tweet_list.html' ,{'form':form})     it is a empty form dicleration (user ko hm empty form de rhe )
     
     
     if request.method == "POST":  # user form bhr ke post kr rha hai 
          form = TweetForms(request.POST , request.FILES) # yha hm form ko handel kr rhe hai (request.POST - se hm jo post kiya user ne use handel kr rhe hai aur request.FILES - se hm file ho bhi ... )
          
          if form.is_valid():  # check the form is valid or not  (csrf security)
               tweet=form.save(commit = False) #  form to save ho but commit = False hone ki vjh se bata base me nhi save hoga
               # check kre ge jo form bhej rha hai vo valod user hai ya nhi 
               
               tweet.user = request.user # user check 
               tweet.save() # ab tweet data base me save hoga
               return redirect('tweet_list')
     else:
          form = TweetForms()
          
     return render (request,'tweet_form.html' ,{'form':form})     

##########################################################################################
# for tweet edit 
@login_required
def tweet_edit(request,tweet_id):
     tweet = get_object_or_404(Tweet,pk= tweet_id, user= request.user) # get_object_or_404 esse ya object mile ga ya fir 404 mile ga 
     # Tweet ye hmara model rhe ga ,pk= tweet_id, ye hmari primary key rhe gi , user= request.user - its use to edit only otherized user
     if request.method == 'POST':
           form = TweetForms(request.POST , request.FILES,instance = tweet)
           if form.is_valid():
              tweet = form.save(commit= False)
              tweet.user = request.user
              tweet.save()
              return redirect('tweet_list')
     else:
          form = TweetForms(instance = tweet)   # instance = tweet it use for form prifill
     return render (request,'Tweet_form.html' ,{'form':form})  
     
     
    ##################################################################################### 
     # for delete the tweet 
@login_required     
def tweet_delete(request , tweet_id):
     
     tweet = get_object_or_404(Tweet,pk= tweet_id,user=request.user) # get_object_or_404 - ye kam kr rha ha ki tweet ko check kro 
     # ki vo kaun si tweet hai (tweet,pk= tweet_id,user=request.user) aur eski use se ye pta kro ki valid user hai ya nhi 
     if request.method == 'POST':  #  this method check that request is POST or nhi 
          tweet.delete()
          return redirect('tweet_list')
     return render (request,'tweet_confirm_delete.html',{'tweet':tweet})  
     
     ###############################################################################
     
     #form ke liye rout create kr rhe hai 
def  register(request): 
     
     if request.method == 'POST':
          form = UserRegistrationForm(request.POST)
          if form.is_valid():
               user = form.save(commit=False)
               user.set_password(form.cleaned_data['password1'])
               user.save()
               # mai chahta hu ki jaise hin user save ho to automatic login ho jaye (below)
               
               login(request,user)
               return redirect('tweet_list') # direct tweet list me phuch jaye ga
     else :
          form=  UserRegistrationForm()
        
     return render (request,'registration/register.html',{'form':form})  


def about(request):
    return render(request, 'about.html')


def profile_view(request, username):
     # get the user by username or return 404
     profile_user = get_object_or_404(User, username=username)
     # get tweets for that user
     tweets = Tweet.objects.filter(user=profile_user).order_by('-create_at')
     return render(request, 'profile.html', {'profile_user': profile_user, 'tweets': tweets})
