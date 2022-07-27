# coding=[shift-jis]


import Iro_RGB as Iro
import GameLib as lib
from GameLocal import *
import pygame as pg
import sys 
import random
import time


SOUND_SET_X = 230
SOUND_SET_Y = 200
SOUND_SET_SIZE = (200,50)

UPDOWN_SIZE = (50,50)
UD_ADDX = 18
UD_ADDY = 10


class Option(lib.Scene):#設定画面
    def __init__(self, sounds: dict,gamemode_list:list, frame_size=5, clock=30, ):
        super().__init__(sounds={}, frame_size=frame_size, clock=clock,)
        self.bgm_vol = 1
        self.bgm_vol_t = lib.TxtBox(txt="0",rect=((SOUND_SET_X,SOUND_SET_Y),SOUND_SET_SIZE))
        self.bgm_up = lib.Bottun(txt=">",rect=((SOUND_SET_X+ SOUND_SET_SIZE[0]+10,SOUND_SET_Y),UPDOWN_SIZE))
        self.bgm_doun = lib.Bottun(txt="<",rect=((SOUND_SET_X- UPDOWN_SIZE[0]-10,SOUND_SET_Y),UPDOWN_SIZE))
        self.bgm_t = lib.TxtBox("BGM",rect=((SOUND_SET_X+40,SOUND_SET_Y-SOUND_SET_SIZE[1]),SOUND_SET_SIZE))
        
        self.se_vol = 3
        self.se_vol_t = lib.TxtBox(txt="0",rect=((SOUND_SET_X,SOUND_SET_Y+ SOUND_SET_SIZE[1]*2+20),SOUND_SET_SIZE))
        self.se_up = lib.Bottun(txt=">",rect=((SOUND_SET_X+ SOUND_SET_SIZE[0]+10,SOUND_SET_Y+ SOUND_SET_SIZE[1]*2+20),UPDOWN_SIZE))
        self.se_doun = lib.Bottun(txt="<",rect=((SOUND_SET_X- UPDOWN_SIZE[0]-10,SOUND_SET_Y+ SOUND_SET_SIZE[1]*2+20),UPDOWN_SIZE))
        self.se_t = lib.TxtBox("SE",rect=((SOUND_SET_X+40,SOUND_SET_Y-SOUND_SET_SIZE[1]+ SOUND_SET_SIZE[1]*2+20),SOUND_SET_SIZE))
        
        self.gamemode = 0
        self.gamemode_t = lib.Bottun(txt="Normal",rect=((SOUND_SET_X,50),SOUND_SET_SIZE))
        self.gamemode_list = [str(gm) for gm in gamemode_list]
        #self.gamemode_list = ["Normal","TimeAttak"]

        self.back = lib.Bottun(txt="戻る",rect=((SOUND_SET_X+50,SOUND_SET_Y+ SOUND_SET_SIZE[1]*3+60),(75,50)))


    def back_ground(self) -> None:
        super().back_ground()
        self.bgm_up.paint(col=Iro.MIZUIRO)
        self.bgm_doun.paint(col=Iro.MIZUIRO)
        self.se_up.paint(col=Iro.MIZUIRO)
        self.se_doun.paint(col=Iro.MIZUIRO)

        self.bgm_up.paint_txt(col=Iro.KURO,add_x=UD_ADDX,add_y=UD_ADDY)
        self.bgm_doun.paint_txt(col=Iro.KURO,add_x=UD_ADDX,add_y=UD_ADDY)
        self.se_up.paint_txt(col=Iro.KURO,add_x=UD_ADDX,add_y=UD_ADDY)
        self.se_doun.paint_txt(col=Iro.KURO,add_x=UD_ADDX,add_y=UD_ADDY)

        self.bgm_vol_t.set_txt(str(self.bgm_vol))
        self.se_vol_t.set_txt(str(self.se_vol))
        self.bgm_vol_t.paint_txt(add_x=UD_ADDX*2)
        self.se_vol_t.paint_txt(add_x=UD_ADDX*2)
        self.bgm_t.paint_txt()
        self.se_t.paint_txt()

        self.gamemode_t.paint(col=Iro.AKA)
        self.gamemode_t.set_txt(self.gamemode_list[self.gamemode])
        self.gamemode_t.paint_txt(add_x=UD_ADDX*1.3,add_y=5)

        self.back.paint(col=Iro.MIZUIRO)
        self.back.paint_txt(add_x=10,add_y=5)


    def main(self,mod=0) -> int:
        self.gamemode = int(mod) 
        return super().main()


    def ev_mouse(self, event: pg.event) -> int:
        super().ev_mouse(event)
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.gamemode_t.hit():
                self.gamemode = (self.gamemode+1)%len(self.gamemode_list)

            elif self.bgm_up.hit():
                if (self.bgm_vol+1) <= 10:
                    self.bgm_vol += 1

            elif self.bgm_doun.hit():
                if (self.bgm_vol-1) >= 0:
                    self.bgm_vol -= 1

            elif self.se_up.hit():
                if (self.se_vol+1) <= 10:
                    self.se_vol += 1

            elif self.se_doun.hit():
                if (self.se_vol-1) >= 0:
                    self.se_vol -= 1

            elif self.back.hit():
                return self.gamemode






if __name__ == "__main__":
    opt = Option(sounds={})
    re=0
    while 1:
        re = opt.main(mod=re)
        print(re)