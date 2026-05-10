from config import grades, levels, subjects


def calculate_subject_credits(subject, grade):
    base = grades.get(grade, 0)
    multiplier = subjects.get(subject, 1.0)
    return int(base * multiplier)


def calculate_achievement_credits(level):
    return levels.get(level, 0)


def total_student_credits(subject_data, achievement_data):
    total = 0
    for s, g in subject_data:
        total += calculate_subject_credits(s, g)
    for row in achievement_data:
        level = row[0] if isinstance(row, (list, tuple)) else row
        total += calculate_achievement_credits(level)
    return total