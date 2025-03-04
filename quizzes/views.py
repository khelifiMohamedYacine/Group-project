from django.shortcuts import render, redirect
from django.http import HttpResponse
import random
from .models import Quiz, TrueFalse, Question, UserQuizScore


def quiz_view(request):
    # Refuse access to users not logged in (defensive programming)
    if not request.user.is_authenticated:
        return redirect('login')


    quiz_id = 1 # hardcoded (temporaily) value that determines which quiz we are going to play

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

    # If quiz is finished, save and redirect to results
    if quiz_finished:
        user = request.user

        if UserQuizScore.objects.filter(user=user, quiz_id=quiz_id).exists():
            # handle case where the results already exists (defensive programming)

            # these lines update the old results to the new ones, need to agree what to actually do in this case
            user_quiz_score = UserQuizScore.objects.get(user=user, quiz_id=quiz_id)
            user_quiz_score.score = request.session['quiz_result']
            user_quiz_score.save()
        else:
            # Record the results in UserQuizScore model if none exists
            UserQuizScore.objects.create(
                user=user,
                quiz_id=quiz_id,
                score=request.session['quiz_result']
            )
        
        return redirect('quizzes:quiz_results')

    # Select unique questions if not already chosen
    if 'selected_questions' not in request.session:

        # Get all the questions belonging to that quiz
        quiz = Quiz.objects.get(quizID=quiz_id)
        all_questions = list(Question.objects.filter(quiz=quiz)) + list(TrueFalse.objects.filter(quiz=quiz))

        
        random.shuffle(all_questions) 

        # Store IDs of the questions we selected
        request.session['selected_questions'] = [q.id for q in all_questions]
        request.session.modified = True

    # Inform the user if there are no questions in that quiz somethings gone wrong
    if len(request.session['selected_questions']) <= 0:
        return HttpResponse("There are no questions selected in the quiz. Add some")

    # Retrieve the current question by ID
    question_id = request.session['selected_questions'][question_number]
    question = Question.objects.filter(id=question_id).first() or TrueFalse.objects.filter(id=question_id).first()

    if request.method == "POST":
        print("POST data:", request.POST)  # DEBUG 
        selected_answer = request.POST.get("question_choice")
        print("Selected Answer:", selected_answer)  # DEBUG

        if selected_answer:
            #store the users answer in session
            request.session[f"answer_{question_id}"] = selected_answer

            # Check if the answer is correct
            if isinstance(question, Question) and selected_answer.strip() == question.correct_choice.strip():
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
            if request.session['question_number'] >= len(request.session['selected_questions']):
                request.session['quiz_finished'] = True
                #return redirect('quizzes:quiz_results')

            return redirect('quizzes:quiz')

    print("Debug the question ", Question.objects.get(id=question_id))
    return render(request, 'quizzes/quiz.html', {'question': question, 'question_number': question_number})

def quiz_results_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if 'quiz_result' not in request.session or 'selected_questions' not in request.session:
        return redirect('core_app:home')

    score = request.session.get('quiz_result', 0)
    total_questions = len(request.session.get('selected_questions', []))
    print(f"Score at Result Page: {score}")

    # Construct the quiz answer feedback data
    quiz_feedback = []
    for question_id in request.session.get('selected_questions', []):
        
        question = Question.objects.filter(id=question_id).first() or TrueFalse.objects.filter(id=question_id).first()
        print("Question:", question)
        selected_answer = request.session.get(f"answer_{question_id}")
        print("selected Answer:", selected_answer)
        correct_answer = question.correct_choice if isinstance(question, Question) else ("True" if question.is_true else "False")
        print("correct Answer:", correct_answer)

        quiz_feedback.append({
            "question_text": question.question_text,
            "selected_answer": selected_answer,
            "correct_answer": correct_answer
        })
    
    response = render(request, 'quizzes/quiz_result.html', {
        'score': score, 
        'total_questions': total_questions, 
        'quiz_feedback': quiz_feedback
    })

    # After showing the result, reset the session for a new quiz
    for question_id in request.session.get('selected_questions', []):
        request.session.pop(f"answer_{question_id}", None)

    del request.session['question_number'] 
    del request.session['quiz_result'] 
    del request.session['quiz_finished']  
    del request.session['selected_questions']
        
    return response
