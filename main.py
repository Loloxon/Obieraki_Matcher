from _csv import writer

from Parser import Parser
from minizinc import Instance, Model, Solver


def run_minizinc(path_mzn, path_dzn):
    faculties = Model(path_mzn)
    gecode = Solver.lookup("cbc")
    instance = Instance(gecode, faculties)
    instance.add_file(path_dzn)
    result = instance.solve()
    with open(output_name, 'w', encoding="utf-8") as output_txt:
        output_txt.write(str(result))


def parse_output():
    with open(final_output_name, 'w', encoding="utf-8") as output_csv:
        output_csv.close()
    with open(output_name, encoding="utf-8") as output_txt:
        for line in output_txt:
            if len(line) < 2:
                break
            x = line.split()
            while len(x) < 3:
                x.append("-1")

            with open(final_output_name, 'a', encoding="utf-8") as output_csv:
                writer_object = writer(output_csv, lineterminator='\n')
                writer_object.writerow(
                    [p.students_names[int(x[0])],
                     p.faculties_names[int(x[1])],
                     p.faculties_names[int(x[2])]])
                output_csv.close()
            print(p.students_names[int(x[0])], ", ",
                  p.faculties_names[int(x[1])], ", ",
                  p.faculties_names[int(x[2])], sep="")


output_name = "data/output.txt"
final_output_name = "data/przypisanie obieraków.csv"
minizinc_model_path = "minizinc/faculties.mzn"
minizinc_data_path = "minizinc/data.dzn"

p = Parser("data/semestr-6-obieraki-05-12-2022 - Arkusz1.csv", "data/obieraki informacje.csv", "ABCDEFG",
           "data/wstęp do obieraka",
           minizinc_data_path)
run_minizinc(minizinc_model_path, minizinc_data_path)
parse_output()
