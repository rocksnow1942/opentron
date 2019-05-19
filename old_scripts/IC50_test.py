
from opentrons import labware, instruments, robot, modules

# mag_deck = modules.load('magdeck', '1')
mag_plate = labware.load('96strip_test','1',share = True)
trough = labware.load('trough-12row', '2')
liquid_trash = labware.load('trough-12row', '6')

tip_rack = [labware.load('tiprack-200ul', slot) for slot in ['7','8']]
single_tip_rack = [labware.load('tiprack-200ul',slot) for slot in ['10','11']]

elisa_strip = labware.load('elisa_strip','3')
ep_rack = labware.load('tube-rack-eppendorf','5')
tube_rack = labware.load('tube-rack-15_50ml_apt','4')
multi_pipette = instruments.P300_Multi(
            mount='left',
            tip_racks=tip_rack)
single_pipette = instruments.P300_Single(
            mount='right',
            tip_racks=single_tip_rack)


#tip position
multi_tip_starting_position = 'A1'
multi_pipette.start_at_tip(tip_rack[0].cols(multi_tip_starting_position[1:]))

# experiment setup
distribute_volume = 100
beads_volume = 50
receptor_buffer = trough['A1']
receptor_buffer_volume = '7ml'
ag_beads = trough['A2']
ag_beads_volume = '5ml'
data_point = 8
dilution_factor = 3.16
transfer_volume = distribute_volume/(dilution_factor-1)
total_volume = distribute_volume+transfer_volume
mix_volume = total_volume/2.0


# distrbute to each column
multi_pipette.set_flow_rate(aspirate=100,dispense=100)
multi_pipette.pick_up_tip(presses=3, increment=0.3)
for col in elisa_strip.cols('2', length=data_point-1):
    multi_pipette.transfer(distribute_volume, receptor_buffer.bottom(1), col.top(),blow_out=True, new_tip='never')
multi_pipette.drop_tip()

#perform serial dilution
multi_pipette.pick_up_tip()
for i,j in zip(elisa_strip.cols('1',length=data_point-2),elisa_strip.cols('2',length=data_point-2)):
    multi_pipette.transfer(transfer_volume,i.bottom(2),j.bottom(2),new_tip='never',mix_after=(5,mix_volume))
    multi_pipette.move_to(j.top())
    multi_pipette.blow_out().delay(seconds=1)._position_for_aspirate()
    multi_pipette.blow_out().delay(seconds=1)._position_for_aspirate()
    temp = j
multi_pipette.transfer(transfer_volume,temp.bottom(1),liquid_trash['A5'].bottom(20),new_tip='never')
# multi_pipette.transfer(transfer_volume,elisa_strip.cols('1',length=data_point-2),elisa_strip.cols('2',length=data_point-2),mix_after=(3,mix_volume),blow_out=True,new_tip='never')
multi_pipette.drop_tip()

# add beads
multi_pipette.pick_up_tip(presses=3, increment=0.3)
for col in elisa_strip.cols(str(data_point), to='1'):
    multi_pipette.distribute(beads_volume,ag_beads.bottom(1), col.top(),blow_out=True,new_tip='never')

# mix beads
for col in elisa_strip.cols(str(data_point), to='1'):
    multi_pipette.mix(repetitions=5, volume=mix_volume, location = col.bottom(2))
    multi_pipette.move_to(col.top()).delay(seconds=1)
    multi_pipette.blow_out().delay(seconds=1)._position_for_aspirate()
    multi_pipette.blow_out().delay(seconds=1)._position_for_aspirate()
multi_pipette.drop_tip()
