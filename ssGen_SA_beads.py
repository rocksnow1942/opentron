from opentrons import labware, instruments, robot, modules

# connect to magnet module, may not be necessary
robot.connect()
for module in robot.modules:
    module.disconnect()
robot.modules = modules.discover_and_connect()

mag_deck = modules.load('magdeck', '1')
mag_plate = labware.load('96strip_test','1',share = True)

trough = labware.load('trough-12row', '2')
liquid_trash = labware.load('trough-12row', '9')

tip_rack = [labware.load('tiprack-200ul', slot) for slot in ['7','8']]
single_tip_rack = [labware.load('tiprack-200ul',slot) for slot in ['10','11']]

ep_rack = labware.load('tube-rack-2ml','5') # need to create a new labware for eppendorf tube, eppendorf_2ml

tube_rack = labware.load('tube-rack-15_50ml_apt','4')

pcr_strip = labware.load('pcr_strip', '3')

multi_pipette = instruments.P300_Multi(
            mount='left',
            tip_racks=tip_rack)

single_pipette = instruments.P300_Single(
            mount='right',
            tip_racks=single_tip_rack)
