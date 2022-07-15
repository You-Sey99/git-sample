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

class CardStorage():#旧カード置き場クラス
    def __init__(self,pos_x=STORAGE_X,pos_y=STORAGE_Y,c_max=C_MAX) -> None:
        self.strg = [lib.Card(0,rect=((pos_x,pos_y+i*STORAGE_ZURE_Y),CARD_SIZE)) for i in range(c_max+1)]
        self.x = pos_x
        self.y = pos_y
        self.w = CARD_SIZE[0]
        self.h = STORAGE_ZURE_Y*(c_max+1) +CARD_SIZE[1]
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

    def paint(self,chan=False) -> None:
        for i in range(self.max):
            self.strg[i].paint()
            if self.strg[i].get_no() == 0:#0のカードを1枚表示したら終わり
                break
        
        if self.get_top() >= self.max:
            self.strg[self.max].paint(alpha=0,alpha2=255,w_change=chan)


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

    def hit(self,num) -> bool:
        return self.strg[num].hit()

    def set_no(self, no:int, num:int) -> bool:#noが変更したい数字,numが変更する場所
        no = self.z_to_m(no,M=MAX_NO)
        num = self.z_to_m(num)

        return self.strg[num].set_no(no)

    
    def reset_rect(self):#ストレージの各カードを初期位置に戻す
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

    def get_max(self) -> int:
        return self.max

class PlayNormal(lib.Scene):#ノーマルモードの管理クラス
    def __init__(self, frame_size=5, bgc=BGC, clock=30, surface=GAMENN):
        super().__init__(frame_size, bgc, clock, surface)
        self.cards = [lib.Card(0,rect=((CARD_X-CARD_ZURE_X*(i-1),CARD_Y),CARD_SIZE)) for i in range(CARD_KAZU)]
        for i in range(CARD_KAZU):
            card_no = random.randint(RAND_MIN,RAND_MAX)
            if i == 0:
                self.cards[i].set_pos(CARD_X*2,CARD_Y)
            else:
                mae_no = self.cards[i-1].get_no()
                while mae_no == card_no:
                    card_no = random.randint(RAND_MIN,RAND_MAX)

            self.cards[i].set_no(card_no)
        self.cards[0].movable_on()
        self.cards[1].movable_on()
                
        self.strgs = [CardStorage(pos_x=STORAGE_X+(STORAGE_ZURE_X)*i) for i in range(OKIBA_KAZU)]
        self.time = 0
        self.score = 0

        self.pose_bottun = lib.Bottun(txt="一時停止",rect=(POSE_RECT))
        #self.gd = lib.GameData()

    def gd_lord(self,gamedata:list) -> bool:#ゲームデータクラスからデータを入れるメソッド
        for i in range(CARD_KAZU):
            self.cards[i].set_no(gamedata[0][i])
        for i in range(OKIBA_KAZU):
            for j in range(C_MAX):
                self.strgs[i].set_no(gamedata[1][j],j)
                if j==0:
                    break
        self.time = gamedata[2]
        self.score = gamedata[3]
        return True

    def get_gd(self) -> lib.GameData:
        return lib.GameData((self.cards[i].get_no() for i in range(CARD_KAZU)),((self.strgs[i].get_no(j) for j in range(self.strgs[i].get_max())) for i in range(OKIBA_KAZU)),self.time,self.score)

    def back_ground(self) -> None:
        super().back_ground()
        for strg in self.strgs:
            strg.paint()
        for i in range(len(self.cards)-1,-1,-1):
            self.cards[i].paint()
        

    def noup(self,num:int) -> bool:
        if self.strgs[num].noup_flag:
            top = self.strgs[num].get_top()
            if top > 1:
                ue = self.strgs[num].get_no(top-1)
                if self.strgs[num].get_no(top) == ue:
                    pos_to = self.strgs[num].get_rect(top-1)
                    #pos_from = self.strgs[num].get_card(top)
                    fin = False
                    while not fin:
                        fin = self.strgs[num].move(pos_to[0],pos_to[1],num_top=top)
                        self.back_ground()
                        pg.display.update()
                        
                    self.strgs[num].reset_rect()
                    self.strgs[num].set_no(0,top)
                    self.strgs[num].set_no(ue+1,top-1)
                    return True
        return False

    def put(self,num:int,c_num:int) -> bool:
        top = self.strgs[num].get_top()
        card_no = self.cards[c_num].get_no()

        if top < self.strgs[num].get_max():
            self.strgs[num].set_no(card_no,top+1)
        
        elif self.strgs[num].get_no(top) == card_no:
            self.strgs[num].set_no(card_no,top+1)

        else:
            return False
        
        return True

    def cards_update(self,num) -> bool:
        self.cards[num] = self.cards[2]
        self.cards[num].movable_on()

        for i in range(2,CARD_KAZU-1):
            self.cards[i] = self.cards[i+1]

        no = self.cards[CARD_KAZU-2].get_no()
        new_no = random.randint(RAND_MIN,RAND_MAX)
        while no == new_no:
            new_no = random.randint(RAND_MIN,RAND_MAX)
        self.cards[CARD_KAZU-1] = lib.Card(new_no,rect=((10,CARD_Y),CARD_SIZE))

        move = False
        rec = self.cards[CARD_KAZU-2].get_rect()
        while not move:
            move = self.cards[CARD_KAZU-1].move(rec[0],rec[1],(rec[0]-10)/CARD_SIZE[0]/10)
            self.cards[num].move(CARD_X+CARD_X*(1-num),CARD_Y)
            for i in range(2,CARD_KAZU-1):
                self.cards[i].move(CARD_X+CARD_ZURE_X*i,CARD_Y)
            self.back_ground()
            pg.display.update()

        return True

    def befor_event(self) -> int:
        res = super().befor_event()
        return res

    def ev_mouse(self, event: pg.event) -> int:
        mov = False
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_bottun = pg.mouse.get_pressed()
            if mouse_bottun[0]:
                mov_num = -1
                if self.pose_bottun.hit():
                    return 1
                for i in [0,1]:
                    mov = self.cards[i].hit()
                    if mov:
                        mov_num = i
                        break
                if mov_num == -1:
                    return ROOP_CODE

                while mouse_bottun[0]:#ドラッグしてる間
                    mpos = pg.mouse.get_pos()
                    #dsize = self.surface.get_size()
                    if not(0 <mpos[0]< self.disp_w-CARD_SIZE[0]) or not(0 <mpos[1]< self.disp_h-CARD_SIZE[1]):
                        while mov:#問題点、ここで止まる
                            mov = self.cards[mov_num].came_back()
                            self.back_ground()
                            pg.display.update()
                        return ROOP_CODE
                    mov = self.cards[mov_num].drag(mov)
                    mouse_bottun = pg.mouse.get_pressed()
                    self.back_ground()
                    pg.display.update()

                
                mov = False
                for i in range(OKIBA_KAZU):
                    if self.strgs[i].hit(self.strgs[i].get_top()+1):
                        p = self.put(i,mov_num)
                        if p:#カードが置かれたとき
                            self.cards_update(mov_num)
                            up = True
                            while up:
                                up = self.noup(i)
                            return ROOP_CODE
                        #else:
                while not mov:#元の位置に戻す
                                mov = self.cards[mov_num].move(CARD_X+CARD_X*(1-mov_num),CARD_Y)
                                self.back_ground()
                                pg.display.update()
                return ROOP_CODE



if __name__ == "__main__":
    game = PlayNormal()
    print(game.main(),"a")