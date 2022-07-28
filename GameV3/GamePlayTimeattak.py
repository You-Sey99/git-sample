
from GameLocal import *
import GamePlayNormal as gpn
import pygame as pg
import time

#音楽：魔王魂


class PlayTA(gpn.PlayNormal):#タイムアタックモード
    def __init__(self,bgc=gpn.BGC, surface=gpn.GAMENN ,limit=60):
        super().__init__(bgc= bgc, surface= surface)
        self.limit = limit

    def time_update(self) -> None:
        self.time = ((time.time()-self.time_st)//0.1)/10 + self.time_pose#今-開始 +前回セーブした分
        if self.time >= 100000000:#桁の制限
            self.time = 99999999

    def befor_event(self) -> int:
        if self.time >= self.limit:
            self.back_ground(gaov=True)
            pg.display.update()
            self.sound_bgm.stop_sound("bgm")
            self.sound_bgm.play_sound("gameover",0)
            pg.time.wait(5000)
            return -1
        else:
            return super().befor_event()

    def back_ground(self, have=False, gaov=False, add=0) -> None:
        return super().back_ground(have, gaov, add=self.limit)





if __name__ == "__main__":
    game = PlayTA(limit=10)
    fin = "yes"
    while fin in ["yes","ye","y","hai"]:
        game.gd_reset()
        game.main()
        fin = input("owaru?(y/n)")


