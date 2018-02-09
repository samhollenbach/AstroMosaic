import csv

darkFrames = 5
waitTime = 30
positions = ["10h 02m 07.674s +68d 41m 27.98s"]
objects = []
exposureTimes = [120]
imageNumber = 2
filters = ["R", "Ha"]

commands_output = []
dark_commands_output = []


def make_dark_commands():
    dark_commands_output.append(["SetFrameMode", "Dark", ""])
    for e in exposureTimes:
        for _ in range(0, darkFrames):
            dark_commands_output.append(["TakeImage", e, "\tdark frame"])


def add_command(command, param, comment=""):
    commands_output.append([command, param, comment])


def take_image_command(exposure, comment=""):
    add_command("TakeImage", exposure, comment)


def run_all_positions():
    frame_mode_light = False
    for p in positions:
        add_command("SlewToRaDec", p)
        add_command("WaitFor", 30)

        for f in filters:
            if not frame_mode_light:
                add_command("SetFrameMode", "Light")
                frame_mode_light = True
            add_command("SetFilter", f)

            for e in exposureTimes:
                for _ in range(0, imageNumber):
                    take_image_command(e)


def make_command_file(commands, filename="orch_commands.txt"):
    with open(filename, 'w') as w:
        writer = csv.writer(w, delimiter=",")
        for c in commands:
            writer.writerow(c)


# Makes normal script for all positions/filters/exposures
run_all_positions()
make_command_file(commands_output)

# Makes script for dark frames only depending on exposures
# make_dark_commands()
# make_command_file(dark_commands_output, "dark_frames.txt")
