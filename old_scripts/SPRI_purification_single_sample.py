from opentrons import labware, instruments, robot, modules

# connect to magnet module, may not be necessary
# robot.connect()
# for module in robot.modules:
#     module.disconnect()
# robot.modules = modules.discover_and_connect()

mag_deck = modules.load('magdeck', '1')
mag_plate = labware.load('96strip_test','1',share = True)

trough = labware.load('trough-12row', '2')
liquid_trash = labware.load('trough-12row', '6')

tip_rack = [labware.load('tiprack-200ul', slot) for slot in ['7','8']]
single_tip_rack = [labware.load('tiprack-200ul',slot) for slot in ['10','11']]

ep_rack = labware.load('tube-rack-eppendorf','5') # need to create a new labware for eppendorf tube, eppendorf_2ml

tube_rack = labware.load('tube-rack-15_50ml_apt','4')

pcr_strip = labware.load('pcr_strip_on_magnet', '3')

multi_pipette = instruments.P300_Multi(
            mount='left',
            tip_racks=tip_rack)

single_pipette = instruments.P300_Single(
            mount='right',
            tip_racks=single_tip_rack)


class Tube_50ml_depth:
    """
    conical tube class, volume stored is in ml.
    """
    def __init__(self,volume):
        if volume[-2:].lower() == 'ul':
            self.volume = float(volume[:-2]) / 1000.0 # in ml
        elif volume[-2:].lower() == 'ml':
            self.volume = float(volume[:-2])
        else:
            raise ValueError( "Use '##ul' or '##ml' for tube volume.")
        if self.volume > 50 or self.volume < 5:
            raise ValueError("load more reagent")
        else:
            self.depth = self.volume_to_depth(self.volume)
    def volume_to_depth(self,volume):
        depth_max = 101.34 # in mm
        depth_min = 17.8
        volume_max = 50 #in ml
        volume_min = 5 #in ml
        volume = max(0,volume)
        depth = (volume - volume_min)* (depth_max - depth_min)/(volume_max - volume_min) + depth_min
        return depth
    def pipette_out(self,volume): # this volume is in ul
        self.volume -= volume/1000.0
        self.depth = self.volume_to_depth(self.volume)
        return self.depth


class eppendorf_2ml_depth:
    """
    eppendorf tube class, volume stored are in ul.
    need calibrate tube
    """
    def __init__(self,volume):
        from bisect import bisect
        if volume[-2:].lower() == 'ul':
            self.volume = float(volume[:-2])
        elif volume[-2:].lower() == 'ml':
            self.volume = float(volume[:-2])*1000 #in ul
        else:
            raise ValueError( "Use '##ul' or '##ml' for tube volume.")
        if self.volume > 1500 or self.volume < 30:
            raise ValueError("load more reagent")
        else:
            self.depth = self.volume_to_depth(self.volume)
    def volume_to_depth(self,volume):
        from bisect import bisect
        volume = max(0,volume)
        volume_book =[0,25, 50,  75, 100,125, 150, 200,   250,  300,  350,  400,  450,  500, 600, 700,800,1000,1200,1400,1505]
        depth_book = [0,2.6,4.04,5.8,6.9,7.99,8.86,10.69, 11.59,12.9, 14.17,16.30, 17.2, 18.2,20.0, 21.9, 23.1, 26.5, 29.5, 32.4,34.3]
        p = bisect(volume_book,volume)
        depth = (volume-volume_book[p-1])*(depth_book[p]-depth_book[p-1])/(volume_book[p]-volume_book[p-1])+depth_book[p-1]
        return depth
    def pipette_out(self,volume): # this volume is in ul
        self.volume -= volume
        self.depth = self.volume_to_depth(self.volume)
        return self.depth


#tip position
single_tip_starting_position = 'A1'
multi_tip_starting_position = 'A1'
single_pipette.start_at_tip(single_tip_rack[0].wells(single_tip_starting_position))
multi_pipette.start_at_tip(tip_rack[0].cols(multi_tip_starting_position[1:]))

# reagent setup
spri_beads = tube_rack['A3']
spri_beads_volume = '40ml' # volume in ml
spri_depth = Tube_50ml_depth(spri_beads_volume)

ethonal = trough['A3'] # need to have >5ml, 6ml preffered.
elution_buffer = ep_rack['A1']
elution_buffer_volume = '500ul'
eb = eppendorf_2ml_depth(elution_buffer_volume)

# sample information
sample_volume = 150 # in ul
beads_to_sample_ratio = 2
sample_position = 1 # int, column number


# output dna position
elute_volume = 40
output_position = pcr_strip.cols('1')

# set values
spri_use_vol = sample_volume * beads_to_sample_ratio
sample_plate_posi = mag_plate.cols(str(sample_position))



"""
use input: sample_position;sample_volume,beads_to_sample_ratio,output_position as input.
"""

mag_deck.disengage()
# Add 2X volume of SPRI beads to sample; with single pipette or multi_pipette??
single_pipette.pick_up_tip(presses=3, increment = 0.3)
single_pipette.set_flow_rate(aspirate=60,dispense=60)


for wells in sample_plate_posi:
    single_pipette.transfer(spri_use_vol,spri_beads.bottom(spri_depth.pipette_out(spri_use_vol)-5),wells.top(-2),new_tip='never',blow_out=True)
single_pipette.drop_tip()

# mix well with multi_pipette and incubate for 10min
multi_pipette.pick_up_tip(presses=3, increment = 0.3)
multi_pipette.set_flow_rate(aspirate=150,dispense=150)
multi_pipette.mix(repetitions=10 ,volume=150,location=sample_plate_posi.bottom(1))

multi_pipette.move_to(sample_plate_posi.bottom(8))  # the blow_out height should be adjusted according to sample+spribeads volume.
for a in range(2):
    multi_pipette.aspirate(200).delay(seconds=5).dispense(200)
    multi_pipette.blow_out()._position_for_aspirate()
multi_pipette.drop_tip()

multi_pipette.delay(minutes=10)

# engage magnet for long time, then aspirate off supernatant
mag_deck.engage(height=13)

multi_pipette.delay(minutes=5)


# aspirate away supernatant
multi_pipette.set_flow_rate(aspirate=150,dispense=150)
multi_pipette.pick_up_tip(presses=3, increment = 0.3)
for i in range(round((sample_volume+spri_use_vol)/200)):
    multi_pipette.transfer(200,sample_plate_posi.bottom(1),liquid_trash['A5'].bottom(20),new_tip='never') # fine tune strip position to remove oil
    multi_pipette.blow_out()._position_for_aspirate()
    multi_pipette.blow_out()._position_for_aspirate()
multi_pipette.transfer(200,sample_plate_posi.bottom(0),liquid_trash['A5'].bottom(20),new_tip='never')
multi_pipette.blow_out()._position_for_aspirate()
multi_pipette.drop_tip()



# wash with 85% ethonal 300ul 2X
multi_pipette.set_flow_rate(aspirate=150,dispense=150)
multi_pipette.pick_up_tip(presses=3, increment = 0.3)
multi_pipette.transfer(300,ethonal.bottom(2),sample_plate_posi.top(-1),new_tip='never',blow_out=True) # position need to be adjusted according to plate
ethonal_tip = multi_pipette.current_tip()
multi_pipette.return_tip()
multi_pipette.delay(seconds=120)

multi_pipette.pick_up_tip(presses=3, increment = 0.3)
for i in range(3):
    multi_pipette.transfer(250,sample_plate_posi.bottom(2-i),liquid_trash['A5'].bottom(20),new_tip='never',blow_out=True)
multi_pipette.drop_tip()

multi_pipette.pick_up_tip(location=ethonal_tip,presses=3, increment = 0.3)
multi_pipette.transfer(300,ethonal.bottom(2),sample_plate_posi.top(-1),new_tip='never',blow_out=True) # position need to be adjusted according to plate
multi_pipette.delay(seconds=120)
for i in range(3):
    multi_pipette.transfer(250,sample_plate_posi.bottom(2-i),liquid_trash['A5'].bottom(20),new_tip='never',blow_out=True)

# air dry for 10minutes; with pipette removing bottom liquid and blow; possibly manually place on heatplate
for i in range(5):
    multi_pipette.transfer(300,sample_plate_posi.bottom(-0.1*i),liquid_trash['A5'].bottom(20),new_tip='never',blow_out=True)
    multi_pipette.delay(seconds=60)

multi_pipette.drop_tip()


# aliquote eb buffer to each well
mag_deck.disengage()
single_pipette.pick_up_tip()
for wells in sample_plate_posi:
    single_pipette.transfer(elute_volume,elution_buffer.bottom(max(0,eb.pipette_out(elute_volume)-3)) ,wells.bottom(10),new_tip='never', blow_out=True)
single_pipette.drop_tip()

# mix with multi_pipette
multi_pipette.pick_up_tip(presses=3, increment = 0.3)
multi_pipette.set_flow_rate(aspirate=50,dispense=150)
## this block is to rinse beads off the side of the well.
# x_off_set = 1 if sample_position % 2 ==1 else -1
# for i in range(5):
#     multi_pipette.aspirate(volume = elute_volume,location = sample_plate_posi.bottom()).delay(seconds=1)
#     multi_pipette.robot.gantry.push_speed()
#     multi_pipette.robot.gantry.set_speed(20)
#     multi_pipette.move_to((sample_plate_posi,sample_plate_posi.from_center(x=0.5*x_off_set,y=0,z=-0.5)),strategy='direct')
#     multi_pipette.robot.gantry.pop_speed()
#     multi_pipette.dispense(elute_volume).delay(seconds=1)
multi_pipette.blow_out()._position_for_aspirate()
multi_pipette.set_flow_rate(aspirate=100,dispense=150)
for i in range(2):
    multi_pipette.mix(repetitions=10,volume=50,location=sample_plate_posi.bottom(1))
    multi_pipette.blow_out()._position_for_aspirate()
    multi_pipette.blow_out()._position_for_aspirate()
multi_pipette.drop_tip().delay(minutes=1)


# engage magnet, aspirate supernatant to a pcr strip
mag_deck.engage(height=13)

multi_pipette.delay(minutes=2)
multi_pipette.pick_up_tip(presses=3, increment = 0.3)
for i in range(2):
    multi_pipette.transfer(80,sample_plate_posi.bottom(0),output_position.bottom(10),new_tip='never', blow_out=True)
multi_pipette.drop_tip()
