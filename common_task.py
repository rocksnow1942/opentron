"""
common_task note
steps: initialize(magnet=False) - load_deck(deck_plan='default') : this will create global variables to use for pipettes and labwares on the deck.
then run tasks.
"""

from time import time
tip_press_increment=0.4
tip_presses = 3

global tube_vol,deck_plan_,execution_time
tube_vol = {}
deck_plan_ = {}
execution_time = time()
"""
tube_vol dictionary use position labels '1-A1' or '1-2' as key.
store corresponding labware_volume class instance, initialized with starting volume, keep track of volume changes.
"""


def initialize(magnet=False,**kwarg):
    """
    connect, reset and home robot. create robot variables to use.
    initialize is already built into load_deck(deck_plan).
    don't need to specifically use initialize.
    """
    from opentrons import labware, instruments, robot, modules
    import sys
    sys.path.append("/data/user_storage/opentrons_data/jupyter/modules_storage")
    import labware_volume as lv
    global robot, labware, instruments, modules, lv
    robot, labware, instruments, modules, lv = robot, labware, instruments, modules, lv
    robot.connect()
    robot.reset()
    if magnet:
        for module in robot.modules:
            module.disconnect()
        robot.modules = modules.discover_and_connect()

def load_deck(deck_plan='default',**kwarg):
    """
    load deck_plan. create global variables for loaded labwares.
    createa global variable deck_plan_: dictionary, slot number '1'/'2' : labware variable
    can use deck_plan_['1'] to refer to labware loaded on the deck.

    current deck plans:
    1).default : 1/3:elisa strip; 2:trough; 4:15-50ml rack; 5:ep rack; 9:trash"
    2).default-1ml-plate 1.1mlPPplate 3:elisa strip; 2:trough; 4:15-50ml rack; 5:ep rack; 9:trash"
    2).default-5ml : 1/3:elisa strip; 2:trough; *4:5ml-50ml rack*; 5:ep rack; 9:trash"
    3).default-mag : *1:magnet*; 2:trough; 3:elisa strip; 4:15-50ml rack; 5:ep rack; 9:trash'
    """
    global trough,liquid_trash,tip_rack,single_tip_rack,elisa_strip,ep_rack,tube_rack,multi_pipette,single_pipette,elisa_strip_2
    if deck_plan == 'default':
        # global trough,liquid_trash,tip_rack,single_tip_rack,elisa_strip,ep_rack,tube_rack,multi_pipette,single_pipette,elisa_strip_2
        initialize(**kwarg)
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
    elif deck_plan == 'default-1ml-plate':
        # global trough,liquid_trash,tip_rack,single_tip_rack,elisa_strip,ep_rack,tube_rack,multi_pipette,single_pipette,elisa_strip_2
        initialize(**kwarg)
        pp_plate = labware.load('ams_1ml_pp_plate','1')
        trough = labware.load('trough-12row', '2')
        liquid_trash = labware.load('trough-12row', '9')
        tip_rack = [labware.load('tiprack-200ul', slot) for slot in ['7','8']]
        single_tip_rack = [labware.load('tiprack-200ul',slot) for slot in ['10','11']]
        elisa_strip = labware.load('elisa_strip','3')
        ep_rack = labware.load('tube-rack-eppendorf','5')
        tube_rack = labware.load('tube-rack-15_50ml_apt','4')
        deck_plan_.update([('5',ep_rack),('4',tube_rack),('1',pp_plate),('2',trough),('3',elisa_strip),('9',liquid_trash)])
        multi_pipette = instruments.P300_Multi(
                    mount='left',
                    tip_racks=tip_rack)
        single_pipette = instruments.P300_Single(
                    mount='right',
                    tip_racks=single_tip_rack)
    elif deck_plan == 'default-mag':
        kwarg['magnet']=True
        initialize(**kwarg)
        global mag_deck,mag_plate,elisa_strip_3,elisa_strip_4
        mag_deck = modules.load('magdeck', '4')
        mag_plate = labware.load('pp_plate_mag','4',share = True)
        trough = labware.load('trough-12row', '2')
        liquid_trash = labware.load('trough-12row', '9')
        tip_rack = [labware.load('tiprack-200ul', slot) for slot in ['7','8']]
        single_tip_rack = [labware.load('tiprack-200ul',slot) for slot in ['10','11']]
        elisa_strip = labware.load('elisa_strip','3')
        elisa_strip_2 = labware.load('elisa_strip','1')
        elisa_strip_3 = labware.load('elisa_strip','5')
        elisa_strip_4 = labware.load('elisa_strip','6')
        # ep_rack = labware.load('tube-rack-eppendorf','5')
        # tube_rack = labware.load('tube-rack-15_50ml_apt','4')
        deck_plan_.update([('5',elisa_strip_3),('1',elisa_strip_2),('4',mag_plate),('2',trough),('6',elisa_strip_4),('3',elisa_strip),('9',liquid_trash)])
        multi_pipette = instruments.P300_Multi(
                    mount='left',
                    tip_racks=tip_rack)
        single_pipette = instruments.P300_Single(
                    mount='right',
                    tip_racks=single_tip_rack)
    elif deck_plan == 'default-5ml':
        initialize(**kwarg)
        elisa_strip_2 = labware.load('elisa_strip','1')
        trough = labware.load('trough-12row', '2')
        liquid_trash = labware.load('trough-12row', '9')
        tip_rack = [labware.load('tiprack-200ul', slot) for slot in ['7','8']]
        single_tip_rack = [labware.load('tiprack-200ul',slot) for slot in ['10','11']]
        elisa_strip = labware.load('elisa_strip','3')
        ep_rack = labware.load('tube-rack-eppendorf','5')
        tube_rack = labware.load('ep_5ml_tube_rack','4')
        deck_plan_.update([('5',ep_rack),('4',tube_rack),('1',elisa_strip_2),('2',trough),('3',elisa_strip),('9',liquid_trash)])
        multi_pipette = instruments.P300_Multi(
                    mount='left',
                    tip_racks=tip_rack)
        single_pipette = instruments.P300_Single(
                    mount='right',
                    tip_racks=single_tip_rack)

    else:
        pass

def initialize_tip(single_tip_starting_position='A1',multi_tip_starting_position='A1',**kwarg):
    """
    initialize tip position.
    """
    if not isinstance(tip_rack,list):
        load_deck(**kwarg)
    single_pipette.start_at_tip(single_tip_rack[0].wells(single_tip_starting_position))
    multi_pipette.start_at_tip(tip_rack[0].cols(multi_tip_starting_position[1:]))

def str_to_list(source):
    """
    parse well slice syntax to a list of wells for access.
    slice syntax : 1-3 ; 1-A1 ; 1-A2:C5 ; 1-C5:A2 ; 1-1:5 ; 1-5:1
    use number before - to indicate deck slot.
    letter after - label wells. 3 or 3:6 means columns 3 or 3 to 6 for multipipette access.
    A1 or A2:C5 means well A1 or the matrix sliced by A2 and C5.
    the function parse the syntax and returns:
    1). list of labels for the individual well or column location, i.e. '1-C5', '1-3'
    2). list of well or column notation robot API can use, i.e. 'A4', '3'

    for example:
    str_to_list(1-1:2) -> (['1-1', '1-2'], ['1', '2'])
    str_to_list(1-A1:B2) -> (['1-A1', '1-A2', '1-B1', '1-B2'], ['A1', 'A2', 'B1', 'B2'])
    """
    alphabet = 'ABCDEFGHIJKLMN'
    if ':' in source:
        output = []
        label = []
        start,end = source[2:].split(':')
        if start[0] in alphabet:
            row_start = alphabet.index(start[0])
            row_end = alphabet.index(end[0])
            col_start = int(start[1:])
            col_end = int(end[1:])
            reverse = False
            if row_start > row_end or col_start > col_end:
                row_start = row_end + row_start
                row_end = row_start - row_end
                row_start = row_start - row_end
                col_start = col_end + col_start
                col_end = col_start - col_end
                col_start = col_start - col_end
                reverse = True
            for r in alphabet[row_start:row_end+1]:
                for c in range(col_start,col_end+1):
                    output.append(r+str(c))
                    label.append(source[0:2]+r+str(c))
            if reverse:
                label.reverse()
                output.reverse()
        else:
            if int(start) < int(end):
                output.extend((str(i) for i in range(int(start),int(end)+1)))
                label.extend(source[0:2]+i for i in output)
            else:
                output.extend((str(i) for i in range(int(start),int(end)-1,-1)))
                label.extend(source[0:2]+i for i in output)
        return label,output
    else:
        return [source],[source[2:]]

def lab_deck_parser(source):
    """
    use well slice syntax to prepare labels/labware_volume class/labware instance for use.
    source will be a string like: "3-A1" or '1-A1:C5' or '1-3:10' or '1-C5:B2'
    3,5 is the slot name, A1,A2 is the well label.
    function return a [list] of
    [ label ('1-B2', '3-2') ],
    [ labware_volume class ( lv.Tube_15ml ) ]
    [ labware instance (elisa_strip['A1'] or elisa_strip.cols('3')) ]
    """
    alphabet = 'ABCDEFGHIJKLMN'
    posi = source[0]
    labware_ = deck_plan_[posi]
    label, well = str_to_list(source)
    if well[0][0] in alphabet:
        labware = [labware_[i] for i in well]
    else:
        labware = [labware_.cols(i) for i in well]
    name = labware_.get_name()
    lab_vol = []
    for i in label:
        if name == 'tube-rack-eppendorf':
            lab_vol.append(lv.eppendorf_2ml_depth)
        elif name == 'tube-rack-15_50ml_apt':
            if source[-1] in ['3','4']:
                lab_vol.append(lv.Tube_50ml_depth)
            else:
                lab_vol.append(lv.Tube_15ml)
        elif name == 'ep_5ml_tube_rack':
            if source[-1] in ['3','4']:
                lab_vol.append(lv.Tube_50ml_depth)
            else:
                lab_vol.append(lv.eppendorf_5ml)
        elif name == 'trough-12row':
            lab_vol.append(lv.Trough_12)
        elif name =='ams_1ml_pp_plate':
            lab_vol.append(lv.ams_1ml_pp_plate)
        else:
            lab_vol.append(lv.elisa_well)
        # else:
        #     lab_vol.append(None)
    return label,lab_vol,labware

def initialize_volume(source, source_vol):
    """
    take well slice syntax and volume or a list of them with equal length; update corresponding labware spot in the tube_vol dictionary.
    soure format: "3-A1" or '1-A1:C5' or '1-3:10' or '1-C5:B2'
    source_vol format: '100ul' or '1ml'; case insensitive.
    source and source can be single element or list of element.
    """
    if isinstance(source,str):
        source = [source]
        source_vol = [source_vol]
    for key,vol in zip(source,source_vol):
        label,lab_vol,labware = lab_deck_parser(key)
        for l,ll,lw in zip(label,lab_vol,labware):
            if l not in tube_vol.keys():
                tube_vol[l] = ll(volume=vol,labware=lw)

def multi_distribute_liquid(volume=0,source=None,target=None,source_vol='0ul',target_vol=0,aspirate_offset=-1,dispense_offset=5,aspirate_speed=150,dispense_speed=150,pick_tip=True,tip_location=None,reuse_tip=False,remove_residual=False,**kwarg):
    """
    distribute liquid from location a to b with multi pipette. Will not change tip unless using [].
    volume / source / target / source_vol / target_vol should be single or list of equal length.
    volume : float or list, volume to distribute in ul
    source : str or list, well slice syntax
    target : str or list, well slice syntax
        * one of source/target should have only 1 column or source/target have same number of columns.
        * if source has 1 column, distribute from source to all columns of target.
        * if target has 1 column, distribute all source columns to same target column.
        * if target cols # = source cols #, distribute from each col of source to target respectively.
    source_vol : str or list, '100ul' or '10ml'
    target_vol : float or list, volume of liquid in target location in ul
    aspirate_offset, dispense_offset: float, distance in mm of the tip position relative to liquid surface.
    aspirate_speed,dispense_speed: float, speed of pipette in ul/s
    """
    global execution_time
    execution_time = time()
    if not isinstance(target, list):
        initialize_volume(source,source_vol)
        if target.lower() == 'trash':
            target = '9-A6'
            target_vol = 20000
            dispense_offset = 0
        initialize_volume(target,str(target_vol)+'ul')
        multi_pipette.set_flow_rate(aspirate=aspirate_speed,dispense=dispense_speed)
        if pick_tip:
            multi_pipette.pick_up_tip(presses=tip_presses, increment=tip_press_increment,location=tip_location)
        source_label,_,source = lab_deck_parser(source)
        target_label,_,target = lab_deck_parser(target)
        if len(source_label) == 1:
            source_label = source_label * len(target_label)
        if len(target_label) == 1:
            target_label = target_label * len(source_label)
        for a,b in zip(source_label,target_label):
            multi_pipette.transfer(volume, tube_vol[a].surface(-volume,aspirate_offset), tube_vol[b].surface(volume,dispense_offset), new_tip='never')
            multi_pipette.blow_out()._position_for_aspirate()
            multi_pipette.delay(seconds=1).blow_out()._position_for_aspirate()
            if remove_residual:
                multi_pipette.transfer(volume, tube_vol[a].surface(-volume,-10), tube_vol[b].surface(volume,dispense_offset), new_tip='never')
                multi_pipette.blow_out()._position_for_aspirate()
                multi_pipette.delay(seconds=1).blow_out()._position_for_aspirate()

        current_tip_location = multi_pipette.current_tip()
        if reuse_tip:
            multi_pipette.return_tip()
        else:
            multi_pipette.drop_tip()
    else:
        for v,s,sv,t,tv in zip(volume,source,source_vol,target,target_vol):
            multi_distribute_liquid(volume=v,source=s,source_vol=sv,target=t,target_vol=tv,aspirate_offset=aspirate_offset, dispense_offset=dispense_offset,aspirate_speed=aspirate_speed,dispense_speed=dispense_speed,**kwarg)
    return current_tip_location


def single_distribute_liquid(volume=0,source=None,target=None,source_vol='0ul',target_vol = 0,aspirate_offset=-1,dispense_offset=5,aspirate_speed=150,dispense_speed=150,**kwarg):
    """
    distribute liquid from location a to b with single pipette. Will change tip every time if distributing from different source tube.
    volume / source / target / source_vol / target_vol should be single or list of equal length.
    volume : float or list, volume to distribute in ul
    source : str or list, well slice syntax
    target : str or list, well slice syntax
        * one of source/target should have only 1 well or source/target have same number of wells.
        * if source has 1 well, distribute from source to all wells of target.
        * if target has 1 well, distribute all source wells to same target well.
        * if target well # = source well #, distribute from each well of source to target respectively.
    source_vol : str or list, '100ul' or '10ml'
    target_vol : float or list, volume of liquid in target location in ul
    aspirate_offset, dispense_offset: float, distance in mm of the tip position relative to liquid surface.
    aspirate_speed,dispense_speed: float, speed of pipette in ul/s
    """
    global execution_time
    execution_time = time()
    if not isinstance(target, list):
        initialize_volume(source,source_vol)
        if target.lower() == 'trash':
            target = '9-A6'
            target_vol = 20000
            dispense_offset = 0
        initialize_volume(target,str(target_vol)+'ul')
        single_pipette.set_flow_rate(aspirate=aspirate_speed,dispense=dispense_speed)
        source_label,_,source = lab_deck_parser(source)
        target_label,_,target = lab_deck_parser(target)
        if len(source_label) == 1:
            single_pipette.pick_up_tip(presses=tip_presses, increment=tip_press_increment)
            for b in target_label:
                single_pipette.transfer(volume, tube_vol[source_label[0]].surface(-volume,aspirate_offset), tube_vol[b].surface(volume,dispense_offset), new_tip='never')
                single_pipette.blow_out()._position_for_aspirate()
                single_pipette.delay(seconds=0.5).blow_out()._position_for_aspirate()
            single_pipette.drop_tip()
        else:
            if len(target_label) == 1:
                target_label = target_label * len(source_label)
            for a,b in zip(source_label,target_label):
                single_pipette.pick_up_tip(presses=tip_presses, increment=tip_press_increment)
                single_pipette.transfer(volume, tube_vol[a].surface(-volume,aspirate_offset), tube_vol[b].surface(volume,dispense_offset),new_tip='never')
                single_pipette.blow_out()._position_for_aspirate()
                single_pipette.delay(seconds=0.5).blow_out()._position_for_aspirate()
                single_pipette.drop_tip()
    else:
        for v,s,sv,t,tv in zip(volume,source,source_vol,target,target_vol):
            single_distribute_liquid(volume=v,source=s,source_vol=sv,target=t,target_vol=tv,aspirate_offset=aspirate_offset, dispense_offset=dispense_offset,aspirate_speed=aspirate_speed,dispense_speed=dispense_speed,**kwarg)


def multi_serial_dilution(volume=0,position=None,dilution_factor=1,aspirate_offset=-1,aspirate_speed=150,dispense_speed=150,mix_no=5,keep_waste=False,**kwarg):
    """
    perform serial dilution with multi pipette.
    volume / position / dilution_factor should be single or list of equal length.
    volume : float or list, final liquid volume in each well after serial dilution in ul
    position : str or list, well slice syntax, the start to end of the dilution series (all will have the solute)
    dilution_factor : float or list, the nearest concentration ratio of the dilution series, high/low.
    aspirate_offset : float, distance of the aspirate position relative to liquid surface.
    aspirate_speed,dispense_speed: float, speed of pipette in ul/s
    mix_no : int, how many times to mix.
    """
    global execution_time
    execution_time = time()
    if not isinstance(volume,list):
        trans_vol = volume/(dilution_factor-1)
        total_vol = volume + trans_vol
        mix_volume = min(total_vol/2,300)
        label,_,labware = lab_deck_parser(position)
        dispense_offset = _[0].volume_to_depth(_[0],volume*0.75) - _[0].volume_to_depth(_[0],total_vol)
        initialize_volume(label[0],str(total_vol)+'ul')
        initialize_volume(position,str(volume)+'ul')
        multi_pipette.set_flow_rate(aspirate=aspirate_speed,dispense=dispense_speed)
        multi_pipette.pick_up_tip(presses=tip_presses,increment=tip_press_increment)
        for i in range(len(label)-1):
            multi_pipette.transfer(trans_vol,tube_vol[label[i]].surface(-trans_vol,aspirate_offset),tube_vol[label[i+1]].surface(trans_vol,dispense_offset),new_tip='never',mix_after=(int(mix_no),mix_volume))
            multi_pipette.move_to(tube_vol[label[i+1]].surface(0,4))
            multi_pipette.blow_out().delay(seconds=1)._position_for_aspirate()
            multi_pipette.blow_out().delay(seconds=1)._position_for_aspirate()
        if not keep_waste:
            multi_pipette.transfer(trans_vol,tube_vol[label[-1]].surface(-trans_vol,aspirate_offset),liquid_trash['A5'].bottom(20),new_tip='never')
        multi_pipette.drop_tip()
    else:
        for v,p,d in zip(volume,position,dilution_factor):
            multi_serial_dilution(volume=v,position=p,dilution_factor=d,aspirate_offset=aspirate_offset,aspirate_speed=aspirate_speed,dispense_speed=dispense_speed,mix_no=mix_no,keep_waste=keep_waste,**kwarg)


def single_serial_dilution(volume=0,position=None,dilution_factor=1,aspirate_offset=-1,aspirate_speed=150,dispense_speed=150,mix_no=5,keep_waste=False,**kwarg):
    """
    perform serial dilution with single pipette.
    volume / position / dilution_factor should be single or list of equal length.
    volume : float or list, final liquid volume in each well after serial dilution in ul
    position : str or list, well slice syntax, the start to end of the dilution series (all will have the solute)
    dilution_factor : float or list, the nearest concentration ratio of the dilution series, high/low.
    aspirate_offset : float, distance of the aspirate position relative to liquid surface.
    aspirate_speed,dispense_speed: float, speed of pipette in ul/s
    mix_no : int, how many times to mix.
    """
    global execution_time
    execution_time = time()
    if not isinstance(volume,list):
        trans_vol = volume/(dilution_factor-1)
        total_vol = volume + trans_vol
        mix_volume = min(total_vol/2,300)
        label,_,labware = lab_deck_parser(position)
        dispense_offset = _[0].volume_to_depth(_[0],volume*0.75) - _[0].volume_to_depth(_[0],total_vol)
        initialize_volume(label[0],str(total_vol)+'ul')
        initialize_volume(position,str(volume)+'ul')
        single_pipette.set_flow_rate(aspirate=aspirate_speed,dispense=dispense_speed)
        single_pipette.pick_up_tip(presses=tip_presses,increment=tip_press_increment)
        for i in range(len(label)-1):
            single_pipette.transfer(trans_vol,tube_vol[label[i]].surface(-trans_vol,aspirate_offset),tube_vol[label[i+1]].surface(trans_vol,dispense_offset),new_tip='never',mix_after=(int(mix_no),mix_volume))
            single_pipette.move_to(tube_vol[label[i+1]].surface(0,4))
            single_pipette.blow_out().delay(seconds=1)._position_for_aspirate()
            single_pipette.blow_out().delay(seconds=1)._position_for_aspirate()
        if not keep_waste:
            single_pipette.transfer(trans_vol,tube_vol[label[-1]].surface(-trans_vol,aspirate_offset),liquid_trash['D5'].bottom(20),new_tip='never')
        single_pipette.drop_tip()
    else:
        for v,p,d in zip(volume,position,dilution_factor):
            single_serial_dilution(volume=v,position=p,dilution_factor=d,aspirate_offset=aspirate_offset,aspirate_speed=aspirate_speed,dispense_speed=dispense_speed,mix_no=mix_no,keep_waste=keep_waste,**kwarg)


def multi_mix(position=None,volume=100,mix_no=5,tip_location=None,drop_tip=True,change_tip=False,aspirate_speed=150,dispense_speed=150):
    """
    use multi pipette to mix liquid.
    position : str or list, well slice syntax or list of position
    volume : folat or list, liquid volume in the well in ul or list of volume
    mix_no : int, how many times to pipette
    change_tip: boolean, False use the same tip, True change tip after each mix.
    """
    global execution_time
    execution_time = time()
    multi_pipette.set_flow_rate(aspirate=aspirate_speed,dispense=dispense_speed)
    if not isinstance(position, list):
        label,_,labware=lab_deck_parser(position)
        initialize_volume(position,str(volume)+'ul')
        volume = min(600,volume)
        if not change_tip:
            multi_pipette.pick_up_tip(presses=tip_presses,increment=tip_press_increment,location=tip_location)
            for i in label:
                multi_pipette.mix(repetitions=int(mix_no),volume=volume/2,location=tube_vol[i].surface(-volume*0.75,0))
                multi_pipette.move_to(tube_vol[i].surface(volume*0.75,5)).delay(seconds=1)
                multi_pipette.blow_out().delay(seconds=0.5)._position_for_aspirate()
                multi_pipette.blow_out().delay(seconds=0.5)._position_for_aspirate()
            if drop_tip:
                multi_pipette.drop_tip()
        else:
            for i in label:
                multi_pipette.pick_up_tip(presses=tip_presses,increment=tip_press_increment)
                multi_pipette.mix(repetitions=mix_no,volume=volume/2,location=tube_vol[i].surface(-volume*0.75,0))
                multi_pipette.move_to(tube_vol[i].surface(volume*0.75,5)).delay(seconds=1)
                multi_pipette.blow_out().delay(seconds=0.5)._position_for_aspirate()
                multi_pipette.blow_out().delay(seconds=0.5)._position_for_aspirate()
                multi_pipette.drop_tip()
    else:
        for p,v in zip(position,volume):
            multi_mix(position=p,volume=v,mix_no=mix_no,change_tip=change_tip)


def single_mix(position=None,volume=100,mix_no=5,change_tip=False,aspirate_speed=150,dispense_speed=150):
    """
    use single pipette to mix liquid.
    position : str or list, well slice syntax or list of position
    volume : folat or list, liquid volume in the well in ul or list of volume
    mix_no : int, how many times to pipette
    change_tip: boolean, False use the same tip, True change tip after each mix.
    """
    global execution_time
    execution_time = time()
    single_pipette.set_flow_rate(aspirate=aspirate_speed,dispense=dispense_speed)
    if not isinstance(position, list):
        label,_,labware=lab_deck_parser(position)
        initialize_volume(position,str(volume)+'ul')
        if not change_tip:
            single_pipette.pick_up_tip(presses=tip_presses,increment=tip_press_increment)
            for i in label:
                single_pipette.mix(repetitions=mix_no,volume=min(volume/2,300),location=tube_vol[i].surface(-volume*0.75,0))
                single_pipette.move_to(tube_vol[i].surface(volume*0.75,5)).delay(seconds=1)
                single_pipette.blow_out().delay(seconds=0.5)._position_for_aspirate()
                single_pipette.blow_out().delay(seconds=0.5)._position_for_aspirate()
            single_pipette.drop_tip()
        else:
            for i in label:
                single_pipette.pick_up_tip(presses=tip_presses,increment=tip_press_increment)
                single_pipette.mix(repetitions=int(mix_no),volume=min(volume/2,300),location=tube_vol[i].surface(-volume*0.75,0))
                single_pipette.move_to(tube_vol[i].surface(volume*0.75,5)).delay(seconds=1)
                single_pipette.blow_out().delay(seconds=0.5)._position_for_aspirate()
                single_pipette.blow_out().delay(seconds=0.5)._position_for_aspirate()
                single_pipette.drop_tip()
    else:
        for p,v in zip(position,volume):
            single_mix(position=p,volume=v,mix_no=mix_no,change_tip=change_tip)


def toggle_mag(operation=False,height=13.3):
    """
    engage or disengage magnet
    operation : boolean, True, engage, False, disengage
    height: float, magnet height in mm when engaged.
    """
    if operation==True:
        mag_deck.engage(height=height)
    else:
        mag_deck.disengage()

def on_hold(time=60):
    """
    pause the robot for a few seconds
    time: float, time in seconds
    """
    multi_pipette.delay(seconds=time)

def wait_for(delay=60):
    global execution_time
    currenttime = time()
    multi_pipette.delay(seconds = max(1, delay - (currenttime-execution_time)))

def mag_wash(wash_location=None,buffer_location=None,buffer_vol='5ml',wash_vol= 150,wash_no=3, mix_no=5, mag_height=13.3, mag_time=60, **kwarg):
    wash_no=int(wash_no)
    mix_no=int(mix_no)
    initialize_volume(wash_location,'100ul')
    initialize_volume(buffer_location,buffer_vol)
    mag_deck.engage(height=mag_height)
    multi_pipette.delay(seconds=mag_time)
    multi_distribute_liquid(volume=150,source=wash_location,target='trash',remove_residual=True)
    mag_deck.disengage()
    buffer_tip=None
    wash_round=int(wash_no/3)
    for j in range(wash_round+1):
        wash_tip=None
        if j < wash_round:
            step_repeat = 3
        else:
            step_repeat = wash_no % 3
        for i in range(step_repeat):
            print('step is {}'.format(1+j*3+i))
            if j*3+i+1==wash_no:
                buffer_tip=multi_distribute_liquid(volume=wash_vol,source=buffer_location,target=wash_location,reuse_tip=False,tip_location=buffer_tip)
            else:
                buffer_tip=multi_distribute_liquid(volume=wash_vol,source=buffer_location,target=wash_location,reuse_tip=True,tip_location=buffer_tip)
            multi_mix(position=wash_location,mix_no=mix_no,drop_tip=False,tip_location=wash_tip)
            mag_deck.engage(height=mag_height)
            multi_pipette.delay(seconds=mag_time)
            if i < step_repeat-1:
                wash_tip = multi_distribute_liquid(volume=wash_vol,source=wash_location,target='trash',pick_tip=False,remove_residual=True,reuse_tip=True)
            else:
                wash_tip = multi_distribute_liquid(volume=wash_vol,source=wash_location,target='trash',pick_tip=False,remove_residual=True,reuse_tip=False)
            mag_deck.disengage()


def mag_wash_v2(wash_location=None,buffer_location=None,buffer_vol='5ml',wash_vol= 150,wash_no=3, mix_no=5, mag_height=13.3, mag_time=60, **kwarg):
    wash_no=int(wash_no)
    mix_no=int(mix_no)
    initialize_volume(wash_location,'100ul')
    initialize_volume(buffer_location,buffer_vol)
    mag_deck.engage(height=mag_height)
    multi_pipette.delay(seconds=mag_time)
    multi_distribute_liquid(volume=150,source=wash_location,target='trash',remove_residual=True)
    mag_deck.disengage()
    wash_round=int(wash_no/3)
    for j in range(wash_round+1):
        buffer_tip=None
        wash_tip=None
        if j < wash_round:
            step_repeat = 3
        else:
            step_repeat = wash_no % 3
        for i in range(step_repeat):
            print('step is {}'.format(1+j*3+i))
            if i < step_repeat-1:
                buffer_tip=multi_distribute_liquid(volume=wash_vol,source=buffer_location,target=wash_location,reuse_tip=True,tip_location=buffer_tip)
            else:
                buffer_tip=multi_distribute_liquid(volume=wash_vol,source=buffer_location,target=wash_location,reuse_tip=False,tip_location=buffer_tip)
            multi_mix(position=wash_location,mix_no=mix_no,drop_tip=False,tip_location=wash_tip)
            mag_deck.engage(height=mag_height)
            multi_pipette.delay(seconds=mag_time)
            if i < step_repeat-1:
                wash_tip = multi_distribute_liquid(volume=wash_vol,source=wash_location,target='trash',pick_tip=False,remove_residual=True,reuse_tip=True)
            else:
                wash_tip = multi_distribute_liquid(volume=wash_vol,source=wash_location,target='trash',pick_tip=False,remove_residual=True,reuse_tip=False)
            mag_deck.disengage()
