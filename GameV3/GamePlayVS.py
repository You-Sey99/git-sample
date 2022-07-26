# coding=[shift-jis]

from tkinter.messagebox import NO
from turtle import pos
import Iro_RGB as Iro
import GameLib as lib
from GameLocal import *
import GamePlayNormal as gpn
import pygame as pg
import sys 
import random
import time


class PlayAut(gpn.PlayNormal):
    def __init__(self,level=1, bgc=gpn.BGC, surface=gpn.GAMENN):
        super().__init__(bgc, surface)
        self.level = int(level)
        self.active_time = int(30/self.level)
        self.active_befor = 0

        self.active_now = False
        self.active_card = -1
        self.active_strg = -1
        self.active_stage = 0
        self.active_strg_top = -2
        self.count = 0
        self.res = False

    def cards_update1(self, num) -> bool:#移動の前まで
        #self.cards = [lib.Card(0,rect=((CARD_X-CARD_ZURE_X*(i),CARD_Y),CARD_SIZE)) for i in range(CARD_KAZU)]
        self.cards[num] = self.cards[2]
        self.cards[num].movable_on()
        if num:#使ったカードが１（手元）の時
            self.cards[num].set_init_pos(((CARD_X-CARD_ZURE_X*1,CARD_Y),CARD_SIZE))
        else:#使ったカードが0（スペア）の時
            self.cards[num].set_init_pos(((CARD_X*2,CARD_Y),CARD_SIZE))

        for i in range(2,CARD_KAZU-1):#カードの入れる場所と初期位置を変更
            self.cards[i] = self.cards[i+1]
            self.cards[i].set_init_pos(((CARD_X-CARD_ZURE_X*i,CARD_Y),CARD_SIZE))

        no = self.cards[CARD_KAZU-2].get_no()#新しいカードを一番最後に入れる
        new_no = random.randint(RAND_MIN,RAND_MAX)
        while no == new_no:
            new_no = random.randint(RAND_MIN,RAND_MAX)
        self.cards[CARD_KAZU-1] = lib.Card(new_no,rect=((CARD_X-CARD_ZURE_X*(CARD_KAZU-1),CARD_Y),CARD_SIZE))
        self.cards[CARD_KAZU-1].set_pos(-CARD_SIZE[0],CARD_Y)
        return True

    def cards_update2(self, num) -> bool:#移動
        move = False#移動
        move2 = False
        
        move = self.cards[num].came_back(speed=3)
        for i in range(2,CARD_KAZU-1):
            self.cards[i].came_back(speed=3)
        move2 = self.cards[CARD_KAZU-1].came_back(speed=10)

        return move and move2

    def cards_update(self, num) -> bool:#前半と後半の2つに分けた
        return super().cards_update(num)


    def back_ground(self, have=False) -> None:
        self.res = self.active(rop=self.res)
        return super().back_ground(have)


    def ev_mouse(self, event: pg.event) -> int:
        return ROOP_CODE

    def befor_event(self) -> int:
        #自動操縦のアルゴリズムスタート
        if self.time - self.active_befor > self.active_time and not self.active_now:#前回実行時から一定時間以上過ぎている＆今実行中じゃないなら実行
            self.active_befor = self.time
            effective = [[1000 for i in range(OKIBA_KAZU)] for j in range(2)]#有効度,小さいほどいい,Zero最強
            mose_effective = 1111#
            moeff_info = (-1,-1)#(手元orスペア,strg)
            c_no = [self.cards[0].get_no(),self.cards[1].get_no()]#手元とスペアのカードの数字を入手
            for i in range(OKIBA_KAZU):#各カード置き場とカードの有効度をはかる
                top = self.strgs[i].get_top()
                strg_no = self.strgs[i].get_no(top)
                
                if strg_no <= 0:#一番上の数字が0,->topが-1,->一枚もない
                    effective[0][i] = 0
                    effective[1][i] = 0

                elif top+1 >= self.strgs[i].get_max():#カードが9枚以上あったら
                    effective[0][i] = 100
                    effective[1][i] = 100
                    if strg_no == c_no[1]:#カード9枚で置けるなら優先しておく,手元が優先
                        effective[1][i] = -1

                    elif strg_no == c_no[0]:
                        effective[0][i] = -1
                    
                else:#カードが1～8枚
                    for j in range(2):
                        effective[j][i] = strg_no - c_no[j]
                        if effective[j][i] < 0:
                            effective[j][i] += 100


            for i in range(OKIBA_KAZU):#有効度が一番いい所を探す
                for j in range(2):
                    if mose_effective > effective[j][i]:
                        mose_effective = effective[j][i]
                        moeff_info = (j,i)

            self.active_strg = moeff_info[1]
            self.active_card = moeff_info[0]
            self.active_strg_top = self.strgs[moeff_info[1]].get_top()
            self.active_now = True

            #ここからは別のメソッドにして同時操作できるようにする
            #ここに書くとこっちを実行中にもう片方が止まる


        return super().befor_event()


    def active(self, rop:bool) -> bool:
        if self.active_now:
            #一番有効な場所にカードを動かす
            if self.active_stage == 0:
                if not rop:
                    pos = self.strgs[self.active_stage].get_rect(self.active_strg_top)
                    rop = self.cards[self.active_card].move(pos_x=pos[0], pos_y=pos[1])
                else:
                    rop = False
                    self.active_stage = 1

                return rop


            #カードを置く
            elif self.active_stage == 1:
                rop = self.put(self.cards[self.active_card].get_no(),self.active_strg)
                
                if rop:#putできたら
                    self.active_stage == 2
                    return True

                else:#できなかったら
                    self.active_stage = 0
                    self.active_now = False
                    return False

            #noupの処理をする
            elif self.active_stage == 2:
                if rop:#初回+前回noupができたとき
                    rop = self.noup(self.active_strg)
                    self.count += 1
                    return rop

                else:#前回noupができなかったとき
                    self.active_stage = 3
                    self.score +=(2**self.strgs[i].get_no(self.strgs[i].get_top()))*(self.count-1)
                    self.cards_update1(self.active_card)
                    self.count = 0
                    return False
            
            #手元の更新
            elif self.active_stage == 3:
                if not rop:
                    rop = self.cards_update2(self.active_card)
                    return rop

                else:
                    self.active_now = False
                    self.active_card = -1
                    self.active_strg = -1
                    self.active_strg = 0
                    self.active_befor = self.time

            #終わり
        


class PlayVS(gpn.PlayNormal):
    def __init__(self, level=1, bgc=gpn.BGC, surface=gpn.GAMENN):
        super().__init__(bgc, surface)


        self.level = level




if __name__ == "__main__":
    vs = PlayAut(level=10)
    a = vs.main()
    print(a)