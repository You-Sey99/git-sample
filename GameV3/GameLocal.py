# coding=[shift-jis]



import Iro_RGB as Iro
import pygame as pg


GAM_SIZE = (600,500)
CARD_X = 100
CARD_Y = 40
CARD_SIZE = (60,120)
KADO_DEFO = 10
WAKU_DEFO = 2
CARD_ZURE_X = int(CARD_SIZE[0]/2)
CARD_ZURE_Y = int(CARD_SIZE[1]/3)

COL_LAS = Iro.iro_last() + 1


RAND_MAX = 6
RAND_MIN = 1
MAX_NO = 11
C_MAX = 9
OKIBA_KAZU = 4
CARD_KAZU = OKIBA_KAZU


SOUND_UNIT = 0.1
BG_UNIT = SOUND_UNIT
SE_UNIT = SOUND_UNIT


pg.init()
font = pg.font.SysFont(None,30)#(フォント、フォントサイズ)
font2 = pg.font.SysFont("hg正楷書体pro",30)
font_tyuu = pg.font.SysFont("hg正楷書体pro",40)
font_Dai = pg.font.SysFont("hg正楷書体pro",50)
font_KyoDai = pg.font.SysFont("hg正楷書体pro",70)
font_KyoDaii = pg.font.SysFont("hg正楷書体pro",75)


