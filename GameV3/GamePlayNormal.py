# coding=[shift-jis]



import Iro_RGB as Iro
import GameLib as lib
from GameLocal import *
import pygame as pg
import sys 
import random
import time

BGC = Iro.MOKKASIN
pg.init()
GAMENN = pg.display.set_mode(GAM_SIZE,pg.RESIZABLE)
pg.display.set_caption("Normal_Mode")

class CardStorage():
    def __init__(self,pos_x=CARD_X,pos_y=CARD_Y,c_max=CARD_X) -> None:
        self.strg = [Card(0,rect=(pos_x,pos_y+i*CARD_ZURE_Y)) for i in range(c_max+1)]
        self.x = pos_x
        self.y = pos_y
        self.w = CARD_X
        self.h = CARD_ZURE_Y*(c_max+1) +CARD_Y
        self.max = c_max

    def z_to_m(self, num:int,Z=0,M=C_MAX) -> int:
        try:
            num = int(num)
        except (ValueError):
            return Z-1
        if num < Z:
            num = 0
        elif M < num:
            num = M
        return num

    def paint(self) -> None:
        for i in range(self.max):
            self.strg[i].paint()
            if self.strg[i].get_no() == 0:
                break
        self.strg[self.max].paint(alpha=0)

    def reset(self) -> list:
        strg = self.strg
        n=0
        for s in self.strg:
            s.set_no(0)
            s.set_pos(self.x,self.y+CARD_ZURE_Y*n)
            n+=1
        return strg

    def noup(self) -> None:#没　noupメソッドはPlayNormalに作る　こっちに作ると背面更新がいるから相互依存しちゃう
        top = self.get_top()
        if top > 1:
            ue = self.strg[top-1].get_no()
            if self.strg[top].get_no() == ue:
                pos_to = self.strg[top-1].get_rect()
                pos_from = self.strg[top].get_rect()
                fin = False
                while not fin:
                    fin = self.strg[top].move(pos_to[0],pos_to[1])
                    
                self.strg[top].set_pos(pos_from[0],pos_from[1])
                self.strg[top].set_no(0)
                self.strg[top-1].set_no(ue+1)

    def set_no(self, no:int, num:int) -> bool:
        no = self.z_to_m(no,M=MAX_NO)
        num = self.z_to_m(num)

        return self.strg[num].set_no(no)

    def get_top(self) -> int:#一番上がどこか返す,何もないときは-1
        a = -1
        for i in range(self.max):
            if self.strg[i].get_no() == 0:
                break
            else:
                a += 1
        return a

    def get_no(self, num:int) -> int:
        num = self.z_to_m(num)
        return self.strg[num].get_no()

    def get_card(self, num:int) -> lib.Card:
        return self.strg[num]


class PlayNormal(lib.Scene):
    def __init__(self, frame_size=5, bgc=BGC, clock=30, surface=GAMENN):
        super().__init__(frame_size, bgc, clock, surface)
        self.strgs = [CardStorage(pos_x=CARD_X+ CARD_ZURE_X*i) for i in range(OKIBA_KAZU)]

    def back_ground(self) -> None:
        super().back_ground()
        for strg in self.strgs:
            strg.paint()

    def noup(self) -> bool:
        A





if __name__ == "__main__":
    pass