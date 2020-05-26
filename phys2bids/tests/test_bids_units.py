from phys2bids.bids_units import bidsify_units


def test_bidsify_units():
    # test normal unit
    bidsify_units("V")
    # test unit with standard prefix
    bidsify_units("centik")
    # test unit with not standard prefix
    bidsify_units("matV")
    # test unit that's not bids standard
    bidsify_units("mmlie")
