import sys
import datetime

class Print:
    """Class for print in console and save for print to files
    """
    lines_to_file = []
    @staticmethod
    def print_to_file(value="", end=None):
        """ to print in console and save value for printing to file
        :param value: value to print
        :type value: str
        :param end: end signal
        :type end: str/None
        :return:
        """
        Print.lines_to_file.append(value)
        if not (end is not None and end == ""):
            Print.lines_to_file.append("\n")
        print(value, end=end)

class FileReadError(Exception):
    """an error class for recording error from file read and show its line no.
    """
    def __init__(self, err_msg):
        Print.print_to_file("File Read Error")
        Print.print_to_file(err_msg)

class FormatError(Exception):
    """an error class for format error.
    """
    def __init__(self, err_msg):
        Print.print_to_file("Format Error")
        Print.print_to_file(err_msg)

class Verify:
    """ Class to verify any values
    """
    @staticmethod
    def str_is_empty(value):
        """check string is NA, instance and ""
        :param value: string value
        :type value: str
        :return: bool
        """
        return value and isinstance(value, str) and value == ""

    @staticmethod
    def float_positive(value):
        """check value is float
        :param value: string value
        :type value: str
        :return: bool
        """
        if not value:
            return False
        try:
            p = float(value)
            return p >= 0
        except ValueError:
            return False

    @staticmethod
    def float(value):
        """ verify input integer value and return True if it is integer, return False if it is not
        :param value:
        :type value: str
        :return: bool
        """
        try:
            float(value)
            return True
        except ValueError:
            return False

    @staticmethod
    def convert_str_to_float(value):
        """ convert string to float
        :param value:
        :type value: str
        :return: float/None
        """
        if Verify.float(value):
            return float(value)
        return None

    @staticmethod
    def value_in_list(value, lst):
        """ check value is in the list provided
        :param value: string value
        :type value: str
        :param lst: list
        :type lst: list
        :return:
        """
        return value in lst

class Read:
    """class with all static method about read file or user input
    """
    @staticmethod
    def file(file_name):
        """read file from file_name and return string list
        :param file_name:
        :type file_name: str
        :exception : Exception
        :return: list
        """
        file = None
        try:
            file = open(file_name, 'r')
            line_from_file = file.readline()
            lines = []
            while line_from_file:
                fields_from_line = line_from_file.split(',')
                lines.append(fields_from_line)
                line_from_file = file.readline()
        except:
            raise FileReadError("File ({}) is missing.".format(file_name))
        finally:
            if file:
                file.close()
        return lines

class Student:
    """Class of a student, which store
    ID(string), name(string), s_type (string)
    """
    def __init__(self, ID, name, s_type):
        if not Student.is_id(ID):
            raise Exception("invalid customer ID")
        if not Student.is_s_type(s_type):
            raise Exception("invalid s_type")
        self.__ID = ID.strip()
        self.__name = name.strip()
        self.__s_type = s_type.strip()
        self.__n_finish = 0
        self.__non_going = 0
        self.__total_time = 0.0
        self.__avg_time = 0.0
        self.__score = 0
        self.__w_score = 0.0

    @property
    def ID(self):
        return self.__ID

    @ID.setter
    def ID(self, ID):
        if Student.is_id(ID):
            self.__ID = ID.strip()
        else:
            raise Exception("error of Student ID")

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def s_type(self):
        return self.__s_type

    @s_type.setter
    def s_type(self, s_type):
        if Student.is_s_type(s_type):
            self.__s_type = s_type.strip()
        else:
            raise Exception("error of Student Type")

    @property
    def n_finish(self):
        return self.__n_finish

    @n_finish.setter
    def n_finish(self, value):
        self.__n_finish = value

    @property
    def non_going(self):
        return self.__non_going

    @non_going.setter
    def non_going(self, value):
        self.__non_going = value

    @property
    def total_time(self):
        return self.__total_time

    @total_time.setter
    def total_time(self, value):
        self.__total_time = value
        self.__avg_time = round(self.total_time / self.n_finish, 2)

    @property
    def avg_time(self):
        return self.__avg_time

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, value):
        self.__score = value

    @property
    def w_score(self):
        return self.__w_score

    @w_score.setter
    def w_score(self, value):
        self.__w_score = value

    @staticmethod
    def is_id(value):
        """validate ID "Sxxx" xxx == integer
        :param value: string value
        :type value: str
        :return: bool
        """
        if Verify.str_is_empty(value):
            return False
        if value[0].upper() == "S":
            try:
                int(value[1:])
                return True
            except ValueError:
                return False
        else:
            return False

    @staticmethod
    def is_s_type(value):
        """validate student type "U" or "P"
        :param value: string value
        :type value: str
        :return: bool
        """
        if Verify.str_is_empty(value):
            return False
        return Verify.value_in_list(value.strip().upper(), ["U", "P"])

class Challenge:
    """Class of a challenge, which consist of
    ID(string), c_type(string), name (string), weight(float)
    """
    def __init__(self, ID, c_type, name, weight):
        if not Challenge.is_id(ID):
            raise Exception("invalid Challenge ID")
        if not Challenge.is_c_type(c_type):
            raise Exception("invalid c_type")
        if not Challenge.is_weight(weight):
            raise Exception("invalid weight")
        if c_type == "S" and weight <= 1.0:
            raise Exception("weight cannot be less than 1.0 for special challenge")
        self.__ID = ID.strip()
        self.__c_type = c_type.strip()
        self.__name = name.strip()
        self.__weight = Verify.convert_str_to_float(weight.strip())
        self.__n_finish = 0
        self.__non_going = 0
        self.__total_time = 0.0
        self.__avg_time = 0.0

    @property
    def ID(self):
        return self.__ID

    @ID.setter
    def ID(self, ID):
        if Student.is_id(ID):
            self.__ID = ID.strip()
        else:
            raise Exception("error of Student ID")

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def c_type(self):
        return self.__c_type

    @c_type.setter
    def c_type(self, c_type):
        if Challenge.is_c_type(c_type):
            self.__c_type = c_type.strip()
        else:
            raise Exception("error of Challenge Type")

    @property
    def weight(self):
        return self.__weight

    @weight.setter
    def weight(self, weight):
        if not Verify.float(weight):
            raise Exception("weight error")
        if self.c_type == "S" and weight <= 1.0:
            raise Exception("weight cannot be less than 1.0 for special challenge")
        self.__weight = Verify.convert_str_to_float(weight.strip())

    @property
    def n_finish(self):
        return self.__n_finish

    @n_finish.setter
    def n_finish(self, value):
        self.__n_finish = value

    @property
    def non_going(self):
        return self.__non_going

    @non_going.setter
    def non_going(self, value):
        self.__non_going = value

    @property
    def total_time(self):
        return self.__total_time

    @total_time.setter
    def total_time(self, value):
        self.__total_time = value
        self.__avg_time = round(self.total_time / self.n_finish, 2)

    @property
    def avg_time(self):
        return self.__avg_time

    @staticmethod
    def is_id(value):
        """validate ID "Cxx" xx = integer
        :param value: id value
        :type value: str
        :return: bool
        """
        if value[0].upper() == "C":
            try:
                int(value[1:])
                return True
            except ValueError:
                return False
        else:
            return False

    @staticmethod
    def is_c_type(value):
        """validate challenge type
        :param value: string value
        :type value: str
        :return: bool
        """
        if Verify.str_is_empty(value):
            return False
        return Verify.value_in_list(value.strip().upper(), ["M", "S"])

    @staticmethod
    def is_weight(value):
        """validate weight is positive float
        :param value: string value
        :type value: str
        :return: bool
        """
        return Verify.float_positive(value)

class Competition:
    student_list = []
    challenge_list = []
    result = {}  # {student: {competition: minutes, "avg": float}}

    taking_challenge = ['444', "TBA", "tba", 444]
    no_join_challenge = ['-1', "NA", "x", -1]

    challenge_margin = [12, 18, 10, 10, 10, 17]
    challenge_header = ["Challenge", "Name", "Weight", "Nfinish", "Nongoing", "AverageTime"]

    std_margin = [14, 10, 8, 10, 10, 17, 10, 10]
    std_header = ["StudentID", "Name", "Type", "Nfinish", "Nongoing", "AverageTime", "Score", "Wscore"]

    def find_student(self, student_id):
        """find student by student ID
        :param student_id:
        :type student_id: str
        :return: Student/None
        """
        for std in self.student_list:
            if student_id == std.ID:
                return std
        return None

    def find_challenge(self, challenge_id):
        """find student by challenge ID
        :param challenge_id:
        :type challenge_id: str
        :return: Challenge/None
        """
        for challenge in self.challenge_list:
            if challenge_id == challenge.ID:
                return challenge
        return None

    def add_result(self, student, challenge, value):
        """ add value to result
        :param student:
        :type student: Student
        :param challenge:
        :type challenge: Challenge
        :param value:
        :type value: float
        :return: None
        """
        if not student in self.result.keys():
            self.result[student] = {challenge: value}
            if self.is_finished_challenge(student, challenge):
                challenge.n_finish += 1
                challenge.total_time += value
                student.n_finish += 1
                student.total_time += value
            elif self.is_taking_challenge(student, challenge):
                challenge.non_going += 1
                student.non_going += 1
        elif not challenge in self.result[student].keys():
            self.result[student][challenge] = value
            if self.is_finished_challenge(student, challenge):
                challenge.n_finish += 1
                challenge.total_time += value
                student.n_finish += 1
                student.total_time += value
            elif self.is_taking_challenge(student, challenge):
                challenge.non_going += 1
                student.non_going += 1
        else:
            raise Exception("Cannot add result as result already added")

    def is_taking_challenge(self, student, challenge):
        """ return boolean if student is taking the challenge, 444 means ongoing
        :param student: student object
        :type student: Student
        :param challenge: challenge object
        :type challenge: Challenge
        :return: bool
        """
        return self.result[student][challenge] in Competition.taking_challenge

    def is_not_taken_challenge(self, student, challenge):
        """ return boolean if student has participated the challenge, -1 means not participate
        :param student: student object
        :type student: Student
        :param challenge: challenge object
        :type challenge: Challenge
        :return: bool
        """
        return self.result[student][challenge] in Competition.no_join_challenge

    def is_finished_challenge(self, student, challenge):
        """ return boolean of checking if student finished the challenge
        :param student:
        :type student: Student
        :param challenge:
        :type challenge: Challenge
        :return: bool
        """
        return not(self.is_taking_challenge(student, challenge)
                   or self.is_not_taken_challenge(student, challenge))

    def read_students(self, file_name):
        """ To read and save student records from file_name
        :param file_name:
        :type file_name: str
        :return: None
        """
        lines = Read.file(file_name)
        for std_line in lines:
            std = Student(std_line[0], std_line[1], std_line[2])
            self.student_list.append(std)

    def read_challenges(self, file_name):
        """ To read and save challenge records from file_name
        :param file_name:
        :type file_name: str
        :return: None
        """
        lines = Read.file(file_name)
        for challenge_line in lines:
            challenge = Challenge(challenge_line[0], challenge_line[1], challenge_line[2], challenge_line[3])
            self.challenge_list.append(challenge)

    def read_results(self, file_name):
        """
        read the result from
        :param file_name: filename
        :type file_name: str
        :return:
        """
        result_lines = Read.file(file_name)
        if len(result_lines) == 0:
            raise FormatError("No results are available for the competition.")
        hdr_ln = result_lines[0]
        columns = len(hdr_ln)
        challenge_list = []
        for hdr_idx in range(1, len(hdr_ln)):
            challenge = self.find_challenge(hdr_ln[hdr_idx].strip())
            if not challenge:
                raise FormatError("Cannot find challenge({}) in result".format(challenge.ID))
            if challenge in challenge_list:
                raise FormatError("Challenge ID({}) duplicated in result".format(challenge.ID))
            challenge_list.append(challenge)

        for idx in range(1, len(result_lines)):
            line = result_lines[idx]
            if len(line) != columns:
                raise FormatError("Result formatting issue at line {}".format(idx+1))
            std = self.find_student(line[0].strip())
            for idx2, challenge in enumerate(challenge_list):
                value = line[idx2+1]
                Competition.verify_result(value.strip())
                value = Competition.convert_result(value.strip())
                value = float(value)
                self.add_result(std, challenge, value)

    @staticmethod
    def verify_result(value):
        """ to verify result value
        :param value:
        :type value: str
        :return:
        """
        if (value in Competition.taking_challenge
                or value in Competition.no_join_challenge):
            return True
        elif Verify.float_positive(value):
            return True
        else:
            raise FormatError("Result value({}) is not in format".format(value))

    @staticmethod
    def convert_result(value):
        """ to convert result from na, x, tba, TBA to -1 or 444
        :param value:
        :type value: str
        :return: float
        """
        if value in Competition.no_join_challenge:
            return -1
        if value in Competition.taking_challenge:
            return 444
        return value

    def display_results(self):
        """to display the result to console and file output
        :return:
        """
        Print.print_to_file("{}\n".format(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
        self.display_dashboard()
        Print.print_to_file()
        self.display_challenge_info()
        Print.print_to_file()
        self.display_std_info()
        Print.print_to_file()
        Print.print_to_file("#"*100)

    def calculate_score(self):
        """ to calculate score & weighted score for students
        :return: None
        """
        tmp = {}
        for clg in self.challenge_list:
            for std in self.student_list:
                minute = self.result[std][clg]
                if not self.is_finished_challenge(std, clg):
                    continue
                if clg not in tmp.keys():
                    tmp[clg] = {std: minute}
                else:
                    tmp[clg][std] = minute
        for clg in tmp.keys():
            tmp[clg] = sorted(tmp[clg].items(), key=lambda item: item[1])

        score_lst = [3,2,1]
        for clg in self.challenge_list:
            list = tmp[clg]
            for idx in range(0, min(len(list), 2)):
                list[idx][0].score += score_lst[idx]
                list[idx][0].w_score += round(score_lst[idx] * clg.weight, 1)
            if len(list) >= 3:
                list[-1][0].score -= 1
                list[-1][0].w_score -= round(1 * clg.weight, 1)

    def display_std_info(self):
        """ to display Student information
        :return: None
        """
        self.calculate_score()
        Print.print_to_file("STUDENT INFORMATION")
        Competition.print_separator_line(Competition.std_margin)
        for idx, header in enumerate(Competition.std_header):
            Competition.print_center(header, Competition.std_margin[idx], False)
        Print.print_to_file("|")
        Competition.print_separator_line(Competition.std_margin)
        self.find_highest_w_score_std()
        for std in self.student_list:
            Competition.print_center(std.ID, Competition.std_margin[0], False)
            qualified = self.qualify(std)
            std_name = std.name
            if not qualified:
                std_name = "!" + std_name
            Competition.print_center(std_name, Competition.std_margin[1], False)
            Competition.print_center(std.s_type, Competition.std_margin[2], False)
            Competition.print_center(str(std.n_finish), Competition.std_margin[3], False)
            Competition.print_center(str(std.non_going), Competition.std_margin[4], False)
            Competition.print_center(str(std.avg_time), Competition.std_margin[5], False)
            Competition.print_center(str(std.score), Competition.std_margin[6], False)
            Competition.print_center(str(std.w_score), Competition.std_margin[7], False)
            Print.print_to_file("|")
        self.print_separator_line(Competition.std_margin)
        std = self.find_fastest_avg_std()
        Print.print_to_file(
            "The student with the fastest average time is {} ({}) with an average time of {:.2f} minutes.".format(
            std.name, std.ID, std.avg_time))
        std = self.find_highest_score_std()
        Print.print_to_file(
            "The student with the highest score is {} ({}) with a score of {}.".format(
                std.name, std.ID, std.score))
        std = self.find_highest_w_score_std()
        Print.print_to_file(
            "The student with the highest weighted score is {} ({}) with a weighted score of {}.".format(
                std.name, std.ID, std.w_score))
        Print.print_to_file("Report competition_report.txt generated!")

    def display_challenge_info(self):
        """ to display challenge information
        :return: None
        """
        Print.print_to_file("CHALLENGE INFORMATION")
        Competition.print_separator_line(Competition.challenge_margin)
        for idx, header in enumerate(Competition.challenge_header):
            Competition.print_center(header, Competition.challenge_margin[idx], False)
        Print.print_to_file("|")
        Competition.print_separator_line(Competition.challenge_margin)
        self.challenge_list.sort(key=lambda x: x.avg_time)
        for challenge in self.challenge_list:
            Competition.print_center(challenge.ID, Competition.challenge_margin[0], False)
            Competition.print_center("{}({})".format(challenge.name, challenge.c_type),
                                     Competition.challenge_margin[1], False)
            Competition.print_center(str(challenge.weight), Competition.challenge_margin[2], False)
            Competition.print_center(str(challenge.n_finish), Competition.challenge_margin[3], False)
            Competition.print_center(str(challenge.non_going), Competition.challenge_margin[4], False)
            Competition.print_center(str(challenge.avg_time), Competition.challenge_margin[5], False)
            Print.print_to_file("|")
        Competition.print_separator_line(Competition.challenge_margin)
        most_diff_challenge = self.find_most_diff_challenge()
        Print.print_to_file("The most difficult challenge is {} ({}) with an average time of {:.2f} minutes".format(
            most_diff_challenge.name, most_diff_challenge.ID, most_diff_challenge.avg_time))
        Print.print_to_file("Report competition_report.txt generated!")

    def display_dashboard(self):
        """ to display competition dashboard
        :return: None
        """
        Print.print_to_file("COMPETITION DASHBOARD")
        self.print_separator_line_dashboard()
        Competition.print_center("Results", 12, False)
        self.challenge_list.sort(key=lambda x : x.ID)
        for challenge in self.challenge_list:
            Competition.print_center(challenge.ID, 7, False)
        Print.print_to_file("|")
        self.print_separator_line_dashboard()
        for std in self.result.keys():
            Competition.print_center(std.ID, 12, False)
            std_challenge_dict = self.result[std]
            for challenge in std_challenge_dict.keys():
                minute = std_challenge_dict[challenge]
                if self.is_not_taken_challenge(std, challenge):
                    minute = ""
                elif self.is_taking_challenge(std, challenge):
                    minute = "--"
                Competition.print_center(str(minute), 7, False)
            Print.print_to_file("|")
        self.print_separator_line_dashboard()
        Print.print_to_file("There are {} students and {} challenges.".format(len(self.student_list), len(self.challenge_list)))
        top_std = self.find_top_std()
        Print.print_to_file("The top student is {} with an average time of {:.2f} minutes".format(top_std.ID, top_std.avg_time))

    @staticmethod
    def print_separator_line(lst):
        """ to print separator line in format
        :param lst:
        :type lst: list
        :return: None
        """
        for margin in lst:
            Competition.print_center("-" * margin, margin, True)
        Print.print_to_file("+")

    def print_separator_line_dashboard(self):
        """ to print separator line for competition dashboard
        :return: None
        """
        Competition.print_center("-"*12, 12, True)
        for challenge in self.challenge_list:
            Competition.print_center("-"*7, 7, True)
        Print.print_to_file("+")

    @staticmethod
    def print_center(value, size, is_boarder):
        """ to print value in center
        :param value:
        :type value: str
        :param size:
        :type size: int
        :param is_boarder: if is boarder use "+", otherwise use "|"
        :type is_boarder: bool
        :return: None
        """
        separator = "|"
        if is_boarder:
            separator = "+"
        Print.print_to_file("{}{}".format(separator, value.center(size)), end="")

    def find_top_std(self):
        """sort and return the top std
        :return: Student
        """
        self.student_list.sort(key=lambda x : x.avg_time)
        return self.student_list[0]

    def find_most_diff_challenge(self):
        """sort and return the most difficult challenge
        :return: Challenge
        """
        self.challenge_list.sort(key=lambda x: x.avg_time, reverse=True)
        return self.challenge_list[0]

    def find_fastest_avg_std(self):
        """sort and return the fastest average student
        :return: Student
        """
        self.student_list.sort(key=lambda x: x.avg_time)
        return self.challenge_list[0]

    def find_highest_score_std(self):
        """sort and return the highest score student
        :return: Student
        """
        self.student_list.sort(key=lambda x: x.score, reverse=True)
        return self.student_list[0]

    def find_highest_w_score_std(self):
        """sort and return the highest weighted score student
        :return: Student
        """
        self.student_list.sort(key=lambda x: x.w_score, reverse=True)
        return self.student_list[0]

    def qualify(self, student):
        """ to calculate the student is qualified for competition (DI level "!")
        , the matrix for no of finish and no of ongoing challenge
        :param student:
        :type student: Student
        :return: bool
        """
        challenges = self.result[student]
        dict = {"mand":{"Nfinish":0, "NonGoing":0}, "spec": {"Nfinish":0, "NonGoing":0}}
        for challenge in challenges.keys():
            if challenge.c_type == "M":
                dict2 = dict["mand"]
            else:
                dict2 = dict["spec"]
            if self.is_finished_challenge(student, challenge):
                dict2["Nfinish"] += 1
            else:
                dict2["NonGoing"] += 1

        if dict["mand"]["NonGoing"] > 0:
            return False

        if student.s_type == "U":
            return dict["spec"]["Nfinish"] >= 1
        else:
            return dict["spec"]["Nfinish"] >= 2

def main(args):
    """ main program
    :param args:
    :type args: list
    :return: None
    """
    comp = Competition()

    challenges_file_name = "challenges.txt"
    if len(args) > 2 and args[2] and args[2].strip():
        challenges_file_name = args[2]
    comp.read_challenges(challenges_file_name)

    students_file_name = "students.txt"
    if len(args) > 3 and args[3] and args[3].strip():
        students_file_name = args[3]
    comp.read_students(students_file_name)

    comp.read_results(args[1])
    comp.display_results()

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        Print.print_to_file("[Usage:] python my_competition.py <result file>")
    else:
        try:
            with open('competition_report.txt', 'r+') as f:
                main(sys.argv)

                file_data = f.read()
                f.seek(0, 0)
                for ln in Print.lines_to_file:
                    f.write(ln)
                f.write('\n' + file_data)
        except FileReadError as err:
            pass
        except FormatError as err:
            pass