#from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from mouseheatmapapp.forms import GetPathForm
from mouseheatmapapp.models import Choice, Question, InitialData

import pandas as pd
import glob
import os

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'mouseheatmapapp/index.html'
    context_object_name = 'initialdata'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        # return Question.objects.filter(
        #     pub_date__lte=timezone.now()
        # ).order_by('-pub_date')[:5]
        return InitialData.objects.filter(id=1)

class DetailView(generic.DetailView):
    model = Question
    template_name = 'mouseheatmapapp/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'mouseheatmapapp/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'mouseheatmapapp/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('mouseheatmapapp:results', args=(question.id,)))

class ReadMinMaxView(generic.ListView):
    model = InitialData
    template_name = 'mouseheatmapapp/read_minmax.html'
    context_object_name = 'latest_heatmap_info_list'

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    def read(request): 
        # path = r'C:\OpalData\Work\FundEducation\Research\MouseHeatmap\PreExperiment\MouseData\csv_file' # use your path
        # all_files = glob.glob(os.path.join(path , "/*.csv"))

        # li = []

        # for filename in all_files:
        #     df = pd.read_csv(filename, index_col=None, header=1)
        #     li.append(df)

        # frame = pd.concat(li, axis=0, ignore_index=True)

        obj = InitialData.objects.filter(id=1)
        path=obj.values('folder_path').first()['folder_path']
        # Get CSV files list from a folder
        # path = 'C:\OpalData\Work\FundEducation\Research\MouseHeatmap\PreExperiment\MouseData\csv_file'
        csv_files = glob.glob(path + "\*.csv")

        # Read each CSV file into DataFrame
        # This creates a list of dataframes
        df_lists1 = (pd.read_csv(file) for file in csv_files)
        # Create new column name 'DURATION_TIME_MS' for each df_list
        print("Datatype is ")
        print(type(df_lists1))
        my_list = list(df_lists1)
        print(type(my_list))
        print(type(my_list[0]))
        print(my_list[0].get('UNIX_TIMESTAMP_MS'))
        i = 0
        # Compute Duration Time and max-min total of all csv file
        mouse_movement_min=99999999
        mouse_movement_max=0

        mouse_click_min=99999999
        mouse_click_max=0
        for x in my_list:
            print("i="+str(i))
            print(x.get('UNIX_TIMESTAMP_MS'))

            # Find min-max value of Mouse movement data in each df
            mm_min = x.groupby(['CLIENTX', 'CLIENTY']).size().min(axis = 0, skipna = True)
            mm_max = x.groupby(['CLIENTX', 'CLIENTY']).size().max(axis = 0, skipna = True)
            print('mm_min=' + str(mm_min))
            print('mm_max=' + str(mm_max))
            if(mouse_movement_min>mm_min):
                mouse_movement_min=mm_min
            if(mouse_movement_max<mm_max):
                mouse_movement_max=mm_max
            
            # Find min-max value of Mouse click data in each df
            # print(type(x.info()))
            x_filter = x.query("MOUSE_CLICKED == True")
            print(x_filter)
            mc_min = x_filter.groupby(['CLIENTX', 'CLIENTY']).size().min(axis = 0, skipna = True)
            mc_max = x_filter.groupby(['CLIENTX', 'CLIENTY']).size().max(axis = 0, skipna = True)
            print('mc_min=' + str(mc_min))
            print('mc_max=' + str(mc_max))
            if(mouse_click_min>mc_min):
                mouse_click_min=mc_min
            if(mouse_click_max<mc_max):
                mouse_click_max=mc_max

            # Compute Duration Time
            j=0
            #for y in x.get('UNIX_TIMESTAMP_MS'):
            duration_value=[]
            print(len(x.index))
            while j < len(x.index):
                if j < (len(x.index)-1):
                    # print("i="+str(i)+" j="+str(j))
                    # print(x.at[j,'UNIX_TIMESTAMP_MS'])
                    duration_value.append(int(x.at[j+1,'UNIX_TIMESTAMP_MS']) - int(x.at[j,'UNIX_TIMESTAMP_MS']))
                else:
                    duration_value.append(0)
                j += 1
            x.insert(1,"DURATION_TIME",duration_value,allow_duplicates=True)
            i += 1


        # Concatenate all DataFrames
        all_df = pd.concat(my_list, ignore_index=True)
        # find min-max value of DURATION_TIME in all_df
        duration_time_min=all_df['DURATION_TIME'].min(axis = 0, skipna = True)
        duration_time_max=all_df['DURATION_TIME'].max(axis = 0, skipna = True)

        print("Mouse Movement Min:"+str(mouse_movement_min))
        print("Mouse Movement Max:"+str(mouse_movement_max))
        print("Duration Time Min:"+str(duration_time_min))
        print("Duration Time Max:"+str(duration_time_max))
        print("Mouse Click Min:"+str(mouse_click_min))
        print("Mouse Click Max:"+str(mouse_click_max))

        # insert or update min-max value of DURATION_TIME in DB
        # get item or create new one if it doesn't exist
        # item, created = InitialData.objects.filter(id=1).get_or_create(
        #     min_duration_time=duration_time_min,
        #     max_duration_time=duration_time_max,
        # )
        # # if it already exist, update quantity
        # if not created:
        #     item.min_duration_time = duration_time_min
        #     item.max_duration_time = duration_time_max
        # # whether item was created or updated save it to database
        # item.save()

        # try:
        #     obj = InitialData.objects.filter(id=1).update(
        #         min_duration_time=duration_time_min,
        #         max_duration_time=duration_time_max
        #         )
        # except InitialData.DoesNotExist:
        #     InitialData.objects.create(
        #         min_duration_time=duration_time_min,
        #         max_duration_time=duration_time_max
        # )

        obj = InitialData.objects.filter(id=1)
        if obj.exists():
            obj.update(
                min_duration_time=duration_time_min,
                max_duration_time=duration_time_max,
                min_mouse_movement=mouse_movement_min,
                max_mouse_movement=mouse_movement_max,
                min_mouse_click=mouse_click_min,
                max_mouse_click=mouse_click_max
                )
        else:
            InitialData.objects.create(
                min_duration_time=duration_time_min,
                max_duration_time=duration_time_max,
                min_mouse_movement=mouse_movement_min,
                max_mouse_movement=mouse_movement_max,
                min_mouse_click=mouse_click_min,
                max_mouse_click=mouse_click_max
                )

        # all_df.info(verbose=True)
        # return render(request, 'mouseheatmapapp/index.html', {'data': all_df})
        # response = redirect('http://127.0.0.1:8000/mouseheatmapapp/')
        # return response
        return HttpResponseRedirect(reverse('mouseheatmapapp:index'))

class GenDurationTimeHMView(generic.ListView):
    template_name = 'mouseheatmapapp/gen_durationtimehm.html'
    context_object_name = 'initialdata'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['use_value'] = self.kwargs['use_value']
        return context

    def get_queryset(self):
        return InitialData.objects.filter(id=1)

class GenMouseMovementHMView(generic.ListView):
    template_name = 'mouseheatmapapp/gen_mousemovementhm.html'
    context_object_name = 'initialdata'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['use_value'] = self.kwargs['use_value']
        return context

    def get_queryset(self):
        return InitialData.objects.filter(id=1)

class GenMouseClickHMView(generic.ListView):
    template_name = 'mouseheatmapapp/gen_mouseclickhm.html'
    context_object_name = 'initialdata'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['use_value'] = self.kwargs['use_value']
        return context

    def get_queryset(self):
        return InitialData.objects.filter(id=1)

def getpath(request):
    """View function for renewing a specific BookInstance by librarian."""
    obj = InitialData.objects.filter(id=1)
    if obj.exists():
        # If this is a POST request then process the Form data
        if request.method == 'POST':

            # Create a form instance and populate it with data from the request (binding):
            form = GetPathForm(request.POST)

            # Check if the form is valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
                obj.folder_path = form.cleaned_data['folder_path']
                obj.update(folder_path=obj.folder_path)

                # redirect to a new URL:
                return HttpResponseRedirect(reverse('mouseheatmapapp:read_minmax'))

        # If this is a GET (or any other method) create the default form.
        else:
            proposed_folder_path = obj.values('folder_path').first()
            form = GetPathForm(initial={'folder_path': proposed_folder_path['folder_path']})
    else:
        form = GetPathForm(initial={'folder_path': ''})
        InitialData.objects.create(
                folder_path='',
                )
        obj = InitialData.objects.filter(id=1)
        

    context = {
        'form': form,
        'instance': obj,
    }

    return render(request, 'mouseheatmapapp/get_path.html', context)