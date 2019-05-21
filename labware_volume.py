from bisect import bisect

class labware_volume:
    """
    labware volume class for store information about liquid and labware instance.
    attributes:
    volume: liquid volume in ul, except for Tube_50ml_depth
    depth: liquid depth in mm
    labware: labware instance, for example: (elisa_strip['A1'],elisa_strip.cols('1'))
    methods:
    pipette_out(vol) : vol in ul. update object volume by vol and return current liquid depth. (positive number means liquid in, negative means out)
    surface(vol,offset): vol in ul, offset in mm. update object volume by vol and return labware positional information with offset relative to liquid surface. +offset means above liquid, -offset below. output of surface() can be directly used, for example ( pipette.move_to(lv.surface(100,-1)) )
    """
    def __init__(self,volume,labware=None):
        if isinstance(volume, (int,float)):
            self.volume = volume
        elif volume[-2:].lower() == 'ul':
            self.volume = float(volume[:-2])
        elif volume[-2:].lower() == 'ml':
            self.volume = float(volume[:-2]) * 1000
        else:
            raise ValueError( "Use '##ul' or '##ml' for tube volume.")
        self.depth = self.volume_to_depth(self.volume)
        self.labware = labware
    def pipette_out(self,volume): # this volume is in ul
        self.volume += volume
        self.volume = max(0,self.volume)
        self.depth = self.volume_to_depth(self.volume)
        return self.depth
    def surface(self,pipette_out_volume,offset=0):
        return self.labware.bottom(self.depth_judge(pipette_out_volume,offset))
    def depth_judge(self,volume,offset):
        """
        if offset is not too big, will only go down to 1 above zero.
        """
        depth = self.pipette_out(volume)
        if offset < -9.9:
            result = max(0,depth+offset)
#         elif depth+offset >0 and depth+offset <1:
#             result = (depth+offset)**0.1
        else:
            result = max(1,depth*0.3, depth+offset)
        return result



class elisa_well(labware_volume):
    def volume_to_depth(self,volume):
        depth = volume*10.77/370
        return min(depth,15)

class ams_1ml_pp_plate(labware_volume):
    def volume_to_depth(self,volume):
        depth = volume*40.7/1300
        return min(depth,44)


class Tube_50ml_depth(labware_volume):
    """
    conical tube with flat stand, volume stored is in ml.
    """
    def __init__(self,volume,labware=None):
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
            self.labware = labware
    def volume_to_depth(self,volume):
        depth_max = 101.34 # in mm2
        depth_min = 17.8
        volume_max = 50 #in ml
        volume_min = 5 #in ml
        volume = min(52,max(0,volume))
        depth = (volume - volume_min)* (depth_max - depth_min)/(volume_max - volume_min) + depth_min
        return depth
    def pipette_out(self,volume): # this volume is in ul
        self.volume += volume/1000.0
        self.volume = max(0,self.volume)
        self.depth = self.volume_to_depth(self.volume)
        return self.depth

class eppendorf_2ml_depth(labware_volume):
    """
    1.5ml eppendorf tube class, volume stored are in ul.
    """
    def __init__(self,volume,labware=None):
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
            self.labware = labware
    def volume_to_depth(self,volume):
        volume = min(1590,max(0,volume))
        volume_book =[0,25, 50,  75, 100,125, 150, 200,   250,  300,  350,  400,  450,  500, 600, 700,800,1000,1200,1400,1505,1600]
        depth_book = [0,2.6,4.04,5.8,6.9,7.99,8.86,10.69, 11.59,12.9, 14.17,16.30, 17.2, 18.2,20.0, 21.9, 23.1, 26.5, 29.5, 32.4,34.3,34.4]
        p = bisect(volume_book,volume)
        depth = (volume-volume_book[p-1])*(depth_book[p]-depth_book[p-1])/(volume_book[p]-volume_book[p-1])+depth_book[p-1]
        return depth

class eppendorf_5ml(labware_volume):
    """
    5ml eppendorf tube
    """
    def volume_to_depth(self,volume):
        volume = min(5399,max(0,volume))
        volume_book = [0,100,200,300,400,500,600,700,800,900,1000,1100,1200,1400,1600,1800,2000,2500,3000,3500,4000,4500,5000,5400]
        depth_book = [0,6.5,9.5,11.8,13.3,14.8,15.9,17.1,18.3,19,19.9,20.5,21.4,23.2,25.2,26.6,28,31.3,34.6,38.2,41.8,44.9,48.8,51]
        p = bisect(volume_book,volume)
        depth = (volume-volume_book[p-1])*(depth_book[p]-depth_book[p-1])/(volume_book[p]-volume_book[p-1])+depth_book[p-1]
        return depth

class Tube_15ml(labware_volume):
    """
    15ml tube with screw cap
    """
    def volume_to_depth(self,volume):
        volume = min(15999,max(0,volume))
        volume_book = [0,100,200,300,400,500,600,800,1000,1200,1400,1600,1800,2000,3000,4000,5000,6000,7000,8000,9000,10000,11000,12000,13000,14000,15000,16000]
        depth_book = [0,4.5,7.2,9.2,10.6,12.2,13.5,15.7,17.3,18.9,20.76,22.7,23.9,25.4,32.1,38.8,45.9,52.4,59,65.6,72.1,78.4,84.5,90.5,97,102.6,108.5,110]
        p = bisect(volume_book,volume)
        depth = (volume-volume_book[p-1])*(depth_book[p]-depth_book[p-1])/(volume_book[p]-volume_book[p-1])+depth_book[p-1]
        return depth


class Trough_12(labware_volume):
    """
    12 column trough.
    """
    def __init__(self, volume,labware=None):
        if volume[-2:].lower() == 'ul':
            self.volume = float(volume[:-2]) / 1000.0  # in ml
        elif volume[-2:].lower() == 'ml':
            self.volume = float(volume[:-2])
        else:
            raise ValueError("Use '##ul' or '##ml' for tube volume.")
        if self.volume > 22:
            raise ValueError("load more reagent")
        else:
            self.depth = self.volume_to_depth(self.volume)
            self.labware = labware
    def volume_to_depth(self,volume):
        volume = max(0, volume)
        return min(volume*1.85,40) # 1.85mm per ml.
    def pipette_out(self, volume):  # this volume is in ul
        self.volume += 8*volume/1000.0
        self.volume = max(0,self.volume)
        self.depth = self.volume_to_depth(self.volume)
        return self.depth
