import os
import logging

from pathlib import Path

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
    Read the input unit of measure and use the dictionary of aliases
    to bidsify its value.
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


def use_heuristic(heur_file, sub, ses, filename, outdir, record_label=''):
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
                 'dir': '', 'rec': '', 'run': '', 'recording': record_label}

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
    bids_keys.update(heur.heur(Path(filename).stem))

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
    utils.path_exists_or_make_it(fldr)

    heurpath = os.path.join(fldr, f'{name}physio')

    return heurpath
