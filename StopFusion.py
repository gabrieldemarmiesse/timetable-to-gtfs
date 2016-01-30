import Other
from tempfile import mkstemp
from shutil import move
from os import remove, close
import re

def replace(file_path, pattern, subst):
    #Create temp file
    fh, abs_path = mkstemp()
    with open(abs_path, 'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                new_file.write(line.replace(pattern, subst))
    close(fh)
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)

def replace_regex(file_path, pattern, subst):
    #Create temp file
    fh, abs_path = mkstemp()
    with open(abs_path, 'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                new_file.write(re.sub(pattern, subst, line))
    close(fh)
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)


def stop_fusion(name_stop_1, new_stop_name):
    id1 = Other.to_id(name_stop_1)
    other_id = Other.to_id(new_stop_name)
    replace("gtfs/stop_times.txt", id1, other_id)
    replace_regex("gtfs/stops.txt", ".*" + id1 + ".*" , "")

stop_fusion("GARE ROUTIÈRE VSA","GR. VALBONNE SOPHIA ANTIPOLIS")
