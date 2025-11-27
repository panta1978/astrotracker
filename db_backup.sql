BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "LOCATIONS" (
	"id"	INTEGER NOT NULL,
	"location"	TEXT NOT NULL UNIQUE,
	"latitude"	REAL,
	"longitude"	REAL,
	"time_zone"	TEXT,
	"civil_utc"	REAL,
	"local_utc"	REAL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "STARS" (
	"id"	INTEGER NOT NULL,
	"star"	TEXT NOT NULL UNIQUE,
	"vizier_name"	TEXT NOT NULL UNIQUE,
	"ra0"	REAL,
	"dec0"	REAL,
	"pm_ra"	REAL,
	"pm_dec"	REAL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO "LOCATIONS" ("location","latitude","longitude","time_zone","civil_utc","local_utc") VALUES ('Astana, Kazakistan',51.1159933,71.4677059,'Asia/Karachi',5.0,4.7645);
INSERT INTO "LOCATIONS" ("location","latitude","longitude","time_zone","civil_utc","local_utc") VALUES ('Athens, Greece',37.9755648,23.7348324,'Europe/Athens',2.0,1.5823);
INSERT INTO "LOCATIONS" ("location","latitude","longitude","time_zone","civil_utc","local_utc") VALUES ('Bangkok, Thailand',13.7524938,100.4935089,'Asia/Jakarta',7.0,6.6996);
INSERT INTO "LOCATIONS" ("location","latitude","longitude","time_zone","civil_utc","local_utc") VALUES ('Beijing, China',40.190632,116.412144,'Asia/Manila',8.0,7.7608);
INSERT INTO "LOCATIONS" ("location","latitude","longitude","time_zone","civil_utc","local_utc") VALUES ('Berlin, Germany',52.5173885,13.3951309,'Europe/Paris',1.0,0.893);
INSERT INTO "LOCATIONS" ("location","latitude","longitude","time_zone","civil_utc","local_utc") VALUES ('Bogotà, Colombia',4.6533817,-74.0836331,'America/Lima',-5.0,-4.9389);
INSERT INTO "LOCATIONS" ("location","latitude","longitude","time_zone","civil_utc","local_utc") VALUES ('Bologna, Italy',44.4938203,11.3426327,'Europe/Paris',1.0,0.7562);
INSERT INTO "LOCATIONS" ("location","latitude","longitude","time_zone","civil_utc","local_utc") VALUES ('Buenos Aires, Argentina',-34.6095579,-58.3887904,'America/Sao_Paulo',-3.0,-3.8926);
INSERT INTO "LOCATIONS" ("location","latitude","longitude","time_zone","civil_utc","local_utc") VALUES ('Cairo, Egypt',30.0443879,31.2357257,'Africa/Cairo',2.0,2.0824);
INSERT INTO "LOCATIONS" ("location","latitude","longitude","time_zone","civil_utc","local_utc") VALUES ('Cape Town, South Africa',-33.9288301,18.4172197,'Africa/Johannesburg',2.0,1.2278);
INSERT INTO "LOCATIONS" ("location","latitude","longitude","time_zone","civil_utc","local_utc") VALUES ('Casablanca, Morocco',33.5945144,-7.6200284,'Africa/Casablanca',1.0,-0.508);
INSERT INTO "LOCATIONS" ("location","latitude","longitude","time_zone","civil_utc","local_utc") VALUES ('Dakar, Senegal',14.693425,-17.447938,'Africa/Abidjan',0.0,-1.1632);
INSERT INTO "LOCATIONS" ("location","latitude","longitude","time_zone","civil_utc","local_utc") VALUES ('Delhi, India',28.6328027,77.2197713,'Asia/Kolkata',5.5,5.148);
INSERT INTO "LOCATIONS" ("location","latitude","longitude","time_zone","civil_utc","local_utc") VALUES ('Denver, USA',39.7392364,-104.984862,'America/Denver',-7.0,-6.999);
INSERT INTO "LOCATIONS" ("location","latitude","longitude","time_zone","civil_utc","local_utc") VALUES ('Dubai, UAE',25.0742823,55.1885387,'Asia/Dubai',4.0,3.6792);
INSERT INTO "LOCATIONS" ("location","latitude","longitude","time_zone","civil_utc","local_utc") VALUES ('Havana, Cuba',23.135305,-82.3589631,'America/Havana',-5.0,-5.4906);
INSERT INTO "LOCATIONS" ("location","latitude","longitude","time_zone","civil_utc","local_utc") VALUES ('Honolulu, USA',21.304547,-157.855676,'Pacific/Honolulu',-10.0,-10.5237);
INSERT INTO "LOCATIONS" ("location","latitude","longitude","time_zone","civil_utc","local_utc") VALUES ('Kabul, Afghanistan',34.5269503,69.1850584,'Asia/Kabul',4.5,4.6123);
INSERT INTO "LOCATIONS" ("location","latitude","longitude","time_zone","civil_utc","local_utc") VALUES ('Kuala Lumpur, Malesia',3.1526589,101.7022205,'Asia/Manila',8.0,6.7801);
INSERT INTO "LOCATIONS" ("location","latitude","longitude","time_zone","civil_utc","local_utc") VALUES ('Lagos, Nigeria',6.4550575,3.3941795,'Africa/Lagos',1.0,0.2263);
INSERT INTO "LOCATIONS" ("location","latitude","longitude","time_zone","civil_utc","local_utc") VALUES ('Lima, Peru',-12.0459808,-77.0305912,'America/Lima',-5.0,-5.1354);
INSERT INTO "LOCATIONS" ("location","latitude","longitude","time_zone","civil_utc","local_utc") VALUES ('London, UK',51.4893335,-0.1440551,'Europe/London',0.0,-0.0096);
INSERT INTO "LOCATIONS" ("location","latitude","longitude","time_zone","civil_utc","local_utc") VALUES ('Los Angeles, USA',34.0536909,-118.242766,'America/Los_Angeles',-8.0,-7.8829);
INSERT INTO "LOCATIONS" ("location","latitude","longitude","time_zone","civil_utc","local_utc") VALUES ('Madrid, Spain',40.416782,-3.703507,'Europe/Paris',1.0,-0.2469);
INSERT INTO "LOCATIONS" ("location","latitude","longitude","time_zone","civil_utc","local_utc") VALUES ('Manila, Philippines',14.5904492,120.9803621,'Asia/Manila',8.0,8.0654);
INSERT INTO "LOCATIONS" ("location","latitude","longitude","time_zone","civil_utc","local_utc") VALUES ('Melbourne, Australia',-37.8142454,144.9631732,'Australia/Sydney',10.0,9.6642);
INSERT INTO "LOCATIONS" ("location","latitude","longitude","time_zone","civil_utc","local_utc") VALUES ('Mexico City, Mexico',19.3207722,-99.1514678,'America/Mexico_City',-6.0,-6.6101);
INSERT INTO "LOCATIONS" ("location","latitude","longitude","time_zone","civil_utc","local_utc") VALUES ('Mogadiscio, Somalia',2.0349312,45.3419183,'Europe/Moscow',3.0,3.0228);
INSERT INTO "LOCATIONS" ("location","latitude","longitude","time_zone","civil_utc","local_utc") VALUES ('Moscow, Russia',55.625578,37.6063916,'Europe/Moscow',3.0,2.5071);
INSERT INTO "LOCATIONS" ("location","latitude","longitude","time_zone","civil_utc","local_utc") VALUES ('Mumbai, India',19.054999,72.8692035,'Asia/Kolkata',5.5,4.8579);
INSERT INTO "LOCATIONS" ("location","latitude","longitude","time_zone","civil_utc","local_utc") VALUES ('Nairobi, Kenya',-1.3026148,36.828842,'Europe/Moscow',3.0,2.4553);
INSERT INTO "LOCATIONS" ("location","latitude","longitude","time_zone","civil_utc","local_utc") VALUES ('New York, USA',40.7127281,-74.0060152,'America/New_York',-5.0,-4.9337);
INSERT INTO "LOCATIONS" ("location","latitude","longitude","time_zone","civil_utc","local_utc") VALUES ('Palmer Station',-64.7742919,-64.0531107,'America/Sao_Paulo',-3.0,-4.2702);
INSERT INTO "LOCATIONS" ("location","latitude","longitude","time_zone","civil_utc","local_utc") VALUES ('Puerto Ayora, Ecuador',-0.7471674,-90.3134198,'America/Mexico_City',-6.0,-6.0209);
INSERT INTO "LOCATIONS" ("location","latitude","longitude","time_zone","civil_utc","local_utc") VALUES ('Punta Arenas, Chile',-53.1625688,-70.907822,'America/Sao_Paulo',-3.0,-4.7272);
INSERT INTO "LOCATIONS" ("location","latitude","longitude","time_zone","civil_utc","local_utc") VALUES ('Rapa Nui, Chile',-27.1259317,-109.3495887,'Pacific/Easter',-6.0,-7.29);
INSERT INTO "LOCATIONS" ("location","latitude","longitude","time_zone","civil_utc","local_utc") VALUES ('Reykjavík, Iceland',64.145981,-21.9422367,'Africa/Abidjan',0.0,-1.4628);
INSERT INTO "LOCATIONS" ("location","latitude","longitude","time_zone","civil_utc","local_utc") VALUES ('Saint Petersburg, Russia',59.9606739,30.1586551,'Europe/Moscow',3.0,2.0106);
INSERT INTO "LOCATIONS" ("location","latitude","longitude","time_zone","civil_utc","local_utc") VALUES ('Santiago, Chile',-33.4377756,-70.6504502,'America/Santiago',-4.0,-4.71);
INSERT INTO "LOCATIONS" ("location","latitude","longitude","time_zone","civil_utc","local_utc") VALUES ('Sao Paulo, Brazil',-23.5506507,-46.6333824,'America/Sao_Paulo',-3.0,-3.1089);
INSERT INTO "LOCATIONS" ("location","latitude","longitude","time_zone","civil_utc","local_utc") VALUES ('Seoul, South Korea',37.5666791,126.9782914,'Asia/Tokyo',9.0,8.4652);
INSERT INTO "LOCATIONS" ("location","latitude","longitude","time_zone","civil_utc","local_utc") VALUES ('Shangai, China',31.2312707,121.4700152,'Asia/Manila',8.0,8.098);
INSERT INTO "LOCATIONS" ("location","latitude","longitude","time_zone","civil_utc","local_utc") VALUES ('Stockholm, Sweden',59.3251172,18.0710935,'Europe/Paris',1.0,1.2047);
INSERT INTO "LOCATIONS" ("location","latitude","longitude","time_zone","civil_utc","local_utc") VALUES ('Suva, Fiji',-18.1415884,178.4421662,'Pacific/Fiji',12.0,11.8961);
INSERT INTO "LOCATIONS" ("location","latitude","longitude","time_zone","civil_utc","local_utc") VALUES ('Sydney, Australia',-33.8698439,151.2082848,'Australia/Sydney',10.0,10.0806);
INSERT INTO "LOCATIONS" ("location","latitude","longitude","time_zone","civil_utc","local_utc") VALUES ('Teheran, Iran',35.6892523,51.3896004,'Asia/Tehran',3.5,3.426);
INSERT INTO "LOCATIONS" ("location","latitude","longitude","time_zone","civil_utc","local_utc") VALUES ('Tokyo, Japan',35.6768601,139.7638947,'Asia/Tokyo',9.0,9.3176);
INSERT INTO "LOCATIONS" ("location","latitude","longitude","time_zone","civil_utc","local_utc") VALUES ('Toronto, Canada',43.6534817,-79.3839347,'America/New_York',-5.0,-5.2923);
INSERT INTO "LOCATIONS" ("location","latitude","longitude","time_zone","civil_utc","local_utc") VALUES ('Warsaw, Poland',52.2333742,21.0711489,'Europe/Paris',1.0,1.4047);
INSERT INTO "LOCATIONS" ("location","latitude","longitude","time_zone","civil_utc","local_utc") VALUES ('Wellington, New Zealand',-41.2887953,174.7772114,'Pacific/Auckland',12.0,11.6518);
INSERT INTO "STARS" ("star","vizier_name","ra0","dec0","pm_ra","pm_dec") VALUES ('Achernar','alf Eri',24.42813204,-57.23666007,88.02,-40.08);
INSERT INTO "STARS" ("star","vizier_name","ra0","dec0","pm_ra","pm_dec") VALUES ('Acrux','alf Cru',186.6497559,-63.09905586,-35.37,-14.73);
INSERT INTO "STARS" ("star","vizier_name","ra0","dec0","pm_ra","pm_dec") VALUES ('Adhara','eps CMa',104.6564445,-28.97208931,2.63,2.29);
INSERT INTO "STARS" ("star","vizier_name","ra0","dec0","pm_ra","pm_dec") VALUES ('Aldebaran','alf Tau',68.98000195,16.50976164,62.78,-189.36);
INSERT INTO "STARS" ("star","vizier_name","ra0","dec0","pm_ra","pm_dec") VALUES ('Alhena','gam Gem',99.42792641,16.39941482,-2.04,-66.92);
INSERT INTO "STARS" ("star","vizier_name","ra0","dec0","pm_ra","pm_dec") VALUES ('Alioth','eps UMa',193.5068041,55.95984301,111.74,-8.99);
INSERT INTO "STARS" ("star","vizier_name","ra0","dec0","pm_ra","pm_dec") VALUES ('Alkaid','eta UMa',206.8856088,49.31330288,-121.23,-15.56);
INSERT INTO "STARS" ("star","vizier_name","ra0","dec0","pm_ra","pm_dec") VALUES ('Alnair','alf Gru',332.0578184,-46.96061593,127.6,-147.91);
INSERT INTO "STARS" ("star","vizier_name","ra0","dec0","pm_ra","pm_dec") VALUES ('Alnilam','eps Ori',84.05338572,-1.20191725,1.49,-1.06);
INSERT INTO "STARS" ("star","vizier_name","ra0","dec0","pm_ra","pm_dec") VALUES ('Alnitak','zet Ori',85.18968672,-1.94257841,3.99,2.54);
INSERT INTO "STARS" ("star","vizier_name","ra0","dec0","pm_ra","pm_dec") VALUES ('Alpha Centauri','alf Cen',219.9141283,-60.83947139,-3600.35,952.11);
INSERT INTO "STARS" ("star","vizier_name","ra0","dec0","pm_ra","pm_dec") VALUES ('Alsephina','del01 Vel',131.1758221,-54.70856797,28.78,-104.14);
INSERT INTO "STARS" ("star","vizier_name","ra0","dec0","pm_ra","pm_dec") VALUES ('Altair','alf Aql',297.6945086,8.86738491,536.82,385.54);
INSERT INTO "STARS" ("star","vizier_name","ra0","dec0","pm_ra","pm_dec") VALUES ('Antares','alf Sco',247.351948,-26.43194608,-10.16,-23.21);
INSERT INTO "STARS" ("star","vizier_name","ra0","dec0","pm_ra","pm_dec") VALUES ('Arcturus','alf Boo',213.918114,19.18726997,-1093.45,-1999.4);
INSERT INTO "STARS" ("star","vizier_name","ra0","dec0","pm_ra","pm_dec") VALUES ('Avior','eps Car',125.628603,-59.50953829,-25.34,22.72);
INSERT INTO "STARS" ("star","vizier_name","ra0","dec0","pm_ra","pm_dec") VALUES ('Bellatrix','gam Ori',81.28278416,6.34973451,-8.75,-13.28);
INSERT INTO "STARS" ("star","vizier_name","ra0","dec0","pm_ra","pm_dec") VALUES ('Betelgeuse','alf Ori',88.79287161,7.40703634,27.33,10.86);
INSERT INTO "STARS" ("star","vizier_name","ra0","dec0","pm_ra","pm_dec") VALUES ('Canopus','alf Car',95.98787763,-52.69571799,19.99,23.67);
INSERT INTO "STARS" ("star","vizier_name","ra0","dec0","pm_ra","pm_dec") VALUES ('Capella','alf Aur',79.17206517,45.99902927,75.52,-427.13);
INSERT INTO "STARS" ("star","vizier_name","ra0","dec0","pm_ra","pm_dec") VALUES ('Castor','alf Gem',113.650019,31.88863645,-206.33,-148.18);
INSERT INTO "STARS" ("star","vizier_name","ra0","dec0","pm_ra","pm_dec") VALUES ('Deneb','alf Cyg',310.3579727,45.28033423,1.56,1.55);
INSERT INTO "STARS" ("star","vizier_name","ra0","dec0","pm_ra","pm_dec") VALUES ('Denebola','bet Leo',177.2661598,14.57233687,-499.02,-113.78);
INSERT INTO "STARS" ("star","vizier_name","ra0","dec0","pm_ra","pm_dec") VALUES ('Diphda','bet Cet',10.89678452,-17.9866841,232.79,32.71);
INSERT INTO "STARS" ("star","vizier_name","ra0","dec0","pm_ra","pm_dec") VALUES ('Dubhe','alf UMa',165.9326537,61.75111888,-136.46,-35.25);
INSERT INTO "STARS" ("star","vizier_name","ra0","dec0","pm_ra","pm_dec") VALUES ('Elnath','bet Tau',81.57290804,28.60787346,23.28,-174.22);
INSERT INTO "STARS" ("star","vizier_name","ra0","dec0","pm_ra","pm_dec") VALUES ('Enif','eps Peg',326.0464181,9.87500791,30.02,1.38);
INSERT INTO "STARS" ("star","vizier_name","ra0","dec0","pm_ra","pm_dec") VALUES ('Fomalhaut','alf PsA',344.4117732,-29.62183701,329.22,-164.22);
INSERT INTO "STARS" ("star","vizier_name","ra0","dec0","pm_ra","pm_dec") VALUES ('Gacrux','gam Cru',187.791372,-57.11256922,27.94,-264.33);
INSERT INTO "STARS" ("star","vizier_name","ra0","dec0","pm_ra","pm_dec") VALUES ('Hadar','bet Cen',210.956019,-60.3729784,-33.96,-25.06);
INSERT INTO "STARS" ("star","vizier_name","ra0","dec0","pm_ra","pm_dec") VALUES ('Kaus Australis','eps Sgr',276.0431097,-34.3843146,-39.61,-124.05);
INSERT INTO "STARS" ("star","vizier_name","ra0","dec0","pm_ra","pm_dec") VALUES ('Menkent','tet Cen',211.6721861,-36.36869575,-519.29,-517.87);
INSERT INTO "STARS" ("star","vizier_name","ra0","dec0","pm_ra","pm_dec") VALUES ('Miaplacidus','bet Car',138.3010033,-69.71747245,-157.66,108.91);
INSERT INTO "STARS" ("star","vizier_name","ra0","dec0","pm_ra","pm_dec") VALUES ('Mimosa','bet Cru',191.9304954,-59.68873246,-48.24,-12.82);
INSERT INTO "STARS" ("star","vizier_name","ra0","dec0","pm_ra","pm_dec") VALUES ('Mirfak','alf Per',51.08061889,49.86124281,24.11,-26.01);
INSERT INTO "STARS" ("star","vizier_name","ra0","dec0","pm_ra","pm_dec") VALUES ('Mirzam','bet CMa',95.6749475,-17.95591658,-3.45,-0.47);
INSERT INTO "STARS" ("star","vizier_name","ra0","dec0","pm_ra","pm_dec") VALUES ('Naos','zet Pup',120.8961256,-40.00318846,-30.82,16.77);
INSERT INTO "STARS" ("star","vizier_name","ra0","dec0","pm_ra","pm_dec") VALUES ('Nunki','sig Sgr',283.8163196,-26.29659428,13.87,-52.65);
INSERT INTO "STARS" ("star","vizier_name","ra0","dec0","pm_ra","pm_dec") VALUES ('Polaris','alf UMi',37.94614689,89.26413805,44.22,-11.74);
INSERT INTO "STARS" ("star","vizier_name","ra0","dec0","pm_ra","pm_dec") VALUES ('Pollux','bet Gem',116.3306826,28.02631031,-625.69,-45.95);
INSERT INTO "STARS" ("star","vizier_name","ra0","dec0","pm_ra","pm_dec") VALUES ('Procyon','alf CMi',114.8272419,5.22750767,-716.57,-1034.58);
INSERT INTO "STARS" ("star","vizier_name","ra0","dec0","pm_ra","pm_dec") VALUES ('Regulus','alf Leo',152.0935808,11.96719513,-249.4,4.91);
INSERT INTO "STARS" ("star","vizier_name","ra0","dec0","pm_ra","pm_dec") VALUES ('Rigel','bet Ori',78.63446353,-8.20163919,1.87,-0.56);
INSERT INTO "STARS" ("star","vizier_name","ra0","dec0","pm_ra","pm_dec") VALUES ('Saiph','kap Ori',86.93911641,-9.66960186,1.55,-1.2);
INSERT INTO "STARS" ("star","vizier_name","ra0","dec0","pm_ra","pm_dec") VALUES ('Sargas','tet Sco',264.3296907,-42.99782155,6.06,-0.95);
INSERT INTO "STARS" ("star","vizier_name","ra0","dec0","pm_ra","pm_dec") VALUES ('Shaula','lam Sco',263.4021937,-37.10374835,-8.9,-29.95);
INSERT INTO "STARS" ("star","vizier_name","ra0","dec0","pm_ra","pm_dec") VALUES ('Sirius','alf CMa',101.2885411,-16.71314306,-546.01,-1223.08);
INSERT INTO "STARS" ("star","vizier_name","ra0","dec0","pm_ra","pm_dec") VALUES ('Spica','alf Vir',201.2983523,-11.16124491,-42.5,-31.73);
INSERT INTO "STARS" ("star","vizier_name","ra0","dec0","pm_ra","pm_dec") VALUES ('Vega','alf Lyr',279.2341083,38.78299311,201.02,287.46);
INSERT INTO "STARS" ("star","vizier_name","ra0","dec0","pm_ra","pm_dec") VALUES ('Wezen','del CMa',107.0978585,-26.39320776,-2.75,3.33);
COMMIT;