import Iro_RGB as Iro
import GameLib as lib
from GameLocal import *
import pygame as pg
import sys

BGC = Iro.MOKKASIN
pg.init()
GAMENN = pg.display.set_mode(GAM_SIZE,pg.RESIZABLE)
pg.display.set_caption("Home")
STORAGE_X = 40
STORAGE_Y = 40
STORAGE_ZURE_X = CARD_SIZE[0]*1.5
STORAGE_ZURE_Y = CARD_ZURE_Y


