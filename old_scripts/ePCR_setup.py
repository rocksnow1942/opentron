from opentrons import labware, instruments


mag_plate = labware.load('96strip_test','1',share = True)


liquid_trash = labware.load('trough-12row', '6')


ep_rack = labware.load('tube-rack-eppendorf','5')
tube_rack = labware.load('tube-rack-15_50ml_apt','4')

trough = labware.load('trough-12row', '2')
pcr_strip = labware.load('pcr_strip_on_magnet', '3')
tip_rack = [labware.load('tiprack-200ul', slot) for slot in ['7', '8']]
single_tip_rack = [labware.load('tiprack-200ul',slot) for slot in ['10','11']]


multi_pipette = instruments.P300_Multi(
            mount='left',
            tip_racks=tip_rack)


def make_epcr_mix(**kwarg):
    """
    need atleast 2 columns of tips.
    need 4ml epcr oil in trough.
    Keyword arguments:
    epcr_oil_position : the well number of epcr oil in trough [A1-A12]
    starting_tip_position : the starting tip position, should be [A1-A12]
    """
    # Todos:
    # 1.add pcr mix volume/epcr strip number as kwarg
    # 2.optimize epcr oil volume
    # 3.optimize epcr mix making method: instead of random, use a fixed list of position.
    #
    #

    # input for ePCR oil position in the trough
    epcr_oil = trough[kwarg['epcr_oil_position']]
    starting_tip_position = kwarg['starting_tip_position']
    #epcr_oil_volume = '1ml' # need to optimize in future
    multi_pipette.start_at_tip(tip_rack[0].cols(starting_tip_position[1:]))

    # transfer ePCR oil from trough to PCR strips
    # trough width 8mm, width 72mm. each 960ul volume, liquid go down by 1.67 mm
    # for pcr tube, 120ul oil is ~10mm from bottom
    multi_pipette.pick_up_tip()
    for strip_no, oil_depth in zip(pcr_strip.cols('4', '7', '10'), [5, 3.34, 1.67]):
        multi_pipette.set_flow_rate(aspirate=15, dispense=15)
        multi_pipette.move_to(epcr_oil.bottom(oil_depth)).aspirate(120)
        multi_pipette.move_to(strip_no.bottom(10))
        # multi_pipette.robot.gantry.push_speed()
        # multi_pipette.robot.gantry.set_speed(20)
        # multi_pipette.move_to((strip_no,strip_no.from_center(x=1,y=0,z=0.6)),strategy='direct')
        # multi_pipette.robot.gantry.pop_speed()
        multi_pipette.dispense(120)
        multi_pipette.set_flow_rate(aspirate=600, dispense=20)
        multi_pipette.aspirate(300).delay(seconds=3)
        multi_pipette.dispense(300)
        multi_pipette.blow_out()._position_for_aspirate()
    multi_pipette.set_flow_rate(aspirate=150, dispense=150)
    multi_pipette.drop_tip()

    # transfer PCR mix to oil
    # pcr tube 66ul - 6.64mm, 10.77mm, 13.44mm
    # location=tip_rack['A'+str(int(starting_tip_position[1])+1)],presses=3,increment=1
    multi_pipette.pick_up_tip()
    multi_pipette.set_flow_rate(aspirate=100, dispense=100)
    for i, j in zip(['4', '7', '10', '10'], [9.77, 5.6, 1, 0.1]):
        multi_pipette.move_to(pcr_strip.cols('1').bottom(j))
        multi_pipette.aspirate(volume=66)
        multi_pipette.delay(seconds=0.5)
        multi_pipette.move_to(pcr_strip.cols(i).top(-5))
        multi_pipette.dispense(66)
        multi_pipette.blow_out()._position_for_aspirate()

    # make e mix with same tip; after each mix, return tip then re-pick up
    import random
    random.seed(42)
    for strip_no in ['4', '7', '10']:  # "4",'7','10'
        current_tip = multi_pipette.current_tip()
        multi_pipette.return_tip()
        multi_pipette.pick_up_tip(location=current_tip)
        multi_pipette.set_flow_rate(aspirate=300, dispense=400)
        multi_pipette.move_to(pcr_strip.cols(strip_no).bottom(1))
        for i in range(80):
            a = random.random() * 4 + 1
            b = random.random() * 4 + 1
            multi_pipette.aspirate(150)
            multi_pipette.delay(seconds=0.5)
            multi_pipette.move_to(pcr_strip.cols(strip_no).bottom(a))
            multi_pipette.dispense(150)
            multi_pipette.delay(seconds=0.5)
            multi_pipette.move_to(pcr_strip.cols(strip_no).bottom(b))
        multi_pipette.move_to(pcr_strip.cols(strip_no).top(-5))
        multi_pipette.set_flow_rate(aspirate=600, dispense=10)
        for a in range(3):
            multi_pipette.aspirate(300)
            multi_pipette.dispense(300)
        multi_pipette.robot.gantry.push_speed()
        multi_pipette.robot.gantry.set_speed(20)
        multi_pipette.move_to((pcr_strip.cols(strip_no), pcr_strip.cols(
            strip_no).from_center(x=0.8, y=0, z=0.6)), strategy='direct')
        multi_pipette.robot.gantry.pop_speed()
    multi_pipette.set_flow_rate(aspirate=150, dispense=300)
    multi_pipette.drop_tip()
    return multi_pipette


make_epcr_mix(epcr_oil_position='A10', starting_tip_position='A2')

# # return all liquid to '1'
# for i in ['4','7','10']:
#     multi_pipette.move_to(pcr_strip.cols(i).bottom(0.2))
#     multi_pipette.aspirate(volume=100)
#     multi_pipette.move_to(pcr_strip.cols('1').top(-4))
#     multi_pipette.dispense(100)

# making ePCR mix

#
# import random
# for well_no in range(4):
#     single_pipette.pick_up_tip()
#     single_pipette.set_flow_rate(aspirate=300, dispense=400)
#     single_pipette.transfer(50,trough['A1'],plate.wells(well_no),new_tip='never')
#     random.seed(42)
#     for a in range(50):
#         single_pipette.aspirate(170)
#         single_pipette.delay(seconds=1)
#         single_pipette.dispense(170)
#         single_pipette.delay(seconds=1)
#         a =  random.randint(1,4)
#         single_pipette.move_to(plate.wells(well_no).bottom(a))
#         print(a)
#     single_pipette.touch_tip(location=plate.wells(well_no), radius=0.6, v_offset=-52.0, speed=20.0)
#     single_pipette.set_flow_rate(aspirate=600, dispense=10)
#     for a in range(2):
#         single_pipette.aspirate(300)
#         single_pipette.dispense(300)
#     single_pipette.drop_tip()
