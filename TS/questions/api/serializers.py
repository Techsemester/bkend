from rest_framework import serializers

from questions.models import Question, Answer, Vote


class QuestionSerializer(serializers.ModelSerializer):
    total_answers = serializers.SerializerMethodField(method_name='all_answers')
    class Meta:
        model = Question
        fields = ['id', 'user', 'create_date', 'body', 'update_date', 'active', 'total_answers']

    def all_answers(self, obj):
        votes = Answer.objects.filter(question=obj).count()
        return votes

class AnswerSerializer(serializers.ModelSerializer):
    upvotes = serializers.SerializerMethodField(method_name='total_upvotes')
    downvotes = serializers.SerializerMethodField(method_name='total_downvotes')
    in_reply_to_details = serializers.SerializerMethodField(method_name='reply_to_body')
    # in_reply_to_comment_name = serializers.CharField(source='in_reply_to')
    # in_reply_to_username = serializers.SerializerMethodField(method_name='reply_to_body_username')
    
    class Meta:
        model = Answer
        fields = ['id', 'user', 'question', 'create_date', 'body', 'update_date',
        'active', 'upvotes', 'downvotes', 'in_reply_to_details']

    def reply_to_body(self, obj):
        "Give us the original answer body or return none if not applicable"
        try: 
            return {
                "id": obj.in_reply_to.id,
                "user_id": obj.in_reply_to.user.id,
                "user": obj.in_reply_to.user.username,
                "body":obj.in_reply_to.body, 
                }
        except:
            return None

    # def reply_to_username(self, obj):
    #     "Give us the original answer body or return none if not applicable"
    #     try:
    #         return obj.in_reply_to.username
    #     except:
    #         return None

    
    def total_upvotes(self, obj):
        votes = Vote.objects.filter(answer=obj, up=True).count()
        return votes

    def total_downvotes(self, obj):
        votes = Vote.objects.filter(answer=obj, down=True).count()
        return votes