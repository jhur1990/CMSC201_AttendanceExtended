"""
File: py2.py
Author: Joshua Hur
Date: 11/13/22
Lab Section: 14
Email: jhur1@umbc.edu
Description: This program import attendance data of students from external .txt files and store
their name, entry time, and entry date in a programmed dictionary.
It also presents different student attendance information from the dictionary by various criteria;
1. Display entire attendance data for a particular student
2. Check if a student attended a class on a specific date
3. List of students who attended a class on a specific date
4. List of students who entered the class on time on a specific date
5. List of students who participate for a certain number of days
6. The first student entered on a specific date
"""


def connect_to_data_file(filename):
    """
    This function imports an external attendance data .txt file and opens it to use in the program
    :param filename: Name of an attendance data .txt file to open
    :return: Data from the opened attendance data .txt file
    """

    # Will return connection to data file
    infile = ""

    try:
        infile = open(filename, "r")

    except FileNotFoundError:
        print("file was not found, try again")

    # Connection with the file
    return infile


def load_dictionary(loaded_data):
    """
    This function accesses, stores, and converts data from the opened .txt file in a dictionary
    for future use in this program
    :param loaded_data: Loaded data from the external attendance data .txt file
    :return: A dictionary that stores students' last names, first names, entry times, and entry dates.
             Students' names are keys, and entry time and date are values.
    """

    new_dict = {}

    LAST_NAME_INDEX = 0
    FIRST_NAME_INDEX = 1
    TIME_INDEX = 2
    DATE_INDEX = 3

    # Split student attendance data into four types; last name, first name, time, and date
    for student in loaded_data:
        data_split = student.split(", ")
        stu_last_name = data_split[LAST_NAME_INDEX]
        stu_first_name = data_split[FIRST_NAME_INDEX]
        stu_time = data_split[TIME_INDEX]
        stu_date = data_split[DATE_INDEX].strip('\n')

        stu_name = stu_last_name + ", " + stu_first_name
        stu_td = stu_time + ", " + stu_date

        # Store student's attendance information in the dictionary excludes duplicates of keys and values
        if stu_name not in new_dict:
            new_dict[stu_name] = []
            new_dict[stu_name].append(stu_td)
        else:
            if stu_td in new_dict[stu_name]:
                pass
            else:
                new_dict[stu_name].append(stu_td)

    return new_dict


def load_roster(file_name):
    """
    This function loads a roster .txt file that has a student roster for future comparison
    :param file_name: Name of a roster .txt file
    :return: A list of students in a roster
    """

    new_list = []

    # Open a roster .txt file
    opened_file = open(file_name)

    # Convert imported data into a list
    for student in opened_file:
        new_list.append(student.strip('\n'))

    opened_file.close()

    return new_list


def display_attendance_data_for_student(student, attend_data):
    """
    This function presents all the attendance data for a particular student when available
    :param student: Name of a student
    :param attend_data: Stored dictionary
    """

    # Check if asked student's name is in the dictionary as keys
    for stu_name, stu_info in attend_data.items():
        if student == stu_name:
            print(stu_name, stu_info)

    # If asked student's name is not in the dictionary as keys, print a warning
    if student not in attend_data:
        print("No student of this name in the attendance log")


def is_present(student, date, attend_data):
    """
    This function displays if a student came to class on that particular date
    :param student: Name of a student
    :param date: A particular date that students attended a class
    :param attend_data: Stored dictionary
    :return: If a student attended a class on that day, it returns true. On the contrary, it returns false
    """

    DATE_STRING_START = 10

    # Check if the student's name is in the dictionary as a key.
    # If so, access its values and check the asked date is a part of the values of the student
    for stu_name, stu_info in attend_data.items():
        if student == stu_name:
            for i in range(len(stu_info)):
                if date == stu_info[i][DATE_STRING_START:]:
                    return True

    return False


def list_all_students_checked_in(date, attend_data):
    """
    This function finds students who showed up to class on a given date and lists all of them
    :param date: A particular class date
    :param attend_data: Stored dictionary
    :return: A list of students who attended a class on a given date
    """

    new_list = []

    DATE_STRING_START = 10

    # Store a separate list of students if a given date is in their values
    for stu_name, stu_info in attend_data.items():
        for i in range(len(stu_info)):
            if stu_info[i][DATE_STRING_START:] == date:
                new_list.append(stu_name)

    return new_list


def list_all_students_checked_in_before(date, timestamp, attend_data):
    """
    This function compares a given time and stored data and
    lists all the students who entered earlier than a given time and date
    :param date: A particular date that students attended class
    :param timestamp: The input time for comparison
    :param attend_data: Stored dictionary
    :return: A list of students who came to class before the given time on the given date
    """

    new_list = []

    DATE_STRING_START = 10

    HOUR_STRING_END = 2
    MIN_STRING_START = 3
    MIN_STRING_END = 5
    SEC_STRING_START = 6
    SEC_STRING_END = 8

    CONV_HOUR_TO_MIN = 60
    CONV_MIN_TO_SEC = 60

    GIVEN_TIME_HOUR_INDEX = 0
    GIVEN_TIME_MIN_INDEX = 1
    GIVEN_TIME_SEC_INDEX = 2

    # Convert the given time to access its hours, minutes, and seconds
    comparison_time = timestamp.split(":")

    # Convert every entry time into seconds to compare the earlier time
    for stu_name, stu_info in attend_data.items():
        for i in range(len(stu_info)):
            if stu_info[i][DATE_STRING_START:] == date:
                if int(stu_info[i][:HOUR_STRING_END]) * CONV_HOUR_TO_MIN * CONV_MIN_TO_SEC + \
                        int(stu_info[i][MIN_STRING_START:MIN_STRING_END]) * CONV_MIN_TO_SEC + \
                        int(stu_info[i][SEC_STRING_START:SEC_STRING_END]) < \
                        int(comparison_time[GIVEN_TIME_HOUR_INDEX]) * CONV_HOUR_TO_MIN * CONV_MIN_TO_SEC + \
                        int(comparison_time[GIVEN_TIME_MIN_INDEX]) * CONV_MIN_TO_SEC + \
                        int(comparison_time[GIVEN_TIME_SEC_INDEX]):
                    new_list.append(stu_name)

    return new_list


def list_students_attendance_count(day, input_roster, attend_data):
    """
    This function checks the number of stored values for each student and differentiates their attendance frequency
    :param day: Number of class attended days of students
    :param input_roster: List of students who supposed to be in a class
    :param attend_data: Stored dictionary
    :return: A list of students who attend a class on the asked number of days
    """

    old_list = []
    new_list = []

    # Compare roster and attendance data if the student's name isn't available
    if int(day) == 0:
        for stu_name, stu_info in attend_data.items():
            old_list.append(stu_name)

        for roster_name in input_roster:
            if roster_name not in old_list:
                new_list.append(roster_name)
    else:
        for stu_name, stu_info in attend_data.items():
            if len(stu_info) == int(day):
                new_list.append(stu_name)

    return new_list


def get_first_student_to_enter(date, attend_data):
    """
    This function finds a student who swiped in first by comparing the entry time on a given date
    :param date: A particular date that students attended a class
    :param attend_data: Stored dictionary
    :return: A name of a student who entered a class for the earliest time on a particular day
    """
    earliest_stu = ""
    DATE_STRING_START = 10

    MAX_SEC_IN_DAY = 86400

    HOUR_STRING_END = 2
    MIN_STRING_START = 3
    MIN_STRING_END = 5
    SEC_STRING_START = 6
    SEC_STRING_END = 8

    CONV_HOUR_TO_MIN = 60
    CONV_MIN_TO_SEC = 60

    for stu_name, stu_info in attend_data.items():
        for i in range(len(stu_info)):

            # Convert every entry time into seconds
            if stu_info[i][DATE_STRING_START:] == date:
                hour_to_sec = int(stu_info[i][:HOUR_STRING_END]) * CONV_HOUR_TO_MIN * CONV_MIN_TO_SEC
                min_to_sec = int(stu_info[i][MIN_STRING_START:MIN_STRING_END]) * CONV_MIN_TO_SEC
                sec = int(stu_info[i][SEC_STRING_START:SEC_STRING_END])

                new_time = hour_to_sec + min_to_sec + sec

                # Compare and find a smaller number of times
                if new_time < MAX_SEC_IN_DAY:
                    MAX_SEC_IN_DAY = new_time
                    earliest_stu = stu_name

    return earliest_stu


def print_list(input_list):
    """
    This function prints the passed list from other functions
    :param input_list: The list of students and their attendance information sent by other functions
    """

    for element in input_list:
        print(element)


def print_count(input_list):
    """
    This function prints counts of qualified output
    :param input_list: The list of students and their attendance information sent by other functions
    """

    count = 0

    for element in input_list:
        count += 1

    print(f"There were {count} records for this query")


def print_dictionary(attend_data):
    """
    This function prints currently loaded dictionary that is created from the imported attendance data .txt file
    :param attend_data: Stored dictionary
    """

    print("** This is the entire Dictionary Data currently stored **")

    for stu_name, stu_info in attend_data.items():
        print(stu_name, stu_info)


if __name__ == '__main__':

    # Open attendance data file
    infile = connect_to_data_file("dataAllShow1stAnd2ndClass.txt")

    # Show if successfully loaded attendance data file or not
    if infile:
        print("connected to data file...")
    else:
        print("issue with data file... STOP")
        exit(1)

    # Access the dictionary and roster from the imported .txt file
    data = load_dictionary(infile)
    roster = load_roster("rosters.txt")

    # Print the currently loaded dictionary from the imported .txt file
    print_dictionary(data)

    # Display selected student's attendance data
    print("********* Looking up Student Attendance Data ***********")
    display_attendance_data_for_student("Morrison, Simon", data)
    display_attendance_data_for_student("Arsenault, Al", data)

    # Display if a student attended a class on the selected date
    print("********* Looking to see if Student was present on date ***********")
    print(is_present("Bower, Amy", "11/5/2022", data))
    print(is_present("Bower, Amy", "11/17/2022", data))

    # Display when students first signed in
    print("**** Students present on this date ****")
    result = list_all_students_checked_in("11/5/2022", data)
    print_list(result)
    print_count(result)

    # Display students who entered before the assigned time on the selected date
    print("**** Those present on date & before a time assigned ****")
    result = list_all_students_checked_in_before("11/5/2022", "08:55:04", data)
    print_list(result)
    print_count(result)

    # List the good students that showed up both days
    print("**** Those who attended BOTH classes ****")
    result = list_students_attendance_count("2", roster, data)
    print_list(result)
    print_count(result)

    # List the  students that showed up ONE of the days
    print("**** Those who attended ONE class ****")
    result = list_students_attendance_count("1", roster, data)
    print_list(result)
    print_count(result)

    # List the students that have not shown up
    print("**** Those who have NOT attended a SINGLE class ****")
    result = list_students_attendance_count("0", roster, data)
    print_list(result)
    print_count(result)

    # List the first student who entered on a particular day
    print("**** First student to enter on 11/2/2022 ****")
    print(get_first_student_to_enter("11/2/2022", data))

    print("**** First student to enter on 11/3/2022 ****")
    print(get_first_student_to_enter("11/3/2022", data))

    print("**** First student to enter on 11/4/2022 ****")
    print(get_first_student_to_enter("11/4/2022", data))

    print("**** First student to enter on 11/5/2022 ****")
    print(get_first_student_to_enter("11/5/2022", data))
