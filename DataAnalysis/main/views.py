from django.shortcuts import render,redirect
from django.http import HttpRequest,HttpResponse
import pandas as pd
from django.contrib import messages

def main_page(request:HttpRequest):
    if request.method == "POST":
        try:
            file = request.FILES.get("file_uploaded")
            if not file:
                messages.error(request, "⚠️ No file uploaded.")
                return redirect('main:main_page')

            df = pd.read_excel(file)

            data = [row.to_dict() for _, row in df.iterrows()]
            
            age_total = 0
            salary_total = 0
            points_total = 0

            highest_age = 0
            highest_points = 0
            highest_salary = 0

            for num, i in enumerate(data):
                age = i["Age"]
                points = i["Points"]
                salary = i["Salary"]

                age_total += age
                salary_total += salary
                points_total += points

                if age > highest_age:
                    highest_age = age
                if points > highest_points:
                    highest_points = points
                if salary > highest_salary:
                    highest_salary = salary

            count = len(data)
            if count > 0:
                age_average = age_total / count
                points_average = points_total / count
                salary_average = salary_total / count
            else:
                age_average = points_average = salary_average = 0

            print("Average Age:", round(age_average, 2))
            print("Average Points:", round(points_average, 2))
            print("Average Salary:", round(salary_average, 2))
            print("Highest Age:", round(highest_age, 2))
            print("Highest Points:", round(highest_points, 2))
            print("Highest Salary:", round(highest_salary, 2))

            needed_data = {
                "aage":round(age_average, 2),
                "apoints":round(points_average, 2),
                "asalary":round(salary_average, 2),
                "hage":round(highest_age, 2),
                "hpoints":round(highest_points, 2),
                "hsalary":round(highest_salary, 2)
            }

            print(age_average/(num+1))
            return render(request, 'main.html', {"data":data,"ne":needed_data})
            

        except Exception as e:
            print("Error reading Excel:", e)
            messages.error(request, "⚠️ Failed to read Excel file. Make sure it’s a valid Excel format.")


        return redirect('main:main_page')


    return render(request, 'main.html')
