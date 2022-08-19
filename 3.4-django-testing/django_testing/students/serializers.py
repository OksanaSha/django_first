from rest_framework import serializers, exceptions

from students.models import Course
from django.conf import settings


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "students")

    def validate_students(self, value):
        max_value = settings.MAX_STUDENTS_PER_COURSE
        if len(value) > max_value:
            raise exceptions.ValidationError(
                f'Max student per course: {max_value}'
            )
        return value
