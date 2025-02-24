from django.shortcuts import render, redirect
from django.http import HttpResponse
import random
from .models import Quiz, TrueFalse

def quiz_view(request):
    # Initialize session variables
    if 'question_number' not in request.session:
        request.session['question_number'] = 0
    if 'quiz_result' not in request.session:
        request.session['quiz_result'] = 0
    if 'quiz_finished' not in request.session:
        request.session['quiz_finished'] = False

    question_number = request.session['question_number']
    quiz_finished = request.session['quiz_finished']

    print(f"Question Number: {question_number}") #DEBUG
    print(f"Current Score: {request.session['quiz_result']}") #DEBUG

    # If quiz is finished, redirect to results
    if quiz_finished:
        return redirect('quizzes:quiz_result')

    # Select unique questions if not already chosen
    if 'selected_questions' not in request.session:
        all_questions = list(Quiz.objects.all()) + list(TrueFalse.objects.all())
        random.shuffle(all_questions)  
        request.session['selected_questions'] = [q.id for q in all_questions[:11]]  
        request.session.modified = True

    # Check for missing questions in database "indexError" and provide clearer error message
    if len(request.session['selected_questions']) < 11:
        return HttpResponse("Error: missing quiz questions in the database. Probably because db.sqlite3 is not tracked by git. Add some questions to make it work")

    # Retrieve the current question by ID
    question_id = request.session['selected_questions'][question_number]
    question = Quiz.objects.filter(id=question_id).first() or TrueFalse.objects.filter(id=question_id).first()

    if request.method == "POST":
        print("POST data:", request.POST)  # DEBUG 
        selected_answer = request.POST.get("question_choice")
        print("Selected Answer:", selected_answer)  # DEBUG

        if selected_answer:
            # Check if the answer is correct
            if isinstance(question, Quiz) and selected_answer.strip() == question.correct_choice.strip():
                print(f"Checking Quiz Question: {question.correct_choice} vs {selected_answer}") #DEBUG
                request.session['quiz_result'] += 1
                print(f"Correct Answer! Updated Score: {request.session['quiz_result']}") #DEBUG
            elif isinstance(question, TrueFalse) and ((selected_answer == "True" and question.is_true) or (selected_answer == "False" and not question.is_true)):
                print(f"Checking True/False Question: {question.is_true} vs {selected_answer}") #DEBUG
                request.session['quiz_result'] += 1
                print(f"Correct Answer! Updated Score: {request.session['quiz_result']}") #DEBUG

            # Move to the next question
            request.session['question_number'] += 1
            request.session.modified = True

            # Check if quiz is completed
            if request.session['question_number'] >= 10:
                request.session['quiz_finished'] = True
                return redirect('quiz:quiz_results')

            return redirect('quiz:quiz')

    return render(request, 'quizzes/quiz.html', {'question': question, 'question_number': question_number})

def quiz_results_view(request):
    score = request.session.get('quiz_result', 0)
    print(f"Score at Result Page: {score}")

    # After showing the result, reset the session for a new quiz
    if 'quiz_finished' in request.session and request.session['quiz_finished']:
        del request.session['question_number'] 
        del request.session['quiz_result'] 
        del request.session['quiz_finished']  
        del request.session['selected_questions']
        
    return render(request, 'quizzes/quiz_result.html', {'score': score})
