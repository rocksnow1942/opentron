


### build plan for RIC50 assay:




concentrations={'vegf27':150e3,'RD165':1.6e3,'A121':13e3,'vegf28.1':200e3,
                    'vegf33.1':175e3,'vegfmAb1':1000,'antimouse647':1500,
                'neutravidin':1000,'SA647':1000,'IronmanTFPC':500e3,'IronmanRP':434e3}


# step 0 : gather information, assume always is a full plate.

concentration_range=(1,1000)
concentration_points=12
aptamer_list=['vegf27','vegf28.1','vegf29.1','vegf33.1','vegf27','vegf28.1','vegf29.1','vegf33.1']
pi_with = ['neutravidin','neutravidin','neutravidin','neutravidin',None,None,None,None]
pi_ratio = [0.25,0.25,0.25,0.25,0,0,0,0]
FPC = [None,'IronmanTFPC','IronmanTFPC','IronmanTFPC','IronmanTFPC',None,None,None]
RP = [None,'IronmanRP','IronmanRP','IronmanRP','IronmanRP','IronmanRP','IronmanRP','IronmanRP']
anneal=[0,1,1,1,1,1,1,1]


buffercomponent=['BSA','hsDNA']
bufferbase='V1'




# PI- means this is PI-with neutravidin.





# step 1: prepare buffers

a=25e3*10e-6*1e3
a
