import font

def fontOverlay(bg_image, font_image ,coordinate, font_color = None, transparent = True):
    if font_color == None:
        font_color = 15 
    bg_size = [len(bg_image), len(bg_image[0])]
    font_size = [len(font_image), len(font_image[0])]

    image = bg_image

    for y in range(font_size[1]):
        if y + coordinate[1] < bg_size[1]:
            for x in range(font_size[0]):
                if x + coordinate[0] < bg_size[0]:
                    #print("x,y",x,y)
                    if transparent == False:
                        image[x + coordinate[0]][y + coordinate[1]] = font_image[x][y] * font_color
                    else:
                        if font_image[x][y] == 1:
                            image[x + coordinate[0]][y + coordinate[1]] = font_image[x][y] * font_color
    return image

def textOverlay(text_image ,offset = [0,0], text_color = None, bg_color = None, transparent = True):
    if text_color == None:
        text_color = 15 # = self.gray_scale_color -1
    if bg_color == None:
        bg_color = 0
    text_size = [len(text_image), len(text_image[0])]
    display_size = [8, 8] #self.pixel_layout

    image = []

    for y in range(display_size[1]):
        list = []
        for x in range(display_size[0]):
            list.append(bg_color)
        image.append(list)

    for y in range(text_size[1]): 
        if y + offset[1] < display_size[1] and y + offset[1] >= 0: 
            for x in range(text_size[0]): 
                if x + offset[0] < display_size[0] and x + offset[0] >= 0:
                    if transparent == False:
                        image[x + offset[0]][y + offset[1]] = text_image[x][y] * text_color
                    else:
                        if text_image[x][y] == 1:
                            image[x + offset[0]][y + offset[1]] = text_image[x][y] * text_color
    return image                    


Font = font.font_5P()

text_image = Font.genTextImage(text = "    AAC",monospace = False)
print("text image")
for y in range(len(text_image)):
    print(text_image[y])
"""
background = [[5,5,5,5,5,5],
              [5,5,5,5,5,5],
              [5,5,5,5,5,5],
              [5,5,5,5,5,5],
              [5,5,5,5,5,5],
              [5,5,5,5,5,5],
              [5,5,5,5,5,5]]

print("background")
for y in range(len(background)):
    print(background[y])

image = fontOverlay(background, text_image, [0,0], 1)
"""



for x in range(len(text_image)):
    image = textOverlay(text_image,[-x, 2], text_color = 1, bg_color = 0, transparent = True)
    print("image",x)
    for y in range(len(image)):
        print(image[y])
