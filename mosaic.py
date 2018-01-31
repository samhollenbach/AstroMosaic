import csv

# EVERYTHING IN DEGREES

# Convert Right Ascension to degrees
def RAtoDeg(hr, min, sec):
    return 15 * (hr + (min / 60) + (sec / 3600))

# Convert arcmin/arcsec to degrees
def ArcMintoDeg(min, sec):
    return min/60 + sec/3600

# Convert Declination to degrees
def DECtoDeg(deg, min, sec):
    return deg + ((min / 60) + (sec / 3600))

# Takes in list of position tuples [(x1, y1), (x2, y2), ...]
def centerPos(objList):
    x = 0
    y = 0
    s = len(objList)
    print("Objects at: ")
    for l in objList:
        print("({}, {}) ".format(round(l[0],2), round(l[1],2)))
        x += l[0]
        y += l[1]
    x /= s
    y /= s
    print("Found the center of {} objects at ({}, {}) degrees\n".format(s, round(x,2), round(y,2)))
    return (x/s, y/s)

# Degree positions of objects to look at
heart_pos = (RAtoDeg(2, 32.8, 0), DECtoDeg(61, 27, 0))
soul_pos = (RAtoDeg(2, 51.4, 0), DECtoDeg(60, 25, 0))

# Center position of
center = centerPos([heart_pos, soul_pos])

# Size of image being taken
image_width = ArcMintoDeg(29, 0)
image_height = ArcMintoDeg(19, 0)

# Amount of area on the sky to cover
cover_width = 5.5
cover_height = 3.9

# Degrees of overlap on edges of each picture
edge_overlap = ArcMintoDeg(0, 1)

# Start and end X/Y positions for camera center position
boundariesX = (center[0] - (cover_width / 2) - edge_overlap + (image_width / 2),
               center[0] + (cover_width / 2) + edge_overlap - (image_width / 2))
boundariesY = (center[1] - cover_height / 2 - edge_overlap + image_height / 2,
               center[1] + cover_height / 2 + edge_overlap - image_height / 2)
print("Finding camera positions...\n")
final_positions = []
currentX = boundariesX[0]
while currentX < boundariesX[1]:
    currentY = boundariesY[0]
    x_row = []
    while currentY < boundariesY[1]:
        currentPosition = (round(currentX, 2), round(currentY,2))
        x_row.append(currentPosition)

        currentY += image_width/2 - edge_overlap
    final_positions.append(x_row)
    currentX += image_width/2 - edge_overlap

print("Calculated {} positions\n".format(len(final_positions)*len(final_positions[0])))

# Name of .csv file to store position data
outfile = "pointing_positions.csv"
with open(outfile, 'w') as w:
    wr = csv.writer(w, delimiter="\t")
    for row in final_positions:
        wr.writerow(row)
    print("Writing results to {}\n".format(outfile))