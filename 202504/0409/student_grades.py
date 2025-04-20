#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
这个脚本生成一个包含学生姓名和成绩的字典，并打印所有学生的成绩。
"""

# 创建一个包含学生姓名和成绩的字典
student_grades = {
    "张三": 85,
    "李四": 92,
    "王五": 78,
    "赵六": 95,
    "钱七": 88,
    "孙八": 76,
    "周九": 90,
    "吴十": 82
}

# 方法1：使用for循环遍历字典并打印每个学生的成绩
print("方法1 - 使用for循环遍历字典:")
for student, grade in student_grades.items():
    print(f"{student}的成绩是: {grade}")

# 方法2：使用字典的keys()方法遍历学生姓名，然后获取对应的成绩
print("\n方法2 - 使用keys()方法遍历:")
for student in student_grades.keys():
    print(f"{student}的成绩是: {student_grades[student]}")

# 方法3：使用字典的values()方法获取所有成绩
print("\n方法3 - 使用values()方法获取所有成绩:")
grades = student_grades.values()
print(f"所有学生的成绩: {list(grades)}")

# 方法4：计算班级平均分
average_grade = sum(student_grades.values()) / len(student_grades)
print(f"\n班级平均分: {average_grade:.2f}")

# 方法5：找出最高分和最低分的学生
max_grade = max(student_grades.values())
min_grade = min(student_grades.values())

max_students = [student for student, grade in student_grades.items() if grade == max_grade]
min_students = [student for student, grade in student_grades.items() if grade == min_grade]

print(f"最高分: {max_grade}, 学生: {', '.join(max_students)}")
print(f"最低分: {min_grade}, 学生: {', '.join(min_students)}")

# 方法6：按成绩从高到低排序并打印
print("\n方法6 - 按成绩从高到低排序:")
sorted_students = sorted(student_grades.items(), key=lambda x: x[1], reverse=True)
for student, grade in sorted_students:
    print(f"{student}: {grade}")

# 方法7：统计成绩分布
print("\n方法7 - 成绩分布统计:")
grade_ranges = {
    "优秀(90-100)": 0,
    "良好(80-89)": 0,
    "中等(70-79)": 0,
    "及格(60-69)": 0,
    "不及格(0-59)": 0
}

for grade in student_grades.values():
    if grade >= 90:
        grade_ranges["优秀(90-100)"] += 1
    elif grade >= 80:
        grade_ranges["良好(80-89)"] += 1
    elif grade >= 70:
        grade_ranges["中等(70-79)"] += 1
    elif grade >= 60:
        grade_ranges["及格(60-69)"] += 1
    else:
        grade_ranges["不及格(0-59)"] += 1

for range_name, count in grade_ranges.items():
    print(f"{range_name}: {count}人")

print("\n所有学生的成绩已打印完成！") 