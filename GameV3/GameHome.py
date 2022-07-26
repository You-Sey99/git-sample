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
    def __init__(self,sounds={"bgm":"SE,BGM\\bgm_maoudamashii_cyber04.mp3"} ,frame_size=5, bgc=BGC, clock=30, surface=GAMENN):
        super().__init__( sounds,frame_size, bgc, clock, surface)

        self.Home_bottun1 = lib.Bottun(txt="はじめから",rect=((POSE_X, POSE_Y),(157,55)))
        self.Home_bottun2 = lib.Bottun(txt="つづきから",rect=((POSE_X, 200),(157,55)))
        self.HighScore = lib.HighScoreRanking
        self.Option_bottun = lib.Bottun(txt="設定",rect=((POSE_X, 300),(157,55)))
        

    def back_ground(self,) -> None:
        super().back_ground()

        self.Home_bottun1.paint(Iro.SIRO)
        self.Home_bottun1.paint_txt(add_y=10)

        self.Home_bottun2.paint(Iro.SIRO)
        self.Home_bottun2.paint_txt(add_y=10)

        self.HighScore.paint(Iro.KURO)

        self.Option_bottun.paint(Iro.GINNIRO)
        self.Option_bottun.paint_txt(add_x=50, add_y=10)



    def ev_mouse(self, event: pg.event) -> int:
        mov = False
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_bottun = pg.mouse.get_pressed()
            if self.Home_bottun1.hit():
                self.sound_bgm.stop_sound("bgm")
                return 1
            
            if self.Home_bottun2.hit():
                self.sound_bgm.stop_sound("bgm")
                return 2
            
            if self.Option_bottun.hit():
                self.sound_bgm.stop_sound("bgm")
                return 3

        

if __name__ == "__main__":
    game = Home()
    #for i in range(9):
        #game.strgs[0].strg[i].set_no(10-i,)
    res = ROOP_CODE
    while res == ROOP_CODE:
        res = game.main()
        print("a")

