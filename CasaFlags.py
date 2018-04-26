import csv


def make_command_file(commands, filename="CasaFlagsOutput_LL.txt"):
    with open(filename, 'w') as w:
        w.write("\n".join(commands))

vis = 'TDEM0025.trim.ms'
all_commands = []
with open('/Users/research/Desktop/LEDA44055/FlagPositions_LL.txt','r') as w:
    reader = csv.reader(w, delimiter=" ")
    for r in reader:
        if r[0].startswith("//"):
            continue
        ant1 = r[0]
        ant2 = r[1]
        spw = r[2]
        tr = ""
        if r[3] != "0":
            tr = r[3]
        command = "flagdata(vis=\'{}\',antenna=\'{}&{}\',spw=\'0:{}\',timerange=\'{}\',correlation=\'LL\',field=\'\',flagbackup=F)".format(vis,ant1,ant2,spw,tr)
        all_commands.append(command)

    make_command_file(all_commands)