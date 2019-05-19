from opentrons import labware, instruments, modules

def load_deck(deck_plan='default',**kwarg):
    """
    load deck_plan. create global variables for loaded labwares.
    createa global variable deck_plan_: dictionary, slot number '1'/'2' : labware variable
    can use deck_plan_['1'] to refer to labware loaded on the deck.

    current deck plans:
    1).default : 1/3:elisa strip; 2:trough; 4:15-50ml rack; 5:ep rack; 9:trash"
    2).default-5ml : 1/3:elisa strip; 2:trough; *4:5ml-50ml rack*; 5:ep rack; 9:trash"
    3).default-mag : *1:magnet*; 2:trough; 3:elisa strip; 4:15-50ml rack; 5:ep rack; 9:trash'
    """
    global deck_plan_
    deck_plan_ = {}
    if deck_plan == 'default':
        global trough,liquid_trash,tip_rack,single_tip_rack,elisa_strip,ep_rack,tube_rack,multi_pipette,single_pipette,elisa_strip_2
        elisa_strip_2 = labware.load('elisa_strip','1')
        trough = labware.load('trough-12row', '2')
        liquid_trash = labware.load('trough-12row', '9')
        tip_rack = [labware.load('tiprack-200ul', slot) for slot in ['7','8']]
        single_tip_rack = [labware.load('tiprack-200ul',slot) for slot in ['10','11']]
        elisa_strip = labware.load('elisa_strip','3')
        ep_rack = labware.load('tube-rack-eppendorf','5')
        tube_rack = labware.load('tube-rack-15_50ml_apt','4')
        deck_plan_.update([('5',ep_rack),('4',tube_rack),('1',elisa_strip_2),('2',trough),('3',elisa_strip),('9',liquid_trash)])
        multi_pipette = instruments.P300_Multi(
                    mount='left',
                    tip_racks=tip_rack)
        single_pipette = instruments.P300_Single(
                    mount='right',
                    tip_racks=single_tip_rack)
    elif deck_plan == 'default-mag':
        kwarg['magnet']=True
        global mag_deck,mag_plate
        mag_deck = modules.load('magdeck', '1')
        mag_plate = labware.load('96strip_test','1',share = True)
        trough = labware.load('trough-12row', '2')
        liquid_trash = labware.load('trough-12row', '9')
        tip_rack = [labware.load('tiprack-200ul', slot) for slot in ['7','8']]
        single_tip_rack = [labware.load('tiprack-200ul',slot) for slot in ['10','11']]
        elisa_strip = labware.load('elisa_strip','3')
        ep_rack = labware.load('tube-rack-eppendorf','5')
        tube_rack = labware.load('tube-rack-15_50ml_apt','4')
        deck_plan_.update([('5',ep_rack),('4',tube_rack),('1',mag_plate),('2',trough),('3',elisa_strip),('9',liquid_trash)])
        multi_pipette = instruments.P300_Multi(
                    mount='left',
                    tip_racks=tip_rack)
        single_pipette = instruments.P300_Single(
                    mount='right',
                    tip_racks=single_tip_rack)
    elif deck_plan == 'default-5ml':
        global ep_tube_rack
        elisa_strip_2 = labware.load('elisa_strip','1')
        trough = labware.load('trough-12row', '2')
        liquid_trash = labware.load('trough-12row', '9')
        tip_rack = [labware.load('tiprack-200ul', slot) for slot in ['7','8']]
        single_tip_rack = [labware.load('tiprack-200ul',slot) for slot in ['10','11']]
        elisa_strip = labware.load('elisa_strip','3')
        ep_rack = labware.load('tube-rack-eppendorf','5')
        ep_tube_rack = labware.load('ep_5ml_tube_rack','4')
        deck_plan_.update([('5',ep_rack),('4',tube_rack),('1',elisa_strip_2),('2',trough),('3',elisa_strip),('9',liquid_trash)])
        multi_pipette = instruments.P300_Multi(
                    mount='left',
                    tip_racks=tip_rack)
        single_pipette = instruments.P300_Single(
                    mount='right',
                    tip_racks=single_tip_rack)

    else:
        pass

def calibrate_deck_single(deck_plan):
    """
    calibrate with single pipette
    """
    load_deck(deck_plan=deck_plan)
    single_pipette.pick_up_tip()
    for key,item in deck_plan_.items():
        single_pipette.move_to(item['A1'].top())
    single_pipette.drop_tip()

def calibrate_deck_multi(deck_plan):
    """
    calibrate with multi pipette
    """
    load_deck(deck_plan=deck_plan)
    single_pipette.pick_up_tip()
    for key,item in deck_plan_.items():
        single_pipette.move_to(item['A1'].top())
    single_pipette.drop_tip()

calibrate_deck_single('default')
