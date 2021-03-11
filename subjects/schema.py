import graphene
from graphene_django import DjangoObjectType, DjangoListField
from subjects import models


class SubjectType(DjangoObjectType):
    class Meta:
        model = models.Subject
        fields = ("id", "name", "exam_type")


class PaperType(DjangoObjectType):
    class Meta:
        model = models.Paper
        fields = ("id", "subject", "exam_year")


class QuestionType(DjangoObjectType):
    class Meta:
        model = models.Question
        fields = ("id", "paper", "question", "instruction", "image", "description")


class ChoiceType(DjangoObjectType):
    class Meta:
        model = models.Choice
        fields = ("id", "question", "choice", "is_correct")


class Query(graphene.ObjectType):

    all_subjects = graphene.List(SubjectType)
    all_papers = DjangoListField(PaperType)
    questions_by_paper = DjangoListField(QuestionType, paper=graphene.Int(required=True))
    choices_by_question = DjangoListField(ChoiceType, question=graphene.Int(required=True))

    def resolve_all_subjects(root, info):
        return models.Subject.objects.all()

    def resolve_all_papers(root, info):
        return models.Paper.objects.all()

    def resolve_questions_by_paper(root, info, paper):
        try:
            return models.Question.objects.filter(paper=paper)
        except models.Question.DoesNotExist:
            return None

    def resolve_choices_by_question(root, info, question):
        try:
            return models.Choice.objects.filter(question=question)
        except models.Choice.DoesNotExist:
            return None


schema = graphene.Schema(query=Query)
