import Iro_RGB as Iro
import GameLib as lib
from GameLocal import *
import GamePlayNormal as gpn
import pygame as pg
import sys 
import random
import time


class PlayTA(gpn.PlayNormal):#タイムアタックモード
    def __init__(self,bgc=gpn.BGC, surface=gpn.GAMENN ,limit=60):
        super().__init__(bgc= bgc, surface= surface)
        self.limit = limit

    def time_update(self) -> None:
        self.time = (self.limit - ((time.time()-self.time_st)//0.1)/10 + self.time_pose)//0.1/10#今-開始 +前回セーブした分
        if self.time >= 100000000:#桁の制限
            self.time = 99999999

    def befor_event(self) -> int:
        if self.time <= 0:
            return -1
        else:
            return super().befor_event()





if __name__ == "__main__":
    game = PlayTA()
    fin = "yes"
    while fin in ["yes","ye","y","hai"]:
        game.gd_reset()
        game.main()
        fin = input("owaru?(y/n)")


