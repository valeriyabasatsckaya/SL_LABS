import json

with open(r'D:\SL_LABS\Lab07\2.2\2.json', 'r', encoding='utf-8') as file:
    data = json.load(file)['employees']

for emp in data:
    for key, value in emp.items():
        print(f"{key} -> {value}")

def find_employees_by_language(data, lang):
    return [emp for emp in data if emp['language'] == lang]

def calculate_avg_salary_by_department(data):
    dept_salaries = {}
    for emp in data:
        dept = emp['department']
        salary = emp['salary']
        if dept not in dept_salaries:
            dept_salaries[dept] = []
        dept_salaries[dept].append(salary)
    return {dept: sum(sal) / len(sal) for dept, sal in dept_salaries.items()}

def find_employees_by_position_level(data, level):
    return [emp for emp in data if emp['position_level'] == level]

def save_filtered_to_json(filtered_data, filename='out.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(filtered_data, f, indent=2, ensure_ascii=False)

lang_employees = find_employees_by_language(data, 'English')
for emp in lang_employees:
    print(emp['first_name'])

avg_salaries = calculate_avg_salary_by_department(data)
for dept, avg in avg_salaries.items():
    print(f"{dept} -> {avg}")

senior_employees = find_employees_by_position_level(data, 'Senior')
for emp in senior_employees:
    print(emp['first_name'])

save_filtered_to_json(senior_employees)