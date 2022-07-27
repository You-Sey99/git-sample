# coding=[shift-jis]


from tkinter.messagebox import NO
from matplotlib.pyplot import cla
import Iro_RGB as Iro
import GameLib as lib
from GameLocal import *
import GamePlayNormal as gpn
import pygame as pg
import sys 
import random
import time


class PlayAut(gpn.PlayNormal):
    def __init__(self,level=1, frame_size=5, bgc=gpn.BGC, clock=300, surface=gpn.GAMENN):
        super().__init__(bgc=bgc, surface=surface, frame_size=frame_size, clock=clock)
        self.level = int(level)
        self.active_time = int(30/self.level)
        self.active_befor = 0

        self.active_now = False
        self.active_card = -1
        self.active_strg = -1
        self.active_stage = 0
        self.active_strg_top = -2
        self.active_noup = 1
        self.count = 0
        self.res = False

        self.active_bonus_now = False

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

    def noup1(self, num: int) -> bool:
        if self.strgs[num].noup_flag():#Cardの数字が同じとき
            self.sound_se.play_sound("chain",0)
            return True
        
        return False
           
    def noup2(self, num: int) -> bool:
        top = self.active_strg_top-1
        #ue_no = self.strgs[num].get_no(top -1)#一番上の一個下の番号
        pos_to = self.strgs[num].get_rect(top-1)#演出の準備
        #print(top)
        #pos_from = self.strgs[num].get_rect(top)
        #演出,self.yはpos_to[1]に近づいてるのにabs(pos_y-self.y)は大きくなってる
        fin = self.strgs[num].move(pos_to[0],pos_to[1],num_top=top,speed=0.5)
        return fin

    
    def noup3(self, num: int) -> bool:
        top = self.active_strg_top-1
        ue_no = self.strgs[num].get_no(top -1)#一番上の一個下の番号
        self.strgs[num].reset_rect()#元に戻す
        self.strgs[num].set_no(0,top)#ゼロにする
        self.strgs[num].set_no(ue_no+1,top-1)#
        return True


    def cards_update(self, num) -> bool:#前半と後半の2つに分けた
        return super().cards_update(num)


    def back_ground(self, have=False, gaov=False, add=0) -> None:
        self.active_mode()
        return super().back_ground(have, gaov, add)

    def active_mode(self) -> None:
        if self.active_bonus_now:
            self.res = self.active_bonus(rop=self.res)

        else:
            if self.bonus:
                self.active_bonus_now = self.do_use_bonus()

            else:
                self.res = self.active(rop=self.res)

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
                        moeff_info = (j,i)#(手元orスペア,strg番号)

                    elif mose_effective == effective[j][i]:
                        if self.strgs[moeff_info[1]].get_no(moeff_info[0]) < self.strgs[i].get_no(j):
                            mose_effective = effective[j][i]
                            moeff_info = (j,i)#(手元orスペア,strg番号)


            self.active_strg = moeff_info[1]
            self.active_card = moeff_info[0]
            self.active_strg_top = self.strgs[moeff_info[1]].get_top() +1
            self.active_now = True

            #ここからは別のメソッドにして同時操作できるようにする
            #ここに書くとこっちを実行中にもう片方が止まる


        return super().befor_event()


    def active(self, rop:bool) -> bool:
        if self.active_now:
            #一番有効な場所にカードを動かす
            if self.active_stage == 0:
                if not rop:
                    pos = self.strgs[self.active_strg].get_rect(self.active_strg_top)
                    rop = self.cards[self.active_card].move(pos_x=pos[0], pos_y=pos[1])
                else:
                    rop = False
                    self.active_stage = 1

                return rop


            #カードを置く
            elif self.active_stage == 1:
                rop = self.put(self.active_strg, self.active_card)
                
                if rop:#putできたら
                    self.active_stage = 2
                    #self.active_strg_top = self.strgs[self.active_strg].get_top() +1
                    self.cards[self.active_card].set_pos(self.disp_w,self.disp_h)
                    return True

                else:#できなかったら
                    self.active_stage = 0
                    self.active_now = False
                    return False

            #noupの処理をする
            elif self.active_stage == 2:
                if self.active_noup == 1:#noupの判定
                    self.count += 1
                    self.active_strg_top = self.strgs[self.active_strg].get_top() +1
                    rop = self.noup1(self.active_strg)#noupできるかできないかの判別
                    if rop:
                        self.active_noup = 2#noupを次に
                    else:
                        self.active_stage = 3#ステージを次に
                        self.score +=(2**self.strgs[self.active_strg].get_no(self.strgs[self.active_strg].get_top()))*(self.count-1)
                        self.cards_update1(self.active_card)
                        self.count = 0

                    return rop

                else:#移動~数字変更
                    if rop:#初回+前回noup2ができたとき -> 移動中
                        rop = self.noup2(self.active_strg) 
                        return not rop

                    else:#前回noup2ができなかったとき -> 移動終了,数字の変更,noup1へ
                        self.active_noup = 1
                        self.noup3(self.active_strg)
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
                    self.active_stage = 0
                    self.active_befor = self.time
                    self.ev_after(pg.KEYUP)

    def do_use_bonus(self) -> bool:
        for i in range(OKIBA_KAZU):#下のカード>上のカード になってるところがあればTrue,なければFalse
            sita = 0
            for j in range(self.strgs[i].get_max()):
                koko = self.strgs[i].get_no(j)
                if koko > sita and sita != 0:
                    self.active_now = True#activeに
                    self.active_strg = i#動かすstrg
                    self.active_card = j#動かす一番上,(i,j)が選んだ場所
                    return True

                else:
                    if koko == 0:
                        break
                    else:
                        sita = koko

        self.bonus = False
        return False


    def active_bonus(self, rop) -> bool:#bonusの時の処理,bonus＆do_use_bonusの時実行
        if self.active_stage == 0:
            #self.bonus = False
            self.active_strg_top = self.strgs[self.active_strg].get_top()
            self.active_stage = 2
            self.sound_se.play_sound("slid",0)
            return True

        else:
            if rop:
                pos_to = self.strgs[self.bonus_strg].get_rect(0)
                rop = self.strgs[self.active_strg].move(pos_x=pos_to[0],pos_y=pos_to[1],speed=8,num_bottom=self.active_card,num_top=self.active_strg_top)
                return not rop

            else:
                self.strgs[self.active_strg].reset_rect()
                            
                for i in range(self.active_strg_top-self.active_card+1):
                    self.strgs[self.bonus_strg].set_no(self.strgs[self.active_strg].get_no(self.active_card+i),i)
                    self.strgs[self.active_strg].set_no(0,self.active_card+i)
                
                self.bonus = False
                self.active_now = False
                self.active_bonus_now = False
                self.active_stage = 0
                self.active_card = -1
                self.active_strg = -1
                self.active_befor = self.time
                return rop

class VSCpu(PlayAut):#AutをVSようにカードの位置を変えたやつ
    def __init__(self, level=1, frame_size=5, bgc=gpn.BGC, clock=300, surface=gpn.GAMENN):
        super().__init__(level, frame_size, bgc, clock, surface)
        for i in range(CARD_KAZU):#pos,init_posの変更
            ca = self.cards[i].get_init_pos()
            ca[0] = GAM_SIZE[0]+ca[0]
            self.cards[i].set_init_pos(ca)
            self.cards[i].set_pos(ca[0],ca[1])
            self.strgs[i].x = GAM_SIZE[0]+ self.strgs[i].x
            for j in range(C_MAX):
                ca = self.strgs[i].strg[j].get_init_pos()
                ca[0] = GAM_SIZE[0]+ca[0]
                self.strgs[i].strg[j].set_init_pos(ca)
                self.strgs[i].strg[j].set_pos(ca[0],ca[1])

    def cards_update1(self, num) -> bool:
        #self.cards = [lib.Card(0,rect=((CARD_X-CARD_ZURE_X*(i),CARD_Y),CARD_SIZE)) for i in range(CARD_KAZU)]
        self.cards[num] = self.cards[2]
        self.cards[num].movable_on()
        if num:#使ったカードが１（手元）の時
            self.cards[num].set_init_pos(((GAM_SIZE[0] +CARD_X-CARD_ZURE_X*1,CARD_Y),CARD_SIZE))
        else:#使ったカードが0（スペア）の時
            self.cards[num].set_init_pos(((GAM_SIZE[0] +CARD_X*2,CARD_Y),CARD_SIZE))

        for i in range(2,CARD_KAZU-1):#カードの入れる場所と初期位置を変更
            self.cards[i] = self.cards[i+1]
            self.cards[i].set_init_pos(((GAM_SIZE[0] +CARD_X-CARD_ZURE_X*i,CARD_Y),CARD_SIZE))

        no = self.cards[CARD_KAZU-2].get_no()#新しいカードを一番最後に入れる
        new_no = random.randint(RAND_MIN,RAND_MAX)
        while no == new_no:
            new_no = random.randint(RAND_MIN,RAND_MAX)
        self.cards[CARD_KAZU-1] = lib.Card(new_no,rect=((GAM_SIZE[0] +CARD_X-CARD_ZURE_X*(CARD_KAZU-1),CARD_Y),CARD_SIZE))
        self.cards[CARD_KAZU-1].set_pos(GAM_SIZE[0] -CARD_SIZE[0],CARD_Y)
        return True

    def gd_reset(self) -> None:
        self.bonus = False
        self.bonus_strg = -1

        self.cards = [lib.Card(0,rect=((GAM_SIZE[0] +CARD_X-CARD_ZURE_X*(i),CARD_Y),CARD_SIZE)) for i in range(CARD_KAZU)]
        for i in range(CARD_KAZU):
            card_no = random.randint(RAND_MIN,RAND_MAX)
            if i == 0:
                self.cards[i].set_pos(GAM_SIZE[0] +CARD_X*2,CARD_Y)
                self.cards[i].set_init_pos(((GAM_SIZE[0] +CARD_X*2,CARD_Y),CARD_SIZE))
            else:
                mae_no = self.cards[i-1].get_no()
                while mae_no == card_no:
                    card_no = random.randint(RAND_MIN,RAND_MAX)

            self.cards[i].set_no(card_no)
        self.cards[0].movable_on()
        self.cards[1].movable_on()

        self.strgs = [gpn.CardStorage(pos_x=GAM_SIZE[0] +gpn.STORAGE_X+(gpn.STORAGE_ZURE_X)*i) for i in range(OKIBA_KAZU)]#strage*4
        self.time = 0
        self.time_pose = 0
        self.time_st = 0
        self.score = 0

class PlayVS():
    def __init__(self,level, frame_size=5, bgc=gpn.BGC, clock=30, surface=gpn.GAMENN):
        self.player = gpn.PlayNormal(frame_size=frame_size,bgc=bgc,clock=clock,surface=surface)
        self.enemy = VSCpu(level=level,frame_size=frame_size,bgc=bgc,clock=clock,surface=surface)

        self.player_hp = 100
        self.enemy_hp = 100

        self.surface = surface
        self.disp_w, self.disp_h = self.surface.get_size()
        self.clock = pg.time.Clock()
        self.clock_time = clock
        self.bgc = bgc
        self.frame_size = frame_size

    def back_ground(self):
        return 0


    def main(self) -> int:
        #準備
        resu = ROOP_CODE#
        self.back_ground()
        pg.display.update()
        self.player.sound_bgm.play_sound("bgm",-1)
        while 1:
            self.clock.tick(self.clock_time)
            
            mo_pos = pg.mouse.get_pos()#マウスカーソルがsurfaceの上にないと止まる
            self.disp_w, self.disp_h = self.surface.get_size()
            if (mo_pos[0] < self.frame_size or self.disp_w + self.frame_size < mo_pos[0]) or (mo_pos[1] < self.frame_size or self.disp_h + self.frame_size < mo_pos[1]):
                self.player.window_out()
                #continue
            resu = self.player.befor_event()
            self.enemy.befor_event()
            self.enemy.active_mode()

            if resu != ROOP_CODE:
                return resu
            event = pg.event.get()
            if event != []:
                for ev in event:
                    self.player.ev_befor(ev)
                    self.back_ground()
                    pg.display.update()
                    if ev.type == pg.QUIT:
                        resu = self.player.ev_quit(ev)
                    elif ev.type == pg.MOUSEBUTTONDOWN or ev.type == pg.MOUSEBUTTONUP or ev.type == pg.MOUSEWHEEL or ev.type == pg.MOUSEMOTION:
                        resu = self.player.ev_mouse(ev)
                    elif ev.type == pg.KEYDOWN or ev.type == pg.KEYUP:
                        resu = self.player.ev_key(ev)
                    elif ev.type == pg.WINDOWENTER or ev.type == pg.WINDOWLEAVE or ev.type == pg.WINDOWFOCUSLOST or ev.type == pg.WINDOWCLOSE:
                        resu = self.player.ev_window(ev)
                    else:
                        resu = self.player.ev_other(ev)
                    self.player.ev_after(ev)

                    #print("R=",ROOP_CODE,", r=",resu)#デバッグ用,後で消す,コメントアウトでprintは大体デバッグ用
                    if resu != ROOP_CODE:
                        #print(resu,"ppp")
                        return resu

            else:
                self.back_ground()
                pg.display.update()
                self.player.ev_no_event()




if __name__ == "__main__":
    #vs = PlayAut(level=30,)
    vs = VSCpu(level=30)
    """
    vs.strgs[0].strg[0].set_no(10)
    for j in range(4):
        vs.cards[j].set_no(10)
        for i in range(9):
            vs.strgs[j].strg[i].set_no(10-i)
    vs.strgs[2].strg[4].set_no(8)#"""
    #vs.cards[1].set_no(10)
    a = vs.main()
    print(a)