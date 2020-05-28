import logging

LGR = logging.getLogger(__name__)

unit_aliases = {
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
                'k': 'K',  'n': 'N', 'v': 'V', 'c': '°C', 'a': 'A', 's': 's',
}

# Init dictionary of aliases for multipliers. Entries are still lowercase
prefix_aliases = {
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
    for u_key in unit_aliases.keys():
        # check that u_key is part of unit
        if unit.endswith(u_key):
            new_unit = unit_aliases[u_key]
            unit = unit[:-len(u_key)]
            if unit != '':
                # for every prefix alias
                prefix = prefix_aliases.get(unit, '')
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
