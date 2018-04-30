from os import listdir
from os.path import isfile, join
import re


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


def find_matching_pointings(main_path, pics_path, ref_prefix):
    ARCMIN_THRESH = 2
    files = [f for f in listdir(pics_path) if isfile(join(pics_path, f))][1:]
    ref_files = []
    match_files = []
    final_matches = []
    for f in files:
        if f.startswith(ref_prefix):
            ref_files.append(f)
        else:
            match_files.append(f)
    counter = 0
    for ref in ref_files:

        ra, dec = get_ra_dec(ref, True, False)
        ra = ra.split(' ')
        dec = dec.split(' ')
        for match in match_files:
            ra_match, dec_match = get_ra_dec(match, True, False)
            ra_match = ra_match.split(' ')
            dec_match = dec_match.split(' ')
            ra_dif = abs(int(ra[1]) - int(ra_match[1]) + (int(ra[2])-int(ra_match[2]))/60.)
            dec_dif = abs(int(dec[1]) - int(dec_match[1]) + (int(dec[2]) - int(dec_match[2]))/60.)
            if ra_dif <= ARCMIN_THRESH and dec_dif <= ARCMIN_THRESH:
                print(ref, match)
                m = {'ref': ref, 'match': match}
                final_matches.append(m)
                counter += 1
    print("Found {} matches".format(counter))
    write_wcs_copy(main_path, final_matches)


def write_wcs_copy(directory, matches):
    with open("{}/wcs.cl".format(directory), 'w') as w:
        for match in matches:
            cmd = "wcscopy {}/{} {}/{}\n".format(pics_path, match['match'], pics_path, match['ref'])
            w.write(cmd)


def ref_match_setup(ref, match):
    with open(ref, 'r') as r_coo:
        with open(match,'r') as m_coo:
            refs = [r for r in r_coo]
            matches = [m for m in m_coo]
            print(refs)
            print(matches)
            return



ref_prefix = 'R'
main_path = "/Users/research/Desktop/PROJECT/IMAGES"
pics_path = "{}/all_coords".format(main_path)
files = [f for f in listdir(pics_path) if isfile(join(pics_path, f))][1:]
find_matching_pointings(main_path, pics_path, ref_prefix)



#ref_path = "{}/koords/ref_coos".format(main_path)
#ref_files = [f for f in listdir(ref_path) if isfile(join(ref_path, f))][1:]



