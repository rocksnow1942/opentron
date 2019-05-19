import os
from opentrons import labware, instruments, modules, robot

# robot.connect()
# for module in robot.modules:
#     module.disconnect()
# robot.modules = modules.discover_and_connect()
#

mag_deck = modules.load('magdeck', '1')
mag_plate = labware.load('96strip_test', '1', share=True)

trough = labware.load('trough-12row', '2')
pcr_strip = labware.load('pcr_strip_on_magnet', '3')
tip_rack = [labware.load('tiprack-200ul', slot) for slot in ['7', '8']]
single_tip_rack = [labware.load('tiprack-200ul', slot)
                   for slot in ['10', '11']]
liquid_trash = labware.load('trough-12row', '6')
multi_pipette = instruments.P300_Multi(
            mount='left',
            tip_racks=tip_rack)

single_pipette = instruments.P300_Single(
            mount='right',
            tip_racks=single_tip_rack)

butanol = 'A2'  # input for butanol position in trough
starting_tip_position = 'A1'

multi_pipette.start_at_tip(tip_rack[0].cols(starting_tip_position[1:]))
butanol_location = trough[butanol]

# remove top oil
# location=tip_rack[starting_tip_position],presses=3,increment=1; tip #1
multi_pipette.pick_up_tip(presses=3, increment=0.3)
for strip_no in pcr_strip.cols('1', '4', '7'):
    multi_pipette.set_flow_rate(aspirate=15, dispense=15)
    multi_pipette.transfer(150, strip_no.bottom(10), liquid_trash['A5'].bottom(
        20), new_tip='never')  # fine tune strip position to remove oil
    multi_pipette.blow_out()._position_for_aspirate()
    multi_pipette.set_flow_rate(aspirate=600, dispense=30)
    multi_pipette.aspirate(200).delay(seconds=1).dispense(200)
    multi_pipette.blow_out()._position_for_aspirate()
multi_pipette.set_flow_rate(aspirate=150, dispense=150)
multi_pipette.drop_tip()

# add 100ul butanol to each well
#trough width 8mm, width 72mm. each 800ul volume, liquid go down by 1.4 mm
# location=tip_rack['A'+str(int(starting_tip_position[1])+1)],presses=3,increment=1 , tip #2
multi_pipette.pick_up_tip(presses=3, increment=0.3)
multi_pipette.set_flow_rate(aspirate=150, dispense=150)
for strip_no, butanol_depth in zip(pcr_strip.cols('1', '4', '7'), [5, 3.6, 2.2]):
    multi_pipette.aspirate(
        volume=100, location=butanol_location.bottom(butanol_depth)).air_gap(20)
    multi_pipette.dispense(strip_no.top(-4))
    multi_pipette.blow_out()._position_for_aspirate()

# mix butanol with emulsion

for strip_no in pcr_strip.cols('1', '4', '7'):
    multi_pipette.set_flow_rate(aspirate=150, dispense=150)
    multi_pipette.move_to(strip_no.top(30))
    for position in [2, 3, 4, 5]:
        multi_pipette.mix(repetitions=10, volume=100,
                          location=strip_no.bottom(position))
    multi_pipette.move_to(strip_no.top(-5)).delay(seconds=5)
    multi_pipette.blow_out()._position_for_aspirate()
    multi_pipette.move_to(strip_no.top(-5)).delay(seconds=2)
    for a in range(5):
        multi_pipette.aspirate(200).delay(seconds=10).dispense(200)

    # no need to touch tip
    # multi_pipette.robot.gantry.push_speed()
    # multi_pipette.robot.gantry.set_speed(20)
    # multi_pipette.move_to((strip_no ,strip_no.from_center(x=0.8,y=0,z=0.6)),strategy='direct')
    # multi_pipette.move_to((strip_no ,strip_no.from_center(x=-0.8,y=0,z=0.6)),strategy='direct')
    # multi_pipette.robot.gantry.pop_speed()
multi_pipette.set_flow_rate(aspirate=150, dispense=150)
multi_pipette.move_to(liquid_trash['A5'].top())
# multi_pipette.drop_tip()

# spin down for faster phase separation.
multi_pipette.delay(minutes=20)


# aspirate off top butanol_oil phase
# since didn't drop tip, may use the same tip.
# multi_pipette.pick_up_tip(presses=3, increment = 0.3) # tip # 3
for strip_no in pcr_strip.cols('1', '4', '7'):
    multi_pipette.set_flow_rate(aspirate=15, dispense=100)
    multi_pipette.transfer(200, strip_no.bottom(8), liquid_trash['A5'].bottom(
        20), new_tip='never')  # fine tune strip position to remove oil
    multi_pipette.blow_out()._position_for_aspirate()
    multi_pipette.set_flow_rate(aspirate=600, dispense=30)
    multi_pipette.aspirate(200).delay(seconds=3).dispense(200)
    multi_pipette.blow_out()._position_for_aspirate()
multi_pipette.set_flow_rate(aspirate=150, dispense=150)
multi_pipette.drop_tip()

# combine all remaining liquid to magdeck
multi_pipette.pick_up_tip(presses=3, increment=0.3)  # tip # 4
for strip_no in pcr_strip.cols('1', '4', '7'):
    multi_pipette.set_flow_rate(aspirate=15, dispense=50)
    multi_pipette.transfer(50, strip_no.bottom(0.5), mag_plate.cols(
        '1')[0].top(-5), new_tip='never')  # fine tune strip position to remove oil
    multi_pipette.blow_out()._position_for_aspirate()
multi_pipette.set_flow_rate(aspirate=150, dispense=150)
multi_pipette.drop_tip()


## make a sound when program is done:
for i in range(10):
    os.system('say "your program has finished"')
