


## clas mechanical_display(i2c, unit_layout[2,2], servo_layout[4,4], gray_scale_bit_size[8])

### self.setImage(img)
imgを表示する
imgはx行y列のリスト

img = -1でrelease
img = (2 ** gray_scale_bit_size) でflat position


### self.setPixel(value, coordinate = None)
coordinateで指定した座標のpixelをvalue色にする

value:-1 ～ 2 ** gray_scale_bit_size
value = -1 :release
value = (2 ** gray_scale_bit_size) : flat position

coordinate: [x, y] x座標 = x, y座標 = y のpixelの色を設定
coordinate = Noneで画面全体
