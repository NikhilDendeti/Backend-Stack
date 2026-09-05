students = [
    {"name": "Nikhil",   "scores": {"Math": 88, "Science": 92, "English": 79}},
    {"name": "Venu",     "scores": {"Math": 72, "Science": 65, "English": 81}},
    {"name": "Sravya", "scores": {"Math": 95, "Science": 89, "English": 91}},
    {"name": "Kiran",   "scores": {"Math": 60, "Science": 70, "English": 68}},
    {"name": "Bhaiii",    "scores": {"Math": 85, "Science": 85, "English": 85}},
]

# for i in students:
#     print(f"Hii {i['name']} how are you")

def average(numbers):
    if(numbers):
         return sum(numbers)/len(numbers)
    else:
        return 0;

def student_average(student_list):
    for i in student_list:
        i['avg'] = round(average(i['scores'].values()), 2)
    return student_list

def top_scorers(student_list):
    student_average(student_list)
    sorted_students = sorted(student_list, key=lambda x: x.get('avg', 0), reverse=True)
    for student in sorted_students:
        print(f"Name: {student['name']}, Avg Score: {student['avg']}")
    return sorted_students[:3]


def sub_stats(student_list):
    subjs={subject for student in students for subject in student['scores']}
    stats={}
    for subs in subjs:
        scores=[
            student['scores'][subs]
            for student in students if subs in student['scores']
        ]
        stats[subs] = {
            'average': round(average(scores), 2),
            'min': min(scores),
            'max': max(scores)
        }
    return stats

print(sub_stats(students))
    





