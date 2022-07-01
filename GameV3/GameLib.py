# coding=[shift-jis]



import Iro_RGB as Iro
import pygame as pg
import numpy as np
import math
import sys 
import random
import time
from GameLocal import *

pg.init()
GAMENN = pg.display.set_mode(GAM_SIZE,pg.RESIZABLE)
pg.display.set_caption("Lib")


class Sound():
    def __init__(self,vol = 5,unit=SOUND_UNIT,sounds={}) -> None:
        if not pg.mixer.get_init:
            pg.mixer.init
        self.vol = vol
        self.unit = unit

        self.sounds = {}
        count = 0
        if isinstance(sounds,dict):#soundsが辞書型の時
            for i in sounds.values():
                if isinstance(sounds[i],pg.mixer.Sound):
                    self.sounds[i] = sounds[i]
                    self.sounds[i].set_volume(self.unit*self.vol)

                elif isinstance(sounds,str):
                    try:
                        self.sounds[i] = pg.mixer.Sound(sounds[i])
                        self.sounds[i].set_volume(self.unit*self.vol)
                    except (FileNotFoundError):
                        count += 1
                
        if count > 0:
            print("era-\n can't found ",count, " files\n")

        if (len(self.sounds) < len(sounds)):
            self.pur = False

        else:
            self.pur = True


    def set_vol(self,vol:int) -> int:
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

    def set_unit(self,unit:float) -> float:
        try:
            self.unit = float(unit)
        except(ValueError):
            return -1.0

        if self.unit <= 0:
            self.unit = 0.01
        elif 1 < self.unit:
            self.unit = 1.0

        return self.unit

    def add_sounds(self,sounds:dict) -> int:
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


    def del_sounds(self,key:str) -> pg.mixer.Sound:
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

    def play_sound(self,key:str,count:int) -> bool:
        if isinstance(key,str):#keyがstr型の時
            if key in self.sounds:#keyがsoundsの中にあるとき
                try:#回数をキャストできなかったら1回
                    count = int(count)
                except:
                    count = 1

                self.sounds[key].play(count)
                return True

        return False

    def stop_sound(self,key:str) -> bool:
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
                
class GameData():
    def __init__(self,card_no=[0 for i in range(CARD_KAZU)],okiba_no=[[0 for i in range(C_MAX)] for j in range(OKIBA_KAZU)],time=float(0),score=0) -> None:
        self.card_no=[0 for i in range(CARD_KAZU)]
        self.okiba_no=[[0 for i in range(C_MAX)] for j in range(OKIBA_KAZU)]
        count = 0

        for i in range(CARD_KAZU):
            try:
                self.card_no[i] = int(card_no[i])
            except (IndexError,ValueError):
                self.card_no[i] = random.randint(RAND_MIN,RAND_MAX)
                count = 1
            
            if self.card_no[i] < RAND_MIN or RAND_MAX <= self.card_no[i]:
                    self.card_no[i] = random.randint(RAND_MIN,RAND_MAX)
                    count = 1
        if count:
            print("era- :can't get card\n")
            count = 0


        for i in range(OKIBA_KAZU):
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
        
    def set_card(self, card_no:list) -> bool:
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

    def set_gamedata(self, gamedata:list) -> bool:
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

    def install(self) -> list:
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

    def save(self) -> None:
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


class Scene():
    def __init__(self, frame_size=5, bgc=Iro.IRO_List[Iro.iro_num(Iro.MOKKASIN)], clock=30, surface=GAMENN):
        self.surface = surface
        self.disp_w, self.disp_h = self.surface.get_size()
        self.clock = pg.time.Clock()
        self.clock_time = clock
        self.bgc = bgc
        self.frame_size = frame_size

    def main(self) -> None:
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


    def befor_event(self) -> None:
        pass

    def window_out(self) -> None:
        pass

    def ev_befor(self, event:pg.event) -> None:
        pass

    def ev_quit(self,event:pg.event) -> None:
        if event.type == pg.QUIT:
            sys.exit()

    def ev_mouse(self,event:pg.event) -> None:
        pass

    def ev_key(self,event:pg.event) -> None:
        pass

    def ev_window(self, event:pg.event) -> None:
        pass

    def ev_no_event(self) -> None:
        pass

    def ev_other(self, event:pg.event) -> None:
        pass

    def ev_after(self, event:pg.event) -> None:
        pass

    def back_ground(self) -> None:#display.updateは別にしとく
        self.surface.fill(self.bgc)
        self.disp_w, self.disp_h = self.surface.get_size()
        pg.draw.rect(self.surface,Iro.KURO, (0,0,self.disp_w,self.disp_h),width=self.frame_size)


class Box():
    def __init__(self, rect=((CARD_X,CARD_Y),CARD_SIZE), kado=KADO_DEFO, surface=GAMENN, img=None) -> None:
        np_rect = np.array(rect)
        np_rect = np.reshape(np_rect,(4, ))
        self.x = float(np_rect[0])
        self.y = float(np_rect[1])
        self.wide = float(np_rect[2])
        self.high = float(np_rect[3])

        self.kado = int(kado)

        self.rect = (self.x, self.y, self.wide, self.high)
        self.sur = surface
        if isinstance(img,pg.Surface):
            self.img = img
        elif isinstance(type(img), str):
            try:
                self.img = pg.image.load(img).convert_alpha()
            except (FileNotFoundError):
                print("era- :no such this file\n")
                self.img = None
        else:
            self.img = None
        
        
    def paint(self,col=Iro.KURO,alpha=255) -> None:
        coler = col + (alpha, )
        pg.draw.rect(self.sur, coler, self.rect, border_radius=self.kado)

    def paint_img(self, alpha=255,add_x=0,add_y=0) -> bool:
        if self.img == None:
            return False
        else:
            self.img.set_alpha(alpha)
            self.sur.blit(self.img, (self.x+add_x,self.y+add_y))
            return True


    def hit(self):
        pg.event.get()
        (mausu_x,mausu_y) = pg.mouse.get_pos()
        if self.x < mausu_x and mausu_x < self.x + self.wide:
            if self.y < mausu_y and mausu_y < self.y + self.high:
                return True
        #print("MISS")
        return False


    def set_rect(self,rect:pg.rect) -> bool:
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

    def set_img(self, img:pg.surface) -> bool:
        try:
            self.img = img
            return True
        except (TypeError):
            return False

    def set_imgpas(self, pas:str) -> bool:
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


class Card(Box):
    def __init__(self, c_no:int, rect=((CARD_X, CARD_Y), CARD_SIZE), kado=KADO_DEFO, surface=GAMENN, img=None) -> None:
        super().__init__(rect, kado, surface, img)
        try:
            self.no = int(c_no)
        except (ValueError):
            self.no = 0

        self.movable = False



    def paint(self, w_col=Iro.KURO,w2_col=Iro.KIMIDORI, alpha=255, alpha2=255, w_change=False, font=font) -> int:
        super().paint(Iro.IRO_List[self.no%COL_LAS], alpha)
        if w_change and self.hit():
            w2_coler = w2_col + (alpha2, )
            pg.draw.rect(self.sur,w2_coler, self.rect, width=WAKU_DEFO, border_radius=KADO_DEFO)
        else:
            w_coler = w_col + (alpha, )
            pg.draw.rect(self.sur,w_coler, self.rect, width=WAKU_DEFO, border_radius=KADO_DEFO)

        if self.no == 0:
            text = font.render('-',True,Iro.KURO)
        elif 1 <= self.no and self.no <=MAX_NO:
            text = font.render(str(2**self.no),True,Iro.KURO)
        elif self.no == MAX_NO:
            text = font.render('',True,Iro.KURO)
        else:
            text = font.render('era---',True,Iro.KURO)
        self.sur.blit(text, (self.x+5,self.y+5))

    def paint_img(self, alpha=255, add_x=0, add_y=0) -> bool:#これ要る？
        g_w, g_h = self.img.get_size()
        g_w = self.high - g_w#画像とカードの表示位置の左下を合わせてる
        g_h = self.wide - g_h
        result = super().paint_img(alpha, add_x, g_h+add_y)
        return result

    def drag(self):
        if self.movable and self.hit():
            mp = pg.mouse.get_pos()
            self.x = mp[0]
            self.y = mp[1]
        return mp

    def move(self, pos_x:float,pos_y:float,speed=10) -> bool:
        if abs(pos_x -self.x) <= speed or abs(pos_y - self.y) <= speed:#近くに来たら合わせる
            self.x = pos_x
            self.y = pos_y
            return True
        else:#どんな角度でも同じ速さで動く.はず
            tan = (pos_y - self.y)/(pos_x - self.x)
            siita = math.atan(tan)
            self.x = speed*math.cos(siita)
            self.y = speed*math.sin(siita)
            return False

    def set_no(self, no:int) -> bool:
        try:
            no = int(no)
            if no < 0 or MAX_NO < no:
                no = 0
                
            self.no = no
            return True
        except (ValueError):
            return False

    def movable_on(self)->bool:
        self.movable = True
        return self.movable

    def movable_off(self)->bool:
        self.movable = False
        return self.movable

    def get_movable(self) -> bool:
        return self.movable

    def get_no(self) -> int:
        return self.no

class TxtBox(Box):
    def __init__(self, txt:str,fonnt=font, rect=((CARD_X, CARD_Y), CARD_SIZE), kado=KADO_DEFO, surface=GAMENN, img=None) -> None:
        super().__init__(rect, kado, surface, img)
        self.txt = str(txt)
        self.font= fonnt

    def paint_txt(self,col=Iro.KURO,add_x=5,add_y=5) -> str:
        text = font.render(self.txt,True,col)
        self.sur.blit(text, (self.x+add_x,self.y+add_y))
        return self.txt

    def set_txt(self, txt:str) -> str:
        old = self.txt
        self.txt = str(txt)
        return old

    def get_txt(self) -> str:
        return self.txt

class Bottun(TxtBox):
    def __init__(self) -> None:
        super().__init__()






if __name__ == "__main__":
    GAMENN.fill(Iro.SIRO)
    a = Card(0)
    a.paint(alpha=230)
    a.set_img(pg.image.load("gazou/migi.png"))
    a.paint_img()
    pg.display.update()
    break_code = False
    can = False

    while 1:
        event = pg.event.get()
        if event != []:
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
                    GAMENN.fill(Iro.PINNKU)
                    a.paint(alpha=200)
                    a.paint_img(alpha=100)
                    pg.display.update()

                elif event[ev].type == pg.MOUSEBUTTONDOWN:
                    mp = pg.mouse.get_pos()
                    fin = False
                    while not fin:
                        fin = a.move(pos_x=mp[0],pos_y=mp[1])
                        GAMENN.fill(Iro.SANDBROWN)
                        a.paint()
                        pg.display.update()

        if break_code:
            break

