#encoding: UTF-8

from PIL import ImageDraw, ImageFont, Image
from random import random
from datetime import datetime, timedelta, date
from time import gmtime, strftime
from sys import maxint


# definicje kolorow
czarny = (0,0,0)
czarny_diag = (0,0,0)
bialy =(255,255,255)
bialy_diag =(255,255,255)
jszary =(218,218,218)
niebieski =(0,0,255)
niebieski_diag =(0,0,255)
ed = (157,145,95)
jasnoniebieski_diag = (133,128,255)
zolty_diag = (255,254,2)


class traxx_renderer(abstractscreenrenderer):
	def __init__(self, lookup_path, name, cab):
		self.podklad = Image.open(lookup_path + "ek1.tga")
		self.ertms = Image.open(lookup_path + "ertms.png")
		self.diag_1_day = Image.open(lookup_path + "diag_1_day.png")
		self.diag_2_day = Image.open(lookup_path + "diag_2_day.png")
		self.diag_3_day = Image.open(lookup_path + "diag_3_day.png")
		self.diag_4_day = Image.open(lookup_path + "diag_4_day.png")
		self.diag_1_night = Image.open(lookup_path + "diag_1_night.png")
		self.diag_2_night = Image.open(lookup_path + "diag_2_night.png")
		self.diag_3_night = Image.open(lookup_path + "diag_3_night.png")
		self.diag_4_night = Image.open(lookup_path + "diag_4_night.png")
		self.maska  = Image.open(lookup_path + "maska.png")
		self.shp  = Image.open(lookup_path + "shp.png")
		self.pedal  = Image.open(lookup_path + "pedal.png")
		self.ws  = Image.open(lookup_path + "ws.png")
		self.szyna_zbiorcza  = Image.open(lookup_path + "szyna_zbiorcza.png")
		self.drzwi  = Image.open(lookup_path + "drzwi.png")
		
		self.sredni_arial = ImageFont.truetype(lookup_path + "arialbd.ttf", 34)
		self.maly_arial = ImageFont.truetype(lookup_path + "arialbd.ttf", 26)
		self.bmaly_arial = ImageFont.truetype(lookup_path + "arialbd.ttf", 16)
		
		self.kilometry = (random()*300000)+5000
		self.last_time_update = 0
		self.dzis = datetime.now().timetuple().tm_yday
		self.rok = datetime.now().year
		self.last_hour = 10
		self.temp = (random()*15) + 20
		
	def print_center(self, draw, text, X, Y, font, color):
		w = draw.textsize(text, font)
		draw.text(((X-w[0]/2),(Y-w[1]/2)), text, font=font, fill=color)
		
	def _render(self, state):
#liczenie pojazdów
		if (state['unit_no'] == 1):
			pojazdy = 1
		if (state['unit_no'] == 2):
			pojazdy = 2
		if (state['unit_no'] == 3):
			pojazdy = 3
		if (state['unit_no'] == 4):
			pojazdy = 4
		if (state['unit_no'] > 4):
			pojazdy = 4
			
#zmiana kolorów na nocne
		global czarny_diag
		global niebieski_diag
		if (state['universal3']==1):
			czarny_diag = (255,255,255)
			# bialy_diag =(255,255,255)
			niebieski_diag =(0,0,132)
			# jasnoniebieski_diag = (133,128,255)
			# zolty_diag = (255,254,2)
		else:
			czarny_diag = (0,0,0)
			niebieski_diag =(0,0,255)
		# kopia obrazka na potrzeby tego jednego renderowania
		obrazek = self.podklad.copy()
		# chcemy rysowac po teksturze pulpitu
		draw = ImageDraw.Draw(obrazek)
		
#Prędkość
		speed = float(state['velocity'])
		if speed > 180:
			speed = 180
#czas
		if state['seconds'] != self.last_time_update:
			dt = state['seconds'] - self.last_time_update
			if dt < 0:
				dt+=60
			self.kilometry += dt*speed * 0.0002778
			self.last_time_update = state['seconds']
		if state['hours']<10:
			godz = "0" + str(state['hours'])
		else:
			godz = str(state['hours'])
		if state['minutes']<10:
			min = "0" + str(state['minutes'])
		else:
			min = str(state['minutes'])
		if state['seconds']<10:
			sec = "0" +str(state['seconds'])
		else:
			sec = str(state['seconds'])
		
		
#data
		if self.last_hour == 23 and state['hours'] == 0:
			self.dzis = self.dzis+1 # wlasnie wybila polnoc
		self.last_hour = state['hours']
		data = datetime(self.rok, 1, 1) + timedelta(self.dzis - 1)
		dzien = datetime.weekday(data)
		data = data.strftime("%d,%m,%Y")
		DayL = ['Pn','Wt',u'Śr','Cz','Pt','So','Nd']

#ERTMS------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		if state['eimp_c1_batt']==1:
			obrazek.paste(self.ertms,(134,1038),self.ertms)
	#ERTMS godzina
			draw.text((576,1045), godz +":"+ min +":"+ sec, fill=jszary, font=self.sredni_arial)
			
	#ERTMS prędkościomierz
			draw.ellipse([(431, 1249), (521, 1339)], fill=bialy)
			rotate = speed * 270 / 180 + 45
			rad =  radians(rotate)
			srodek_tacho = (476, 1294)
			point = (-10,37)
			p1 = (point[0]*cos(rad)-point[1]*sin(rad) + srodek_tacho[0],point[0]*sin(rad)+point[1]*cos(rad) + srodek_tacho[1])
			point = (-10,137)
			p2 = (point[0]*cos(rad)-point[1]*sin(rad) + srodek_tacho[0],point[0]*sin(rad)+point[1]*cos(rad) + srodek_tacho[1])
			point = (-4,145)
			p3 = (point[0]*cos(rad)-point[1]*sin(rad) + srodek_tacho[0],point[0]*sin(rad)+point[1]*cos(rad) + srodek_tacho[1])
			point = (-4,187)
			p4 = (point[0]*cos(rad)-point[1]*sin(rad) + srodek_tacho[0],point[0]*sin(rad)+point[1]*cos(rad) + srodek_tacho[1])
			point = (10,37)
			p8 = (point[0]*cos(rad)-point[1]*sin(rad) + srodek_tacho[0],point[0]*sin(rad)+point[1]*cos(rad) + srodek_tacho[1])
			point = (10,137)
			p7 = (point[0]*cos(rad)-point[1]*sin(rad) + srodek_tacho[0],point[0]*sin(rad)+point[1]*cos(rad) + srodek_tacho[1])
			point = (4,145)
			p6 = (point[0]*cos(rad)-point[1]*sin(rad) + srodek_tacho[0],point[0]*sin(rad)+point[1]*cos(rad) + srodek_tacho[1])
			point = (4,187)
			p5 = (point[0]*cos(rad)-point[1]*sin(rad) + srodek_tacho[0],point[0]*sin(rad)+point[1]*cos(rad) + srodek_tacho[1])
			draw.polygon([p1,p2,p3,p4,p5,p6,p7,p8],fill=bialy)
			
			self.print_center(draw, '%d' % speed, 476, 1294, self.sredni_arial, czarny)
			
	#ERTMS siła pociągowa/hamowania
			
			#siła pociągowa
			frt = (state['eimp_c1_frt'])
			if not -maxint-1 <= frt <= maxint:
				frt = (frt + (maxint + 1)) % (2 * (maxint + 1)) - maxint - 1
			end = int(frt / 2 - 90)
			draw.pieslice((771,1071,1220, 1520), -90, end, fill=niebieski)
			#siła hamowania
			frb = (state['eimp_c1_frb'])
			if not -maxint-1 <= frb <= maxint:
				frb = (frb + (maxint + 1)) % (2 * (maxint + 1)) - maxint - 1
			end = int(-frb - 90)
			draw.pieslice((771,1071,1220, 1520), end, -90 , fill=ed)
			
			obrazek.paste(self.maska,(730,1041),self.maska)
			
			#siła zadana
			# fd = state['eimp_t_fd']
			# if (fd<0):
				# fd=fd*2
			# rotate = fd * 70 / 140
			# if (rotate>140 and fd>0):
				# rotate=140
			# if (rotate<-140 and fd<0):
				# rotate=-140
			pd = state['eimp_t_pd']
			rotate = pd * 150
			if (rotate>140 and pd>0):
				rotate=140
			if (rotate<-140 and pd<0):
				rotate=-140
			rad =  radians(rotate)
			srodek = (995, 1295)
			point = (0,-220)
			p1 = (srodek[0]+point[0]*cos(rad)-point[1]*sin(rad),srodek[1]+point[1]*cos(rad)+point[0]*sin(rad))
			point = (-13,-249)
			p2 = (srodek[0]+point[0]*cos(rad)-point[1]*sin(rad),srodek[1]+point[1]*cos(rad)+point[0]*sin(rad))
			point = (13,-249)
			p3 = (srodek[0]+point[0]*cos(rad)-point[1]*sin(rad),srodek[1]+point[1]*cos(rad)+point[0]*sin(rad))
			draw.polygon([p1,p2,p3],fill=bialy)
	#ERTMS Ikonki
			if (state['shp']):
				obrazek.paste(self.shp,(303,1551),self.shp)
			if (state['ca']):
				obrazek.paste(self.pedal,(1155,1551),self.pedal)
			if (state['eimp_c1_heat']==0):
				obrazek.paste(self.szyna_zbiorcza,(729,1551),self.szyna_zbiorcza)
			if (state['eimp_c1_ms']==0):
				obrazek.paste(self.ws,(801,1551),self.ws)
			if (state['doors_2']==0 and state['doors_no_2']>0):
				obrazek.paste(self.drzwi,(942,1551),self.drzwi)
			# draw.text((942,1651), "door_2=" + str(state['doors_2']), fill=czarny_diag, font=self.maly_arial)
			# draw.text((942,1751), "doors_no_2=" + str(state['doors_no_2']), fill=czarny_diag, font=self.maly_arial)
			
#Ekran diagnostyczny--------------------------------------------------------------------------------------------------------------------------------------------------------------------
			if (pojazdy ==1):
				if (state['universal3']==0):
					obrazek.paste(self.diag_1_day,(130,54),self.diag_1_day)
				if (state['universal3']==1):
					obrazek.paste(self.diag_1_night,(130,54),self.diag_1_night)
			if (pojazdy ==2):
				if (state['universal3']==0):
					obrazek.paste(self.diag_2_day,(130,54),self.diag_2_day)
				if (state['universal3']==1):
					obrazek.paste(self.diag_2_night,(130,54),self.diag_2_night)
			if (pojazdy ==3):
				if (state['universal3']==0):
					obrazek.paste(self.diag_3_day,(130,54),self.diag_3_day)
				if (state['universal3']==1):
					obrazek.paste(self.diag_3_night,(130,54),self.diag_3_night)
			if (pojazdy ==4):
				if (state['universal3']==0):
					obrazek.paste(self.diag_4_day,(130,54),self.diag_4_day)
				if (state['universal3']==1):
					obrazek.paste(self.diag_4_night,(130,54),self.diag_4_night)
	#diag data
			draw.text((1021,60), DayL[dzien] + ", " + data, fill=czarny_diag, font=self.sredni_arial)
	#diag nr pociągu
			trainnumber = state['trainnumber']
			if ((state['trainnumber'] == 'none') or (state['trainnumber'] == 'rozklad') ):
				trainnumber = ' '
			draw.text((1112,387), trainnumber, fill=czarny_diag, font=self.maly_arial)
	#diag zegarek
			#obroty wskazówek w radianach
			sekundy = radians((state['seconds']*6))
			minuty = radians((state['minutes']*6))
			godziny = radians((state['hours']*30 + state['minutes']*0.5)) #składowa minutowa dla płynnego ruchu
			srodek = (1130, 242)
			#długości wskazówek
			r_s = 105
			r_m = 98
			r_g = 82
			#punkty końcowe
			k_s = (srodek[0]+(r_s*sin(sekundy)), srodek[1]-(r_s*cos(sekundy)))
			k_m = (srodek[0]+(r_m*sin(minuty)), srodek[1]-(r_m*cos(minuty)))
			k_g = (srodek[0]+(r_g*sin(godziny)), srodek[1]-(r_g*cos(godziny)))
			p_s = (srodek[0]+(7*(-sin(sekundy))), srodek[1]-(7*(-cos(sekundy))))
			p_m = (srodek[0]+(7*(-sin(minuty))), srodek[1]-(7*(-cos(minuty))))
			p_g = (srodek[0]+(7*(-sin(godziny))), srodek[1]-(7*(-cos(godziny))))
			#rysowanie wskazówek
			draw.line((p_s[0], p_s[1],k_s[0], k_s[1]),fill=czarny_diag, width=2)
			draw.line((p_m[0], p_m[1],k_m[0], k_m[1]),fill=czarny_diag, width=4)
			draw.line((p_g[0], p_g[1],k_g[0], k_g[1]),fill=czarny_diag, width=8)
			
			
	#diag status3
			#Hamulec bezpośredni nie jest luzowany
			#Blokada trakcji (wywaliło szybki)
			#Blokada trakcji przy zmianie pantografu
			#Trwa przegrupowanie przetwornicy pokładowej
			#Zmiana sterowania hamowaniem wyrównać przewód główny
			if ((state['manual_brake'] == 1) and (state['direction'] != 0)):
				draw.rectangle(((558,720),(969,784)), fill=jasnoniebieski_diag)
				self.print_center(draw, u'Zluzować sprężynowy hamulec postojowy', 763, 752, self.bmaly_arial, bialy)
			#Odblokować urządzenie czuwakowe
			#Zakłócenie systemów sterowania
			if (state['eimp_c1_ms'] == 0 and state['eimp_c1_uhv'] > 2500):
				draw.rectangle(((558,720),(969,784)), fill=jasnoniebieski_diag)
				self.print_center(draw, u'Włączyć wyłącznik szybki', 763, 752, self.sredni_arial, bialy)
			#Blokada wyłącznika szybkiego
			#Przegrupowanie napędu
			if (state['eimp_c1_ms'] == 0 and state['main_ctrl_actual_pos'] !=0): #dodać 'main_ctrl_desired_pos' do pythona i blokadę do fizyki, bo teraz da się załączyć
				draw.rectangle(((558,720),(969,784)), fill=jasnoniebieski_diag)
				self.print_center(draw, u'Nastawnik jazdy w pozycji „0” w celu włączenia wyłącznika szybkiego', 763, 752, self.bmaly_arial, bialy)
			#Kabina maszynisty bez obsady
			#Zbyt niskie ciśnienie powietrza wyłącznika głównego
			if ((state['direction'] != 0) and ((state['eimp_u1_pf'] == 0) and (state['eimp_u1_pr'] == 0))):
				draw.rectangle(((558,720),(969,784)), fill=jasnoniebieski_diag)
				self.print_center(draw, u'Podnieść pantograf', 763, 752, self.sredni_arial, bialy)
			
			#Odblokować pantografy
			#Zakłócenie systemów sterowania
			
	#diag slupki 1
			if (pojazdy ==1):
				#wolto
				wolt = state['eimp_c1_uhv']
				if wolt>5000:
					wolt=5000
				napiecie = 586-(0.0866*wolt)
				draw.rectangle(((266,586),(358,napiecie)), fill=niebieski_diag)
				if wolt>2500:
					draw.rectangle(((267,608),(358,646)), fill=niebieski_diag)
				if state['eimp_c1_ms']:
					draw.text((271,613), u'WG wł', font=self.maly_arial, fill=bialy_diag)
				elif wolt>2500:
					draw.text((265,613), u'WG wył', font=self.maly_arial, fill=bialy_diag)
				else:
					draw.text((265,613), u'WG wył', font=self.maly_arial, fill=czarny_diag)
					
				#ampery
				prad = state['eimp_c1_ihv']
				if prad<0:
					prad=0
				self.print_fixed_with(draw, '2000', (535,607), 4, self.sredni_arial, czarny_diag)
				if prad>3700:
					prad=3700
				ampery = 586-(0.1183*prad)
				draw.rectangle(((532,586),(625,ampery)), fill=niebieski_diag)
				
				
				#hbl
				hbl = state['eimp_pn1_bp']
				cisn = 586-(34.6666*hbl) 
				draw.rectangle(((727,647),(820,cisn)), fill=niebieski_diag)
	#diag slupki 2
			if (pojazdy == 2):
				#wolto1
				wolt = state['eimp_c1_uhv']
				if wolt>5000:
					wolt=5000
				napiecie = 586-(0.0866*wolt)
				draw.rectangle(((266,586),(358,napiecie)), fill=niebieski_diag)
				if wolt>2500:
					draw.rectangle(((267,608),(358,646)), fill=niebieski_diag)
				if state['eimp_c1_ms']:
					draw.text((271,613), u'WG wł', font=self.maly_arial, fill=bialy_diag)
				elif wolt>2500:
					draw.text((265,613), u'WG wył', font=self.maly_arial, fill=bialy_diag)
				else:
					draw.text((265,613), u'WG wył', font=self.maly_arial, fill=czarny_diag)
				#wolto2
				wolt = state['eimp_c2_uhv']
				if wolt>5000:
					wolt=5000
				napiecie = 586-(0.0866*wolt)
				draw.rectangle(((449,586),(541,napiecie)), fill=niebieski_diag)
				if wolt>2500:
					draw.rectangle(((450,608),(541,646)), fill=niebieski_diag)
				if state['eimp_c2_ms']:
					draw.text((454,613), u'WG wł', font=self.maly_arial, fill=bialy_diag)
				elif wolt>2500:
					draw.text((448,613), u'WG wył', font=self.maly_arial, fill=bialy_diag)
				else:
					draw.text((448,613), u'WG wył', font=self.maly_arial, fill=czarny_diag)
					
				#ampery
				prad = state['eimp_t_itothv']
				if prad<0:
					prad=0
				self.print_fixed_with(draw, '2000', (728,607), 4, self.sredni_arial, czarny_diag)
				if prad>3700:
					prad=3700
				ampery = 586-(0.1183*prad)
				draw.rectangle(((725,586),(818,ampery)), fill=niebieski_diag)
				
	#diag slupki 3
			if (pojazdy == 3):
				#wolto1
				wolt = state['eimp_c1_uhv']
				if wolt>5000:
					wolt=5000
				napiecie = 586-(0.0866*wolt)
				draw.rectangle(((267,586),(358,napiecie)), fill=niebieski_diag)
				if wolt>2500:
					draw.rectangle(((267,608),(358,646)), fill=niebieski_diag)
				if state['eimp_c1_ms']:
					draw.text((271,613), u'WG wł', font=self.maly_arial, fill=bialy_diag)
				elif wolt>2500:
					draw.text((265,613), u'WG wył', font=self.maly_arial, fill=bialy_diag)
				else:
					draw.text((265,613), u'WG wył', font=self.maly_arial, fill=czarny_diag)
				#wolto2
				wolt = state['eimp_c2_uhv']
				if wolt>5000:
					wolt=5000
				napiecie = 586-(0.0866*wolt)
				draw.rectangle(((448,586),(541,napiecie)), fill=niebieski_diag)
				if wolt>2500:
					draw.rectangle(((448,608),(541,646)), fill=niebieski_diag)
				if state['eimp_c2_ms']:
					draw.text((452,613), u'WG wł', font=self.maly_arial, fill=bialy_diag)
				elif wolt>2500:
					draw.text((446,613), u'WG wył', font=self.maly_arial, fill=bialy_diag)
				else:
					draw.text((446,613), u'WG wył', font=self.maly_arial, fill=czarny_diag)
				#wolto3
				wolt = state['eimp_c3_uhv']
				if wolt>5000:
					wolt=5000
				napiecie = 586-(0.0866*wolt)
				draw.rectangle(((630,586),(722,napiecie)), fill=niebieski_diag)
				if wolt>2500:
					draw.rectangle(((630,608),(722,646)), fill=niebieski_diag)
				if state['eimp_c3_ms']:
					draw.text((634,613), u'WG wł', font=self.maly_arial, fill=bialy_diag)
				elif wolt>2500:
					draw.text((628,613), u'WG wył', font=self.maly_arial, fill=bialy_diag)
				else:
					draw.text((628,613), u'WG wył', font=self.maly_arial, fill=czarny_diag)
				#ampery
				prad = state['eimp_t_itothv']
				if prad<0:
					prad=0
				self.print_fixed_with(draw, '2000', (836,607), 4, self.sredni_arial, czarny_diag)
				if prad>3700:
					prad=3700
				ampery = 586-(0.1183*prad)
				draw.rectangle(((833,586),(925,ampery)), fill=niebieski_diag)

	#diag slupki 4
			if (pojazdy == 4):
				#wolto1
				wolt = state['eimp_c1_uhv']
				if wolt>5000:
					wolt=5000
				napiecie = 586-(0.0866*wolt)
				draw.rectangle(((229,586),(302,napiecie)), fill=niebieski_diag)
				if wolt>2500:
					draw.rectangle(((229,608),(302,646)), fill=niebieski_diag)
				if state['eimp_c1_ms']:
					draw.text((241,618), u'WG wł', font=self.bmaly_arial, fill=bialy_diag)
				elif wolt>2500:
					draw.text((235,618), u'WG wył', font=self.bmaly_arial, fill=bialy_diag)
				else:
					draw.text((235,618), u'WG wył', font=self.bmaly_arial, fill=czarny_diag)
				#wolto2
				wolt = state['eimp_c2_uhv']
				if wolt>5000:
					wolt=5000
				napiecie = 586-(0.0866*wolt)
				draw.rectangle(((392,586),(465,napiecie)), fill=niebieski_diag)
				if wolt>2500:
					draw.rectangle(((392,608),(465,646)), fill=niebieski_diag)
				if state['eimp_c2_ms']:
					draw.text((404,618), u'WG wł', font=self.bmaly_arial, fill=bialy_diag)
				elif wolt>2500:
					draw.text((398,618), u'WG wył', font=self.bmaly_arial, fill=bialy_diag)
				else:
					draw.text((398,618), u'WG wył', font=self.bmaly_arial, fill=czarny_diag)
				#wolto3
				wolt = state['eimp_c3_uhv']
				if wolt>5000:
					wolt=5000
				napiecie = 586-(0.0866*wolt)
				draw.rectangle(((555,586),(628,napiecie)), fill=niebieski_diag)
				if wolt>2500:
					draw.rectangle(((555,608),(628,646)), fill=niebieski_diag)
				if state['eimp_c3_ms']:
					draw.text((567,618), u'WG wł', font=self.bmaly_arial, fill=bialy_diag)
				elif wolt>2500:
					draw.text((561,618), u'WG wył', font=self.bmaly_arial, fill=bialy_diag)
				else:
					draw.text((561,618), u'WG wył', font=self.bmaly_arial, fill=czarny_diag)
				#wolto4
				wolt = state['eimp_c4_uhv']
				if wolt>5000:
					wolt=5000
				napiecie = 586-(0.0866*wolt)
				draw.rectangle(((717,586),(790,napiecie)), fill=niebieski_diag)
				if wolt>2500:
					draw.rectangle(((717,608),(790,646)), fill=niebieski_diag)
				if state['eimp_c4_ms']:
					draw.text((729,618), u'WG wł', font=self.bmaly_arial, fill=bialy_diag)
				elif wolt>2500:
					draw.text((723,618), u'WG wył', font=self.bmaly_arial, fill=bialy_diag)
				else:
					draw.text((723,618), u'WG wył', font=self.bmaly_arial, fill=czarny_diag)
				#ampery
				prad = state['eimp_t_itothv']
				if prad<0:
					prad=0
				self.print_fixed_with(draw, '2000', (886,607), 4, self.sredni_arial, czarny_diag)
				if prad>3700:
					prad=3700
				ampery = 586-(0.1183*prad)
				draw.rectangle(((882,586),(959,ampery)), fill=niebieski_diag)
		
		return obrazek