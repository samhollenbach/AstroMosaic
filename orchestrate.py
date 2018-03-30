import csv

darkFrames = 5
waitTime = 30
positions = []
objects = []
exposureTimes = [60, 120]
filterTimes = {"R": [60], "Ha": [120], "I": [60]}
imageNumber = 1
filters = ["Ha", "I", "R"]

commands_output = []
dark_commands_output = []


image_counter = 0
time_counter = 0


def read_pointings(regfile):
    with open(regfile, "r") as w:
        reader = csv.reader(w, delimiter=" ")
        for r in reader:
            ra = r[0]
            dec = r[1]
            ra_split = ra.split(":")
            dec_split = dec.split(":")
            coord = "{}h {}m {}s {}d {}m {}s".format(ra_split[0],ra_split[1],ra_split[2],dec_split[0],dec_split[1],dec_split[2])
            positions.append(coord)

def make_dark_commands():
    dark_commands_output.append(["SetFrameMode", "Dark", ""])
    dark_frame_num = 0
    dark_time = 0
    for e in exposureTimes:
        dark_frame_num += darkFrames
        dark_time += e * darkFrames
        for _ in range(0, darkFrames):
            dark_commands_output.append(["TakeImage", e, "\tdark frame"])
    print("Dark frames script will take {} dark frames, totalling {} seconds of exposure time".format(dark_frame_num, dark_time))


def add_command(command, param, comment=""):
    commands_output.append([command, param, comment])


def take_image_command(exposure, comment=""):
    global image_counter
    global time_counter
    image_counter += 1
    time_counter += exposure
    add_command("TakeImage", exposure, comment)


def run_all_positions():
    global time_counter
    frame_mode_light = False
    for p in positions:
        add_command("SlewToRaDec", p)
        add_command("WaitFor", 1)
        time_counter += 1

        for f in filters:
            if not frame_mode_light:
                add_command("SetFrameMode", "Light")
                frame_mode_light = True
            add_command("SetFilter", f)
            exp_times = filterTimes[f]
            for e in exp_times:
                for _ in range(0, imageNumber):
                    take_image_command(e)


def make_command_file(commands, filename="orch_commands.txt"):
    with open(filename, 'w') as w:
        writer = csv.writer(w, delimiter=",")
        for c in commands:
            writer.writerow(c)


# Makes normal script for all positions/filters/exposures

read_pointings("pointings_trimmed.reg")
run_all_positions()
make_command_file(commands_output)
print("Script contains {} imaging commands, totalling {} ({} minutes) seconds of exposure time\n".format(image_counter, time_counter, time_counter/60))


# Makes script for dark frames only depending on exposures
make_dark_commands()
make_command_file(dark_commands_output, "dark_frames.txt")
