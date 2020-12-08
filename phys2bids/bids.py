"""BIDS functions for phys2bids package."""
import logging
import os
from csv import reader
from pathlib import Path

import yaml

from phys2bids import utils

LGR = logging.getLogger(__name__)

UNIT_ALIASES = {
                # kelvin: thermodynamic temperature
                'kelvin': 'K', 'kelvins': 'K',
                # mole: amount of substance
                'mol': 'mol', 'mole': 'mol',
                # newton: force, weight
                'newton': 'N', 'newtons': 'N',
                # pascal: pressure, stress
                'pascal': 'Pa', 'pascals': 'Pa', 'pa': 'Pa',
                # volt: voltage (electrical potential), emf
                'volt': 'V', 'volts': 'V',
                # degree Celsius: temperature relative to 273.15 K
                '°c': '°C', '°celsius': '°C', 'celsius': '°C',
                # ampere: electric current
                'ampere': 'A', 'amp': 'A', 'amps': 'A',
                # second: time and hertzs: frequency
                # siemens: electric conductance (e.g. EDA)
                'siemens': 'S',
                # second: time and hertzs
                '1/hz': 's', '1/hertz': 's', 'hz': 'Hz',
                '1/s': 'Hz', '1/second': 'Hz', '1/seconds': 'Hz',
                '1/sec': 'Hz', '1/secs': 'Hz', 'hertz': 'Hz',
                'second': 's', 'seconds': 's', 'sec': 's',
                'secs': 's',
                # All the aliases with one letter (to avoid issues)
                'k': 'K', 'n': 'N', 'v': 'V', 'c': '°C', 'a': 'A', 's': 's',
}

# Init dictionary of aliases for multipliers. Entries are still lowercase
PREFIX_ALIASES = {
                    # Multiples - skip "mega" and only up to "tera"
                    'da': 'da', 'deca': 'da', 'h': 'h', 'hecto': 'h',
                    'k': 'k', 'kilo': 'k', 'g': 'G', 'giga': 'G', 't': 'T',
                    'tera': 'T',
                    # Submultipliers
                    'd': 'd', 'deci': 'd', 'c': 'c', 'centi': 'c',
                    'milli': 'm', 'm': 'm', 'µ': 'µ', 'micro': 'µ',
                    'n': 'n', 'nano': 'n', 'p': 'p', 'pico': 'p',
                    'f': 'f', 'femto': 'f', 'a': 'a', 'atto': 'a',
                    'z': 'z', 'zepto': 'z', 'y': 'y', 'yocto': 'y',
}


def bidsify_units(orig_unit):
    """
    Read the input unit of measure and use the dictionary of aliases to bidsify its value.

    It is possible to make simple conversions.

    Parameters
    ----------
    unit: string
        Unit of measure, might or might not be BIDS compliant.

    Returns
    -------
    new_unit: str
        BIDSified alias of input unit

    Notes
    -----
    This function should implement a double check, one for unit and
    the other for prefixes (e.g. "milli"). However, that is going to be tricky,
    unless there is a weird way to multiply two dictionaries together.
    """
    # for every unit alias in the dict
    unit = orig_unit.lower()
    for u_key in UNIT_ALIASES.keys():
        # check that u_key is part of unit
        if unit.endswith(u_key):
            new_unit = UNIT_ALIASES[u_key]
            unit = unit[:-len(u_key)]
            if unit != '':
                # for every prefix alias
                prefix = PREFIX_ALIASES.get(unit, '')
                if prefix == '':
                    LGR.warning(f'The given unit prefix {unit} does not '
                                'have aliases, passing it as is')
                    prefix = orig_unit[:len(unit)]

                return prefix + new_unit
            else:
                return new_unit

    # If we conclude the loop without returning, it means the unit doesn't have aliases
    LGR.warning(f'The given unit {orig_unit} does not have aliases, '
                f'passing it as is')
    return orig_unit


def use_heuristic(heur_file, sub, ses, filename, outdir, run='', record_label=''):
    """
    Import and use the heuristic specified by the user to rename the file.

    Parameters
    ----------
    heur_file: path
        Fullpath to heuristic file.
    sub: str or int
        Name of subject.
    ses: str or int or None
        Name of session.
    filename: path
        Name of the input of phys2bids.
    outdir: str or path
        Path to the directory that will become the "site" folder
        ("root" folder of BIDS database).
    record_label: str
        Optional label for the "record" entry of BIDS.

    Returns
    -------
    heurpath: str or path
        Returned fullpath to tsv.gz new file (post BIDS formatting).

    Raises
    ------
    KeyError
        if `bids_keys['task']` is empty
    """
    utils.check_file_exists(heur_file)

    # Initialise a dictionary of bids_keys that has already "recording"
    bids_keys = {'sub': '', 'ses': '', 'task': '', 'acq': '', 'ce': '',
                 'dir': '', 'rec': '', 'run': run, 'recording': record_label}

    # Start filling bids_keys dictionary and path with subject and session
    if sub.startswith('sub-'):
        bids_keys['sub'] = sub[4:]
        fldr = os.path.join(outdir, sub)
    else:
        bids_keys['sub'] = sub
        fldr = os.path.join(outdir, f'sub-{sub}')

    if ses:
        if ses.startswith('ses-'):
            bids_keys['ses'] = ses[4:]
            fldr = os.path.join(fldr, ses)
        else:
            bids_keys['ses'] = ses
            fldr = os.path.join(fldr, f'ses-{ses}')

    # Load heuristic and use it to fill dictionary
    heur = utils.load_heuristic(heur_file)
    bids_keys.update(heur.heur(Path(filename).stem, run))

    # If bids_keys['task'] is still empty, stop the program
    if not bids_keys['task']:
        LGR.warning(f'The heuristic {heur_file} could not deal with'
                    f'{Path(filename).stem}')
        raise KeyError('No "task" attribute found')

    # Compose name by looping in the bids_keys dictionary
    # and adding nonempty keys
    name = ''
    for key in bids_keys:
        if bids_keys[key] != '':
            name = f'{name}{key}-{bids_keys[key]}_'

    # Finish path, create it, add filename, export
    fldr = os.path.join(fldr, 'func')
    os.makedirs(fldr, exist_ok=True)

    heurpath = os.path.join(fldr, f'{name}physio')

    return heurpath


def participants_file(outdir, yml, sub):
    """
    Create participants.tsv file if it does not exist.

    If it exists and the subject is missing, then add it.
    Otherwise, do nothing.

    Parameters
    ----------
    outdir: path
        Full path to the output directory.
    yml: path
        Full path to the yaml file.
    sub: str
        Subject ID.

    """
    LGR.info('Updating participants.tsv ...')
    file_path = os.path.join(outdir, 'participants.tsv')
    if not os.path.exists(file_path):
        LGR.warning('phys2bids could not find participants.tsv')
        # Read yaml info if file exists
        if '.yml' in yml and os.path.exists(yml):
            LGR.info('Using yaml data to populate participants.tsv')
            with open(yml) as f:
                yaml_data = yaml.load(f, Loader=yaml.FullLoader)
            p_id = f'sub-{sub}'
            p_age = yaml_data['participant']['age']
            p_sex = yaml_data['participant']['sex']
            p_handedness = yaml_data['participant']['handedness']
        else:
            LGR.info('No yaml file was provided. Using phys2bids data to '
                     'populate participants.tsv')
            # Fill in with data from phys2bids
            p_id = f'sub-{sub}'
            p_age = 'n/a'
            p_sex = 'n/a'
            p_handedness = 'n/a'

        # Write to participants.tsv file
        header = ['participant_id', 'age', 'sex', 'handedness']
        utils.append_list_as_row(file_path, header)

        participants_data = [p_id, p_age, p_sex, p_handedness]
        utils.append_list_as_row(file_path, participants_data)

    else:  # If participants.tsv exists only update when subject is not there
        LGR.info('phys2bids found participants.tsv. Updating if needed...')
        # Find participant_id column in header
        pf = open(file_path, 'r')
        header = pf.readline().split("\t")
        header_length = len(header)
        pf.close()
        p_id_idx = header.index('participant_id')

        # Check if subject is already in the file
        sub_exists = False
        with open(file_path) as pf:
            tsvreader = reader(pf, delimiter="\t")
            for line in tsvreader:
                if sub in line[p_id_idx]:
                    sub_exists = True
                    break
        # Only append to file if subject is not in the file
        if not sub_exists:
            LGR.info(f'Appending subjet sub-{sub} to participants.tsv ...')
            participants_data = ['n/a'] * header_length
            participants_data[p_id_idx] = f'sub-{sub}'
            utils.append_list_as_row(file_path, participants_data)


def dataset_description_file(outdir):
    """
    Create dataset_description.json file if it does not exist.

    If it exists, do nothing.

    Parameters
    ----------
    outdir: path
        Full path to the output directory.

    """
    # dictionary that will be written for the basic dataset description version
    data_dict = {"Name": os.path.splitext(os.path.basename(outdir))[0],
                 "BIDSVersion": "1.4.0", "DatasetType": "raw"}
    file_path = os.path.join(outdir, 'dataset_description.json')
    # check if dataset_description.json exists, if it doesn't create it
    if not os.path.exists(file_path):
        LGR.warning('phys2bids could not find dataset_description.json,'
                    'generating it with provided info')
        utils.write_json(file_path, data_dict)


def readme_file(outdir):
    """
    Create README file if it does not exist.

    If it exists, do nothing.

    Parameters
    ----------
    outdir: path
        Full path to the output directory.

    """
    file_path = os.path.join(outdir, 'README')
    if not os.path.exists(file_path):
        text = 'Empty README, please fill in describing the dataset in more detail.'
        LGR.warning('phys2bids could not find README,'
                    'generating it EMPTY, please fill in the necessary info')
        utils.write_file(file_path, '', text)
