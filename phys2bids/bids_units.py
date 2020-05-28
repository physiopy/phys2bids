import logging

LGR = logging.getLogger(__name__)

unit_aliases = {
                # ampere: electric current
                'a': 'A', 'ampere': 'A', 'amp': 'A', 'amps': 'A',
                # kelvin: thermodynamic temperature
                'k': 'K', 'kelvin': 'K', 'kelvins': 'K',
                # mole: amount of substance
                'mol': 'mol', 'mole': 'mol',
                # hertz: frequency
                'hz': 'Hz', 'hertz': 'Hz',
                '1/s': 'Hz', '1/second': 'Hz', '1/seconds': 'Hz',
                '1/sec': 'Hz', '1/secs': 'Hz',
                # newton: force, weight
                'n': 'N', 'newton': 'N', 'newtons': 'N',
                # pascal: pressure, stress
                'pa': 'Pa', 'pascal': 'Pa', 'pascals': 'Pa',
                # volt: voltage (electrical potential), emf
                'v': 'V', 'volt': 'V', 'volts': 'V',
                # degree Celsius: temperature relative to 273.15 K
                '°c': '°C', 'celsius': '°C', '°celsius': '°C',
                # second: time
                'second': 's', 'seconds': 's', 'sec': 's',
                'secs': 's',
                '1/hz': 's', '1/hertz': 's', 's': 's'
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
    It is possible to make simple conversions

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
    # call prefix and unit dicts
    new_unit = ""
    # for every unit alias in the dict
    for u_key in unit_aliases.keys():
        unit = orig_unit.lower()
        # check that u_key is part of unit
        if unit.endswith(u_key):
            new_unit = unit[-len(u_key):]
            # check that it is at the end
            if new_unit == u_key:
                # leave only the prefix
                unit = unit.replace(u_key, "")
                # check prefix in not null
                if unit != "":
                    # for every prefix alias
                    prefix = prefix_aliases.get(unit, '')
                    if prefix == '':
                        LGR.warning(f'The given unit prefix {unit} does not have aliases, '
                                    f'passing it as is')
                        return unit + new_unit
                    else:
                        return prefix + new_unit
                return new_unit
    LGR.warning(f'The given unit {orig_unit} does not have aliases, '
                f'passing it as is')
    return orig_unit
