# coding=[shift-jis]



#色のRGBを入れたやつ



SIRO = (255, 255, 255)
KURO = (0, 0, 0)

MOKKASIN = (255, 228, 181)

CRIMSON = (220,20,60)
AKA = (255, 10, 10)
PINNKU = (255, 105, 180)
DEEPPINNKU = (255,182,193)
MAGENTA = (255,0,255)
TYAIRO = (165, 42, 42)
CHOCO = (210,105,30)
SANDBROWN = (244, 164, 96)
ORENNGE = (255, 127,80)
ORENZIRED = (255,69,0)
KIIRO = (255, 215, 0)

AO = (30, 144, 255)
AOMURASAKI = (138,43,226)
MURASAKI = (128, 0, 128)
MIDORI = (50, 205, 50)
MORIMIDORI = (34,139,34)
INDIGO = (75, 0, 130)
KIMIDORI = (0,255,0)
MIZUIRO = (0, 255, 255)
TURQUOISE = (64,224,208)


#listにまとめたやつ
#IRO_List = [SIRO,AKA,TYAIRO,PINNKU,MURASAKI,ORENNGE,AO,KIIRO,MIDORI,KIMIDORI,MIZUIRO,INDIGO,TURQUOISE,MOKKASIN,KURO]
IRO_List =[SIRO,AKA,ORENZIRED,ORENNGE,SANDBROWN,KIIRO,MORIMIDORI,TURQUOISE,AO,AOMURASAKI,MURASAKI,INDIGO,MOKKASIN,KURO,KIMIDORI,MAGENTA,MIZUIRO]

def iro_last():
    i = 0
    while 1:
        if IRO_List[i] == IRO_List[-1]:
            break
        i += 1
    return i


def iro_num(rgb = (0,0,0)):
    iro = -1
    try:
        for i in range(3):
            if rgb[i] < 0:
                rgb[i]=0
            elif 255 < rgb[i]:
                rgb[i] = 255
    except IndexError:
        return -2

    for i in range(len(IRO_List)):
        if IRO_List[i] == rgb:
            iro = i
            break
    return iro

#print(IRO_List[iro_last()],"==",TURQUOISE)