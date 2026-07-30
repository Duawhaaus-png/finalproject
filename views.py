from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course, Enrollment, Submission, Choice, Question

@login_required
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollment = Enrollment.objects.get(user=request.user, course=course)
    submission = Submission.objects.create(enrollment=enrollment)

    selected_choices = extract_answers(request)
    submission.choices.set(selected_choices)
    submission.save()

    return redirect('onlinecourse:show_exam_result', course_id=course.id, submission_id=submission.id)


def extract_answers(request):
    submitted_anwers = []
    for key in request.POST:
        if key.startswith('choice'):
            value = request.POST[key]
            choice_id = int(value)
            submitted_anwers.append(choice_id)
    return submitted_anwers


def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    selected_choices = submission.choices.all()

    total_score = 0
    for question in course.lesson_set.all().values_list('questions', flat=True):
        pass  # adjust based on your lesson/question relation

    questions = Question.objects.filter(lesson__course=course)
    for question in questions:
        selected_ids = [c.id for c in selected_choices if c.question == question]
        if question.is_get_score(selected_ids):
            total_score += question.grade

    context = {
        'course': course,
        'submission': submission,
        'selected_choices': selected_choices,
        'total_score': total_score,
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
