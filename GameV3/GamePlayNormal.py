# coding=[shift-jis]


#上手くいくかな？
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
STORAGE_X = 40
STORAGE_Y = 40
STORAGE_ZURE_X = CARD_SIZE[0]*1.5
STORAGE_ZURE_Y = CARD_ZURE_Y

TIME_X = 20
TIME_Y = 10


SCORE_X = TIME_X#scoreの表示位置,画面の右端からの距離
SCORE_Y = TIME_Y+(TBOX_SIZE[1]+TBOX_ZURE_Y)*1#上からの距離

POSE_X = TIME_X#一時停止ボタンの表示位置
POSE_Y = TIME_Y+(TBOX_SIZE[1]+TBOX_ZURE_Y)*2

#SCORE_RECT = (SCORE_X,SCORE_Y,0,0)#rect型
#SCORE_T_RECT = (SCORE_T_X,SCORE_T_Y,0,0)
#POSE_RECT = (POSE_X,POSE_Y,0,0)


class CardStorage():#旧カード置き場クラス
    def __init__(self,pos_x=STORAGE_X,pos_y=STORAGE_Y,c_max=C_MAX) -> None:
        self.strg = [lib.Card(0,rect=((pos_x,pos_y+i*STORAGE_ZURE_Y),CARD_SIZE)) for i in range(c_max+1)]
        self.x = pos_x
        self.y = pos_y
        self.w = CARD_SIZE[0]
        self.h = STORAGE_ZURE_Y*(c_max+1) +CARD_SIZE[1]
        self.max = c_max#cardの最大枚数,実際にはmax+1枚置ける,最大枚数でも数値が同じときは置けるようにするため

    def z_to_m(self, num:int,Z=0,M=C_MAX) -> int:#numの値をZからMに制限する
        num = int(num)
        if num < Z:
            num = 0
        elif M < num:
            num = M
        return num

    def paint(self,chan=False) -> None:
        #"""
        for i in range(self.max):
            self.strg[i].paint(w_change=chan,w2_col=Iro.AO)
            if self.strg[i].hit():
                chan = False
            #print(i)
            if self.strg[i].get_no() == 0:#0のカードを1枚表示したら終わり
                break
        """
        top = self.get_top()
        for i in range(top+1):#topまで表示
            self.strg[i].paint()
        self.strg[top+1].paint(w_change=True)#"""
        
        #if self.get_top() >= self.max:
            #self.strg[self.max].paint(alpha=10,alpha2=255,w_change=chan)

    def paint_one(self,num, w_col=Iro.KURO,w2_col=Iro.KIMIDORI, alpha=255, alpha2=255, w_change=False, font=font) -> int:
        return self.strg[num].paint(w_col=w_col,w2_col=w2_col, alpha=alpha, alpha2=alpha2, w_change=w_change, font=font)


    def reset(self) -> None:#list:#カードの数字を全部0にする
        strg = self.strg
        n=0
        for s in range(self.max):
            self.strg[s].set_no(0)
            self.strg[s].set_pos(self.x,self.y+CARD_ZURE_Y*s)
            n+=1
        #return strg


    def noup_flag(self) -> bool:#↓noupメソッドを実行するフラグにした,stragにnoupできるとこがるときの判定にも使える
        #没　noupメソッドはPlayNormalに作る　こっちに作ると背面更新がいるから相互依存しちゃう
        top = self.get_top()#-1~self.max(たぶん9)
        if top < 1:#カードの枚数が2より小さいと0==0で次のif文を突破できちゃう
            return False
        else:
            if self.strg[top].get_no() == self.strg[top-1].get_no():
                return True
            else:
                if top == self.max-1:#top==8
                    if self.strg[top].get_no() == self.strg[top+1].get_no():#[8]==[9]
                        return True
                return False

    
    def move(self,pos_x:float,pos_y:float,speed=10,num_top=-1,num_bottom=-1) -> bool:#ストレージのカード複数を同時にmoveする
        top = self.get_top()
        num_top = self.z_to_m(num_top,M=top)#num_top(動かす一番鵺のカードの番号)を0~一番上に調整
        if num_bottom == -1:#初期値なら下を上と同じにする,一枚だけ動かす
            num_bottom = num_top
        else:
            num_bottom = self.z_to_m(num_bottom,M=num_top)#初期値以外なら調整

        for i in range(num_bottom,num_top+1):
            res = self.strg[i].move(pos_x=pos_x,pos_y=pos_y+CARD_ZURE_Y*(i-num_bottom),speed=speed)
            # self.okiba[i].idou(dx,dy+gk.C_ZUREY*(i-under),speed)
        return res

    def hit(self,num) -> bool:
        return self.strg[num].hit()

    def set_no(self, no:int, num:int) -> bool:#noが変更したい数字,numが変更する場所
        no = self.z_to_m(no,M=MAX_NO)
        num = self.z_to_m(num)

        return self.strg[num].set_no(no)

    
    def reset_rect(self):#ストレージの各カードを初期位置に戻す
        #self.strg = [lib.Card(0,rect=(pos_x,pos_y+i*CARD_ZURE_Y)) for i in range(c_max+1)]
        for i in range(self.max+1):
            self.strg[i].set_rect(((self.x,self.y+i*CARD_ZURE_Y),CARD_SIZE))


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

    def get_max(self) -> int:
        return self.max

class PlayNormal(lib.Scene):#ノーマルモードの管理クラス
    def __init__(self,bgc=BGC, surface=GAMENN):
        super().__init__(sounds={"bgm":"SE,BGM\\bgm_maoudamashii_neorock10.mp3", "gameover":"SE,BGM\se_maoudamashii_jingle02.mp3"} ,bgc=bgc, surface=surface)
        self.cards = [lib.Card(0,rect=((CARD_X-CARD_ZURE_X*(i),CARD_Y),CARD_SIZE)) for i in range(CARD_KAZU)]
        for i in range(CARD_KAZU):
            card_no = random.randint(RAND_MIN,RAND_MAX)
            if i == 0:
                self.cards[i].set_pos(CARD_X*2,CARD_Y)
                self.cards[i].set_init_pos(((CARD_X*2,CARD_Y),CARD_SIZE))
            else:
                mae_no = self.cards[i-1].get_no()
                while mae_no == card_no:
                    card_no = random.randint(RAND_MIN,RAND_MAX)

            self.cards[i].set_no(card_no)
        self.cards[0].movable_on()
        self.cards[1].movable_on()
                
        
        self.strgs = [CardStorage(pos_x=STORAGE_X+(STORAGE_ZURE_X)*i) for i in range(OKIBA_KAZU)]#strage*4

        self.bonus = False#2048ができてるかどうか
        self.bonus_strg = -1

        self.time = 0#時間を入れとくやつ
        self.time_pose = 0
        self.time_st = time.time()
        self.score = 0#スコアを入れとくやつ
        self.time_t = lib.TxtBox("0",rect=((SCORE_X,SCORE_Y+TBOX_ZURE_Y),TBOX_SIZE))#以下4つは表示用
        self.time_tbox = lib.TxtBox("時間",rect=((SCORE_X,SCORE_Y),TBOX_SIZE))
        self.score_t = lib.TxtBox("0",rect=((SCORE_X,SCORE_Y+(TBOX_ZURE_Y)*3),TBOX_SIZE))
        self.score_tbox = lib.TxtBox("スコア",rect=((SCORE_X,SCORE_Y+(TBOX_ZURE_Y)*2),TBOX_SIZE))

        self.pose_bottun = lib.Bottun(txt="一時停止",rect=((POSE_X, POSE_Y),TBOX_SIZE))#一時停止(pose)のボタン
        #self.gd = lib.GameData()

        self.sound_se = lib.Sound(sounds={"put":"SE,BGM\\analog_game_5.mp3","chain":"SE,BGM\se_maoudamashii_system23.mp3","bonus":"SE,BGM\maou_se_8bit21.mp3","pose":"SE,BGM\maou_se_8bit08.mp3","slid":"SE,BGM\se_maoudamashii_element_wind02.mp3"})
        self.sound_se.set_vol(3)
        

    def gd_lord(self,gamedata:list) -> bool:#ゲームデータクラスからデータを入れるメソッド
        for i in range(CARD_KAZU):
            self.cards[i].set_no(gamedata[0][i])
        for i in range(OKIBA_KAZU):
            for j in range(C_MAX):
                self.strgs[i].set_no(gamedata[1][i][j],j)
                if j==0:
                    break
        self.time_pose = gamedata[2]
        #self.time_t.set_txt(str(self.time))
        self.score = gamedata[3]
        #self.score_t.set_txt(str(self.score))
        return True

    def get_gd(self) -> lib.GameData:
        res = lib.GameData(list(self.cards[i].get_no() for i in range(CARD_KAZU)),list(list(self.strgs[i].get_no(j) for j in range(self.strgs[i].get_max())) for i in range(OKIBA_KAZU)),self.time,self.score)
        return res

    def gd_reset(self) -> None:
        self.bonus = False
        self.bonus_strg = -1

        self.cards = [lib.Card(0,rect=((CARD_X-CARD_ZURE_X*(i),CARD_Y),CARD_SIZE)) for i in range(CARD_KAZU)]
        for i in range(CARD_KAZU):
            card_no = random.randint(RAND_MIN,RAND_MAX)
            if i == 0:
                self.cards[i].set_pos(CARD_X*2,CARD_Y)
                self.cards[i].set_init_pos(((CARD_X*2,CARD_Y),CARD_SIZE))
            else:
                mae_no = self.cards[i-1].get_no()
                while mae_no == card_no:
                    card_no = random.randint(RAND_MIN,RAND_MAX)

            self.cards[i].set_no(card_no)
        self.cards[0].movable_on()
        self.cards[1].movable_on()

        self.strgs = [CardStorage(pos_x=STORAGE_X+(STORAGE_ZURE_X)*i) for i in range(OKIBA_KAZU)]#strage*4
        self.time = 0
        self.time_pose = 0
        self.time_st = 0
        self.score = 0

    def set_time_pose(self) -> None:
        self.time_pose = self.time

    

    def time_update(self) -> None:
        self.time = (((time.time()-self.time_st)//0.1)/10 + self.time_pose)//0.1/10#今-開始 +前回セーブした分
        if self.time >= 100000000:#桁の制限
            self.time = 99999999

    def back_ground(self,have=False) -> None:
        super().back_ground()

        #self.time = ((time.time()-self.time_st)//0.1)/10 + self.time_pose#今-開始 +前回セーブした分
        #if self.time >= 100000000:#桁の制限
        #    self.time = 99999999
        self.time_update()
        #lib.HighScoreRanking.paint()

        tb_pos = self.time_t.get_rect()#スコアとかの位置調整
        n_posx = self.disp_w - (TIME_X + tb_pos[2])
        if n_posx < STORAGE_X+(STORAGE_ZURE_X)*OKIBA_KAZU:
            n_posx = STORAGE_X+(STORAGE_ZURE_X)*OKIBA_KAZU +10
        self.time_t.set_txt(str(self.time))
        self.time_t.set_pos(n_posx,TIME_Y+TBOX_ZURE_Y)
        self.time_tbox.set_pos(n_posx,TIME_Y)
        self.score_t.set_txt(str(int(self.score)))
        self.score_t.set_pos(n_posx,SCORE_Y+TBOX_ZURE_Y)
        self.score_tbox.set_pos(n_posx,SCORE_Y)
        self.pose_bottun.set_pos(n_posx,POSE_Y)

        self.score_t.paint_txt()#スコア
        self.score_tbox.paint_txt()
        self.time_t.paint_txt()#時間
        self.time_tbox.paint_txt()
        
        self.pose_bottun.paint(Iro.AOMURASAKI)
        self.pose_bottun.paint_txt(add_y=10)

        for strg in self.strgs:#strgの表示
            top = strg.get_top()
            mx = strg.get_max()
            
            strg.paint()#chan=self.bonus)
            if top+1 < mx:
                strg.paint_one(strg.get_top()+1,alpha=0,alpha2=0,w_change=have)
            elif strg.get_no(top) in (self.cards[0].get_no(),self.cards[1].get_no()):
                strg.paint_one(strg.get_top()+1,alpha=100,alpha2=100,w_change=have)

        for i in range(len(self.cards)-1,-1,-1):#cardの表示
            self.cards[i].paint(w_change=self.cards[i].get_movable())

        if self.bonus:
            self.bonus_move()
        

    def noup(self,num:int) -> bool:#バグったw   num==stragの番号, strageのカードの数字を上げるメソッド,上がったらTrue
        if self.strgs[num].noup_flag():#Cardの数字が同じとき
            top = self.strgs[num].get_top()#一番上

            if self.strgs[num].get_no(top+1) != 0:
                top += 1
            ue_no = self.strgs[num].get_no(top-1)#一番上の一個下の番号
            pos_to = self.strgs[num].get_rect(top-1)#演出の準備
            #print(top)
            #pos_from = self.strgs[num].get_rect(top)
            fin = False
            self.sound_se.play_sound("chain",0)
            while not fin:#演出,self.yはpos_to[1]に近づいてるのにabs(pos_y-self.y)は大きくなってる
                fin = self.strgs[num].move(pos_to[0],pos_to[1],num_top=top,speed=0.5)
                self.back_ground()
                pg.display.update()
                        
            self.strgs[num].reset_rect()#元に戻す
            self.strgs[num].set_no(0,top)#ゼロにする
            self.strgs[num].set_no(ue_no+1,top-1)#
            return True
        return False

    def put(self,num:int,c_num:int) -> bool:#num==stragの番号,c_num=cardの番号 cardが置ける時に置いてTrue
        top = self.strgs[num].get_top()#-1~8
        card_no = self.cards[c_num].get_no()

        if top+1 < self.strgs[num].get_max():#カード枚数が最大値より小さいとき
            self.strgs[num].set_no(card_no,top+1)
        
        elif self.strgs[num].get_no(top) == card_no:#最大値だけど数値が同じとき
            self.strgs[num].set_no(card_no,top+1)

        else:#それ以外==置けなかったとき
            return False
        
        self.sound_se.play_sound("put",0)
        return True

    def cards_update(self,num) -> bool:#cardsを更新するメソッド,numには使ったカードの番号(0か1)を入れる
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

        move = False#移動
        move2 = False
        while not (move and move2):
            move = self.cards[num].came_back(speed=3)
            for i in range(2,CARD_KAZU-1):
                self.cards[i].came_back(speed=3)
            move2 = self.cards[CARD_KAZU-1].came_back(speed=10)
            self.back_ground()
            pg.display.update()

        return True

    def bonus_move(self) -> list:#2048を作ったボーナス
        for i in range(OKIBA_KAZU):
            top = self.strgs[i].get_top()
            for j in range(top,-1,-1):
                if self.strgs[i].hit(j):
                    rec = self.strgs[i].get_rect(j)
                    pg.draw.rect(self.surface,Iro.AO,(rec[0] -5,rec[1],rec[2] +5+5,STORAGE_ZURE_Y*(top-j+1) +rec[3] +5),2)#ここの+5はなくてもいいかも
                    return [i,j]

        return [-1,-1]


    def main(self) -> int:
        self.time_st = time.time()
        self.bonus = False
        self.bonus_strg = -1
        
        if self.cards[0].get_no() == 0:#初期化されてた時
            for i in range(CARD_KAZU):
                card_no = random.randint(RAND_MIN,RAND_MAX)
                if i == 0:
                    self.cards[i].set_pos(CARD_X*2,CARD_Y)
                    self.cards[i].set_init_pos(((CARD_X*2,CARD_Y),CARD_SIZE))
                else:
                    mae_no = self.cards[i-1].get_no()
                    while mae_no == card_no:
                        card_no = random.randint(RAND_MIN,RAND_MAX)

                self.cards[i].set_no(card_no)
            self.cards[0].movable_on()
            self.cards[1].movable_on()

        return super().main()

    def befor_event(self) -> int:
        super().befor_event()
        caunt = 0
        for i in range(OKIBA_KAZU):#GAMEOVERの判別
            top = self.strgs[i].get_top()
            if top+1 >= self.strgs[i].get_max():
                if not self.strgs[i].get_no(top) in (self.cards[0].get_no(),self.cards[1].get_no()):
                    caunt += 1
        if caunt >= OKIBA_KAZU:#GameOver
            self.sound_bgm.stop_sound("bgm")
            self.sound_bgm.play_sound("gameover",0)
            pg.time.wait(5000)
            return -1
        else:
            return ROOP_CODE

    def ev_after(self, event: pg.event) -> int:
        super().ev_after(event)
        #print(self.strgs[0].get_no(0))
        for i in range(OKIBA_KAZU):
            top = self.strgs[i].get_top()
            for j in range(top+1):
                if self.strgs[i].get_no(j) > 10:
                    #print("aaaaaaa")
                    self.strgs[i].reset()
                    self.sound_se.play_sound("bonus",0)
                    self.bonus = True
                    self.bonus_strg = i
                    break
        return ROOP_CODE

    def ev_no_event(self) -> int:
        super().ev_no_event()
        return -1

    def ev_mouse(self, event: pg.event) -> int:
        mov = False
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_bottun = pg.mouse.get_pressed()
            if mouse_bottun[0]:
                if self.bonus:#ボーナス処理
                    bou = self.bonus_move()
                    if not(bou[0] == -1 or bou[1] == -1):
                        self.bonus = False
                        btop = self.strgs[bou[0]].get_top()
                        
                        looop = False
                        pos_to = self.strgs[self.bonus_strg].get_rect(0)
                        self.sound_se.play_sound("slid",0)
                        while not looop:
                            self.back_ground()
                            looop = self.strgs[bou[0]].move(pos_x=pos_to[0],pos_y=pos_to[1],speed=8,num_bottom=bou[1],num_top=btop)
                            pg.display.update()
                        self.strgs[bou[0]].reset_rect()
                        self.back_ground()
                        pg.display.update()
                        
                        for i in range(btop-bou[1]+1):
                            self.strgs[self.bonus_strg].set_no(self.strgs[bou[0]].get_no(bou[1]+i),i)
                            self.strgs[bou[0]].set_no(0,bou[1]+i)
                        return ROOP_CODE

                mov_num = -1
                if self.pose_bottun.hit():#pose
                    self.sound_bgm.stop_sound("bgm")
                    self.sound_se.play_sound("pose",0)
                    return 1

                for i in [0,1]:#dragするかどうか
                    mov = self.cards[i].hit()
                    if mov:
                        mov_num = i
                        #self.cards[i].sound.play_sound("slid",0)
                        self.bonus = False
                        break
                if mov_num == -1:
                    return ROOP_CODE

                farst=True
                while mouse_bottun[0]:#ドラッグしてる間
                    mpos = pg.mouse.get_pos()
                    #dsize = self.surface.get_size()
                    if not(0 <mpos[0]< self.disp_w-CARD_SIZE[0]/2) or not(0 <mpos[1]< self.disp_h-CARD_SIZE[1]/2):
                        #print("soto")
                        break
                        """
                        while not mov:#問題点、ここで止まる
                            mov = self.cards[mov_num].came_back()
                            self.back_ground()
                            pg.display.update()
                        return ROOP_CODE#"""
                    mov = self.cards[mov_num].drag(mov,farst)
                    if farst:
                        self.sound_se.play_sound("slid",0)
                    farst = False
                    mouse_bottun = pg.mouse.get_pressed()
                    self.back_ground(have=True)
                    pg.display.update()

                
                mov = False
                for i in range(OKIBA_KAZU):
                    if self.strgs[i].hit(self.strgs[i].get_top()+1):
                        p = self.put(i,mov_num)
                        if p:#カードが置かれたとき
                            #self.cards_update(mov_num)
                            up = True
                            count=0
                            while up:
                                up = self.noup(i)
                                count +=1
                            self.score += (2**self.strgs[i].get_no(self.strgs[i].get_top()))*(count-1)
                            self.cards_update(mov_num)
                            return ROOP_CODE
                        #else:
                while not mov:#元の位置に戻す
                    mov = self.cards[mov_num].came_back()
                    self.back_ground()
                    pg.display.update()
        return ROOP_CODE



if __name__ == "__main__":
    game = PlayNormal()
    #"""
    for j in range(4):
        game.cards[j].set_no(2)
        for i in range(9):
            game.strgs[j].strg[i].set_no(10-i)#"""
    res = ROOP_CODE
    while 1:
        res = game.main()
        print(res)