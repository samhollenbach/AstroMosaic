import csv
import math
import re
from os import listdir
from os.path import isfile, join

def compare_files(ref_coo, match_coo):
    SHIFT_THRESHOLD = 100
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

            max = []
            for h in hits:
                if len(max) < len(h):
                    max = h
            sum_x = 0
            sum_y = 0
            for entry in max:
                sum_x += entry[0]
                sum_y += entry[1]
            avg_x = round(sum_x / len(max), 3)
            avg_y = round(sum_y / len(max), 3)

            return ref_coo, match_coo, avg_x, avg_y


def find_matching_pointings(centers_path, pics_path, out_path, ref_prefix, shift_all=False):
    ARCMIN_THRESH = 1.5
    files = [f for f in listdir(centers_path) if isfile(join(centers_path, f))][1:]
    files = [f for f in files if ".fits.coo" in f]

    ref_files = []
    match_files = []
    final_matches = []
    for f in files:
        if f.startswith(ref_prefix):
            ref_files.append(f)
        else:
            match_files.append(f)

    if len(ref_files) < 1:
        print("No reference files found, check ref_prefix parameter")
        return
    if len(match_files) < 1:
        print("No match files found")
    if shift_all and len(ref_files) > 1:
        print("Cannot shift all images in folder to more than one reference image "
              "(Check shift_all and ref_prefix parameters)")
        return

    counter = 0

    if shift_all:
        ref = ref_files[0]
        for match in match_files:
            _, _, x, y = compare_files("{}/{}".format(centers_path, ref), "{}/{}".format(centers_path, match))
            final_matches.append((ref, match, x, y))
        counter = len(match_files)
    else:
        for ref in ref_files:
            ra, dec = get_ra_dec(ref, True, False)
            ra = ra.split(' ')
            dec = dec.split(' ')
            for match in match_files:
                ra_match, dec_match = get_ra_dec(match, True, False)
                ra_match = ra_match.split(' ')
                dec_match = dec_match.split(' ')
                ra_dif = abs(int(ra[1]) - int(ra_match[1]) + (int(ra[2]) - int(ra_match[2])) / 60.)
                dec_dif = abs(int(dec[1]) - int(dec_match[1]) + (int(dec[2]) - int(dec_match[2])) / 60.)
                if ra_dif <= ARCMIN_THRESH and dec_dif <= ARCMIN_THRESH:
                    _, _, x, y = compare_files("{}/{}".format(centers_path, ref), "{}/{}".format(centers_path, match))
                    final_matches.append((ref, match, x, y))
                    counter += 1
    print("Found {} matches".format(counter))
    write_shifts(out_path, final_matches)


def write_shifts(out_path, shifts):
    print("Writing shifts.cl file to current directory...")
    with open("shifts.cl", 'w') as w:
        for m in shifts:
            cmd = "imshift {}/{} {}/{} {} {}\n".format(pics_path, m[1][:-6], out_path, m[1][:-6], m[2], m[3])
            w.write(cmd)
    print("Run \'cl < shifts.cl\' in IRAF to apply shifts")

def get_ra_dec(file_name, with_s, with_labels):
    if with_s:
        ra_re = re.search('.{2}h.{2}m.{4}s', file_name)
        ra = re.sub('\..s', 's', ra_re.group(0))
        dec = re.search('.{2}d.{2}m.{2}s', file_name).group(0)
    else:
        ra_re = re.search('.{2}h.{2}m', file_name)
        ra = re.sub('\..s', 's', ra_re.group(0))
        dec = re.search('.{2}d.{2}m', file_name).group(0)

    if not with_labels:
        ra = ra.replace("h", " ").replace("m", " ").replace("s", "")
        dec = dec.replace("d", " ").replace("m", " ").replace("s", "")
    return ra, dec


ref_prefix = "R"
main_path = "/Users/research/Desktop/PROJECT/IMAGES"
centers_path = "{}/imshift/centers".format(main_path)
pics_path = "{}/final_science".format(main_path)
out_path = "{}/all_coords".format(main_path)
shift_all = False

find_matching_pointings(centers_path, pics_path, out_path, ref_prefix, shift_all)