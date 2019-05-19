import ast,json,glob,os,re
import sys
# sys.path.append("/data/user_storage/opentrons_data/jupyter/modules_storage")
import common_task as ct

# save_path is the location to store saved protocols.
# save_path = '/data/user_storage/opentrons_data/jupyter/saved_protocols'
save_path = '/Users/hui/Scripts/!misc/opentron_scripts/custom_script/saved_protocol'
save_path_len = len(save_path)+1

"""
UI note:

print_available_operations()
         |
build_operation_para - capture_input - para_fetcher/lp
         | - execute_plan
         | - save_plan - execute_plan
                |
       choose_saved_protocol - read_saved_protocol - execute_plan
"""

def build_operation_para():
    """
    Start of create a protocol. Will return a dict contain protocol steps and step name and step parameters.
    format : {'0-1':{'name': 'step name', 'parameter': {kwargs for common_task functions}}}
    """
    print("Deck plan options: ")
    print_deck_plans()
    try:
        pick = int(input("Pick a deck plan to use (1,2,3) : ")) - 1
    except:
        print('Type error, choose default instead.')
        pick = 1
    deckplan_list = ['default','default-1ml-plate','default-5ml','default-mag','']
    operation_para = {}
    operation_para['0-1'] = {'name':'initialize_deck'}
    operation_para['0-1']['parameter'] = {'deck_plan':deckplan_list[pick]}
    print('+'*50)
    st = lp_input('s',("Single tip start position (*A1, C5) : "))
    mt = lp_input('s',('Multi tip start position (*A4, A2) : '))
    operation_para['0-2'] = {'name':'initialize_tip'}
    operation_para['0-2']['parameter'] = {'single_tip_starting_position':st,'multi_tip_starting_position':mt}
    print('+'*50)
    print('Build your experiment procedures: ')
    print('+'*50+'\n')
    print_available_operations()
    print('\n'+'+'*50+'\n')
    step_no = 1
    while 1:
        yes_or_no = input("Add step [ {} ]? y/n :  ".format(step_no))
        if yes_or_no == 'y':
            re_run_step = 1
            while re_run_step:
                got_input = 1
                operation_para[str(step_no)] = capture_input()
                while got_input:
                    input_value = input('Confirm the step ? y/n : ')
                    got_input = not (input_value == 'y' or input_value=='n')
                    re_run_step = not input_value=='y'
                print('\n'+'+'*50+'\n')
                if re_run_step:
                    print('Re-enter the step [ {} ] parameter. '.format(step_no))
            step_no += 1
        elif yes_or_no == 'n':
            break
        else:
            pass
    return operation_para

def print_deck_plans():
    """
    print out currently supported deck_plan.
    """
    print("1).default : 1/3:elisa strip; 2:trough; 4:15-50ml rack; 5:ep rack; 9:trash")
    print('2).default-1ml-Plate : *1:1ml-PP plate*; 2:trough; 3:elisa strip; 4:15-50ml rack; 5:ep rack; 9:trash')
    print("3).default-5ml : 1/3:elisa strip; 2:trough; *4:5ml-50ml rack*; 5:ep rack; 9:trash")
    print('4).default-mag : *1:magnet*; 2:trough; 3:elisa strip; 4:15-50ml rack; 5:ep rack; 9:trash')

def print_available_operations():
    """
    print out currently supported common tasks.
    """
    print('Currently these operations are available:\n')
    print('md or multi-distribute : distribute liquid with multi pipette.')
    print('sd or single-distribute : distribute liquid with single pipette.')
    print('msd or multi-serial-dilution : serial dilution with multi pipette.')
    print('ssd or single-serial-dilution : serial dilution with single pipette.')
    print('mmx or multi-mix : mix liquid with multi pipette.')
    print('smx or multi-mix : mix liquid with single pipette.')
    print('tm or toggle-magnet : engage or disengage magnet')
    print('oh or on-hold : put robot on hold for certain time')

def capture_input():
    """
    function to capture inputs for a step and return a dict for the step.
    capture task name first.
    """
    step = {}
    while True:
        step_name = input('What\'s the task? : ')
        temp = para_fetcher(step_name)
        if temp != None:
            step['parameter'] = temp
            step['name'] = step_name
            break
        else:
            pass
    return step




def para_fetcher(step_name):
    """
    parse the step_name and prompt to enter proper parameters for a specific task.
    return the parameter dict for step dict.
    """
    parameter = {}
    if step_name in ['multi-distribute','md','single-distribute','sd']:
        parameter['source'] = lp_input('w',('From where? (2-A3,4-4:8,[,]) : '))
        parameter['source_vol'] = lp_input('v',('Starting volume? (100ul,15ml,[,]) :'))
        parameter['target'] = lp_input('w',('Distribute to where? (2-A1,3-2:8,trash,[,]) : '))
        parameter['volume'] = lp_input('f',('Volume to distribute in ul (100,150,[,]) : '))
        parameter['target_vol'] = lp_input('f',('How much liquid already there in ul? (50,300,[,])  : '))
        if input('Type no to access optional parameters, any key to pass : ').lower() == 'no':
            parameter['aspirate_offset'] = lp_input('f',('Aspirate offset (-1) : '))
            parameter['dispense_offset'] = lp_input('f',('Dispense offset (5) : '))
            parameter['aspirate_speed'] = lp_input('f',('Aspirate speed in ul/s (150) : '))
            parameter['dispense_speed'] = lp_input('f',('Dispense speed in ul/s (150) : '))
        else:
            pass

    elif step_name in ['multi-serial-dilution','msd','single-serial-dilution','ssd']:
        parameter['position'] = lp_input('w',('Dilution series position? (5-A1:A6,3-4:8,[,]) : '))
        parameter['dilution_factor'] = lp_input('f',('Dilution factor (3.162,2.0,[,]) : '))
        parameter['volume'] = lp_input('f',('Final volume in ul (100,150,[,]) : '))
        if input('Type no to access optional parameters, any key to pass : ').lower() == 'no':
            parameter['keep_waste'] = lp_input('yn',('Keep liquid in the last dilution? y/n : '))
            parameter['mix_no'] = lp_input('f',('How many mixes? (5) : '))
            parameter['aspirate_offset'] = lp_input('f',('Aspirate offset (-1) : '))
            parameter['aspirate_speed'] = lp_input('f',('Aspirate speed in ul/s (150) : '))
            parameter['dispense_speed'] = lp_input('f',('Dispense speed in ul/s (150) : '))
        else:
            pass

    elif step_name in ['multi-mix','mmx','single-mix','smx']:
        parameter['position'] = lp_input('w',('Where to mix? (5-A1:A6,3-4:8,[,]) : '))
        parameter['volume'] = lp_input('f',('Volume in the well in ul (100,200,[,]) : '))
        if input('Type no to access optional parameters, any key to pass : ').lower() == 'no':
            parameter['mix_no'] = lp_input('f',('How many mixes? (5) : '))
            parameter['change_tip'] = lp_input('yn',('Change tip after each mix? y/n : '))
        else:
            pass
    elif step_name in ['oh','on-hold']:
        parameter['time'] = lp_input('f',('How many seconds to wait? time in seconds (60,100) : '))
    elif step_name in ['tm','toggle-magnet']:
        parameter['operation'] = input('Engage or disengage magnet? (en/dis) : ')=='en'
        if input('Type no to access optional parameters, any key to pass : ').lower() == 'no':
            parameter['height'] = lp_input('f',('Magnet engage height (default 13.3) : '))
        else:
            pass
    else:
        print("Task not supported, re-enter the task.")
        parameter = None
    return parameter


def lp_input(type_, prompt):
    """
    parser for parameter input.
    will interpret full number string to a float, partial number stirng to a string, list like string to a list.
    return the interpretation.
    type = 'f', 'well', 'yn', 'str', 'vol' for input format type.
    f, float: should return a number
    w, well: should return a well_syntax
    yn: should return a boolean
    s, string: should return a string
    v, volume: should return a volume format 100ul or 10ml
    """
    re_run = 1
    well_syntax = re.compile(r'[1-9]-[a-hA-H][1-9][012]?:[a-hA-H][1-9][012]?|[1-9]-[1-9][012]?:[1-9][012]?|[1-9]-[a-hA-H]?[1-9][012]?|TRASH')
    vol_syntax = re.compile(r'[0-9]+[uUmM][lL]')
    while re_run:
        str_ = input(prompt)
        re_run = 0
        try:
            if str_[0] == '*':
                result = str_
                break
            elif '[' in str_:
                str_ = str_.upper()
                result = ast.literal_eval(str_)
            else:
                try:
                    result = float(str_)
                except ValueError:
                    if str_ == 'y' or str_ == 'n':
                        result = str_=='y'
                    else:
                        result = str_.upper()
            if not isinstance(result,list):
                temp_result = [result]
            else:
                temp_result = result
            for item in temp_result:
                if type_ == 'f':
                    re_run = not isinstance(item,(float,int)) or re_run
                elif type_ == 's':
                    re_run = not isinstance(item,str) or re_run
                elif type_ == 'yn':
                    re_run = not isinstance(item,bool) or re_run
                elif type_ == 'w':
                        re_run = well_syntax.fullmatch(str(item)) == None or re_run
                elif type_ == 'v':
                        re_run = vol_syntax.fullmatch(str(item)) == None or re_run
                else:
                    pass
            re_run = len(temp_result)==0 or re_run
            if re_run:
                print('Wrong input format - {}, retry: '.format(str(result)))
        except:
            re_run = 1
            print('Wrong input format - exception error, retry:')
    return result




def execute_plan(operation_para):
    """
    with the operation_para dict as input, print out the plan details first. if confirm to execute,
    execute the plan.
    """
    print('Current parameters:')
    print('\n'+'+'*50+'\n')
    for key,item in operation_para.items():
        print('Step {} parameters: '.format(key))
        print(json.dumps(operation_para[key],indent=4))
    print('\n'+'+'*50+'\n')
    if input('Review the parameters. Ready to execute? y/n : ') == 'y':
        print("Starting protocol ......")
        for i in sorted(operation_para.keys()):
            operation = operation_interpreter(operation_para[i]['name'])
            operation(**operation_para[i]['parameter'])
            print('Step {} is done!'.format(i))
        print('Protocol is finished!')
    else:
        pass


def operation_interpreter(step_name):
    """
    interpret the step_name keyword and return a corresponding common_task function.
    """
    if step_name == 'initialize_deck':
        operation = ct.load_deck
    elif step_name == 'initialize_tip':
        operation = ct.initialize_tip
    elif step_name in ['multi-distribute','md']:
        operation = ct.multi_distribute_liquid
    elif step_name in ['single-distribute','sd']:
        operation = ct.single_distribute_liquid
    elif step_name in ['multi-serial-dilution','msd']:
        operation = ct.multi_serial_dilution
    elif step_name in ['single-serial-dilution','ssd']:
        operation = ct.single_serial_dilution
    elif step_name in ['multi-mix','mmx']:
        operation = ct.multi_mix
    elif step_name in ['single-mix','smx']:
        operation = ct.single_mix
    else:
        raise ValueError ('Don\'t understand the task.')
    return operation

def save_plan(operation_para):
    """
    print out the operation_para dict and prompt to save results.
    """
    print('Current parameters:')
    print('\n'+'+'*50+'\n')
    for key,item in operation_para.items():
        print('Step {} parameters: '.format(key))
        print(json.dumps(operation_para[key],indent=4))
    print('\n'+'+'*50+'\n')
    if input('Review the parameters. Ready to save? y/n : ') == 'y':
        try:
            print('Folders found: ')
            folder_list=sorted([os.path.join(save_path,i) for i in os.listdir(save_path) if os.path.isdir(os.path.join(save_path,i)) and i[0]!='.'])
            for i,folder in enumerate(folder_list):
                print('\t{}). {}'.format(i+1, folder[save_path_len:]))
            folder_choice = input('Which folder to save? (1,2,3) : ')
            folder_path = folder_list[int(folder_choice)-1]
            name = os.path.join(folder_path,(input('Name the protocol : ')+'.json'))
            with open(name,'wt') as file:
                json.dump(operation_para,file,indent=4)
            print('Protocol is saved.')
        except:
            name = os.path.join(save_path,'temp_protocol.json')
            with open(name,'wt') as file:
                json.dump(operation_para,file,indent=4)
            print('Protocol is saved as temp, salvage if you need.')

    else:
        name = os.path.join(save_path,'temp_protocol.json')
        with open(name,'wt') as file:
            json.dump(operation_para,file,indent=4)
        print('Protocol is saved as temp, salvage if you need.')
    return name

def choose_saved_protocol():
    """
    print out name of all the saved json file in save_path, prompt to choose a protocol to execute.
    return the file_path of the chosen protocol.
    """
    folder_list=sorted([os.path.join(save_path,i) for i in os.listdir(save_path) if os.path.isdir(os.path.join(save_path,i)) and i[0]!='.'])
    print('Folders found: ')

    for i,folder in enumerate(folder_list):
        print('\t{}). {}'.format(i+1, folder[save_path_len:]))
    folder_choice = input('Which folder ? (1,2,3) : ')
    folder_path = folder_list[int(folder_choice)-1]
    protocol_list = glob.glob(os.path.join(folder_path,'*.json'))
    print('\n List of saved protocols:')
    for i,name in enumerate(protocol_list):
        print('{}). {}'.format(i+1, name[save_path_len:-5]))
    protocol_choice = input('Which protocol to run? (1,2,3) : ')
    file_path = protocol_list[int(protocol_choice)-1]
    return file_path

def read_saved_protocol(file_path):
    """
    read the json file in file_path. check if any parameters start with *. print out the key and value and prompt to enter a new value for protocol.
    return the completed protocl parameter in a dict.
    """
    with open(file_path,'rt') as file:
        para = json.load(file)
    print('+'*50)
    print("Type in parameters for the protocol:")
    for step,item in para.items():
        for key,value in item['parameter'].items():
            if str(value)[0] == '*':
                # new_value = input(key+value)
                para[step]['parameter'][key] = lp_input('',(key+value))
    return para




input('Get start?')
print('+'*50+'\n')
print("What to do?\n 1). create protocol and run \n 2). create protocol and save\n 3). run saved protocol\n manual mode \n")
job_to_do = input('Choose one (1,2,3) : ')
print('+'*50+'\n')
if job_to_do == '1':
    para = build_operation_para()
    execute_plan(para)
elif job_to_do == '2':
    para = build_operation_para()
    file = save_plan(para)
    if input("Run the saved protocol now? y/n : ") == 'y':
        new_para = read_saved_protocol(file)
        execute_plan(new_para)
    else:
        pass
elif job_to_do == '3':
    file = choose_saved_protocol()
    para = read_saved_protocol(file)
    execute_plan(para)
elif job_to_do == 'manual':
    print("Using manual mode:")
    print("Use ct.load_deck(deck_plan='default') to connect to robot.")
    print('Use dir(ct) and help(ct.function) for help doc.')
else:
    print("Don\'t understand.")
