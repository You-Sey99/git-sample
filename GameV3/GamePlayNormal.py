# coding=[shift-jis]



from GameV3.GameLib import Card
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

class CardStorage():#旧カード置き場クラス
    def __init__(self,pos_x=CARD_X,pos_y=CARD_Y,c_max=CARD_X) -> None:
        self.strg = [lib.Card(0,rect=(pos_x,pos_y+i*CARD_ZURE_Y)) for i in range(c_max+1)]
        self.x = pos_x
        self.y = pos_y
        self.w = CARD_X
        self.h = CARD_ZURE_Y*(c_max+1) +CARD_Y
        self.max = c_max

    def z_to_m(self, num:int,Z=0,M=C_MAX) -> int:#numの値をZからMに制限する
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

    def reset(self) -> list:#カードの数字を全部0にする
        strg = self.strg
        n=0
        for s in self.strg:
            s.set_no(0)
            s.set_pos(self.x,self.y+CARD_ZURE_Y*n)
            n+=1
        return strg

    def noup_flag(self) -> bool:#↓noupメソッドを実行するフラグにした
        #没　noupメソッドはPlayNormalに作る　こっちに作ると背面更新がいるから相互依存しちゃう
        top = self.get_top()
        if top < 2:#2より小さいと0==0で次のif文を突破できちゃう
            return False
        else:
            if self.strg[top].get_no() == self.strg[top-1].get_no():
                return True
            else:
                return False

    
    def move(self,pos_x:float,pos_y:float,speed=10,num_top=-1,num_bottom=-1) -> bool:#ストレージのカード複数を同時にmoveする
        top = self.get_top()
        num_top = self.z_to_m(num_top,M=top)
        if num_bottom == -1:
            num_bottom = num_top
        else:
            num_bottom = self.z_to_m(num_bottom,M=top)

        for i in range(num_bottom,num_top+1):
            res = self.strg[i].move(pos_x=pos_x,pos_y=pos_y+CARD_ZURE_Y*i,speed=speed)
            # self.okiba[i].idou(dx,dy+gk.C_ZUREY*(i-under),speed)
        return res


    def set_no(self, no:int, num:int) -> bool:#noが変更したい数字,numが変更する場所
        no = self.z_to_m(no,M=MAX_NO)
        num = self.z_to_m(num)

        return self.strg[num].set_no(no)

    
    def reset_rect(self,rect:pg.rect):#ストレージの各カードを初期位置に戻す
        #self.strg = [lib.Card(0,rect=(pos_x,pos_y+i*CARD_ZURE_Y)) for i in range(c_max+1)]
        for i in range(self.max+1):
            self.strg[i].set_rect((self.x,self.y+i*CARD_ZURE_Y,CARD_SIZE))


    def get_rect(self,num:int) -> pg.Rect:
        return self.strg[num].get_rect()


    def get_top(self) -> int:#一番上がどこか返す,何もないときは-1
        res = -1
        for i in range(self.max):
            if self.strg[i].get_no() == 0:
                break
            else:
                res += 1
        return res

    def get_no(self, num:int) -> int:
        num = self.z_to_m(num)
        return self.strg[num].get_no()

    def get_card(self, num:int) -> lib.Card:#できれば使いたくないけど特定の場所のCardオブジェクトを返す
        return self.strg[num]


class PlayNormal(lib.Scene):#ノーマルモードの管理クラス
    def __init__(self, frame_size=5, bgc=BGC, clock=30, surface=GAMENN):
        super().__init__(frame_size, bgc, clock, surface)
        self.cards = [Card(0,rect=(CARD_X-CARD_ZURE_X*i,CARD_Y)) for i in range(CARD_KAZU)]
        for i in range(CARD_KAZU):
            card_no = random.randint(RAND_MIN,RAND_MAX)
            if i == 0:
                self.cards[i].set_pos(CARD_X*2,CARD_Y)
            else:
                mae_no = self.cards[i-1].get_no()
                while mae_no == card_no:
                    card_no = random.randint(RAND_MIN,RAND_MAX)

            self.cards[i].set_no(card_no)
                
        self.strgs = [CardStorage(pos_x=CARD_X+ CARD_ZURE_X*i) for i in range(OKIBA_KAZU)]
        self.time = 0
        self.score = 0

    def gd_lord(self,gamedata:list) -> bool:
        for i in range(CARD_KAZU):
            self.cards[i].set_no(gamedata[0][i])
        for i in range(OKIBA_KAZU):
            for j in range(C_MAX):
                self.strgs[i].set_no(gamedata[1][j],j)
                if j==0:
                    break
        self.time = gamedata[2]
        self.score = gamedata[3]

    def back_ground(self) -> None:
        super().back_ground()
        for strg in self.strgs:
            strg.paint()

    def noup(self,num:int) -> bool:
        if self.strgs[num].noup_flag:
            top = self.strgs[num].get_top()
            if top > 1:
                ue = self.strgs[num].get_no(top-1)
                if self.strgs[num].get_no(top) == ue:
                    pos_to = self.strgs[num].get_card(top-1)
                    pos_from = self.strgs[num].get_card(top)
                    fin = False
                    while not fin:
                        fin = self.strgs[num].move(pos_to[0],pos_to[1],num_top=top)
                        
                    self.strgs[num].reset_rect()
                    self.strgs[num].set_no(0,top)
                    self.strg[top-1].set_no(ue+1)





if __name__ == "__main__":
    pass