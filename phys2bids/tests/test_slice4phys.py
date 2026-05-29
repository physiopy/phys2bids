import os

import matplotlib

from phys2bids import io, slice4phys


def test_estimate_ntp_and_tr(multi_run_file):
    chtrig = 1
    test_path, test_filename = os.path.split(multi_run_file)
    phys_obj = io.load_txt(multi_run_file, chtrig)

    est_ntp, est_tr = slice4phys.estimate_ntp_and_tr(phys_obj)

    assert est_ntp == [534, 513]
    assert est_tr == [1.2, 1.2]

    est_ntp, est_tr = slice4phys.estimate_ntp_and_tr(phys_obj, ci=0.01)

    assert est_ntp == [534, 513]
    assert est_tr == [1.2, 1.2]

    # BREAK
    with raises(ValueError) as errorinfo:
        est_ntp, est_tr = slice4phys.estimate_ntp_and_tr(phys_obj, ci=1.20)
    assert "percentages above 1" in str(errorinfo.value)
    with raises(ValueError) as errorinfo:
        est_ntp, est_tr = slice4phys.estimate_ntp_and_tr(phys_obj, ci="left")
    assert "integers or floats" in str(errorinfo.value)

    # Add test on single take file → maybe as integration test.
