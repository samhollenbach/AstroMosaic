from os import listdir
from os.path import isfile, join
import re

def get_ra_dec(file_name, with_s, no_labels):
    if with_s:
        ra_re = re.search('.{2}h.{2}m.{4}s', file_name)
        ra = re.sub('\..s', 's', ra_re.group(0))
        dec = re.search('.{2}d.{2}m.{2}s', file_name).group(0)
    else:
        ra_re = re.search('.{2}h.{2}m', file_name)
        ra = re.sub('\..s', 's', ra_re.group(0))
        dec = re.search('.{2}d.{2}m', file_name).group(0)

    if no_labels:
        ra = ra.replace("h", " ").replace("m", " ").replace("s", "")
        dec = dec.replace("d", " ").replace("m", " ").replace("s", "")
    return ra, dec



def ref_match_setup(ref, match):
    with open(ref, 'r') as r_coo:
        with open(match,'r') as m_coo:
            refs = [r for r in r_coo]
            matches = [m for m in m_coo]

            print(refs)
            print(matches)



            return




main_path = "/Users/research/Desktop/PROJECT/IMAGES"
centers_path = "{}/koords/final_image_coos".format(main_path)
files = [f for f in listdir(centers_path) if isfile(join(centers_path, f))][1:]

ref_path = "{}/koords/ref_coos".format(main_path)
ref_files = [f for f in listdir(ref_path) if isfile(join(ref_path, f))][1:]

with open('dss_get.in', 'w') as w:
    for f in files:
        ra_full, dec_full = get_ra_dec(f, True, False)
        name = 'ref_{}_{}'.format(ra_full,dec_full)
        ra, dec = get_ra_dec(f, True, True)
        w.write('{} {} {} 29 19\n'.format(name, ra, dec))


        #for ref in ref_files:
        #    if get_ra_dec(f, False, True) == get_ra_dec(ref, False, True):
        #        print(f, ref)
        #ref_match_setup(f, ref)
        print(get_ra_dec(f, True, True))


