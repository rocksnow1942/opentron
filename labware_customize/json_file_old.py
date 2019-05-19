# import json
#
# with open('default-containers.json') as file:
#     container = json.load(file)
#
# print(container.keys())
# print(type(container))
#
# print(container['containers'].keys())
#
#
# def labware_constructor(grid=(8, 12), offset=(11.24, 14.34), x_sep=9,
#     y_sep=9, z=0, diameter=6.4, depth=15.4, volume=300):
#     location = {}
#     alpha_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G',
#                  'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']
#     for i in range(1, grid[1]+1):
#         for k, j in enumerate(alpha_list[0:grid[0]]):
#             location[j+str(i)] = {"x": k*x_sep, "y": (i-1)*y_sep, "z": z,
#                                   "depth": depth, "diameter": diameter,
#                                   "total-liquid-volume": volume}
#     labware = OrderedDict({
#         "origin-offset": {"x": offset[0], "y": offset[1]},
#         "locations": location
#     })
#     return labware
#
#
# test_container = labware_constructor(grid=(3,5),x_sep=10,y_sep=10,depth=10)
#
# container['containers']['test_labware'] = test_container
#
#
# with open('container-modified.json', 'w') as to_write:
#     dump_temp = json.dump(container, to_write, indent=4)
#



# write a json file
import json

file = {'ordering': [['A1', 'B1', 'C1'], ['A2', 'B2', 'C2'], ['A3', 'B3'], ['A4', 'B4']], 'wells': {'A1': {'diameter': 13.5, 'depth': 55.3, 'total-liquid-volume': 5300, 'width': 13.5, 'y': 50.0, 'x': 0, 'z': 16.75, 'length': 13.5, 'height': 60}, 'B4': {'diameter': 26.9, 'depth': 112.6, 'total-liquid-volume': 50000, 'width': 26.9, 'y': 0.8, 'x': 86.5, 'z': 4, 'length': 26.9, 'height': 112.6}, 'A3': {'diameter': 26.9, 'depth': 112.6, 'total-liquid-volume': 50000, 'width': 26.9, 'y': 36.3, 'x': 51.0, 'z': 4, 'length': 26.9, 'height': 112.6}, 'A2': {'diameter': 13.5, 'depth': 55.3, 'total-liquid-volume': 5300, 'width': 13.5, 'y': 50.0, 'x': 25.0, 'z': 16.75, 'length': 13.5, 'height': 60}, 'A4': {'diameter': 26.9, 'depth': 112.6, 'total-liquid-volume': 50000, 'width': 26.9, 'y': 36.3, 'x': 86.5, 'z': 4, 'length': 26.9, 'height': 112.6}, 'B2': {'diameter': 13.5, 'depth': 55.3, 'total-liquid-volume': 5300, 'width': 13.5, 'y': 25.0, 'x': 25.0, 'z': 16.75, 'length': 13.5, 'height': 60}, 'B3': {'diameter': 26.9, 'depth': 112.6, 'total-liquid-volume': 50000, 'width': 26.9, 'y': 0.8, 'x': 51.0, 'z': 4, 'length': 26.9, 'height': 112.6}, 'C2': {'diameter': 13.5, 'depth': 55.3, 'total-liquid-volume': 5300, 'width': 13.5, 'y': 0, 'x': 25.0, 'z': 16.75, 'length': 13.5, 'height': 60}, 'C1': {'diameter': 13.5, 'depth': 55.3, 'total-liquid-volume': 5300, 'width': 13.5, 'y': 0, 'x': 0, 'z': 16.75, 'length': 13.5, 'height': 60}, 'B1': {'diameter': 13.5, 'depth': 55.3, 'total-liquid-volume': 5300, 'width': 13.5, 'y': 25.0, 'x': 0, 'z': 16.75, 'length': 13.5, 'height': 60}}, 'metadata': {'displayCategory': 'tube-rack', 'name': 'ep_5ml_tube_rack', 'format': 'irregular'}}

with open('ep_5ml_tube_rack.json', 'w') as to_write:
    dump_temp = json.dump(file, to_write, indent=4)
