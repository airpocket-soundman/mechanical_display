# textを受け取って、5pointフォントの配列データに変換して返すライブラリ


import numpy as np

class dotsFont():
    def __init__(self):
        self.dotsFont5pDict = {  "sp1"  :   np.array([[0,0,0,0,0]]),
                                 "a"    :   np.array([[0,0,1,1,0],[0,1,0,0,1],[0,1,0,0,1],[0,1,1,1,0],[0,0,0,0,1]]),
                                 "b"    :   np.array([[1,1,1,1,1],[0,0,1,0,1],[0,0,1,0,1],[0,0,0,1,0]]),
                                 "c"    :   np.array([[0,0,1,1,0],[0,1,0,0,1],[0,1,0,0,1]]),
                                 "d"    :   np.array([[0,0,0,1,0],[0,0,1,0,1],[0,0,1,0,1],[1,1,1,1,1]]),
                                 "e"    :   np.array([[0,1,1,1,0],[1,0,1,0,1],[1,0,1,0,1],[0,1,1,0,0]]),
                                 "f"    :   np.array([[0,0,1,0,0],[0,1,1,1,1],[1,0,1,0,0]]),
                                 "g"    :   np.array([[0,1,0,0,0],[1,0,1,0,1],[1,0,1,0,1],[0,1,1,1,0]]),
                                 "h"    :   np.array([[1,1,1,1,1],[0,0,1,0,0],[0,0,0,1,1]]),
                                 "i"    :   np.array([[1,0,1,1,1]]),
                                 "j"    :   np.array([[0,0,0,0,1],[1,0,1,1,1]]),
                                 "k"    :   np.array([[1,1,1,1,1],[0,0,0,1,0],[0,0,1,0,1]]),
                                 "l"    :   np.array([[1,0,0,0,0],[1,1,1,1,1]]),
                                 "m"    :   np.array([[0,1,1,1,1],[0,1,0,0,0],[0,1,1,1,1],[0,1,0,0,0],[0,0,1,1,1]]),
                                 "n"    :   np.array([[0,1,1,1,1],[0,1,0,0,0],[0,1,0,0,0],[0,0,1,1,1]]),
                                 "o"    :   np.array([[0,0,1,1,0],[0,1,0,0,1],[0,1,0,0,1],[0,0,1,1,0]]),
                                 "p"    :   np.array([[0,1,1,1,1],[0,1,0,1,0],[0,1,0,1,0],[0,0,1,0,0]]),
                                 "q"    :   np.array([[0,0,1,0,0],[0,1,0,1,0],[0,1,0,1,0],[0,1,1,1,1]]),
                                 "r"    :   np.array([[0,1,1,1,1],[0,0,1,0,0],[0,1,0,0,0],[0,1,0,0,0]]),
                                 "s"    :   np.array([[0,1,0,0,1],[1,0,1,0,1],[1,0,0,1,0]]),
                                 "t"    :   np.array([[0,1,0,0,0],[1,1,1,1,0],[0,1,0,0,1]]),
                                 "u"    :   np.array([[0,1,1,1,0],[0,0,0,0,1],[0,0,0,0,1],[0,1,1,1,1]]),
                                 "v"    :   np.array([[0,1,1,0,0],[0,0,0,1,0],[0,0,0,0,1],[0,0,0,1,0],[0,1,1,0,0]]),
                                 "w"    :   np.array([[0,1,1,1,0],[0,0,0,0,1],[0,0,1,1,0],[0,0,0,0,1],[0,1,1,1,0]]),
                                 "x"    :   np.array([[0,1,0,0,1],[0,0,1,1,0],[0,0,1,1,0],[0,1,0,0,1]]),
                                 "y"    :   np.array([[0,1,0,0,1],[0,0,1,0,1],[0,0,1,1,0],[0,1,0,0,0]]),
                                 "z"    :   np.array([[0,1,0,0,1],[0,1,0,1,1],[0,1,1,0,1],[0,1,0,0,1]]),

                                 "A"    :   np.array([[0,1,1,1,1],[1,0,1,0,0],[1,0,1,0,0],[0,1,1,1,1]]),
                                 "B"    :   np.array([[1,1,1,1,1],[1,0,1,0,1],[1,0,1,0,1],[0,1,0,1,0]]),
                                 "C"    :   np.array([[0,1,1,1,0],[1,0,0,0,1],[1,0,0,0,1],[0,1,0,1,0]]),
                                 "D"    :   np.array([[1,1,1,1,1],[1,0,0,0,1],[1,0,0,0,1],[0,1,1,1,0]]),
                                 "E"    :   np.array([[1,1,1,1,1],[1,0,1,0,1],[1,0,1,0,1],[1,0,0,0,1]]),
                                 "F"    :   np.array([[1,1,1,1,1],[1,0,1,0,0],[1,0,1,0,0],[1,0,0,0,0]]),
                                 "G"    :   np.array([[0,1,1,1,0],[1,0,0,0,1],[1,0,1,0,1],[1,0,1,1,1]]),
                                 "H"    :   np.array([[1,1,1,1,1],[0,0,1,0,0],[0,0,1,0,0],[1,1,1,1,1]]),
                                 "I"    :   np.array([[1,0,0,0,1],[1,1,1,1,1],[1,0,0,0,1]]),
                                 "J"    :   np.array([[0,0,0,1,0],[1,0,0,0,1],[1,1,1,1,0],[1,0,0,0,0]]),
                                 "K"    :   np.array([[1,1,1,1,1],[0,0,1,0,0],[0,1,0,1,0],[1,0,0,0,1]]),
                                 "L"    :   np.array([[1,1,1,1,1],[0,0,0,0,1],[0,0,0,0,1],[0,0,0,0,1]]),
                                 "M"    :   np.array([[1,1,1,1,1],[0,1,0,0,0],[0,0,1,0,0],[0,1,0,0,0],[1,1,1,1,1]]),
                                 "N"    :   np.array([[1,1,1,1,1],[0,1,0,0,0],[0,0,1,0,0],[0,0,0,1,0],[1,1,1,1,1]]),
                                 "O"    :   np.array([[0,1,1,1,0],[1,0,0,0,1],[1,0,0,0,1],[0,1,1,1,0]]),
                                 "P"    :   np.array([[1,1,1,1,1],[1,0,1,0,0],[1,0,1,0,0],[0,1,0,0,0]]),
                                 "Q"    :   np.array([[0,1,1,1,0],[1,0,0,0,1],[1,0,0,1,1],[0,1,1,1,1]]),
                                 "R"    :   np.array([[1,1,1,1,1],[1,0,1,0,0],[1,0,1,0,1],[0,1,0,1,1]]),
                                 "S"    :   np.array([[0,1,0,0,1],[1,0,1,0,1],[1,0,1,0,1],[1,0,0,1,0]]),
                                 "T"    :   np.array([[1,0,0,0,0],[1,0,0,0,0],[1,1,1,1,1],[1,0,0,0,0],[1,0,0,0,0]]),
                                 "U"    :   np.array([[1,1,1,1,0],[0,0,0,0,1],[0,0,0,0,1],[1,1,1,1,0]]),
                                 "V"    :   np.array([[1,1,0,0,0],[0,0,1,1,0],[0,0,0,0,1],[0,0,1,1,0],[1,1,0,0,0]]),
                                 "W"    :   np.array([[1,1,1,0,0],[0,0,0,1,1],[0,1,1,1,0],[0,0,0,1,1],[1,1,1,0,0]]),
                                 "X"    :   np.array([[1,0,0,0,1],[0,1,0,1,0],[0,0,1,0,0],[0,1,0,1,0],[1,0,0,0,1]]),
                                 "Y"    :   np.array([[1,0,0,0,0],[0,1,0,0,0],[0,0,1,1,1],[0,1,0,0,0],[1,0,0,0,0]]),
                                 "Z"    :   np.array([[1,0,0,0,1],[1,0,0,1,1],[1,0,1,0,1],[1,1,0,0,1],[1,0,0,0,1]]),

                                 "0"    :   np.array([[0,1,1,1,0],[1,0,0,0,1],[1,0,0,0,1],[0,1,1,1,0]]),
                                 "1"    :   np.array([[0,1,0,0,1],[1,1,1,1,1],[0,0,0,0,1]]),
                                 "2"    :   np.array([[0,1,0,0,1],[1,0,0,1,1],[1,0,1,0,1],[0,1,0,0,1]]),
                                 "3"    :   np.array([[1,0,0,0,1],[1,0,1,0,1],[1,0,1,0,1],[0,1,0,1,0]]),
                                 "4"    :   np.array([[0,1,1,1,0],[1,0,0,1,0],[1,1,1,1,1],[0,0,0,1,0]]),
                                 "5"    :   np.array([[1,1,1,0,1],[1,0,1,0,1],[1,0,1,0,1],[1,0,0,1,0]]),
                                 "6"    :   np.array([[0,1,1,1,0],[1,0,1,0,1],[1,0,1,0,1],[0,0,0,1,0]]),
                                 "7"    :   np.array([[1,0,0,0,0],[1,0,0,1,1],[1,0,1,0,0],[1,1,0,0,0]]),
                                 "8"    :   np.array([[0,1,0,1,0],[1,0,1,0,1],[1,0,1,0,1],[0,1,0,1,0]]),
                                 "9"    :   np.array([[0,1,0,0,0],[1,0,1,0,1],[1,0,1,1,0],[0,1,1,0,0]]),

                                 "!"    :   np.array([[1,1,1,0,1]]),
                                 "@"    :   np.array([[0,1,1,1,0],[1,0,0,0,1],[1,0,1,1,0],[0,1,1,1,0]]),
                                 "#"    :   np.array([[0,1,0,1,0],[1,1,1,1,1],[0,1,0,1,0],[1,1,1,1,1],[0,1,0,1,0]]),
                                 "$"    :   np.array([[0,1,0,0,0],[1,0,1,0,1],[1,1,1,1,1],[1,0,1,0,1],[0,0,0,1,0]]),
                                 "%"    :   np.array([[1,0,0,1,1],[0,0,1,0,0],[1,1,0,0,1]]),
                                 "^"    :   np.array([[0,1,0,0,0],[1,0,0,0,0],[0,1,0,0,0]]),
                                 "&"    :   np.array([[0,1,0,1,0],[1,0,1,0,1],[0,1,1,0,1],[0,0,0,1,0],[0,0,1,0,1]]),
                                 "*"    :   np.array([[0,1,0,1,0],[0,0,1,0,0],[0,1,0,1,0]]),
                                 "("    :   np.array([[0,1,1,1,0],[1,0,0,0,1]]),
                                 ")"    :   np.array([[1,0,0,0,1],[0,1,1,1,0]]),
                                 "-"    :   np.array([[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0]]),
                                 "_"    :   np.array([[0,0,0,0,1],[0,0,0,0,1],[0,0,0,0,1]]),
                                 "="    :   np.array([[0,1,0,1,0],[0,1,0,1,0],[0,1,0,1,0]]),
                                 "+"    :   np.array([[0,0,1,0,0],[0,1,1,1,0],[0,0,1,0,0]]),
                                 "["    :   np.array([[1,1,1,1,1],[1,0,0,0,1]]),
                                 "]"    :   np.array([[1,0,0,0,1],[1,1,1,1,1]]),
                                 "{"    :   np.array([[0,0,1,0,0],[1,1,1,1,1],[1,0,0,0,1]]),
                                 "}"    :   np.array([[1,0,0,0,1],[1,1,1,1,1],[0,0,1,0,0]]),
                                 "|"    :   np.array([[1,1,1,1,1]]),
                                 "~"    :   np.array([[0,0,0,1,0],[0,0,1,0,0],[0,0,0,1,0],[0,0,1,0,0]]),
                                 ";"    :   np.array([[0,1,0,1,1]]),
                                 ":"    :   np.array([[0,1,0,1,0]]),
                                 "'"    :   np.array([[1,1,0,0,0]]),
                                 '"'    :   np.array([[1,1,0,0,0],[0,0,0,0,0],[1,1,0,0,0]]),
                                 ","    :   np.array([[0,0,0,1,1]]),
                                 "."    :   np.array([[0,0,0,0,1]]),
                                 '/'    :   np.array([[0,0,0,0,1],[0,1,1,1,0],[1,0,0,0,0]]),
                                 "<"    :   np.array([[0,0,1,0,0],[0,1,0,1,0],[1,0,0,0,1]]),
                                 ">"    :   np.array([[1,0,0,0,1],[0,1,0,1,0],[0,0,1,0,0]]),
                                 "?"    :   np.array([[1,0,1,0,1],[1,0,1,0,0],[0,1,0,0,0]]),
                                 " "    :   np.array([[0,0,0,0,0],[0,0,0,0,0]])
        }
        self.dotsFont4pDict = { "sp1"   :   np.array([[0,0,0,0]]),
                                "0"     :   np.array([[1,1,1,1],[1,0,0,1],[1,1,1,1]]),
                                "1"     :   np.array([[0,1,0,0],[1,1,1,1]]),
                                "2"     :   np.array([[1,0,1,1],[1,1,1,1],[1,1,0,1]]),     
                                "3"     :   np.array([[1,0,0,1],[1,1,0,1],[1,1,1,1]]),
                                "4"     :   np.array([[1,1,1,0],[0,0,1,0],[1,1,1,1]]),
                                "5"     :   np.array([[1,1,0,1],[1,1,0,1],[1,0,1,1]]),
                                "6"     :   np.array([[1,1,1,1],[0,1,0,1],[0,1,1,1]]),
                                "7"     :   np.array([[1,0,0,0],[1,0,0,0],[1,1,1,1]]),
                                "8"     :   np.array([[1,1,1,1],[1,1,0,1],[1,1,1,1]]),
                                "9"     :   np.array([[1,1,1,0],[1,0,1,0],[1,1,1,1]])
                                }

    def checkFont(self, char):
        print(ord(str(char)))

# 受け取ったtextを指定のポイント数のフォントを使ったドットイメージに変換
    def setDotImg(self, text, point = 5):
        #print(text)
        dotImage = []

        # textの文字を空白列を追加して連結
        for char in text:
            #print(self.dotsFont5pDict[ord(char)])
            if point == 5:
                #if isinstance(dotImage, int):
                if isinstance(dotImage, list) and not dotImage:
                    dotImage = self.dotsFont5pDict[char]
                else:
                    dotImage = np.concatenate([dotImage,self.dotsFont5pDict[char]])

                dotImage = np.concatenate([dotImage,self.dotsFont5pDict["sp1"]])

            if point == 4:
                if isinstance(dotImage, int):
                    dotImage = self.dotsFont4pDict[char]
                else:
                    dotImage = np.concatenate([dotImage,self.dotsFont4pDict[char]])

                dotImage = np.concatenate([dotImage,self.dotsFont4pDict["sp1"]])

        dotImage = np.delete(dotImage, -1, axis = 0)
        #print(dotImage)
        return dotImage

