from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.urls import reverse


def image_file_path(instance, filename):
    """Generate file path for lodge image"""
    return '/'.join(['questions', str(instance.paper.subject.name).replace(' ', '_'), filename])


class Subject(models.Model):
    # Subject of the past questions
    name = models.CharField(max_length=255)
    exam_type = models.CharField(max_length=255)

    class Meta:
        unique_together = [
            ('name', 'exam_type')
        ]

    def get_absolute_url(self):
        return reverse('subjects:detail', kwargs={'subject_id': self.pk})

    def __str__(self):
        return self.name + " - " + self.exam_type


class Paper(models.Model):
    # the paper and year
    subject = models.ForeignKey(
        Subject, models.CASCADE, related_name="papers")
    exam_year = models.IntegerField(validators=[
        MaxValueValidator(9999),
        MinValueValidator(1000)
    ])

    class Meta:
        ordering = ['exam_year']
        unique_together = [
            ('subject', 'exam_year')
        ]

    def get_absolute_url(self):
        return reverse('subjects:paper', kwargs={'paper_id': self.pk})

    def __str__(self):
        return f'{self.subject} {self.exam_year}'


class Question(models.Model):
    paper = models.ForeignKey(
        Paper, models.CASCADE, related_name="questions")
    question = models.CharField(max_length=1000)
    image = models.ImageField(blank=True, null=True, upload_to=image_file_path)
    description = models.TextField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse('subjects:paper', kwargs={'paper_id': self.paper.pk})

    def __str__(self):
        return self.question


class Choice(models.Model):
    question = models.ForeignKey(
        Question, models.CASCADE, related_name="choices")
    choice = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False, help_text="Please an answer is required!")

    def save(self, *args, **kwargs):
        if self.is_correct:
            try:
                temp = Choice.objects.get(question=self.question, is_correct=True)
                if self != temp:
                    temp.is_correct = False
                    temp.save()
            except Choice.DoesNotExist:
                pass
        super(Choice, self).save(*args, **kwargs)

    def __str__(self):
        return self.choice
