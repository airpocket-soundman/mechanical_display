class dot_image():
    def __init__(self):
        self.mario        =   {
            "standing"      :   [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                 [0,0,0,0,0,0,0,0,0,6,3,3,3,0,0,6],
                                 [0,0,0,6,6,6,0,0,6,6,3,3,3,0,6,6],
                                 [0,7,6,3,3,6,0,6,6,6,6,3,7,7,6,6],
                                 [7,7,6,6,6,3,3,6,6,6,7,7,7,7,6,6],
                                 [7,7,6,3,6,3,3,7,7,7,3,7,7,7,0,0],
                                 [7,7,3,3,3,3,3,6,6,7,7,7,7,0,0,0],
                                 [7,7,3,3,3,3,3,6,6,7,7,7,7,0,0,0],
                                 [7,7,6,6,3,6,3,6,7,7,3,7,7,7,0,0],
                                 [0,7,3,3,6,6,3,0,6,6,7,7,7,7,6,6],
                                 [0,7,0,3,3,6,3,0,6,6,6,3,7,7,6,6],
                                 [0,7,0,3,3,6,0,0,6,6,3,3,3,0,6,6],
                                 [0,0,0,0,3,0,0,0,0,6,3,3,3,0,0,6],
                                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],

            "run1"          :   [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                 [0,0,0,0,0,0,0,0,0,0,0,0,0,6,6,0],
                                 [0,0,0,0,0,0,0,0,0,0,3,6,6,6,0,0],
                                 [0,0,0,0,6,6,6,0,0,3,3,6,7,7,0,0],
                                 [0,0,7,6,3,3,6,0,6,6,7,7,7,7,0,0],
                                 [0,7,7,6,6,6,3,3,6,6,6,7,7,7,0,0],
                                 [0,7,7,6,3,6,3,3,6,6,6,7,7,0,6,6],
                                 [0,7,7,3,3,3,3,3,6,6,6,7,7,7,6,6],
                                 [0,7,7,3,3,3,3,3,7,6,6,7,7,7,6,6],
                                 [0,7,7,6,6,3,6,3,6,6,6,7,7,7,0,6],
                                 [0,0,7,3,3,6,6,3,0,3,3,7,7,0,0,0],
                                 [0,0,7,0,3,3,6,3,3,3,3,0,0,0,0,0],
                                 [0,0,7,0,3,3,6,0,0,3,0,0,0,0,0,0],
                                 [0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0],
                                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],

            "run2"          :   [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                 [0,0,0,6,6,6,0,0,6,6,6,7,0,0,0,0],
                                 [0,7,6,3,3,6,0,6,6,6,6,6,7,0,0,0],
                                 [7,7,6,6,6,3,3,6,6,6,6,6,7,0,0,0],
                                 [7,7,6,3,6,3,3,7,6,7,6,3,3,7,6,6],
                                 [7,7,3,3,3,3,3,6,7,7,7,3,3,7,6,6],
                                 [7,7,3,3,3,3,3,6,7,3,7,3,7,6,6,6],
                                 [7,7,6,6,3,6,3,6,6,7,7,7,7,6,6,0],
                                 [0,7,3,3,6,6,3,0,6,7,7,7,7,6,6,0],
                                 [0,7,0,3,3,6,3,0,0,0,7,7,0,0,6,0],
                                 [0,7,0,3,3,6,0,0,0,0,0,0,0,0,0,0],
                                 [0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0],
                                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],

            "turn"          :   [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                 [0,0,0,3,3,0,0,0,0,0,0,0,0,6,6,0],
                                 [0,0,6,3,3,3,0,7,7,7,0,0,0,0,6,6],
                                 [0,6,6,6,6,3,7,7,6,7,7,7,0,6,6,6],
                                 [0,7,6,3,3,6,7,3,3,7,7,6,6,7,6,6],
                                 [7,7,6,3,3,3,7,3,3,3,7,6,6,7,6,6],
                                 [7,7,6,6,6,3,6,3,3,3,7,6,6,6,7,0],
                                 [7,7,6,3,6,3,6,6,6,6,7,7,6,6,0,0],
                                 [7,7,3,3,3,3,6,7,6,6,6,7,7,6,0,0],
                                 [7,7,6,3,3,3,7,7,6,6,6,7,7,7,0,0],
                                 [0,7,3,3,6,3,3,6,6,6,6,7,7,0,0,0],
                                 [0,7,0,3,6,6,3,6,6,6,6,0,0,0,0,0],
                                 [0,0,0,3,3,6,0,6,6,6,0,0,0,0,0,0],
                                 [0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0],
                                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],

            "jump"          :   [[0,0,0,0,0,0,0,0,0,0,3,3,0,0,0,0],
                                 [0,0,0,0,0,0,0,0,0,6,3,3,3,0,6,6],
                                 [0,0,0,0,0,0,0,0,6,6,6,3,0,6,6,0],
                                 [0,0,0,0,0,0,0,0,6,6,6,0,6,6,6,0],
                                 [0,0,0,0,6,6,6,0,6,6,6,7,7,6,7,7],
                                 [0,0,7,6,3,3,6,0,6,6,6,7,7,7,7,7],
                                 [0,7,7,6,6,6,3,3,6,6,6,6,7,7,7,7],
                                 [0,7,7,6,3,6,3,3,7,6,6,7,7,7,7,7],
                                 [0,7,7,3,3,3,3,3,6,7,7,7,7,7,7,0],
                                 [0,7,7,3,3,3,3,3,6,6,7,3,7,7,7,0],
                                 [0,7,7,6,6,3,6,3,6,6,7,7,7,7,7,0],
                                 [0,0,7,3,3,6,6,3,7,6,7,7,7,7,0,0],
                                 [0,0,7,0,3,3,6,3,0,7,7,3,7,7,0,0],
                                 [3,3,7,6,6,3,6,6,0,0,0,7,7,7,0,0],
                                 [3,3,3,6,6,3,6,0,0,0,0,6,6,6,0,0],
                                 [3,3,3,6,6,6,0,0,0,6,6,6,6,6,0,0]],

            "dead"          :   [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                 [0,0,0,3,3,3,0,0,0,0,0,0,0,0,0,0],
                                 [0,0,0,3,3,3,0,0,0,0,6,6,6,6,0,0],
                                 [0,0,3,3,6,6,6,0,0,7,6,6,6,6,6,0],
                                 [0,0,0,6,6,6,6,6,6,7,7,6,6,6,6,0],
                                 [0,0,7,3,3,6,6,3,3,7,7,7,7,7,7,0],
                                 [0,7,7,6,6,3,6,6,3,3,6,7,3,7,7,0],
                                 [0,7,7,3,3,3,3,6,3,3,6,6,7,7,7,0],
                                 [0,7,7,3,3,3,3,6,3,3,6,6,7,7,7,0],
                                 [0,7,7,6,6,3,6,6,3,3,6,7,3,7,7,0],
                                 [0,0,7,3,3,6,6,3,3,7,7,7,7,7,7,0],
                                 [0,0,0,6,6,6,6,6,6,7,7,6,6,6,6,0],
                                 [0,0,3,3,6,6,6,0,0,7,6,6,6,6,6,0],
                                 [0,0,0,3,3,3,0,0,0,0,6,6,6,6,0,0],
                                 [0,0,0,3,3,3,0,0,0,0,0,0,0,0,0,0],
                                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]


        }