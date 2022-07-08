# coding=[shift-jis]



import Iro_RGB as Iro
import pygame as pg
import numpy as np
import math
import sys 
import random
import time
from GameLocal import *

pg.init()#見える？
GAMENN = pg.display.set_mode(GAM_SIZE,pg.RESIZABLE)
pg.display.set_caption("Lib")


class Sound():#SEとかBGMを管理するクラス,インスタンス化して使う.
    def __init__(self,volum = 5,unit=SOUND_UNIT,sounds={}) -> None:
        if not pg.mixer.get_init:#mixirが初期化されてなかったら初期化する
            pg.mixer.init
        self.vol = volum#音量
        self.unit = unit#音量を調整する単位

        self.sounds = {}#辞書型で各音と名前をセットにする
        count = 0
        if isinstance(sounds,dict):#soundsが辞書型の時
            for i in sounds.values():#引数soundsの各要素を1つずつ取り出し
                if isinstance(sounds[i],pg.mixer.Sound):#Soundオブジェクトを渡してきたとき
                    self.sounds[i] = sounds[i]
                    self.sounds[i].set_volume(self.unit*self.vol)

                elif isinstance(sounds,str):#パスを指定してきたとき
                    try:
                        self.sounds[i] = pg.mixer.Sound(sounds[i])
                        self.sounds[i].set_volume(self.unit*self.vol)
                    except (FileNotFoundError):
                        count += 1
                
        if count > 0:
            print("era-\n can't found ",count, " files\n")

        if (len(self.sounds) < len(sounds)):#purは全部読込めたかどうか,
            self.pur = False#__init__は返り値を設定できないから一応インスタンス変数に入れておいた
        else:
            self.pur = True


    def set_vol(self,vol:int) -> int:#音量を変更するメソッド
        try:
            self.vol = int(vol)
        except(ValueError):
            return -1

        if self.vol < 0:
            self.vol = 0
        elif 1 < self.vol*self.unit:
            self.vol = int(1/self.unit)

        self.sounds.set_volume(self.unit*self.vol)

        return self.vol

    def set_unit(self,unit:float) -> float:#音量変更の単位を変えるメソッド
        try:
            self.unit = float(unit)
        except(ValueError):
            return -1.0

        if self.unit <= 0:
            self.unit = 0.01
        elif 1 < self.unit:
            self.unit = 1.0

        return self.unit

    def add_sounds(self,sounds:dict) -> int:#音の種類を追加するメソッド
        count = 0
        if isinstance(sounds,dict):#soundsが辞書型の時
            for i in sounds.values():
                if i in self.sounds:
                    count += 1

                if isinstance(sounds[i],pg.mixer.Sound):
                    self.sounds[i] = sounds[i]
                    self.sounds[i].set_volume(self.unit*self.vol)

                elif isinstance(sounds,str):
                    try:
                        self.sounds[i] = pg.mixer.Sound(sounds[i])
                        self.sounds[i].set_volume(self.unit*self.vol)
                    except (FileNotFoundError):
                        print("can't found ", i, " filse\n")
                
        return count


    def del_sounds(self,key:str) -> pg.mixer.Sound:#音の種類を減らすメソッド
        if isinstance(key,str):#soundsが辞書型の時
            if key in self.sounds:
                return self.sounds.pop(key)
            else:
                print("\"",key,"\" key is not found\n")
                return None
        
        elif key == -1:
            print("sounds all clear\n")
            self.sounds.clear()
        
        return None

    def play_sound(self,key:str,count:int) -> bool:#keyに一致する音を再生するメソッド,count=-1でずっと繰り返し
        if isinstance(key,str):#keyがstr型の時
            if key in self.sounds:#keyがsoundsの中にあるとき
                try:#回数をキャストできなかったら1回
                    count = int(count)
                except:
                    count = 1

                self.sounds[key].play(count)
                return True

        return False

    def stop_sound(self,key:str) -> bool:#keyに一致する音の再生を停止するメソッド
        if isinstance(key,str):#keyがstr型の時
            if key in self.sounds:#keyがsoundsの中にあるとき
                self.sounds[key].stop()
                return True
        return False

    
    def get_sounds(self,key="") -> pg.mixer.Sound:
        if isinstance(key,str):#keyがstr型の時
            if key in self.sounds:#keyがsoundsの中にあるとき
                return self.sounds[key]

        print("can't found this key\n")
        return None

    def get_vol(self) -> int:
        return self.vol

    def get_unit(self) -> float:
        return self.unit

                
class GameData():#ゲームデータのやり取りをするクラス,あったら便利だと思ったから作った
    def __init__(self,card_no=[0 for i in range(CARD_KAZU)],okiba_no=[[0 for i in range(C_MAX)] for j in range(OKIBA_KAZU)],time=float(0),score=0) -> None:
        self.card_no=[0 for i in range(CARD_KAZU)]#最初にデータを入れる場所を作る
        self.okiba_no=[[0 for i in range(C_MAX)] for j in range(OKIBA_KAZU)]
        count = 0

        for i in range(CARD_KAZU):#ここからデータを取り込んでいく
            try:#プレイヤーがいじれるところにはできるだけtryを付けたい
                self.card_no[i] = int(card_no[i])
            except (IndexError,ValueError):#エラー名のところは一個なら()はいらない
                self.card_no[i] = random.randint(RAND_MIN,RAND_MAX)
                count = 1
            
            if self.card_no[i] < RAND_MIN or RAND_MAX <= self.card_no[i]:
                    self.card_no[i] = random.randint(RAND_MIN,RAND_MAX)
                    count = 1
        if count:#データの取り込みがうまくいってないとこがあったら教える
            print("era- :can't get card\n")#<-は実際にエラーにして文章を表示することもできる
            count = 0


        for i in range(OKIBA_KAZU):#↑とおんなじ感じ
            for j in range(C_MAX):
                try:
                    self.okiba_no[i][j] = int(okiba_no[i][j])
                except(ValueError,ImportError):
                    self.okiba_no[i][j] = [k+1 for k in range(C_MAX)]
                    count = 1

                if self.okiba_no[i][j] < 0 or MAX_NO < self.okiba_no[i][j]:
                    self.okiba_no[i] = [k+1 for k in range(C_MAX)]
                    count = 1            
            if count:
                print("era- :can't get card_okiba",i ,"\n")
                count = 0


        try:
            self.time = float(time)
        except (ValueError):
            print("era- :can't get time\n")
            self.time = 0

        try:
            self.score = int(score)
        except (ValueError):
            print("era- :can't get score\n")
            self.score = 0
        
    def set_card(self, card_no:list) -> bool:#この後のset系はCardとかStrageとかだけデータを取り込むメソッド
        count = True
        for i in range(CARD_KAZU):
            try:
                card_no[i] = int(card_no[i])
            except (IndexError,ValueError):
                count = False
                break
            
            if card_no[i] < RAND_MIN or RAND_MAX <= card_no[i]:
                    count = False
        if count:
            self.card_no = card_no

        return count

    def set_strage_no(self, no:int, okiba_c_no:list) -> bool:
        self.okiba_no[no]
        count=True
        for j in range(C_MAX):
            try:
                okiba_c_no[j] = int(okiba_c_no[j])
            except (ValueError,ImportError):
                count = False
                break

            if okiba_c_no[j] < 0 or MAX_NO < okiba_c_no[j]:
                count = False
                break
        if count:
            self.okiba_no = okiba_c_no

        return count

    def set_time(self, time:float) -> bool:
        try:
            self.time = float(time)
        except (ValueError):
            return False
        return True

    def set_score(self, score:int) -> bool:
        try:
            self.score = float(score)
        except (ValueError):
            return False
        return True

    def set_gamedata(self, gamedata:list) -> bool:#これはsetメソッド4つを一気にできるメソッド
        card = self.card_no
        okiba = self.okiba_no
        time = self.time
        score = self.score
        res = True
        res = res and self.set_card(gamedata[0])
        for i in range(OKIBA_KAZU):
            res = res and self.set_strage_no(gamedata[1][i])
        res = res and self.set_time(gamedata[2])
        res = res and self.set_score(gamedata[3])

        if res:
            pass
        else:
            self.card_no = card
            self.okiba_no = okiba
            self.time = time
            self.score = score

        return res

    def get_gamedata(self) -> list:
        return [self.card_no,self.okiba_no,self.time,self.score]

    def install(self) -> list:#ファイルからデータを取り込むメソッド
        try:#ゲームデータを取得
            with open("GameData.txt",mode="r") as g_data:
                card = g_data.readline()
                strg = [[] for i in range(OKIBA_KAZU)]
                for i in range(OKIBA_KAZU):
                    strg[i] = g_data.readline()
                time = g_data.readline()
                score = g_data.readline()
        except FileNotFoundError:
            print("era- :can't find file\ncreat no data file\n")
            self.save()

        num = ""
        a = 0
        card2 = [ 0 for i in range(CARD_KAZU)]
        for t in card:
            if t == "\n" or a>=CARD_KAZU:
                break
            elif t in (",","[","]"," "):
                if num != "":
                    card2[a] = int(num)
                    a += 1
                    num = ""
            elif t in (str(i) for i in range(MAX_NO)):
                num += t
            else:
                continue
                #raise ValueError("era- :GameData is breaked\n")


        num = ""
        a=0
        strg2 = [[] for i in range(OKIBA_KAZU)]
        for j in range(OKIBA_KAZU):
            for t in strg[j]:
                if t == "\n" or a>=CARD_KAZU:
                    break
                elif t in (",","[","]"," "):
                    if num != "":
                        strg2[j][a] = int(num)
                        a += 1
                        num = ""
                elif t in (str(i) for i in range(MAX_NO)):
                    num += t
                else:
                    continue
                    #raise ValueError("era- :GameData is breaked\n")
        time2 = ""
        fl = True
        for t in time:
            if t in (str(i) in range(0,11,1)):
                time2 = time2+t
            elif t == "." and fl:
                time2 = time2+t
                fl = False
            elif time2 != "":
                break
        
        score2 = ""
        for t in score:
            if t in (str(i) in range(0,11,1)):
                score2 = score2+t
            elif score2 != "":
                break

        res = self.set_gamedata([card2,strg2,time2,score2])
        if res:
            return [card2,strg2,time2,score2]
        else:
            return [None]

    def save(self) -> None:#ファイルにデータを書き込むメソッド
        with open("GameData.txt",'w') as g_data:
            g_data.write(self.card_no)
            g_data.write("\n")
            for i in range(OKIBA_KAZU):
                g_data.write(self.okiba_no[i])
                g_data.write("\n")
            g_data.write(self.time)
            g_data.write("\n")
            g_data.write(self.score)
            g_data.write("\n")


class Scene():#ゲームの各場面を管理するクラスの元,必要なメソッドだけオーバーライドして使う想定
    def __init__(self, frame_size=5, bgc=Iro.IRO_List[Iro.iro_num(Iro.MOKKASIN)], clock=30, surface=GAMENN):
        self.surface = surface
        self.disp_w, self.disp_h = self.surface.get_size()
        self.clock = pg.time.Clock()
        self.clock_time = clock
        self.bgc = bgc
        self.frame_size = frame_size
#kokomade

    def main(self) -> None:#メインループ,
        while 1:
            self.clock.tick(self.clock_time)
            mo_pos = pg.mouse.get_pos()
            self.disp_w, self.disp_h = self.surface.get_size()
            if (mo_pos[0] < self.frame_size or self.disp_w + self.frame_size < mo_pos[0]) or (mo_pos[1] < self.frame_size or self.disp_h + self.frame_size < mo_pos[1]):
                self.window_out()
            self.befor_event()
            event = pg.event.get()
            if event != []:
                for ev in event:
                    self.ev_befor(ev)
                    self.back_ground()
                    pg.display.update()
                    if ev.type == pg.QUIT:
                        self.ev_quit(ev)
                    elif ev.type == pg.MOUSEBUTTONDOWN or ev.type == pg.MOUSEBUTTONUP or ev.type == pg.MOUSEWHEEL or ev.type == pg.MOUSEMOTION:
                        self.ev_mouse(ev)
                    elif ev.type == pg.KEYDOWN or ev.type == pg.KEYUP:
                        self.ev_key(ev)
                    elif ev.type == pg.WINDOWENTER or ev.type == pg.WINDOWLEAVE or ev.type == pg.WINDOWFOCUSLOST or ev.type == pg.WINDOWCLOSE:
                        self.ev_window(ev)
                    else:
                        self.ev_other(ev)
                    self.ev_after

            else:
                self.back_ground()
                pg.display.update()
                self.ev_no_event()


    def befor_event(self) -> None:#イベント取得前にやること
        pass

    def window_out(self) -> None:#マウスカーソルが指定範囲外に出たときにやること
        pass

    #ev_シリーズは各イベントを処理するメソッド,主にこれをオーバーライドする
    def ev_befor(self, event:pg.event) -> None:#イベントを処理する前に毎回やること
        pass

    def ev_quit(self,event:pg.event) -> None:#右上の×を押したときのやつ
        if event.type == pg.QUIT:
            sys.exit()

    def ev_mouse(self,event:pg.event) -> None:#マウス関連のイベント
        pass

    def ev_key(self,event:pg.event) -> None:#キーボードが押されたor放した時のイベント
        pass

    def ev_window(self, event:pg.event) -> None:#画面から出たり,画面に入ったりした時のイベント,たぶん使わん
        pass

    def ev_no_event(self) -> None:#イベントが何もなかった時にやるイベント
        pass

    def ev_other(self, event:pg.event) -> None:#上に描かれてないイベントが起こったときのイベント
        pass

    def ev_after(self, event:pg.event) -> None:#イベントを処理した後に毎回やること
        pass

    def back_ground(self) -> None:#背景の更新,デフォルトで背景の塗りつぶしと外枠の(サイズ変更+表示)をする
        #display.updateをここに入れると追加でカードとかを表示するときにチカチカするから別にしとく
        self.surface.fill(self.bgc)#背景の塗りつぶし
        self.disp_w, self.disp_h = self.surface.get_size()#画面のサイズを取得
        pg.draw.rect(self.surface,Iro.KURO, (0,0,self.disp_w,self.disp_h),width=self.frame_size)#画面の外枠を表示


class Box():#Card,TxtBox,Bottunのもとになるクラス
    def __init__(self, rect=((CARD_X,CARD_Y),CARD_SIZE), kado=KADO_DEFO, surface=GAMENN, img=None) -> None:
        np_rect = np.array(rect)#ここと一個下の文でrectの形をそろえる
        np_rect = np_rect.flatten()
        self.x = float(np_rect[0])
        self.y = float(np_rect[1])
        self.wide = float(np_rect[2])
        self.high = float(np_rect[3])

        self.kado = int(kado)#角の丸み

        self.rect = (self.x, self.y, self.wide, self.high)#rect型で扱った方が楽なところもあるから用意した,x,y,wide,highをいじるときはこれも書き換えるかset_posとかで書き換えること
        self.sur = surface#表示する画面の指定
        if isinstance(img,pg.Surface):#表示する画像の設定,初期値では画像無し,分岐はSoundsクラスのとこと一緒
            self.img = img
        elif isinstance(type(img), str):
            try:
                self.img = pg.image.load(img).convert_alpha()
            except (FileNotFoundError):
                print("era- :no such this file\n")
                self.img = None
        else:
            self.img = None
        
        
    def paint(self,col=Iro.KURO,alpha=255) -> None:#pygameの四角を表示するメソッド,alphaで透明度を変えれる(0~255)
        coler = col + (alpha, )
        pg.draw.rect(self.sur, coler, self.rect, border_radius=self.kado)

    def paint_img(self, alpha=255,add_x=0,add_y=0) -> bool:#画像を表示するメソッド,画像がないときはFalseを返す
        if self.img == None:
            return False
        else:
            self.img.set_alpha(alpha)
            self.sur.blit(self.img, (self.x+add_x,self.y+add_y))
            return True


    def hit(self) -> bool:#マウスカーソルが四角の中にあるかを判定するメソッド
        pg.event.get()
        (mausu_x,mausu_y) = pg.mouse.get_pos()
        if self.x < mausu_x and mausu_x < self.x + self.wide:
            if self.y < mausu_y and mausu_y < self.y + self.high:
                return True
        #print("MISS")
        return False


    def set_rect(self,rect:pg.rect) -> bool:#rectを変更するメソッド,たぶんそのうち他のsetメソッドも含めてtryは消す
        try:
            self.x = float(rect[0])
            self.y = float(rect[1])
            self.wide = float(rect[2])
            self.high = float(rect[3])
            self.rect = (self.x, self.y, self.wide, self.high)
            return True
        except (ValueError,IndexError):
            self.x = self.rect[0]
            self.y = self.rect[1]
            self.wide = self.rect[2]
            self.high = self.rect[3]
            return False

    def set_rect_img(self) -> bool:#四角の大きさを画像と同じにするメソッド,上手くいくかわからん
        if self.img == None:
            return False
        else:
            rec = self.img.get_rect()
            res = self.set_rect(rec)
            return res

    def set_kado(self,kado:int) -> bool:
        try:
            self.kado = int(kado)
            return True
        except ValueError:
            return False

    def set_pos(self, x:float,y:float) -> bool:
        try:
            self.x = float(x)#キャスト
            self.y = float(y)#
            if self.x<0:#範囲外なら調整
                self.x=0
            if self.y<0:#
                self.y=0
            self.rect = (self.x, self.y, self.wide, self.high)
            return True
        except (ValueError):#キャストするとこ
            self.x = self.rect[0]
            self.y = self.rect[1]
            return False
        except (TypeError):#範囲外なら調整の所
            return False

    def set_img(self, img:pg.surface) -> bool:#画像を変更するメソッド,ここのtryはいるけど完成してない
        try:
            self.img = img
            return True
        except (TypeError):
            return False

    def set_img_pos(self, pas:str) -> bool:
        try:
            self.img = pg.image.load(pas).convert_alpha(self.sur)
            return True
        except (FileNotFoundError):
            return False

    def set_img_size(self, size=[-1,-1]) -> bool:
        if self.img is None:
            return None

        else:
            try:
                if size[0]<0 or size[1]<0:
                    size = [self.wide,self.high]
                
                pg.transform.scale(self.img, size)
                return True
            except (IndexError):
                return False


    def get_rect(self) -> pg.rect:
        return (self.x,self.y,self.wide,self.high)

    def get_kado(self) -> int:
        return self.kado

    def get_img(self) -> pg.surface:
        return self.img

    def get_img_size(self):
        return self.img.get_size()


class Card(Box):#カードのクラス
    def __init__(self, c_no:int, rect=((CARD_X, CARD_Y), CARD_SIZE), kado=KADO_DEFO, surface=GAMENN, img=None) -> None:
        super().__init__(rect, kado, surface, img)
        self.init_pos = self.rect#カードの初期位置,元の位置に戻すときに使う
        self.no = int(c_no)#数字
        self.movable = False#dragで動かせるかどうか


    def paint(self, w_col=Iro.KURO,w2_col=Iro.KIMIDORI, alpha=255, alpha2=255, w_change=False, font=font) -> int:#w_change=Trueかつhit()で枠と透明度とかが2の方に変わる
        super().paint(Iro.IRO_List[self.no%COL_LAS], alpha)#本体
        if w_change and self.hit():
            w2_coler = w2_col + (alpha2, )
            pg.draw.rect(self.sur,w2_coler, self.rect, width=WAKU_DEFO, border_radius=KADO_DEFO)#枠
        else:
            w_coler = w_col + (alpha, )
            pg.draw.rect(self.sur,w_coler, self.rect, width=WAKU_DEFO, border_radius=KADO_DEFO)#枠

        if self.no == 0:#数字の表示
            text = font.render('-',True,Iro.KURO)
        elif 1 <= self.no and self.no <=MAX_NO:
            text = font.render(str(2**self.no),True,Iro.KURO)
        elif self.no == MAX_NO:
            text = font.render('',True,Iro.KURO)
        else:
            text = font.render('era---',True,Iro.KURO)
        self.sur.blit(text, (self.x+5,self.y+5))

    def paint_img(self, alpha=255, add_x=0, add_y=0) -> bool:#画像の表示
        g_w, g_h = self.img.get_size()
        g_w = self.high - g_w#画像とカードの表示位置の左下を合わせてる,もとは左上で合わせてあった
        g_h = self.wide - g_h
        result = super().paint_img(alpha, add_x, g_h+add_y)
        return result

    def drag(self,catch=True) -> bool:#カードをドラッグするメソッド,使い方は下の「デバッグ用」のところにある
        res = self.hit()#memo ^- back_ground関数を渡したい <- 他のとこと相互に関連するからできればやめたい <- dragの使い方を工夫した
        if self.movable and (res or catch):
            #print("mo")
            mp = pg.mouse.get_pos()#マウスの位置を取得
            x = mp[0] - self.wide/2#カードの真ん中にマウスカーソルが来るようにした
            y = mp[1] - self.high/2
            self.set_pos(x,y)#カードの位置の更新
        else:
            pass

        return res


    def move(self, pos_x:float,pos_y:float,speed=10) -> bool:#カードを指定した場所までもっていくメソッド,旧idouの改良版
        if abs(pos_x -self.x) <= speed or abs(pos_y - self.y) <= speed:#近くに来たら合わせる
            self.x = pos_x
            self.y = pos_y
            self.set_pos(self.x,self.y)
            return True
        else:#どんな角度でも同じ速さで動く.はず
            if pos_x == self.x:
                siita = math.radians(90)
            else:
                tan = ((pos_y - self.y)/(pos_x - self.x))
                siita = math.atan(tan)#-pi/2~pi/2
            #print(siita/math.pi,"π\n")
            if pos_x < self.x:#この時がおかしい <- なおした
                speed = -speed

            #print("rad=",siita/math.pi,"π\n")
            self.x = self.x + speed*math.cos(siita)
            self.y = self.y + speed*math.sin(siita)
            self.set_pos(self.x,self.y)
            return False

    def came_back(self,speed=10) -> bool:#カードを初期位置に戻すメソッド,大まかな使い方はmoveと一緒
        return self.move(self.init_pos[0],self.init_pos[1],speed=speed)

    def set_no(self, no:int) -> bool:#setシリーズ
        try:
            no = int(no)
            if no < 0 or MAX_NO < no:
                no = 0
                
            self.no = no
            return True
        except (ValueError):
            return False

    def movable_on(self)->bool:#これもsetと同じだけどTrueとFalseしかないから専用のやつを作った
        self.movable = True
        return self.movable

    def movable_off(self)->bool:
        self.movable = False
        return self.movable

    def set_init_pos(self,rect:pg.Rect) -> bool:
        rect = np.array(rect)
        rect = np.reshape(rect,(4, ))
        self.init_pos = rect
        return True

    def get_init_pos(self) -> pg.Rect:#getシリーズ,
        return self.init_pos

    def get_movable(self) -> bool:
        return self.movable

    def get_no(self) -> int:
        return self.no

class TxtBox(Box):#文字を表示できるようになったBox
    def __init__(self, txt:str,fonnt=font, rect=((CARD_X, CARD_Y), CARD_SIZE), kado=KADO_DEFO, surface=GAMENN, img=None) -> None:
        super().__init__(rect, kado, surface, img)
        self.txt = str(txt)#文字
        self.font= fonnt#フォント

    def paint_txt(self,col=Iro.KURO,add_x=5,add_y=5) -> str:#文字だけ表示
        text = font.render(self.txt,True,col)
        self.sur.blit(text, (self.x+add_x,self.y+add_y))
        return self.txt

    def set_txt(self, txt:str) -> str:#setシリーズ
        old = self.txt
        self.txt = str(txt)
        return old

    def set_font(self,font=font) -> None:
        self.font = font

    def get_font(self) -> pg.font:#getシリーズ
        return self.font

    def get_txt(self) -> str:
        return self.txt

class Bottun(TxtBox):#クリックとかしたら反応するボタンのクラス
    def __init__(self, txt: str, fonnt=font, rect=((CARD_X, CARD_Y), CARD_SIZE), kado=KADO_DEFO, surface=GAMENN, img=None) -> None:
        super().__init__(txt, fonnt, rect, kado, surface, img)

    def hit(self):#ボタンを押したら押された演出をする,...予定
        res = super().hit()
        if res:
            pass
            #ボタンが押される演出、音とか動き
        return res





if __name__ == "__main__":#デバッグ用
    GAMENN.fill(Iro.SIRO)
    a = Card(0)
    a.paint(alpha=230)
    a.set_img(pg.image.load("GameV3/gazou/migi.png"))
    a.paint_img()
    a.movable_on()
    pg.display.update()
    break_code = False
    can = False
    cb = False
    drg = False

    def bg_update():
        GAMENN.fill(Iro.PINNKU)
        a.paint(alpha=200)
        a.paint_img(alpha=100)
        pg.display.update()

    while 1:
        event = pg.event.get()

        if event != []:
            bg_update()
            for ev in range(len(event)):
                if event[ev].type == pg.QUIT:
                    fin = input("owaru?(y/n) -> ")
                    if fin =="y" or fin == "yes":
                        break_code = True
                        break

                elif event[ev].type == pg.KEYDOWN:
                    #print("p")
                    posi = a.get_rect()
                    can = a.set_pos(str(10+posi[0]),str(10 +posi[1]))
                    if not can:
                        print("Sippai")
                    bg_update()
                    

                elif event[ev].type == pg.MOUSEBUTTONDOWN:
                    mb = pg.mouse.get_pressed()#dragの使い方はここ
                    while mb[0]:
                        drg = a.drag(drg)
                        mb = pg.mouse.get_pressed()
                        bg_update()
                    else:
                        drg = False
                        while not drg:
                            drg = a.came_back()
                            bg_update()

                        

        if break_code:
            break

