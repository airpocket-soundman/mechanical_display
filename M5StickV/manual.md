


## class mechanical_display(i2c, unit_layout[2,2], servo_layout[4,4], gray_scale_bit_size[8])

### self.setImage(img = None)
imgを表示する
imgはx行y列のリスト。要素の値は0～gray_scale_level - 1

img = None:全画面release



### self.setPixel(coordinate = None, value = None)
coordinateで指定した座標のpixelをvalue色にする

value:0 ～ gray_scale_level
value = None :release
value = gray_scale_level : flat position

coordinate: [x, y] x座標 = x, y座標 = y 
coordinate = None :画面全体

### self.flatPosition()

### self.maxPosition()

### self.minPosition()

### self.release(coordinate = None)
coordinate = None:画面全体release
coordinate = [x,y]: 座標[x,y]をrelease