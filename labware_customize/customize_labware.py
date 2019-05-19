import json

def labware_constructor(name, dimension_x, dimension_y, grid=(8,12), type='custom' ,diameter= None,height= None ,depth = None , width=None , length=None ,volume=None ):
    labware = {}
    labware['metadata'] = {'name': name}
    alpha = 'ABCDEFGHIJKLMNOPQRST'
    x_sep = dimension_x/(grid[1]-1)
    y_sep = dimension_y/(grid[0]-1)
    wells = {}
    for i in range(grid[0]):
        for j in range(grid[1]):
            wells[alpha[i]+str(j+1)] = {"x": x_sep*j, "y": y_sep*(grid[0]-1-i),"z":0,"type":type}
            if diameter is not None:
                wells[alpha[i]+str(j+1)]["diameter"] = diameter
                wells[alpha[i]+str(j+1)]["width"] = diameter
                wells[alpha[i]+str(j+1)]["length"] = diameter
            if height is not None:
                wells[alpha[i]+str(j+1)]["height"] = height
            if depth is not None:
                wells[alpha[i]+str(j+1)]["depth"] = depth
            if width is not None and length is not None:
                wells[alpha[i]+str(j+1)]["width"] = width
                wells[alpha[i]+str(j+1)]["length"] = length
            if volume is not None:
                wells[alpha[i]+str(j+1)]["total-liquid-volume"] = volume
    labware["wells"] = wells
    ordering = [[alpha[i]+str(j+1) for i in range(grid[0])] for j in range(grid[1])]
    labware["ordering"] = ordering
    return labware

import json
with open('96strip_test.json') as file:
    container = json.load(file)

with open('new_labware.json') as file1:
    container_1 = json.load(file1)
print(container)
print(container_1)


new_container = labware_constructor("96strip_test",9.02*11,9.02*7,grid=(8,12),diameter=6.9,height=9,volume=350)




new_labware = 'new_labware.json'

with open(new_labware, 'w') as to_write:
    dump_temp = json.dump(new_container, to_write, indent=4)
