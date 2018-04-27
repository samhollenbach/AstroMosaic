import csv
import math
import re
from os import listdir
from os.path import isfile, join

def compare_files(ref_coo, match_coo):
    SHIFT_THRESHOLD = 20
    with open(ref_coo, 'r') as r_coo:
        with open(match_coo,'r') as m_coo:
            ref_reader = csv.reader(r_coo, delimiter=" ")
            ref_list = []
            for r in ref_reader:
                r = filter(None, r)
                if r[0].startswith("#"):
                    continue
                ref_list.append(r)


            match_reader = csv.reader(m_coo, delimiter=" ")
            match_list = []
            for m in match_reader:
                m = filter(None, m)
                if m[0].startswith("#"):
                    continue
                match_list.append(m)


            dif_list = []
            for r in ref_list:
                for m in match_list:
                    dif_x = round(float(r[0])-float(m[0]), 3)
                    dif_y = round(float(r[1])-float(m[1]), 3)
                    if abs(dif_x) > SHIFT_THRESHOLD or abs(dif_y) > SHIFT_THRESHOLD:
                        continue
                    dif = (dif_x, dif_y)
                    dif_list.append(dif)
            print(dif_list)
            hits = []
            HIT_THRESH = 1.0
            for d in dif_list:
                d_hits = [d]
                for d2 in dif_list:
                    if d2 is d:
                        continue

                    dx = d2[0]-d[0]
                    dy = d2[1]-d[1]

                    d_thresh = math.sqrt(dx**2 + dy**2)
                    if d_thresh < HIT_THRESH:
                        d_hits.append(d2)
                hits.append(d_hits)

            print(hits)
            max = []
            for h in hits:
                if len(max) < len(h):
                    max = h
            print(max)
            sum_x = 0
            sum_y = 0
            for entry in max:
                sum_x += entry[0]
                sum_y += entry[1]
            avg_x = round(sum_x / len(max), 3)
            avg_y = round(sum_y / len(max), 3)

            make_shift_cmd(ref_coo, match_coo, (avg_x, avg_y))
            return ref_coo, match_coo, (avg_x, avg_y)




def make_shift_cmd(ref, match, shift):
    print(ref, match, shift)
    return

def find_matching_pointings(directory):
    #onlyfiles = [f for f in listdir(directory) if isfile(join(directory, f))][1:]
    #print(onlyfiles)
    files = ["R_Hollenbach.00000595.02h28m53.2s_62d03m58sN.fits.coo.1", "Ha_Hollenbach.00000594.02h28m53.4s_62d03m58sN.fits.coo.1"]
    ref = files[0]

    ra = re.search('.{2}h.{2}m.{4}s',ref)
    dec = re.search('.{2}d.{2}m.{2}s',ref)
    ra_fixed = re.sub('\..{1}s', 's', ra.group(0))
    print(ra.group(0), ra_fixed)
    print(dec.group(0))
    return



ref_prefix = "R"
main_path = "/Users/research/Desktop/PROJECT/IMAGES"
centers_path = "{}/imshift/centers".format(main_path)
#compare_files("{}/R_Hollenbach.00000595.02h28m53.2s_62d03m58sN.fits.coo.1".format(centers_path), "{}/Ha_Hollenbach.00000594.02h28m53.4s_62d03m58sN.fits.coo.1".format(centers_path))

find_matching_pointings(centers_path)