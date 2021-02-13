from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
# from django.contrib import messages
from django.db.models import Q

# from django.views.generic.list import ListView
from subjects.models import Subject, Paper, Question, Choice


def index(request, subject_id=None):
    subject_list = Subject.objects.all()

    if subject_id is not None:
        paper_list = get_list_or_404(Paper.objects.order_by('-exam_year'), subject=subject_id)
        context = {'subject_list': subject_list, 'paper_list': paper_list}
    else:
        context = {'subject_list': subject_list}

    return render(request, 'subjects/index.html', context)


def paper_view(request, paper_id):
    # question_list = Question.objects.filter(subject=subject_id)
    if request.method == 'POST':
        # print(request.POST)
        # print('choice', int(request.POST['choice']))
        # print("question_id", int(request.POST['question_id']))

        question = get_object_or_404(Question, pk=int(request.POST['question_id']))
        is_correct = question.choices.get(is_correct=True)
        is_answer = False
        if int(request.POST['choice']) == is_correct.id:
            is_answer = True
        else:
            is_answer = False

        answer = 'The answer is ' + is_correct.choice
        return JsonResponse({'is_answer': is_answer, 'answer': answer}, status=200)

    elif request.method == "GET":
        paper_list = get_list_or_404(Question, paper=paper_id)

        return render(request, 'subjects/questions.html', {'paper_list': paper_list})


def search(request):
    print(request.GET)
    # , kwargs={'bar': "FooBar"}
    # return render(request, "subjects/search.html")
    return redirect(reverse("subjects/search.html"))


def autosuggest(request):
    # + ',' + str(i.get_absolute_url())
    q = request.GET.get('term')
    subjects = Subject.objects.filter(Q(name__icontains=q) | Q(exam_type__icontains=q))
    papers = Paper.objects.filter(Q(exam_year__icontains=q))
    question = Question.objects.filter(Q(question__icontains=q) | Q(description__icontains=q))
    s_list = [str(i) + ',__' + i.get_absolute_url() for i in subjects]
    p_list = [str(i) + ',__' + i.get_absolute_url() for i in papers]
    q_list = [str(i) + ',__' + i.get_absolute_url() for i in question]
    # print(s_list)
    # print(p_list)
    return JsonResponse(s_list + p_list + q_list, safe=False)
