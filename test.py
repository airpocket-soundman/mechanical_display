


dic =   {
            "t" :   [[0,0,0,0],[0,0,0,0]],
            "e" :   [[1,1,1,1],[1,1,1,1],[1,1,1,1]],
            "x" :   [[2,2,2,2],[2,2,2,2],[2,2,2,2],[2,2,2,2]]
        }

def text2image(text):
    img = []
    for i in text:
        for j in range(len(dic[i])):

            img.append(dic[i][j])
    return img


print(text2image("text"))