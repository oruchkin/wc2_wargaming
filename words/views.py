from django.shortcuts import render
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
import math


from django.shortcuts import redirect, render

from django.db.models import Sum
from django.db.models import Count


from .forms import Query_form, Query_txt_form
from .models import Document, User, Word, Query_name, Query_name_Words
from .helpers import counter
# Create your views here.

def index(request):
    return render(request, "words/index.html")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "words/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "words/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "words/register.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "words/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "words/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def query(request):
    if request.method == "POST":
        query_form = Query_form(request.POST)
        if query_form.is_valid():            
            query_text = query_form.cleaned_data["query_text"]
            query_title = query_form.cleaned_data["query_title"]            
            # saving new Query_name
            new_query_name = Query_name(username = request.user, query_title=query_title)
            new_query_name.save()            
            #temporary dict(no sql saving) for page output !LOGIC here!
            dictionary = counter(query_text)                                            
            # sql saving here                                            
            for i in dictionary:                        
                #check if word does NOT exist
                if len(Word.objects.filter(word=i)) < 1:
                    new_word = Word(word=i, counter=dictionary[i])
                    new_word.save()   
                    
                    new_query_name_words = Query_name_Words(word_id=new_word, query_name_id=new_query_name, counter=dictionary[i])  
                    new_query_name_words.save()  
                                                      
                #if word EXISTs
                else:
                    word = Word.objects.filter(word=i).first()                    
                    word.counter += dictionary[i]
                    word.save()                    
                        
                    new_query_name_words = Query_name_Words(word_id=word, query_name_id=new_query_name, counter=dictionary[i])
                    new_query_name_words.save()                                                                        
                      
            return render(request, "words/query_result.html", {
                "query_detailed": dictionary,
            })                      
            
        return HttpResponseRedirect(reverse("index"))
        
    elif request.method == "GET":                
        query_form = Query_form()
        return render(request, "words/query.html",{
            "query_form":query_form,
        })
        
        
def query_txt(request):
    if request.method == "POST":        
        query_txt_form = Query_txt_form(request.POST, request.FILES)
        
        if query_txt_form.is_valid():
            query_title = query_txt_form.cleaned_data["query_title"]           
            new_file = Document(docfile = request.FILES['docfile'])
            new_file.save() 
            
            #converting .txt to string
            string_obj = new_file.docfile            
            text_from_obj = string_obj.read().decode()   
                     
            #counitng words in this string
            dictionary = counter(text_from_obj)            
            
            #deleting object and its file
            new_file.docfile.delete()
            new_file.delete()
            
            #saving data to objects
            new_query_name = Query_name(username=request.user, query_title=query_title)
            new_query_name.save()
            
            ammount_of_documents = len(Query_name.objects.all()) #TF-IDF logic
            
            
            # sql saving here
            for i in dictionary:
                #check if word does NOT exist
                if len(Word.objects.filter(word=i)) < 1:
                    new_word = Word(word=i, counter=dictionary[i], idf_ammount=1) #TF-IDF logic
                    
                    new_word.save()

                    new_query_name_words = Query_name_Words(word_id=new_word, query_name_id=new_query_name, counter=dictionary[i])  #TF-IDF logic
                    new_query_name_words.save()

                #if word EXISTs
                else:
                    word = Word.objects.filter(word=i).first()
                    word.counter += dictionary[i]
                    word.idf_ammount += 1  #TF-IDF logic
                    
                    
                    word.save()

                    new_query_name_words = Query_name_Words(word_id=word, query_name_id=new_query_name, counter=dictionary[i]) #TF-IDF logic
                    new_query_name_words.save()      
                    
            # update all words idf  TF-IDF logic
            all_words = Word.objects.all()      
            for i in all_words:
                
                i.idf = math.log10(ammount_of_documents / i.idf_ammount)                
                i.save()
                
            return render(request, "words/query_result.html", {
                "query_detailed": dictionary,
            })
        
        else:        
            print("form is not valid")
            query_txt_form = Query_txt_form()
            return render(request, "words/query_txt.html", {
                "query_txt_form": query_txt_form,
                "message" : "form is not valid"
            })
                
        
    else:        
        query_txt_form = Query_txt_form()
        return render(request, "words/query_txt.html", {
            "query_txt_form": query_txt_form,
        })
        

# https://stackoverflow.com/questions/629551/how-to-query-as-group-by-in-django
def history(request):
    query_name_list = Query_name.objects.filter(username=request.user)   
    #query_name_words_stats_dict = Query_name_Words.objects.select_related("query_name_id").values("query_name_id").distinct()
    query_name_words_stats = Query_name_Words.objects.filter(query_name_id__in=query_name_list).values(
        "query_name_id").distinct().annotate(different_words=Count('word_id'), total_words=Sum('counter'))  
    rows = zip(query_name_list, query_name_words_stats)    
                

    return render(request, "words/history.html",{        
        "rows":rows,
    })


def query_detailed(request, query_name_pk):
    # words, and number of different words
    words_are = Query_name_Words.objects.filter(query_name_id=query_name_pk).select_related('word_id').order_by('-counter')
    # Title, time created
    query_name = Query_name.objects.get(pk=query_name_pk)    
    # number words_total
    words_total = Query_name_Words.objects.filter(query_name_id=query_name_pk).values('query_name_id').annotate(Sum('counter'))   
    
    
    len_of_column = math.floor(int(len(words_are)) / 5)
    
    
    first_table = words_are[0 : len_of_column+1]
    second_table = words_are[len_of_column+1 : 2*len_of_column+1]
    third_table = words_are[2*len_of_column+1: 3*len_of_column+1]
    fourth_table = words_are[3*len_of_column+1: 4*len_of_column+1]
    fifth_table = words_are[4*len_of_column+1: 5*len_of_column+1]
    
    # WARGAMING LOGIC    
    words_are_wargaming = Query_name_Words.objects.filter(query_name_id=query_name_pk)
    words_are_wargaming  = words_are_wargaming.order_by('-word_id__idf')[0:50]

    return render(request, "words/query_detailed.html", {
        "words_are": words_are,
        "query_name": query_name,
        "words_total": words_total,
        #tables
        "first_table": first_table,
        "second_table": second_table,     
        "third_table": third_table,
        "fourth_table": fourth_table,
        "fifth_table": fifth_table,
        # wargaming
        "words_are_wargaming":words_are_wargaming,
    })


def global_words(request):
    words = Word.objects.all().order_by('-counter', 'word')    
    words_total_number = Word.objects.all().aggregate(Sum('counter'))
    
    return render(request, "words/global_words.html",{
        "words": words,
        "words_total_number": words_total_number,
    })

# https://docs.djangoproject.com/en/dev/ref/models/querysets/#select-related
def global_words_personal(request):
    query_names = Query_name.objects.filter(username = request.user).select_related('username')          
    words = Query_name_Words.objects.filter(query_name_id__in=query_names).select_related(
        'query_name_id', 'word_id').values('word_id').annotate(Sum('counter')).order_by("-counter__sum")
    
    list_of_words_id = []   
    for i in words:
        list_of_words_id.append(i["word_id"])    
    particular_word = Word.objects.filter(pk__in=list_of_words_id)    
    
    this_words_counter = []
    this_words_counter_summ = 0
    for i in words:
        this_words_counter.append(i["counter__sum"])
        this_words_counter_summ += int(i["counter__sum"])
    print(this_words_counter_summ)
    
    words_stat = zip(particular_word, this_words_counter)
    
    return render(request, "words/global_words_personal.html", {
        "words": words,        
        "words_stat": words_stat,
        "this_words_counter_summ": this_words_counter_summ,
    })
