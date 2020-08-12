import glob
import json
import math
import re
import shutil
import subprocess
from os import remove
from os.path import isfile, join, split
from pkg_resources import resource_filename

from phys2bids._version import get_versions
from phys2bids.phys2bids import phys2bids


def check_string(str_container, str_to_find, str_expected, is_num=True):
    idx = [log_idx for log_idx, log_str in enumerate(
                      str_container) if str_to_find in log_str]
    str_found = str_container[idx[0]]
    if is_num:
        num_found = re.findall(r"[-+]?\d*\.\d+|\d+", str_found)
        return str_expected in num_found
    else:
        return str_expected in str_found
