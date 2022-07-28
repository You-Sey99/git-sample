# coding=[shift-jis]



from multiprocessing.connection import wait
from re import S
import Iro_RGB as Iro
import GameLib as lib
from GameLocal import *
import GamePlayNormal as gpn
import pygame as pg
import sys 
import random
import time


LIFE_BAR_SIZE = (300,40)
LIFE_BAR_X = 100
LIFE_BAR_Y = CARD_Y+CARD_SIZE[1]+30
LIFE_BAR_FRAME = (LIFE_BAR_X-5,LIFE_BAR_Y-5,LIFE_BAR_SIZE[0]+10,LIFE_BAR_SIZE[1]+10)

E_LIFE_BAR_X = GAM_SIZE[0]+LIFE_BAR_X
E_LIFE_BAR_Y = LIFE_BAR_Y
E_LIFE_BAR_FRAME = (E_LIFE_BAR_X-5,E_LIFE_BAR_Y-5,LIFE_BAR_SIZE[0]+10,LIFE_BAR_SIZE[1]+10)


class VSGameData():
    def __init__(self,card_no=[0 for i in range(CARD_KAZU)],okiba_no=[[0 for i in range(C_MAX)] for j in range(OKIBA_KAZU)],time=float(0),score=0,hp=0, max_hp=0  ,card_no2=[0 for i in range(CARD_KAZU)],okiba_no2=[[0 for i in range(C_MAX)] for j in range(OKIBA_KAZU)],time2=float(0),score2=0,hp2=0,max_hp2=0) -> None:
        self.pl_gd = lib.GameData(card_no=card_no,okiba_no=okiba_no,time=time,score=score)
        self.en_gd = lib.GameData(card_no=card_no2,okiba_no=okiba_no2,time=time2,score=score2)

        try:
            self.pl_hp = int(hp)
            self.en_hp = int(hp2)
            self.pl_hp_m = int(max_hp)
            self.en_hp_m = int(max_hp2)
        except (ValueError):
            print("era- :can't get hp data\n")
            self.pl_hp = 0
            self.en_hp = 0
            self.pl_hp_m = 0
            self.en_hp_m = 0


    def set_card(self, card_no:int,card_no2:int) -> bool:
        res = self.pl_gd.set_card(card_no=card_no)
        res2 = self.en_gd.set_card(card_no=card_no2)
        return res and res2

    def set_strag_no(self, no:int,okiba_no:int, no2:int,okiba_no2:int) -> bool:
        res = self.pl_gd.set_strage_no(no=no,okiba_c_no=okiba_no)
        res2 = self.en_gd.set_strage_no(no=no2,okiba_c_no=okiba_no2)
        return res and res2

    def set_time(self, time:float,time2:float) -> bool:
        res = self.pl_gd.set_time(time=time)
        res2 = self.en_gd.set_time(time=time2)
        return res and res2

    def set_score(self, score:int,score2:int) -> bool:
        res = self.pl_gd.set_score(score=score)
        res2 = self.en_gd.set_score(score=score2)
        return res and res2

    def set_hp(self, hp:int,max_hp:int, hp2:int,max_hp2:int) -> bool:
        try:
            hp = int(hp)
            max_hp = int(max_hp)
            hp2 = int(hp2)
            max_hp2 = int(max_hp2)

            self.pl_hp = int(hp)
            self.en_hp = int(hp2)
            self.pl_hp_m = int(max_hp)
            self.en_hp_m = int(max_hp2)
        except (ValueError):
            return False

    def set_gamedata(self, gamedata:list) -> bool:
        res = self.pl_gd.set_gamedata(gamedata=gamedata[0])
        res2 = self.en_gd.set_gamedata(gamedata=gamedata[2])
        res3 = self.set_hp(gamedata[1][0],gamedata[1][1],gamedata[3][0],gamedata[3][1])
        return res and res2 and res3

    def get_gamedata(self) -> list:
        gd_1 = self.pl_gd.get_gamedata()
        gd_2 = self.en_gd.get_gamedata()
        return [gd_1, [self.pl_hp,self.pl_hp_m], gd_2, [self.en_hp, self.en_hp_m]]



    def install(self, mod=2):
        try:#ゲームデータを取得
            with open("GameData"+str(mod)+".txt",mode="r") as g_data:
                card = g_data.readline()
                strg = [[] for i in range(OKIBA_KAZU)]
                for i in range(OKIBA_KAZU):
                    strg[i] = g_data.readline()
                time = g_data.readline()
                score = g_data.readline()
                hp = g_data.readline()
                max_hp = g_data.readline()

                card2 = g_data.readline()
                strg2 = [[] for i in range(OKIBA_KAZU)]
                for i in range(OKIBA_KAZU):
                    strg2[i] = g_data.readline()
                time2 = g_data.readline()
                score2 = g_data.readline()
                hp2 = g_data.readline()
                max_hp2 = g_data.readline()


        except FileNotFoundError:
            print("era- :can't find file\ncreat no data file\n")
            self.pl_gd = lib.GameData()
            self.en_gd = lib.GameData()
            self.pl_hp = 0
            self.pl_hp_m = 0
            self.en_hp = 0
            self.en_hp_m = 0
            return [self.pl_gd.get_gamedata(), [self.pl_hp,self.pl_hp_m], self.en_gd.get_gamedata(), [self.en_hp,self.en_hp_m]]
            #self.save()



        #pl
        num = ""
        a = 0
        card_sub = [ 0 for i in range(CARD_KAZU)]
        for t in card:
            if t == "\n" or a>=CARD_KAZU:
                break
            elif t in (",","[","]"," "):
                if num != "":
                    card_sub[a] = int(num)
                    a += 1
                    num = ""
            elif t in (str(i) for i in range(MAX_NO)):
                num += t
            else:
                continue
   
        num = ""
        a=0
        strg_sub = [[0 for i in range(C_MAX)] for j in range(OKIBA_KAZU)]
        for j in range(OKIBA_KAZU):
            a=0
            for t in strg[j]:
                if t == "\n" or a>=C_MAX:
                    break
                elif t in (",","[","]"," "):
                    if num != "":
                        strg_sub[j][a] = int(num)
                        a += 1
                        num = ""
                elif t in (str(i) for i in range(MAX_NO)):
                    num += t
                else:
                    continue
                    #raise ValueError("era- :GameData is breaked\n")

        time = float(time)
        score = int(score)
        res = self.pl_gd.set_gamedata([card_sub,strg_sub,time,score])



        #en
        num = ""
        a = 0
        card_sub = [ 0 for i in range(CARD_KAZU)]
        for t in card2:
            if t == "\n" or a>=CARD_KAZU:
                break
            elif t in (",","[","]"," "):
                if num != "":
                    card_sub[a] = int(num)
                    a += 1
                    num = ""
            elif t in (str(i) for i in range(MAX_NO)):
                num += t
            else:
                continue
   


        num = ""
        a=0
        strg_sub = [[0 for i in range(C_MAX)] for j in range(OKIBA_KAZU)]
        for j in range(OKIBA_KAZU):
            a=0
            for t in strg2[j]:
                if t == "\n" or a>=C_MAX:
                    break
                elif t in (",","[","]"," "):
                    if num != "":
                        strg_sub[j][a] = int(num)
                        a += 1
                        num = ""
                elif t in (str(i) for i in range(MAX_NO)):
                    num += t
                else:
                    continue
                    #raise ValueError("era- :GameData is breaked\n")

        time2 = float(time2)
        score2 = int(score2)
        res2 = self.en_gd.set_gamedata([card_sub,strg_sub,time2,score2])


        #hp
        self.pl_hp = int(hp)
        self.pl_hp_m = int(max_hp)
        self.en_hp = int(hp2)
        self.en_hp_m = int(max_hp2)

        if res and res2:
            return [self.pl_gd.get_gamedata(), [self.pl_hp,self.pl_hp_m], self.en_gd.get_gamedata(), [self.en_hp,self.en_hp_m]]
        else:
            return [None]



    def save(self, mod=2):
        with open("GameData"+str(mod)+".txt",'w') as g_data:
            g_data.write(str(self.pl_gd.card_no))
            g_data.write("\n")
            for i in range(OKIBA_KAZU):
                g_data.write(str(self.pl_gd.okiba_no[i]))
                g_data.write("\n")
            g_data.write(str(self.pl_gd.time))
            g_data.write("\n")
            g_data.write(str(self.pl_gd.score))
            g_data.write("\n")
            g_data.write(str(self.pl_hp))
            g_data.write("\n")
            g_data.write(str(self.pl_hp_m))
            g_data.write("\n")

            g_data.write(str(self.en_gd.card_no))
            g_data.write("\n")
            for i in range(OKIBA_KAZU):
                g_data.write(str(self.en_gd.okiba_no[i]))
                g_data.write("\n")
            g_data.write(str(self.en_gd.time))
            g_data.write("\n")
            g_data.write(str(self.en_gd.score))
            g_data.write("\n")
            g_data.write(str(self.en_hp))
            g_data.write("\n")
            g_data.write(str(self.en_hp_m))
            g_data.write("\n")




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
        bairitu = 10
        
        move = self.cards[num].came_back(speed=3*bairitu)
        for i in range(2,CARD_KAZU-1):
            self.cards[i].came_back(speed=3*bairitu)
        move2 = self.cards[CARD_KAZU-1].came_back(speed=10*bairitu)

        return move and move2

    def noup1(self, num: int) -> bool:
        if self.strgs[num].noup_flag():#Cardの数字が同じとき
            self.sound_se.play_sound("chain",0)
            return True
        
        return False
           
    def noup2(self, num: int) -> bool:#移動
        top = self.active_strg_top-1
        #ue_no = self.strgs[num].get_no(top -1)#一番上の一個下の番号
        pos_to = self.strgs[num].get_rect(top-1)#演出の準備
        #print(top)
        #pos_from = self.strgs[num].get_rect(top)
        #演出,self.yはpos_to[1]に近づいてるのにabs(pos_y-self.y)は大きくなってる
        fin = self.strgs[num].move(pos_to[0],pos_to[1],num_top=top,speed=0.5*10)
        return fin

    
    def noup3(self, num: int) -> bool:
        top = self.active_strg_top-1
        ue_no = self.strgs[num].get_no(top -1)#一番上の一個下の番号
        self.strgs[num].reset_rect()#元に戻す
        self.strgs[num].set_no(0,top)#ゼロにする
        self.strgs[num].set_no(ue_no+1,top-1)#
        return True

    def noup(self, rop:bool) -> bool:
        if self.active_noup == 1:#noupの判定
            self.count += 1
            self.active_strg_top = self.strgs[self.active_strg].get_top() +1
            rop = self.noup1(self.active_strg)#noupできるかできないかの判別
            if rop:
                self.active_noup = 2#noupを次に
            else:
                self.active_stage += 1#ステージを次に
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

            elif self.active_now:
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
            self.res = False
            self.active_now = True

            #ここからは別のメソッドにして同時操作できるようにする
            #ここに書くとこっちを実行中にもう片方が止まる
        #self.active_mode()

        return super().befor_event()


    def active(self, rop:bool) -> bool:
        if self.active_now:
            #一番有効な場所にカードを動かす
            if self.active_stage == 0:
                if not rop:
                    pos = self.strgs[self.active_strg].get_rect(self.active_strg_top)
                    rop = self.cards[self.active_card].move(pos_x=pos[0], pos_y=pos[1], speed=50)
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
                    self.cards[self.active_card].set_pos(self.disp_w,CARD_Y)
                    return True

                else:#できなかったら
                    self.active_stage = 0
                    self.active_now = False
                    self.res = False
                    return False

            #noupの処理をする
            elif self.active_stage == 2:
                rop = self.noup(rop)
                return rop

            
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
                    return True

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

class VSNormal(PlayAut):
    def __init__(self, level=1, frame_size=5, bgc=gpn.BGC, clock=300, surface=gpn.GAMENN):
        super().__init__(level, frame_size, bgc, clock, surface)

    def ev_mouse1(self, event: pg.event) -> int:#どの操作をしたのか
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.active_stage == 0:
                mouse_bottun = pg.mouse.get_pressed()
                if mouse_bottun[0]:
                    if self.bonus:#ボーナス処理
                        bou = self.bonus_move()
                        if not(bou[0] == -1 or bou[1] == -1):
                            self.active_bonus_now = True
                            self.active_card = bou[1]
                            self.active_strg = bou[0]

                    
                    elif self.pose_bottun.hit():#pose
                        self.sound_bgm.stop_sound("bgm")
                        self.sound_se.play_sound("pose",0)
                        return 1

                    else:
                        for i in [0,1]:#dragするかどうか
                            mov = self.cards[i].hit()
                            if mov:
                                #self.cards[i].sound.play_sound("slid",0)
                                self.bonus = False
                                self.active_now = True
                                self.active_card = i
                                self.active_stage = 1
                                self.res = False
                                break

        return ROOP_CODE


    def ev_mouse2(self) -> int:#dragしてる時の操作
        mou = pg.mouse.get_pressed()
        if mou[0]:
            #self.active_now = True
            self.cards[self.active_card].drag(catch=True)
        
        else:
            #self.active_now = False
            p = False
            for i in range(OKIBA_KAZU):
                if self.strgs[i].hit(self.strgs[i].get_top()+1):
                    p = self.put(i, self.active_card)
                    self.active_strg = i
                    self.active_strg_top = self.strgs[i].get_top() +1
                    break
            if p:
                self.active_stage = 2
            else:
                self.active_stage = 5
                self.active_strg = -1
                #self.active_card = -1
                #self.active_now = False

        return ROOP_CODE


    def ev_mouse3(self,rop:bool) -> bool:
        rop = self.noup(rop=rop)
        return rop

    def ev_mouse4(self, rop:bool) -> bool:
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
            return True

    def active(self, rop: bool) -> bool:
        if self.active_stage == 1:
            self.ev_mouse2()

        elif self.active_stage == 2:
            rop = self.ev_mouse3(rop=rop)

        elif self.active_stage == 3:
            rop = self.ev_mouse4(rop=rop)

        elif self.active_stage == 5:#ev_mo2でputできなかったとき
            rop = self.cards[self.active_card].came_back(speed=80)
            if rop:
                self.active_stage = 0
                self.active_strg = -1
                self.active_card = -1
                self.active_now = False


        else:
            self.active_now = False
        
        return rop

    def active_mode(self) -> None:
        if self.active_bonus_now:
            self.res = self.active_bonus(rop=self.res)

        elif self.active_now:
            self.res = self.active(rop=self.res)


class PlayVS():
    def __init__(self, life=3000, hande=0, level=30, frame_size=5, bgc=gpn.BGC, clock=30, surface=gpn.GAMENN):
        self.surface = surface
        self.disp_w, self.disp_h = self.surface.get_size()
        self.clock = pg.time.Clock()
        self.clock_time = clock
        self.bgc = bgc
        self.frame_size = frame_size

        self.player = VSNormal(frame_size=frame_size,bgc=bgc,clock=clock,surface=surface)
        self.enemy = VSCpu(level=level,frame_size=frame_size,bgc=bgc,clock=clock,surface=surface)

        self.player_hp = int(life)#HP
        self.enemy_hp = int(life - hande)
        self.player_hp_m = int(life)#MAX_HP
        self.enemy_hp_m = int(life - hande)
        self.win = 0#勝敗

        self.player_hpbar = lib.Box(surface=self.surface, rect=((LIFE_BAR_X,LIFE_BAR_Y),LIFE_BAR_SIZE))#HPの表示用
        self.player_hpbar_b = lib.Box(surface=self.surface, rect=((LIFE_BAR_X,LIFE_BAR_Y),LIFE_BAR_SIZE))
        self.player_hpbar_f = lib.Box(surface=self.surface, rect=LIFE_BAR_FRAME)

        self.enemy_hpbar = lib.Box(surface=self.surface, rect=((E_LIFE_BAR_X,E_LIFE_BAR_Y),LIFE_BAR_SIZE))
        self.enemy_hpbar_b = lib.Box(surface=self.surface, rect=((E_LIFE_BAR_X,E_LIFE_BAR_Y),LIFE_BAR_SIZE))
        self.enemy_hpbar_f = lib.Box(surface=self.surface, rect=E_LIFE_BAR_FRAME)

        self.sound_se = lib.Sound(sounds={"damage":"SE,BGM\maou_se_8bit28.mp3","win":"SE,BGM\maou_se_inst_guitar15.mp3","lose":"SE,BGM\se_maoudamashii_jingle02.mp3"})
 

    def damage(self, scr:int) -> int:
        if scr < 10:
            return 0
        else:
            score = scr
            n = 1
            while score >= 10:
                score = int(score/10)
                n += 1

            dam = (10+score) * ((n-1)**2)
            return int(dam)

    def life_bar_update(self) -> None:
        wari = (self.enemy_hp)/(self.enemy_hp_m)
        self.enemy_hpbar.set_rect(((E_LIFE_BAR_X,E_LIFE_BAR_Y),(LIFE_BAR_SIZE[0]*wari,LIFE_BAR_SIZE[1])))

        wari = (self.player_hp)/self.player_hp_m
        self.player_hpbar.set_rect(((LIFE_BAR_X,LIFE_BAR_Y),(LIFE_BAR_SIZE[0]*wari,LIFE_BAR_SIZE[1])))



    def ba_g1(self, have:bool, add:float) -> None:
        self.surface.fill(self.bgc)#背景の塗りつぶし
        self.disp_w, self.disp_h = self.surface.get_size()#画面のサイズを取得
        pg.draw.rect(self.surface,Iro.KURO, (0,0,self.disp_w,self.disp_h),width=self.frame_size)#画面の外枠を表示


    def ba_g_p(self, have:bool) -> None:
        for strg in self.player.strgs:#strgの表示 by player
            top = strg.get_top()
            mx = strg.get_max()
            
            strg.paint()#chan=self.bonus)
            if top+1 < mx:
                strg.paint_one(strg.get_top()+1,alpha=0,alpha2=0,w_change=have)
            elif strg.get_no(top) in (self.player.cards[0].get_no(),self.player.cards[1].get_no()):
                strg.paint_one(strg.get_top()+1,alpha=100,alpha2=100,w_change=have)

        for i in range(len(self.player.cards)-1,-1,-1):#cardの表示 by player
            self.player.cards[i].paint(w_change=self.player.cards[i].get_movable())

        if self.player.bonus:
            self.player.bonus_move()


    def ba_g_e(self, have:bool) -> None:
        for strg in self.enemy.strgs:#strgの表示 by enemy
            top = strg.get_top()
            mx = strg.get_max()
            
            strg.paint()#chan=self.bonus)
            if top+1 < mx:
                strg.paint_one(strg.get_top()+1,alpha=0,alpha2=0,w_change=have)
            elif strg.get_no(top) in (self.enemy.cards[0].get_no(),self.enemy.cards[1].get_no()):
                strg.paint_one(strg.get_top()+1,alpha=100,alpha2=100,w_change=have)

        for i in range(len(self.enemy.cards)-1,-1,-1):#cardの表示 by enemy
            self.enemy.cards[i].paint(w_change=self.enemy.cards[i].get_movable())


    def ba_g_box(self, add:float) -> None:
        self.player.time_update()
        self.enemy.time_update()

        tb_pos = self.player.time_t.get_rect()#スコアとかの位置調整
        n_posx = self.disp_w - (gpn.TIME_X + tb_pos[2])
        if n_posx < gpn.STORAGE_X+(gpn.STORAGE_ZURE_X)*OKIBA_KAZU:
            n_posx = gpn.STORAGE_X+(gpn.STORAGE_ZURE_X)*OKIBA_KAZU +10
        self.player.time_t.set_txt(str(abs(add -self.enemy.time)))
        self.player.time_t.set_pos(n_posx,gpn.TIME_Y+TBOX_ZURE_Y)
        self.player.time_tbox.set_pos(n_posx,gpn.TIME_Y)
        self.player.score_t.set_txt(str(int(self.player.score)))
        self.player.score_t.set_pos(n_posx,gpn.SCORE_Y+TBOX_ZURE_Y)
        self.player.score_tbox.set_pos(n_posx,gpn.SCORE_Y)
        self.player.pose_bottun.set_pos(n_posx,gpn.POSE_Y)

        self.player.score_t.paint_txt()#スコア
        self.player.score_tbox.paint_txt()
        self.player.time_t.paint_txt()#時間
        self.player.time_tbox.paint_txt()
        
        self.player.pose_bottun.paint(Iro.AOMURASAKI)
        self.player.pose_bottun.paint_txt(add_y=10)


    def back_ground(self, add=0, have=False, gaov=False):
        self.enemy.time_update()
        self.player.time_update()
        self.enemy.active_mode()
        self.player.active_mode()

        self.ba_g1(have=have,add=add)
        self.ba_g_e(have=have)
        self.ba_g_box(add=add)
        self.ba_g_p(have=have)

        self.player_hpbar_f.paint(col=Iro.GINNIRO)
        self.player_hpbar_b.paint(col=Iro.AKA)
        self.player_hpbar.paint(col=Iro.KIMIDORI)

        self.enemy_hpbar_f.paint(col=Iro.GINNIRO)
        self.enemy_hpbar_b.paint(col=Iro.AKA)
        self.enemy_hpbar.paint(col=Iro.KIMIDORI)
        

        if gaov:#ゲームオーバー
            rec = [[self.disp_w/4,self.disp_h/4],[self.disp_w/2,self.disp_h/2]]
            rec_ga = self.player.gameovera.get_rect()
            if rec[1][0] < rec_ga[2]:
                rec[1][0] = rec_ga[2]

            elif rec[1][1] < rec_ga[3]:
                rec[1][1] = rec_ga[3]
            
            self.player.gameovera.set_rect(rect=rec)
            self.player.gameovera.paint(Iro.SIRO)
            self.player.gameovera.paint_txt(Iro.KURO,add_x=rec[1][0]/2 -170, add_y=rec[1][1]/2 -35)#350,70
        return 0

    def gd_init(self) -> None:
            self.player_hp_m = 3000
            self.enemy_hp_m = 3000
            self.player_hp = 3000
            self.enemy_hp = 3000
            self.enemy.active_befor = 0
            self.player.active_befor = 0

            for i in range(CARD_KAZU):
                card_no = random.randint(RAND_MIN,RAND_MAX)
                if i == 0:
                    self.player.cards[i].set_pos(CARD_X*2,CARD_Y)
                    self.player.cards[i].set_init_pos(((CARD_X*2,CARD_Y),CARD_SIZE))
                else:
                    mae_no = self.player.cards[i-1].get_no()
                    while mae_no == card_no:
                        card_no = random.randint(RAND_MIN,RAND_MAX)

                self.player.cards[i].set_no(card_no)
            self.player.cards[0].movable_on()
            self.player.cards[1].movable_on()

            for i in range(CARD_KAZU):
                card_no = random.randint(RAND_MIN,RAND_MAX)
                if i == 0:
                    self.enemy.cards[i].set_pos(GAM_SIZE[0] +CARD_X*2,CARD_Y)
                    self.enemy.cards[i].set_init_pos(((GAM_SIZE[0] +CARD_X*2,CARD_Y),CARD_SIZE))
                else:
                    mae_no = self.enemy.cards[i-1].get_no()
                    while mae_no == card_no:
                        card_no = random.randint(RAND_MIN,RAND_MAX)

                self.enemy.cards[i].set_no(card_no)
            self.enemy.cards[0].movable_on()
            self.enemy.cards[1].movable_on()

    def main(self) -> int:
        #準備
        self.player.time_st = time.time()
        self.player.bonus = False
        self.player.bonus_strg = -1
        self.player.active_now = False

        self.enemy.time_st = time.time()
        self.enemy.bonus = False
        self.enemy.bonus_strg = -1
        self.enemy.active_now = False

        #self.enemy.active_befor = 0
        #self.player.active_befor = 0

        if 0 in (self.player.cards[0].get_no(),self.enemy.cards[0].get_no(),self.player_hp_m,self.enemy_hp_m):
            self.gd_init()

        resu = ROOP_CODE#
        self.back_ground()
        pg.display.update()
        self.player.sound_bgm.play_sound("bgm",-1)
        while 1:
            self.clock.tick(self.clock_time)
            if self.enemy.time -self.enemy.active_befor > self.enemy.active_time:
                print(self.enemy.time," : ",self.enemy.active_befor,"\n",self.enemy.active_now,"\n")
            
            dam = self.damage(self.player.score)
            if dam != 0:
                self.enemy_hp -= dam
                self.player.score = 0
                self.sound_se.play_sound("damage",0)
                if self.enemy_hp <= 0:
                    self.win = 10

            dam = self.damage(self.enemy.score)
            if dam != 0:
                self.player_hp -= dam
                self.enemy.score = 0
                self.sound_se.play_sound("damage",0)
                if self.player_hp <= 0:
                    self.win = -10

            self.life_bar_update()
            if self.win != 0:
                if self.win > 0:
                    self.player.gameovera.set_txt("YOU WIN!!")
                    self.sound_se.play_sound("win",0)
                else:
                    self.player.gameovera.set_txt("YOU LOSE..")
                    self.sound_se.play_sound("lose",0)

                self.back_ground(gaov=True)
                pg.display.update()
                pg.time.wait(5000)
                return -1

            mo_pos = pg.mouse.get_pos()#マウスカーソルがsurfaceの上にないと止まる
            self.disp_w, self.disp_h = self.surface.get_size()
            if (mo_pos[0] < self.frame_size or self.disp_w + self.frame_size < mo_pos[0]) or (mo_pos[1] < self.frame_size or self.disp_h + self.frame_size < mo_pos[1]):
                self.player.window_out()
                #continue

            resu = self.player.befor_event()
            self.enemy.befor_event()
            #self.enemy.active_mode()
            #self.player.active_mode()

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
                        resu = self.player.ev_mouse1(ev)
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

    def gd_lord(self,gamedata:list) -> bool:
        res = self.player.gd_lord(gamedata=gamedata[0])
        res2 = self.enemy.gd_lord(gamedata=gamedata[2])
        self.player_hp = gamedata[1][0]
        self.player_hp_m = gamedata[1][1]
        self.enemy_hp = gamedata[3][0]
        self.enemy_hp_m = gamedata[3][1]
        self.enemy.active_befor = 0
        self.player.active_befor = 0

        return res and res2

    def gd_reset(self) -> None:
        self.player.gd_reset()
        self.enemy.gd_reset()
        self.player_hp = 0
        self.player_hp_m = 0
        self.enemy_hp = 0
        self.enemy_hp_m = 0
        self.win = 0
        self.enemy.active_befor = 0
        self.player.active_befor = 0

    def get_gd(self) -> VSGameData:
        pl = self.player.get_gd()
        pld = pl.get_gamedata()

        en = self.enemy.get_gd()
        end = en.get_gamedata()

        res = VSGameData(*pld,self.player_hp,self.player_hp_m, *end,self.enemy_hp,self.enemy_hp_m)
        return res


    def set_vol(self,bgc_vol:int,se_vol:int) -> None:
        se_vol = int(se_vol)
        bgc_vol = int(bgc_vol)
        self.player.set_vol(bgc_vol=bgc_vol,se_vol=se_vol)
        self.enemy.set_vol(bgc_vol=bgc_vol,se_vol=se_vol)
        self.sound_se.set_vol(se_vol)




if __name__ == "__main__":
    vs = PlayAut(level=30,)
    #vs = PlayVS(level=300,life=30)
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