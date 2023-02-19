import csv


class Parser:
    def __init__(self, path_csv, path_csv_info, faculties_available, path_additional, path_dzn):
        self.faculties_total = None
        self.faculties_available = None
        self.preferences_matrix = []
        self.student_faculties_no = []
        self.preferences = []
        self.faculties_names = {-1: "*Obierak_zaliczony*"}
        self.faculties_sizes = []
        self.students_names = {}
        self.prepared_students = []

        self.read(path_csv, path_csv_info, path_additional)
        self.reformat_preferences(faculties_available)
        self.save_to_dzn(path_dzn)

    def read(self, path, path2, path3):
        with open(path, encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            first_line = True
            for row in csv_reader:
                if first_line:
                    first_line = False
                else:
                    if len(row[4]) > 0:
                        self.preferences.append([row[0], row[1], row[2], row[4]])
                    else:
                        self.preferences.append([row[0], row[1], row[2], row[3]])

        with open(path2, encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            first_line = True
            for row in csv_reader:
                if first_line:
                    first_line = False
                else:
                    self.faculties_names[row[0]] = row[1]
                    self.faculties_names[ord(row[1].lower()) - 97 + 1] = row[0]
                    self.faculties_sizes.append(int(row[2]))

        self.prepared_students = [0 for _ in range(len(self.preferences))]
        with open(path3, encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=' ')
            for row in csv_reader:
                for idx, record in enumerate(self.preferences):
                    if record[0] == row[0] and record[1] == row[1]:
                        self.prepared_students[idx] = 1
                # print(row)
        # print(self.prepared_students)

    def reformat_preferences(self, faculties_available):
        self.faculties_total = 0
        for idx, record in enumerate(self.preferences):
            self.students_names[idx + 1] = record[0] + " " + record[1]

            preference_int = []
            for letter in record[3].lower():
                faculty_id = ord(letter) - 97
                self.faculties_total = max(self.faculties_total, faculty_id + 1)
                preference_int.append(faculty_id)
            record[3] = preference_int

            self.student_faculties_no.append(int(record[2]))

            def check_if_valid(record_pref):
                if len(record_pref) > self.faculties_total:
                    record_pref = record_pref[:self.faculties_total]
                while len(record_pref) < self.faculties_total:
                    record_pref.append(-1)

                for i in range(self.faculties_total):
                    contains = False
                    for idx, value in enumerate(record_pref):
                        if value == i:
                            if not contains:
                                contains = True
                            else:
                                record_pref[idx] = -1
                for i in range(self.faculties_total):
                    contains = False
                    for idx, value in enumerate(record_pref):
                        if value == i:
                            if not contains:
                                contains = True
                    if not contains:
                        for idx, value in enumerate(record_pref):
                            if value == -1:
                                record_pref[idx] = i
                                break
                return record_pref

            record[3] = check_if_valid(record[3])

            preference_row = [0 for _ in range(self.faculties_total)]
            for idx, i in enumerate(record[3]):
                preference_row[i] = self.faculties_total - idx
            self.preferences_matrix.append(preference_row)

        self.faculties_available = [0 for _ in range(self.faculties_total)]
        for faculty in faculties_available.lower():
            self.faculties_available[ord(faculty) - 97] = 1

    def save_to_dzn(self, path):
        variables = {"n_students": len(self.preferences),
                     "n_faculties_total": self.faculties_total,
                     "faculties_available": self.faculties_available,
                     "faculties_sizes": self.faculties_sizes,
                     "student_faculties_no": self.student_faculties_no,
                     "student_prefers": self.preferences_matrix,
                     "prepared_students": self.prepared_students}
        with open(path, 'w') as dzn_file:
            for variable, value in variables.items():
                dzn_file.write(variable)
                if variable == "student_prefers":
                    self.save_matrix_to_dzn(dzn_file, value, "Student", "Faculty")
                else:
                    dzn_file.write(" = " + str(value) + ";\n")

    def save_matrix_to_dzn(self, file, array, rows, columns):
        file.write(" = array2d(" + rows + ", " + columns + ", [")
        content = ""
        for row in array:
            for value in row:
                if value == 0:
                    print(row, value)
                content += str(value) + ", "
            content += "\n"

        file.write(content[:-3] + "]);\n")
