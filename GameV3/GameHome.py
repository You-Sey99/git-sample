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
POSE_X = 100
POSE_Y = 100




class Home(lib.Scene):#ノーマルモードの管理クラス
    def __init__(self, frame_size=5, bgc=BGC, clock=30, surface=GAMENN):
        super().__init__(frame_size, bgc, clock, surface)

        self.pose_bottun = lib.Bottun(txt="一時停止",rect=((POSE_X, POSE_Y),TBOX_SIZE))
    
    def back_ground(self,) -> None:
        super().back_ground()

        self.pose_bottun.paint(Iro.SIRO)
        self.pose_bottun.paint_txt(add_y=10)

if __name__ == "__main__":
    game = Home()
    #for i in range(9):
        #game.strgs[0].strg[i].set_no(10-i,)
    res = ROOP_CODE
    while res == ROOP_CODE:
        res = game.main()
        print("a")

