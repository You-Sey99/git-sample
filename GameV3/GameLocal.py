# coding=[shift-jis]


import Iro_RGB as Iro
import pygame as pg
#音楽：魔王魂


#定数とかを入れたファイル
GAM_SIZE = (600,500)#最初の画面の大きさ
CARD_X = 200#カードの位置
CARD_Y = 350

CARD_SIZE = (60,120)#カードの大きさ
CARD_ZURE_X = int(CARD_SIZE[0]/2)#カードのずれ
CARD_ZURE_Y = int(CARD_SIZE[1]/6)
KADO_DEFO = 10#角の丸み
WAKU_DEFO = 2#枠の太さ


TBOX_SIZE = (130,55)
TBOX_ZURE_Y = 5 +TBOX_SIZE[1]

GAM_SOTO =5

COL_LAS = Iro.iro_last() + 1#IroListの数+1,これで%しとけばindenterrarはしないはず


RAND_MAX = 6#手元のカードの数字の範囲
RAND_MIN = 1#
MAX_NO = 11#カード置き場の数字の指数の数字
C_MAX = 9#カード置き場におけるカードの枚数
OKIBA_KAZU = 4#カード置き場の数
CARD_KAZU = OKIBA_KAZU#手元のカードの見える数


SOUND_UNIT = 0.1#soundクラスの音量調整の単位
BG_UNIT = SOUND_UNIT#
SE_UNIT = SOUND_UNIT#

ROOP_CODE = None#Sceneクラスのmainメソッドでリターンしない数字,ev_とかでまだ繰り返したいときはこれをリターンする


pg.init()
font = pg.font.SysFont(None,30)#(フォント、フォントサイズ),必要なのがあったら追加
font2 = pg.font.SysFont("hg正楷書体pro",30)
font_tyuu = pg.font.SysFont("hg正楷書体pro",40)
font_Dai = pg.font.SysFont("hg正楷書体pro",50)
font_KyoDai = pg.font.SysFont("hg正楷書体pro",70)
font_KyoDaii = pg.font.SysFont("hg正楷書体pro",75)


pg.mixer.init()



if __name__ == "__main__":
    import math
    import numpy as np
    #print(math.acos(0.2)/math.pi)

    rect = (CARD_X,CARD_Y,(CARD_SIZE))
    np_rect = rect
    for i in range(len(rect)):
        np_rect[i] = list(rect[i])
    np_rect = np.array(rect)#ここと一個下の文でrectの形をそろえる
    rect = np_rect.flatten()

