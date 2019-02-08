def analyze_students(data: typing.Dict[str, typing.Dict]) -> typing.Set:
    return {(student_name, subject, functools.reduce(lambda acc, x: acc * x, marks, 1)) for student_name, subjects in data.items() for subject, marks in subjects.items() if subject != '1C'}


def validate_data(data: typing.Dict[str, typing.Dict]) -> bool:
    for student, subjects in data.items():
        if not student.isalpha():
            raise ValueError
        for subject, marks in subjects.items():
            if not isinstance(subject, str):
                raise TypeError
            if not subject.isalpha():
                raise ValueError
            if any(
                    map(
                        lambda x: not isinstance(x, int) or
                        isinstance(x, bool),
                        marks
                    )
            ):
                raise TypeError
            if not all(1 <= i <= 10 for i in marks):
                raise ValueError
    return True
