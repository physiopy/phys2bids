import os
from pkg_resources import resource_filename

import pytest
import yaml
from csv import reader

from phys2bids import bids
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
        assert bids.bidsify_units(unit_key) == unit_tests[unit_key]
    # test there is not problem with every unit in the dict
    for unit_key in UNIT_ALIASES.keys():
        assert bids.bidsify_units(unit_key) == bids.UNIT_ALIASES[unit_key]


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

    heur_path = bids.use_heuristic(test_full_heur_path, test_sub, test_ses,
                                   test_full_input_path, test_outdir,
                                   record_label=test_record_label)

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


@pytest.mark.parametrize('outdir', '.')
def test_README_file(outdir):
    bids.readme_file(outdir)
    assert os.path.join(outdir, "README")
    os.remove(os.path.join(outdir, "README"))


@pytest.mark.parametrize('outdir', '.')
def test_dataset_description_file(outdir):
    bids.dataset_description_file(outdir)
    assert os.path.join(outdir, "dataset_description.json")
    os.remove(os.path.join(outdir, "dataset_description.json"))


@pytest.mark.parametrize('outdir', '.')
def test_participants_file(outdir):

    # Checks first condition in line 198
    test_sub = '001'
    test_sub_no_yml = '002'
    test_missing_sub = '003'
    test_yaml_path = os.path.join(outdir, 'test.yml')

    # Populate yaml file
    data = dict(participant=dict(
                participant_id=f'sub-{test_sub}',
                age='25',
                sex='m',
                handedness='r'))

    test_header = ['participant_id', 'age', 'sex', 'handedness']
    test_data = [f'sub-{test_sub}', '25', 'm', 'r']
    test_na = [f'sub-{test_sub_no_yml}', 'n/a', 'n/a', 'n/a']
    test_missing = [f'sub-{test_missing_sub}', 'n/a', 'n/a', 'n/a']
    test_list = [test_header, test_data]
    test_no_yml = [test_header, test_data, test_na]
    test_missing_list = [test_header, test_data, test_na, test_missing]

    # Checks validity of tsv lines when yml file is given
    with open(test_yaml_path, 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False)

    bids.participants_file(outdir, test_yaml_path, test_sub)

    counter = 0
    with open(os.path.join(outdir, 'participants.tsv')) as pf:
        tsvreader = reader(pf, delimiter="\t")
        for line in tsvreader:
            assert line == test_list[counter]
            counter += 1

    # Checks when no yml file is given
    bids.participants_file(outdir=outdir, yml='', sub=test_sub_no_yml)
    counter = 0
    with open(os.path.join(outdir, 'participants.tsv')) as pf:
        tsvreader = reader(pf, delimiter="\t")
        for line in tsvreader:
            assert line == test_no_yml[counter]
            counter += 1

    # Checks validity of tsv lines when file exists but no line for Subject
    bids.participants_file(outdir=outdir, yml='', sub=test_missing_sub)
    counter = 0
    with open(os.path.join(outdir, 'participants.tsv')) as pf:
        tsvreader = reader(pf, delimiter="\t")
        for line in tsvreader:
            assert line == test_missing_list[counter]
            counter += 1

    # Test that subject from previous check is already there
    bids.participants_file(outdir=outdir, yml='', sub=test_missing_sub)
    counter = 0
    with open(os.path.join(outdir, 'participants.tsv')) as pf:
        tsvreader = reader(pf, delimiter="\t")
        for line in tsvreader:
            assert line == test_missing_list[counter]
            counter += 1

    os.remove(os.path.join(outdir, "participants.tsv"))
    os.remove(os.path.join(outdir, "test.yml"))
