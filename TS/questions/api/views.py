from account.notifications import sendEmail
from django.utils import timezone
from questions.models import Answer, Question, Vote
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from account.api.views import CustomPagination
from questions.api.serializers import QuestionSerializer, AnswerSerializer

@api_view(['POST',])
@permission_classes([IsAuthenticated])
def ask_question(request):
    """
    Create a question
    """
    user = request.user
    body = request.data.get('body')

    if not body:
        return Response({"message":"Body cannot be empty"}, status=status.HTTP_417_EXPECTATION_FAILED)

    question = Question(user=user, body=body)
    question.save()
    #Count for user
    user.total_questions += 1
    user.save()
    return Response({"message":"Question created!"}, status=status.HTTP_201_CREATED)



@api_view(['GET',])
@permission_classes([])
def all_questions(request):
    """
    Get all active questions on the system
    Deliver result 20 items per page.
    """
    try:
        paginator = CustomPagination()
        paginator.page_size = 20
        questions = Question.objects.filter(active=True).order_by('-create_date')
        if not questions:
            return Response( {'message': 'No questions created yet'},status=status.HTTP_404_NOT_FOUND)
        result_page = paginator.paginate_queryset(questions, request)
    except Exception as e:
        print(e)
        return Response({'message': 'There was an issue processing this request'}, status=status.HTTP_400_BAD_REQUEST)

    questionserializer = QuestionSerializer(result_page, many=True)
    return paginator.get_paginated_response(questionserializer.data)



@api_view(['POST',])
@permission_classes([IsAuthenticated])
def answer_a_question(request):
    """
    Create an answer (by a user) to a question
    """
    user = request.user
    body = request.data.get('body')
    answer_id = request.data.get('answer_id')
    question_id = request.data.get('question_id')

    if not body:
        return Response({"message":"Body cannot be empty"}, status=status.HTTP_417_EXPECTATION_FAILED)

    if not question_id:
        return Response({"message":"We did not get the question id"}, status=status.HTTP_417_EXPECTATION_FAILED)

    question = Question.objects.filter(id=question_id)
    if not question:
        return Response({"message":f"there is no question with id {question_id}"}, status=status.HTTP_417_EXPECTATION_FAILED)

    question = question[0]
    if answer_id:
        try:
            in_reply = Answer.objects.get(id=answer_id)
            answer = Answer(user=user, question=question, body=body, in_reply_to=in_reply)
            answer.save()
            return Response({"message":"Answer created!"}, status=status.HTTP_201_CREATED)
        except:
            return Response({"message":f"there is no answer with id {answer_id}"}, status=status.HTTP_417_EXPECTATION_FAILED)

    answer = Answer(user=user, question=question, body=body)
    answer.save()
    user.total_answers += 1
    user.save()
    return Response({"message":"Answer created!"}, status=status.HTTP_201_CREATED)


@api_view(['POST',])
@permission_classes([])
def all_answers_to_question(request):
    """
    Get all answers to a question by question id
    """
    question_id = request.data.get('question_id')
    if not question_id:
        return Response({"message":"We did not get the question id"}, status=status.HTTP_417_EXPECTATION_FAILED)

    try:
        paginator = CustomPagination()
        paginator.page_size = 20
        answers = Answer.objects.filter(active=True).order_by('-create_date')
        if not answers:
            return Response( {'message': 'No answers to this question yet.'},status=status.HTTP_404_NOT_FOUND)
        
        result_page = paginator.paginate_queryset(answers, request)
    except Exception as e:
        print(e)
        return Response({'message': 'There was an issue processing this request'}, status=status.HTTP_400_BAD_REQUEST)

    answerserializer = AnswerSerializer(result_page, many=True)
    return paginator.get_paginated_response(answerserializer.data)

@api_view(['POST',])
@permission_classes([IsAuthenticated])
def vote(request):
    """
    Upvote or downvote a question by a user
    """
    user = request.user
    answer_id = request.data.get('answer_id')
    vote_value = request.data.get('vote')
    if not answer_id:
        return Response({"message":"We did not get the answer id"}, status=status.HTTP_417_EXPECTATION_FAILED)

    if not vote_value:
        return Response({"message":"We did not get the vote param"}, status=status.HTTP_417_EXPECTATION_FAILED)
    
    if vote_value.lower() not in ['up', 'down']:
        return Response({"message":f"We expect only 'up' or 'down' as value here. We got {vote_value}"}, status=status.HTTP_417_EXPECTATION_FAILED)

    #find the answer
    answer = Answer.objects.filter(id=answer_id)
    if not answer:
        return Response( {'message': f'We could not find an answer with id {answer_id}'},status=status.HTTP_404_NOT_FOUND)

    #Parse out the answer
    answer = answer[0]

    #Check if use has voted on this answer before and which way
    check = Vote.objects.filter(answer=answer, user=user)
    print(f"There are {len(check)} votes for answer {answer_id}")
    if not check: #They have note voted before. Get their votes in and mark their profiles
        print("user has no vote on this answer yet")
        if vote_value.lower() == 'up':
            vote = Vote(user=user, answer=answer, up=True)
            user.total_upvotes += 1
        elif vote_value.lower() == 'down':
            vote = Vote(user=user, answer=answer, down=True)
            user.total_downvotes += 1
        vote.save()
        user.save()
        return Response({"message":"Vote counted!"}, status=status.HTTP_201_CREATED)


    check = check[0]
    if vote_value == 'up':
        if check.up:
            print("user has a previous upvote on this answer")
            check.up = False #remove that vote. decrement their total votes count
            user.total_upvotes -= 1
        else:
            check.up = True
            user.total_upvotes += 1 #increment their total votes count
        user.save()
        check.save()
        return Response({"message":"Vote counted!"}, status=status.HTTP_201_CREATED)
    
    if vote_value == 'down':
        if check.down:
            print("user has a previous downvote on this answer")
            check.down = False #remove that vote. decrement their total votes count
            user.total_downvotes -= 1
        else:
            check.down = True
            user.total_downvotes += 1 #increment their total votes count
        user.save()
        check.save()
        return Response({"message":"Vote counted!"}, status=status.HTTP_201_CREATED)