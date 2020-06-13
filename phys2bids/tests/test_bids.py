import os

from pkg_resources import resource_filename

import pytest

from phys2bids.bids import bidsify_units, use_heuristic
from phys2bids.bids import UNIT_ALIASES


def test_bidsify_units():
    # Add a dictionary of test possibilities
    unit_tests = {
                  # test unit with standard prefix
                  'centik': 'cK', 'CENTIk': 'cK',
                  # test unit with not standard prefix
                  'matV': 'matV', 'BigV': 'BigV',
                  # test unit that are not bids standard
                  'mmHg': 'mmHg', 'mmlie': 'mmlie', 'MMLIE': 'MMLIE',
                 }
    # Actually test
    for unit_key in unit_tests.keys():
        assert bidsify_units(unit_key) == unit_tests[unit_key]
    # test there is not problem with every unit in the dict
    for unit_key in UNIT_ALIASES.keys():
        assert bidsify_units(unit_key) == UNIT_ALIASES[unit_key]


@pytest.mark.parametrize('test_sub', ['SBJ01', 'sub-006', '006'])
@pytest.mark.parametrize('test_ses', ['', 'S05', 'ses-42', '42'])
def test_use_heuristic(tmpdir, test_sub, test_ses):
    test_heur_path = resource_filename('phys2bids', 'heuristics')
    test_heur_file = 'heur_test_acq.py'
    test_full_heur_path = os.path.join(test_heur_path, test_heur_file)
    test_input_path = resource_filename('phys2bids', 'tests/data')
    test_input_file = 'Test_belt_pulse_samefreq.acq'
    test_full_input_path = os.path.join(test_input_path, test_input_file)
    test_outdir = tmpdir
    test_record_label = 'test'

    heur_path = use_heuristic(test_full_heur_path, test_sub, test_ses,
                              test_full_input_path, test_outdir, test_record_label)

    if test_sub[:4] == 'sub-':
        test_sub = test_sub[4:]

    test_result_path = (f'{tmpdir}/sub-{test_sub}')
    test_result_name = (f'sub-{test_sub}')

    if test_ses[:4] == 'ses-':
        test_ses = test_ses[4:]

    if test_ses:
        test_result_path = (f'{test_result_path}/ses-{test_ses}')
        test_result_name = (f'{test_result_name}_ses-{test_ses}')

    test_result = (f'{test_result_path}/func/{test_result_name}'
                   f'_task-test_rec-biopac_run-01_recording-test_physio')

    assert os.path.normpath(test_result) == os.path.normpath(str(heur_path))
