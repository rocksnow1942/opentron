"""
###standard name to use when loading labwares###
### postition can change.
"""
from opentrons import labware
mag_plate = labware.load('96strip_test','1',share = True)
trough = labware.load('trough-12row', '2')
liquid_trash = labware.load('trough-12row', '6')
tip_rack = [labware.load('tiprack-200ul', slot) for slot in ['7','8']]
single_tip_rack = [labware.load('tiprack-200ul',slot) for slot in ['10','11']]
elisa_strip = labware.load('elisa_strip','3')
ep_rack = labware.load('tube-rack-eppendorf','5')
tube_rack = labware.load('tube-rack-15_50ml_apt','4')
ep_tube_rack = labware.load('ep_5ml_tube_rack','4')


"""
'pp_plate_mag' for PP plate on magnet modules

'trough-12row' for trough 12 row

'elisa_strip' for pierce elisa_strip put on slot directly

'tube_rack-eppendorf' for 26 tube rack with 1.5ml eppendorf tube

'tube-rack-15-15_50ml_apt' for the rack with 15ml and 50ml tubes

'pcr_strip_on_magnet' for pcr strip put on the heat block plate and on slot directly

'deep_well_0_5ml_mag' for 0.5ml PP plate on magnet module

'deep_well_1ml_mag' for 1ml PP plate on magnet module

'ep_5ml_tube_rack' for the rack with 5ml eppendorf tube and 50ml tubes.


"""

"""
To add to common task deck plan:

1. deep_well_0_5ml_mag
2. deep_well_1ml_mag

3. deep_


"""
