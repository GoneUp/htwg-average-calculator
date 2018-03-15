import argparse
import locale

from bs4 import BeautifulSoup
import sys
import json

cmd_args = None


# parse html page
# get course
# load course exemptions for undergradute grades
# calcucale
# table output?


class GradeRow():
    def __init__(self, entry):
        #init object from html table row
        fields = entry.find_all('td')
        assert (len(fields) == 9)
        #print(entry)

        #set to german locale for float parsing
        locale.setlocale(locale.LC_ALL, '')
        self.STG = fields[0].get_text().strip()
        self.number = int(fields[1].get_text().strip())
        self.text = fields[2].get_text().strip()
        self.semester = fields[3].get_text().strip()
        self.etcs = locale.atof(fields[4].get_text().strip())

        grade = fields[5].get_text().strip()
        if grade != "":
            self.grade = locale.atof(grade)
        else:
            self.grade = None

    def __str__(self):
        return "Subject {} - CP {} - Grade {}".format(self.text, self.etcs, self.grade)

''' 
:returns list of courses taken
'''
def parse_html(path):
    results = list()

    f = open(path, "rb")
    soup = BeautifulSoup(f, "lxml")

    grade_table = soup.find_all('table')[1]

    entrys = grade_table.find_all('tr')[2:-1] #drop header and last row

    for entry in entrys:
        grade_obj = GradeRow(entry)
        results.append(grade_obj)

    f.close()
    return results

def filter_grades(grades):
    new_grades = list()

    for grade in grades:
        #Observations:
        #Everything under semester 3 is lower than num 21000
        #Lets filter that


        if grade.number < 21000 or grade.etcs == 0 or grade.grade == None or grade.number == 22262:
            if cmd_args.debug:
                print("Filtered course: {}".format(grade))
            continue

        new_grades.append(grade)

    return new_grades

def calc_average(grades):
    #get weights relative to max etcs sum
    #calc avg based on weights

    sum_etcs = 0
    sum_grades = 0
    for row in grades:
        sum_etcs += row.etcs
        sum_grades += row.etcs * row.grade

    average = 0
    if sum_etcs > 0:
        average = sum_grades / sum_etcs

    return average

def main():
    global cmd_args

    print("HTWG QIS Average calculator, created by Henry Strobel (GoneUp)")

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', action='store_true', default=False, help='verbose logging',
                        dest='debug')
    parser.add_argument('--course', default="ain",
                        help='Choose the ruleset based on which the grades are filtered. Available: ain')
    parser.add_argument('file', metavar='HTML_FILE',
                        help='Location of your downloaded html file')

    cmd_args = parser.parse_args()

    parsed_courses = parse_html(cmd_args.file)
    filterd_courses = filter_grades(parsed_courses)

    print("\nCourses to include into the average:")
    for i in filterd_courses: print(str(i))

    avg = calc_average(filterd_courses)
    print("\n\nCalculated Average: {:.2f}".format(avg))

if __name__ == '__main__':
    print(sys.argv)
    main()
