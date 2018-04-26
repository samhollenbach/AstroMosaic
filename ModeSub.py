import csv

main_path = "/Users/research/Desktop/PROJECT/IMAGES"
def make_mode_sub(prefix, pics_path):
    with open("{}/{}_stats.txt".format(main_path,prefix), 'r') as r:
        with open("{}/{}_mode_commands.cl".format(main_path, prefix), 'w') as w:
            reader = csv.reader(r, delimiter=' ')
            i = 2
            for line in reader:
                line = filter(None, line)
                if line[0] == "#":
                    i = line.index("MODE") - 1
                    continue
                if len(line) < i+1 or line[0] == "Error":
                    continue
                w.write("imarith {}/{} - {} {}/{}\n".format(pics_path, line[0], line[i], pics_path, line[0]))



pics_path = "{}/final_science".format(main_path)

make_mode_sub("Ha", pics_path)
make_mode_sub("I", pics_path)
make_mode_sub("R", pics_path)