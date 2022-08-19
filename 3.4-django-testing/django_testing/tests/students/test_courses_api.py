import pytest
from model_bakery import baker
from rest_framework.test import APIClient
from students.models import Student, Course


@pytest.fixture()
def client():
    return APIClient()


@pytest.fixture()
def student():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory


@pytest.fixture()
def course():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.mark.django_db
def test_get_course(course, client):
    course = course()
    response = client.get(f'/api/v1/courses/{course.id}/')
    assert response.status_code == 200
    assert response.json()['name'] == course.name


@pytest.mark.django_db
def test_get_courses(course, client):
    courses = course(_quantity=6)
    response = client.get('/api/v1/courses/')
    data = response.json()
    assert response.status_code == 200
    for i, course in enumerate(data):
        assert courses[i].name == course['name']


@pytest.mark.django_db
def test_filter_id(course, client):
    courses = course(_quantity=6)
    test_course = courses[3]
    response = client.get(f'/api/v1/courses/?id={test_course.id}')
    data = response.json()[0]
    assert response.status_code == 200
    assert data['id'] == test_course.id
    assert data['name'] == test_course.name

@pytest.mark.django_db
def test_filter_name(course, client):
    courses = course(_quantity=6)
    test_course = courses[3]
    response = client.get(f'/api/v1/courses/?name={test_course.name}')
    data = response.json()[0]
    assert response.status_code == 200
    assert data['id'] == test_course.id
    assert data['name'] == test_course.name


@pytest.mark.django_db
def test_create_course(client):
    content = {'name': 'Python-developer'}
    response = client.post('/api/v1/courses/', content)
    data = response.json()
    assert response.status_code == 201
    assert data['name'] == content['name']


@pytest.mark.django_db
def test_update_course(client, course):
    test_course = course(_quantity=4)[2]
    content = {
        "name": "Python-developer",
    }
    response = client.patch(f'/api/v1/courses/{test_course.id}/', content)
    data = response.json()
    assert response.status_code == 200
    assert data['name'] == content['name']


@pytest.mark.django_db
def test_delete_course(client, course):
    test_course = course(_quantity=4)[2]
    response = client.delete(f'/api/v1/courses/{test_course.id}/')
    response_courses = client.get('/api/v1/courses/')
    assert response.status_code == 204
    assert len(response_courses.json()) == 3


@pytest.mark.parametrize(
    'max_students, students_on_course, status_code',
    [(5, 4, 200), (5, 6, 400)]
)
@pytest.mark.django_db
def test_max_students_value(
        client, course, settings, student,
        max_students, students_on_course, status_code):
    settings.MAX_STUDENTS_PER_COURSE = max_students
    course = course()
    students = student(_quantity=students_on_course)
    content = {
        'students': [student.id for student in students]
    }
    response = client.patch(f'/api/v1/courses/{course.id}/', content)
    assert response.status_code == status_code
