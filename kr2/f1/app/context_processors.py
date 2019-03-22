from app.models import Mark


def marks_processors(request):
    marks = Mark.objects.count()
    return {'MARKS_AMOUNT': marks}
