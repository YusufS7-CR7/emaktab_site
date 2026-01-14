from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Grade(models.Model):
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='grades'
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='grades'
    )
    teacher = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='given_grades'
    )
    value = models.IntegerField()
    comment = models.CharField(max_length=255, blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.student.username} - {self.subject.name}: {self.value}'


class Profile(models.Model):
    ROLE_CHOICES = (
        ('student', 'Ученик'),
        ('teacher', 'Учитель'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f'{self.user.username} ({self.role})'


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, role='student')

