from django.db import models

# MCQ Quiz Model
class Quiz(models.Model):
    question_text = models.CharField(max_length=200, unique=True)
    choice1 = models.CharField(max_length=200)
    choice2 = models.CharField(max_length=200)
    choice3 = models.CharField(max_length=200)
    choice4 = models.CharField(max_length=200)
    correct_choice = models.CharField(max_length=200)

    def __str__(self):
        return self.question_text

    @property
    def get_choices(self):
        return [self.choice1, self.choice2, self.choice3, self.choice4]

# True/False Model
class TrueFalse(models.Model):
    question_text = models.CharField(max_length=200, unique=True)
    is_true = models.BooleanField(default=True)

    def __str__(self):
        return self.question_text

    @property
    def get_choices(self):
        return ['True', 'False']
