import random
from datacenter.models import Schoolkid, Lesson, Mark, Chastisement, Commendation


def get_schoolkid(student_name):
    try:
        return Schoolkid.objects.get(full_name__contains=student_name)
    except Schoolkid.MultipleObjectsReturned:
        print(f"Найдено несколько учеников с именем '{student_name}'. Уточните запрос.")
    except Schoolkid.DoesNotExist:
        print(f"Ученик с именем '{student_name}' не найден.")
    return None


def fix_marks(student_name):
    schoolkid = get_schoolkid(student_name)
    if not schoolkid:
        return

    Mark.objects.filter(schoolkid=schoolkid, points__lte=3).update(points=4)


def remove_chastisements(student_name):
    schoolkid = get_schoolkid(student_name)
    if not schoolkid:
        return

    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    chastisements.delete()


def create_commendation(student_name, subject_title):
    commendation_texts = [
        "Молодец!",
        "Отличная работа!",
        "Так держать!",
        "Прекрасный результат!",
        "Горжусь тобой!",
        "Великолепно!",
        "Очень хороший ответ!",
        "Талантливо!",
        "Потрясающе!",
        "Ты на верном пути!",
    ]
    schoolkid = get_schoolkid(student_name)
    if not schoolkid:
        return

    lesson = (
        Lesson.objects.filter(
            year_of_study=schoolkid.year_of_study,
            group_letter=schoolkid.group_letter,
            subject__title=subject_title,
        )
        .order_by("-date")
        .first()
    )

    if not lesson:
        print(f"Не найден урок по предмету '{subject_title}' для ученика {student_name}.")
        return

    Commendation.objects.create(
        text=random.choice(commendation_texts),
        schoolkid=schoolkid,
        subject=lesson.subject,
        teacher=lesson.teacher,
        created=lesson.date,
    )
