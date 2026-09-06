"""Built-in French <-> English <-> Turkish core dictionary (A1-B1, ~900 entries).

Line format:  headword|pos [gender] [plural]|english; english 2[|note[|türkçe; türkçe 2]]
Nouns carry their gender (m / f / mf / pl) and an irregular plural when needed
(``n m yeux``). Irregular verb notes go into the optional fourth field.
The optional fifth field is the Turkish gloss (senses separated by ``; ``); leave the note field empty
to add one without a note (``maison|n f|house||ev``). Entries without it show "—" in the
Turkish column until the AI fills the gloss in.
"""

DATA = r"""
# ---- greetings / politeness ----
bonjour|int|hello; good morning||merhaba; günaydın
bonsoir|int|good evening||iyi akşamlar
bonne nuit|phr|good night||iyi geceler
salut|int|hi; bye (informal)||selam; hoşça kal
au revoir|phr|goodbye||hoşça kal; güle güle
à bientôt|phr|see you soon||yakında görüşürüz
à plus tard|phr|see you later||sonra görüşürüz
à demain|phr|see you tomorrow||yarın görüşürüz
merci|int|thank you||teşekkürler
merci beaucoup|phr|thank you very much||çok teşekkür ederim
s'il vous plaît|phr|please (formal)||lütfen (resmi)
s'il te plaît|phr|please (informal)||lütfen (samimi)
de rien|phr|you are welcome||bir şey değil
je vous en prie|phr|you are welcome (formal)||rica ederim
pardon|int|sorry; excuse me||affedersiniz; pardon
excusez-moi|phr|excuse me||affedersiniz
désolé|adj|sorry||üzgün
oui|part|yes||evet
non|part|no||hayır
si|part|yes (contradicting a negative); if||evet (olumsuza karşı); eğer
d'accord|phr|okay; agreed||tamam; anlaştık
bien sûr|phr|of course||tabii ki; elbette
peut-être|adv|maybe; perhaps||belki
bienvenue|int|welcome||hoş geldiniz
félicitations|int|congratulations||tebrikler
bonne chance|phr|good luck||iyi şanslar
bon appétit|phr|enjoy your meal||afiyet olsun
santé|int|cheers||şerefe
à vos souhaits|phr|bless you||çok yaşa
joyeux anniversaire|phr|happy birthday||doğum günün kutlu olsun
comment allez-vous|phr|how are you (formal)||nasılsınız
comment ça va|phr|how are you (informal)||nasılsın
ça va|phr|I am fine; how are you||iyiyim; nasıl gidiyor
comment vous appelez-vous|phr|what is your name (formal)||adınız ne
je m'appelle|phr|my name is||benim adım
je viens de|phr|I come from||ben ...'den geliyorum
je ne comprends pas|phr|I do not understand||anlamıyorum
je ne sais pas|phr|I do not know||bilmiyorum
parlez-vous anglais|phr|do you speak English||İngilizce konuşuyor musunuz
pouvez-vous répéter|phr|can you repeat||tekrar edebilir misiniz
combien ça coûte|phr|how much does it cost||bu ne kadar
où est|phr|where is||nerede
je voudrais|phr|I would like||istiyorum; isterdim
il y a|phr|there is; there are||var
qu'est-ce que c'est|phr|what is it||bu ne
# ---- question words ----
qui|pron|who||kim
que|pron|what; that||ne; ki
quoi|pron|what||ne
où|adv|where||nerede
quand|adv|when||ne zaman
pourquoi|adv|why||neden
comment|adv|how||nasıl
quel|pron|which; what||hangi
combien|adv|how much; how many||ne kadar; kaç
lequel|pron|which one||hangisi
# ---- pronouns / articles ----
je|pron|I||ben
tu|pron|you (singular, informal)||sen
il|pron|he; it||o (erkek)
elle|pron|she; it||o (kadın)
on|pron|one; we (informal); people||insan; biz (samimi); insanlar
nous|pron|we; us||biz; bizi
vous|pron|you (plural or formal)||siz
ils|pron|they (masculine)||onlar (eril)
elles|pron|they (feminine)||onlar (dişil)
me|pron|me; myself||beni; bana; kendimi
te|pron|you; yourself||seni; sana; kendini
se|pron|oneself; himself; herself||kendini; kendisini
le|art|the (masculine); him; it||belirli tanımlık (eril); onu
la|art|the (feminine); her; it||belirli tanımlık (dişil); onu
les|art|the (plural); them||belirli tanımlık (çoğul); onları
un|art|a; an (masculine); one||bir (eril tanımlık)
une|art|a; an (feminine)||bir (dişil tanımlık)
des|art|some (plural)||birkaç; bazı (çoğul)
du|art|some (masculine); of the||biraz (eril); -in
de la|art|some (feminine)||biraz (dişil)
mon|pron|my (masculine)||benim (eril)
ma|pron|my (feminine)||benim (dişil)
mes|pron|my (plural)||benim (çoğul)
ton|pron|your (masculine, informal)||senin (eril)
ta|pron|your (feminine, informal)||senin (dişil)
son|pron|his; her; its (masculine)||onun (eril)
sa|pron|his; her; its (feminine)||onun (dişil)
notre|pron|our||bizim
votre|pron|your (formal or plural)||sizin
leur|pron|their; to them||onların; onlara
ce|pron|this; that; it||bu; şu; o
cette|pron|this; that (feminine)||bu; şu (dişil)
ces|pron|these; those||bunlar; şunlar
celui|pron|the one; this one||o; bu (olan)
tout|pron|all; everything||hepsi; her şey
tous|pron|all; everyone||hepsi; herkes
chaque|pron|each; every||her
quelque chose|phr|something||bir şey
quelqu'un|pron|someone||biri; birisi
rien|pron|nothing||hiçbir şey
personne|pron|nobody; person||hiç kimse; kişi
lui|pron|him; to him; to her||onu; ona
eux|pron|them (masculine)||onlar; onları (eril)
moi|pron|me (stressed)||ben; beni (vurgulu)
toi|pron|you (stressed)||sen; seni (vurgulu)
y|pron|there; to it||orada; oraya; ona
en|pron|of it; some; in||ondan; biraz; -de
# ---- numbers ----
zéro|num|zero||sıfır
un|num|one||bir
deux|num|two||iki
trois|num|three||üç
quatre|num|four||dört
cinq|num|five||beş
six|num|six||altı
sept|num|seven||yedi
huit|num|eight||sekiz
neuf|num|nine||dokuz
dix|num|ten||on
onze|num|eleven||on bir
douze|num|twelve||on iki
treize|num|thirteen||on üç
quatorze|num|fourteen||on dört
quinze|num|fifteen||on beş
seize|num|sixteen||on altı
dix-sept|num|seventeen||on yedi
dix-huit|num|eighteen||on sekiz
dix-neuf|num|nineteen||on dokuz
vingt|num|twenty||yirmi
vingt et un|num|twenty-one||yirmi bir
trente|num|thirty||otuz
quarante|num|forty||kırk
cinquante|num|fifty||elli
soixante|num|sixty||altmış
soixante-dix|num|seventy||yetmiş
quatre-vingts|num|eighty||seksen
quatre-vingt-dix|num|ninety||doksan
cent|num|hundred||yüz
mille|num|thousand||bin
million|n m|million||milyon
premier|num|first||birinci; ilk
deuxième|num|second||ikinci
troisième|num|third||üçüncü
dernier|adj|last||son; sonuncu
moitié|n f|half||yarı; yarım
demi|adj|half||yarım; buçuk
fois|n f|time (occasion)||kez; defa
beaucoup|adv|much; many; a lot||çok
peu|adv|little; few||az
plusieurs|pron|several||birçok; birkaç
quelques|pron|some; a few||birkaç; bazı
un peu|phr|a little||biraz
# ---- time ----
temps|n m|time; weather||zaman; hava
heure|n f|hour; o'clock||saat
minute|n f|minute||dakika
seconde|n f|second||saniye
jour|n m|day||gün
journée|n f|day (duration)||gün (süre)
nuit|n f|night||gece
matin|n m|morning||sabah
après-midi|n m|afternoon||öğleden sonra
soir|n m|evening||akşam
soirée|n f|evening (duration); party||akşam (süre); eğlence; parti
semaine|n f|week||hafta
week-end|n m|weekend||hafta sonu
mois|n m|month||ay
an|n m|year||yıl; sene
année|n f|year (duration)||yıl (süre)
siècle|n m|century||yüzyıl; asır
aujourd'hui|adv|today||bugün
demain|adv|tomorrow||yarın
hier|adv|yesterday||dün
après-demain|adv|the day after tomorrow||öbür gün
avant-hier|adv|the day before yesterday||evvelsi gün
maintenant|adv|now||şimdi
tout de suite|phr|right away||hemen
bientôt|adv|soon||yakında
plus tard|phr|later||daha sonra
avant|prep|before||önce; -den önce
après|prep|after||sonra; -den sonra
tôt|adv|early||erken
tard|adv|late||geç
toujours|adv|always; still||her zaman; hâlâ
jamais|adv|never||asla; hiç
parfois|adv|sometimes||bazen
souvent|adv|often||sık sık
rarement|adv|rarely||nadiren
d'habitude|phr|usually||genellikle
déjà|adv|already||zaten; çoktan
encore|adv|still; again; more||hâlâ; yine; daha
pas encore|phr|not yet||henüz değil
d'abord|adv|first; at first||önce; ilk olarak
puis|adv|then||sonra
ensuite|adv|then; next||sonra; ardından
enfin|adv|finally||sonunda; nihayet
soudain|adv|suddenly||aniden; birden
longtemps|adv|for a long time||uzun süre; uzun zamandır
lundi|n m|Monday||pazartesi
mardi|n m|Tuesday||salı
mercredi|n m|Wednesday||çarşamba
jeudi|n m|Thursday||perşembe
vendredi|n m|Friday||cuma
samedi|n m|Saturday||cumartesi
dimanche|n m|Sunday||pazar
janvier|n m|January||ocak
février|n m|February||şubat
mars|n m|March||mart
avril|n m|April||nisan
mai|n m|May||mayıs
juin|n m|June||haziran
juillet|n m|July||temmuz
août|n m|August||ağustos
septembre|n m|September||eylül
octobre|n m|October||ekim
novembre|n m|November||kasım
décembre|n m|December||aralık
printemps|n m|spring||ilkbahar
été|n m|summer||yaz
automne|n m|autumn||sonbahar
hiver|n m|winter||kış
fête|n f|party; holiday; festival||bayram; parti; şenlik
vacances|n f pl|holidays; vacation||tatil
anniversaire|n m|birthday; anniversary||doğum günü; yıl dönümü
rendez-vous|n m|appointment; date||randevu
calendrier|n m|calendar||takvim
date|n f|date||tarih
# ---- family / people ----
homme|n m|man||adam; erkek
femme|n f|woman; wife||kadın; eş (karı)
enfant|n mf|child||çocuk
garçon|n m|boy; waiter||oğlan; garson
fille|n f|girl; daughter||kız
bébé|n m|baby||bebek
famille|n f|family||aile
parents|n m pl|parents||anne baba; ebeveynler
mère|n f|mother||anne
père|n m|father||baba
maman|n f|mom||anne; anneciğim
papa|n m|dad||baba; babacığım
fils|n m|son||oğul
frère|n m|brother||erkek kardeş; ağabey
sœur|n f|sister||kız kardeş; abla
grand-mère|n f|grandmother||büyükanne
grand-père|n m|grandfather||büyükbaba
grands-parents|n m pl|grandparents||büyükanne ve büyükbaba
petit-fils|n m|grandson||erkek torun
petite-fille|n f|granddaughter||kız torun
oncle|n m|uncle||amca; dayı
tante|n f|aunt||teyze; hala
cousin|n m|cousin (male)||kuzen (erkek)
cousine|n f|cousin (female)||kuzen (kız)
mari|n m|husband||koca
époux|n m|husband; spouse||koca; eş
ami|n m|friend (male)||arkadaş (erkek)
amie|n f|friend (female)||arkadaş (kız)
copain|n m|friend; boyfriend||arkadaş; erkek arkadaş
copine|n f|friend; girlfriend||arkadaş; kız arkadaş
voisin|n m|neighbour||komşu
invité|n m|guest||misafir; davetli
collègue|n mf|colleague||meslektaş; iş arkadaşı
patron|n m|boss||patron
monsieur|n m|Mr; sir; gentleman||bay; beyefendi
madame|n f|Mrs; madam||bayan; hanımefendi
mademoiselle|n f|Miss||küçük hanım; bayan (evlenmemiş)
nom|n m|name; surname||ad; soyadı
prénom|n m|first name||ad; ilk ad
âge|n m|age||yaş
adulte|n mf|adult||yetişkin
adolescent|n m|teenager||ergen; genç
personne|n f|person||kişi
gens|n m pl|people||insanlar
peuple|n m|people; nation||halk; millet
# ---- jobs ----
travail|n m|work; job||iş; çalışma
métier|n m|profession; trade||meslek; zanaat
médecin|n m|doctor||doktor
professeur|n m|teacher; professor||öğretmen; profesör
élève|n mf|pupil||öğrenci
étudiant|n m|student||öğrenci (üniversite)
ingénieur|n m|engineer||mühendis
informaticien|n m|computer scientist; IT specialist||bilgisayarcı; bilişim uzmanı
vendeur|n m|shop assistant; seller||satıcı; tezgâhtar
cuisinier|n m|cook; chef||aşçı
serveur|n m|waiter||garson
chauffeur|n m|driver||şoför
policier|n m|police officer||polis
journaliste|n mf|journalist||gazeteci
artiste|n mf|artist||sanatçı
musicien|n m|musician||müzisyen
acteur|n m|actor||oyuncu; aktör
écrivain|n m|writer||yazar
avocat|n m|lawyer||avukat
boulanger|n m|baker||fırıncı
coiffeur|n m|hairdresser||kuaför; berber
infirmier|n m|nurse (male)||hemşire (erkek); hastabakıcı
infirmière|n f|nurse (female)||hemşire
ouvrier|n m|worker||işçi
mécanicien|n m|mechanic||tamirci; makinist
secrétaire|n mf|secretary||sekreter
fonctionnaire|n mf|civil servant||memur; devlet memuru
entrepreneur|n m|entrepreneur||girişimci; müteşebbis
scientifique|n mf|scientist||bilim insanı
traducteur|n m|translator||çevirmen; tercüman
entreprise|n f|company; enterprise||şirket; işletme
société|n f|company; society||şirket; toplum
bureau|n m|office; desk||büro; ofis; çalışma masası
usine|n f|factory||fabrika
salaire|n m|salary||maaş
client|n m|customer||müşteri
réunion|n f|meeting||toplantı
contrat|n m|contract||sözleşme
candidature|n f|application (job)||iş başvurusu; adaylık
CV|n m|CV; résumé||öz geçmiş
poste|n m|position; job||görev; pozisyon; kadro
chômage|n m|unemployment||işsizlik
carrière|n f|career||kariyer
# ---- home ----
maison|n f|house||ev
appartement|n m|flat; apartment||daire; apartman dairesi
pièce|n f|room; piece; coin||oda; parça; madenî para
chambre|n f|bedroom; room||yatak odası; oda
cuisine|n f|kitchen; cooking||mutfak; yemek pişirme
salon|n m|living room||salon; oturma odası
salle de bains|n f|bathroom||banyo
toilettes|n f pl|toilet||tuvalet
couloir|n m|corridor||koridor
balcon|n m|balcony||balkon
jardin|n m|garden||bahçe
cave|n f|cellar||bodrum; mahzen
toit|n m|roof||çatı; dam
étage|n m|floor; storey||kat
escalier|n m|stairs||merdiven
ascenseur|n m|lift; elevator||asansör
porte|n f|door||kapı
fenêtre|n f|window||pencere
mur|n m|wall||duvar
sol|n m|floor; ground||zemin; yer; toprak
plafond|n m|ceiling||tavan
meuble|n m|piece of furniture||mobilya
table|n f|table||masa
chaise|n f|chair||sandalye
fauteuil|n m|armchair||koltuk
canapé|n m|sofa||kanepe
lit|n m|bed||yatak
armoire|n f|wardrobe||dolap; gardırop
étagère|n f|shelf||raf
miroir|n m|mirror||ayna
lampe|n f|lamp||lamba
lumière|n f|light||ışık
tapis|n m|carpet; rug||halı; kilim
tableau|n m tableaux|painting; board; blackboard; table (chart)||tablo; pano; yazı tahtası; çizelge
frigo|n m|fridge||buzdolabı
réfrigérateur|n m|refrigerator||buzdolabı
cuisinière|n f|cooker; stove||ocak; fırınlı ocak
four|n m|oven||fırın
machine à laver|n f|washing machine||çamaşır makinesi
télévision|n f|television||televizyon
clé|n f|key||anahtar
poubelle|n f|bin; trash can||çöp kutusu
loyer|n m|rent||kira
quartier|n m|neighbourhood; district||mahalle; semt
ranger|v|to tidy up; to put away||toplamak; düzenlemek; yerine kaldırmak
nettoyer|v|to clean||temizlemek
laver|v|to wash||yıkamak
cuisiner|v|to cook||yemek pişirmek
habiter|v|to live (in a place)||oturmak; ikamet etmek
déménager|v|to move (house)||taşınmak
louer|v|to rent||kiralamak
# ---- everyday objects ----
chose|n f|thing||şey
objet|n m|object||nesne; eşya
sac|n m|bag||çanta; torba
sac à dos|n m|backpack||sırt çantası
valise|n f|suitcase||valiz; bavul
portefeuille|n m|wallet||cüzdan
argent|n m|money; silver||para; gümüş
portable|n m|mobile phone; laptop||cep telefonu; dizüstü bilgisayar
téléphone|n m|telephone||telefon
ordinateur|n m|computer||bilgisayar
lunettes|n f pl|glasses||gözlük
parapluie|n m|umbrella||şemsiye
livre|n m|book||kitap
cahier|n m|notebook; exercise book||defter
stylo|n m|pen||kalem; tükenmez kalem
crayon|n m|pencil||kurşun kalem
papier|n m|paper||kâğıt
lettre|n f|letter (mail); letter (alphabet)||mektup; harf
journal|n m journaux|newspaper; diary||gazete; günlük
magazine|n m|magazine||dergi
photo|n f|photo||fotoğraf
cadeau|n m cadeaux|present; gift||hediye; armağan
jouet|n m|toy||oyuncak
ballon|n m|ball; balloon||top; balon
montre|n f|watch||kol saati; saat
carte|n f|card; map; menu||kart; harita; menü
boîte|n f|box; can; nightclub||kutu; konserve; gece kulübü
bouteille|n f|bottle||şişe
# ---- clothing ----
vêtement|n m|piece of clothing||giysi; elbise
robe|n f|dress||elbise
chemise|n f|shirt||gömlek
t-shirt|n m|T-shirt||tişört
pantalon|n m|trousers; pants||pantolon
jean|n m|jeans||kot pantolon
jupe|n f|skirt||etek
manteau|n m manteaux|coat||palto; manto
veste|n f|jacket||ceket
costume|n m|suit; costume||takım elbise; kostüm
pull|n m|sweater||kazak
bonnet|n m|beanie; cap||bere
chapeau|n m chapeaux|hat||şapka
écharpe|n f|scarf||atkı; eşarp
gant|n m|glove||eldiven
chaussette|n f|sock||çorap
chaussure|n f|shoe||ayakkabı
botte|n f|boot||çizme; bot
basket|n f|sneaker||spor ayakkabı
taille|n f|size; waist; height||beden; bel; boy
mettre|v|to put; to put on|mis|koymak; giymek
enlever|v|to take off; to remove||çıkarmak; kaldırmak
porter|v|to wear; to carry||giymek; taşımak
essayer|v|to try; to try on||denemek; prova etmek
# ---- body / health ----
corps|n m|body||vücut; beden
tête|n f|head||baş; kafa
visage|n m|face||yüz
œil|n m yeux|eye||göz
oreille|n f|ear||kulak
nez|n m|nose||burun
bouche|n f|mouth||ağız
dent|n f|tooth||diş
cheveux|n m pl|hair||saç
cou|n m|neck||boyun
gorge|n f|throat||boğaz
épaule|n f|shoulder||omuz
bras|n m|arm||kol
main|n f|hand||el
doigt|n m|finger||parmak
jambe|n f|leg||bacak
pied|n m|foot||ayak
genou|n m genoux|knee||diz
dos|n m|back||sırt
ventre|n m|belly; stomach||karın; mide
cœur|n m|heart||kalp; yürek
sang|n m|blood||kan
peau|n f|skin||deri; cilt
santé|n f|health||sağlık
en bonne santé|phr|healthy||sağlıklı
malade|adj|ill; sick||hasta
maladie|n f|illness; disease||hastalık
douleur|n f|pain||ağrı; acı
mal de tête|n m|headache||baş ağrısı
fièvre|n f|fever||ateş
rhume|n m|cold (illness)||nezle; soğuk algınlığı
toux|n f|cough||öksürük
médicament|n m|medicine; drug||ilaç
comprimé|n m|tablet; pill||tablet; hap
pharmacie|n f|pharmacy||eczane
hôpital|n m hôpitaux|hospital||hastane
cabinet|n m|doctor's office||muayenehane
urgences|n f pl|emergency room||acil servis
accident|n m|accident||kaza
fatigué|adj|tired||yorgun
dormir|v|to sleep|dormi|uyumak
s'endormir|v|to fall asleep||uykuya dalmak
se réveiller|v|to wake up||uyanmak
se lever|v|to get up||kalkmak
se reposer|v|to rest||dinlenmek
avoir mal|phr|to hurt; to be in pain||ağrımak; canı acımak
# ---- food / drink ----
nourriture|n f|food||yiyecek; besin
repas|n m|meal||yemek; öğün
petit déjeuner|n m|breakfast||kahvaltı
déjeuner|n m|lunch||öğle yemeği
dîner|n m|dinner||akşam yemeği
pain|n m|bread||ekmek
beurre|n m|butter||tereyağı
fromage|n m|cheese||peynir
lait|n m|milk||süt
œuf|n m|egg||yumurta
viande|n f|meat||et
poulet|n m|chicken||tavuk
poisson|n m|fish||balık
saucisse|n f|sausage||sosis
jambon|n m|ham||jambon
soupe|n f|soup||çorba
riz|n m|rice||pirinç; pilav
pâtes|n f pl|pasta||makarna
pomme de terre|n f|potato||patates
frites|n f pl|chips; French fries||patates kızartması
légume|n m|vegetable||sebze
fruit|n m|fruit||meyve
pomme|n f|apple||elma
poire|n f|pear||armut
banane|n f|banana||muz
orange|n f|orange||portakal
citron|n m|lemon||limon
raisin|n m|grape||üzüm
fraise|n f|strawberry||çilek
tomate|n f|tomato||domates
concombre|n m|cucumber||salatalık
oignon|n m|onion||soğan
ail|n m|garlic||sarımsak
salade|n f|salad; lettuce||salata; marul
carotte|n f|carrot||havuç
champignon|n m|mushroom||mantar
sel|n m|salt||tuz
sucre|n m|sugar||şeker
poivre|n m|pepper||karabiber
huile|n f|oil||yağ (sıvı)
miel|n m|honey||bal
gâteau|n m gâteaux|cake||pasta; kek
biscuit|n m|biscuit; cookie||bisküvi; kurabiye
chocolat|n m|chocolate||çikolata
glace|n f|ice cream; ice; mirror||dondurma; buz; ayna
bonbon|n m|sweet; candy||şeker (bonbon); şekerleme
eau|n f eaux|water||su
thé|n m|tea||çay
café|n m|coffee; cafe||kahve; kafe
jus|n m|juice||meyve suyu
bière|n f|beer||bira
vin|n m|wine||şarap
verre|n m|glass||bardak; cam
tasse|n f|cup||fincan
assiette|n f|plate||tabak
cuillère|n f|spoon||kaşık
fourchette|n f|fork||çatal
couteau|n m couteaux|knife||bıçak
casserole|n f|saucepan||tencere
poêle|n f|frying pan||tava
restaurant|n m|restaurant||restoran; lokanta
boulangerie|n f|bakery||fırın (ekmek)
menu|n m|menu; set meal||menü; tabldot
addition|n f|bill (restaurant); addition||hesap (restoran); toplama
pourboire|n m|tip (money)||bahşiş
délicieux|adj|delicious||lezzetli; nefis
sucré|adj|sweet||tatlı; şekerli
salé|adj|salty||tuzlu
épicé|adj|spicy||baharatlı; acı
frais|adj|fresh; cool||taze; serin
faim|n f|hunger||açlık
soif|n f|thirst||susuzluk
avoir faim|phr|to be hungry||acıkmak; aç olmak
avoir soif|phr|to be thirsty||susamak; susuz olmak
manger|v|to eat||yemek
boire|v|to drink|bu|içmek
prendre le petit déjeuner|phr|to have breakfast||kahvaltı yapmak
commander|v|to order||sipariş vermek; ısmarlamak
payer|v|to pay||ödemek
goûter|v|to taste||tatmak; tadına bakmak
# ---- city / transport ----
ville|n f|city; town||şehir; kent
village|n m|village||köy
pays|n m|country||ülke
capitale|n f|capital city||başkent
rue|n f|street||sokak; cadde
place|n f|square; place; seat||meydan; yer; koltuk
route|n f|road||yol; karayolu
chemin|n m|path; way||patika; yol
pont|n m|bridge||köprü
parc|n m|park||park
centre|n m|centre||merkez
centre-ville|n m|city centre||şehir merkezi
bâtiment|n m|building||bina; yapı
immeuble|n m|apartment building||apartman
église|n f|church||kilise
musée|n m|museum||müze
théâtre|n m|theatre||tiyatro
cinéma|n m|cinema||sinema
bibliothèque|n f|library||kütüphane
école|n f|school||okul
lycée|n m|secondary school; high school||lise
université|n f|university||üniversite
banque|n f|bank||banka
poste|n f|post office||postane
hôtel|n m|hotel||otel
gare|n f|railway station||tren istasyonu; gar
arrêt|n m|stop (bus)||durak
aéroport|n m|airport||havalimanı; havaalanı
métro|n m|metro; underground||metro
bus|n m|bus||otobüs
tramway|n m|tram||tramvay
voiture|n f|car||araba; otomobil
taxi|n m|taxi||taksi
train|n m|train||tren
avion|n m|plane||uçak
bateau|n m bateaux|boat; ship||tekne; gemi
vélo|n m|bicycle||bisiklet
billet|n m|ticket; banknote||bilet; banknot
ticket|n m|ticket (metro, bus)||bilet (metro, otobüs)
passeport|n m|passport||pasaport
carte d'identité|n f|ID card||kimlik kartı
frontière|n f|border||sınır
voyage|n m|journey; trip||yolculuk; seyahat
excursion|n f|excursion||gezi
touriste|n mf|tourist||turist
plan|n m|map (city); plan||şehir haritası; plan
adresse|n f|address||adres
feu|n m feux|traffic light; fire||trafik ışığı; ateş
carrefour|n m|crossroads||kavşak
coin|n m|corner||köşe
parking|n m|car park||otopark
station-service|n f|petrol station||benzin istasyonu
embouteillage|n m|traffic jam||trafik sıkışıklığı
horaire|n m|timetable; schedule||tarife; zaman çizelgesi
départ|n m|departure||kalkış; hareket
arrivée|n f|arrival||varış
quai|n m|platform; quay||peron; rıhtım
entrée|n f|entrance; starter||giriş; başlangıç yemeği
sortie|n f|exit||çıkış
à droite|phr|on the right; to the right||sağda; sağa
à gauche|phr|on the left; to the left||solda; sola
tout droit|phr|straight ahead||dümdüz; doğru ileri
loin|adv|far||uzak; uzakta
près|adv|near||yakın; yakında
ici|adv|here||burada
là|adv|there||orada
là-bas|adv|over there||şurada; orada (uzakta)
chez|prep|at the home of||-in evinde; -in yanında
à la maison|phr|at home||evde
en haut|phr|upstairs; above||yukarıda; üst katta
en bas|phr|downstairs; below||aşağıda; alt katta
dedans|adv|inside||içeride
dehors|adv|outside||dışarıda
partout|adv|everywhere||her yerde
nulle part|phr|nowhere||hiçbir yerde
# ---- movement verbs ----
aller|v|to go|allé (être)|gitmek
venir|v|to come|venu (être)|gelmek
partir|v|to leave|parti (être)|ayrılmak; yola çıkmak
arriver|v|to arrive; to happen|arrivé (être)|varmak; olmak (gerçekleşmek)
entrer|v|to enter|entré (être)|girmek
sortir|v|to go out|sorti (être)|çıkmak; dışarı çıkmak
monter|v|to go up; to get on|monté (être)|çıkmak (yukarı); binmek
descendre|v|to go down; to get off|descendu (être)|inmek
rentrer|v|to return home|rentré (être)|eve dönmek
revenir|v|to come back|revenu (être)|geri gelmek
retourner|v|to return; to go back|retourné (être)|geri dönmek
passer|v|to pass; to spend (time)||geçmek; (zaman) geçirmek
traverser|v|to cross||karşıya geçmek; geçmek
marcher|v|to walk; to work (function)||yürümek; çalışmak (işlemek)
courir|v|to run|couru|koşmak
voler|v|to fly; to steal||uçmak; çalmak (hırsızlık)
nager|v|to swim||yüzmek
conduire|v|to drive|conduit|araba kullanmak; sürmek
voyager|v|to travel||seyahat etmek
apporter|v|to bring (a thing)||getirmek (bir şeyi)
amener|v|to bring (a person)||getirmek (birini)
emmener|v|to take (a person) along||götürmek (birini)
chercher|v|to look for; to fetch||aramak; almaya gitmek
suivre|v|to follow|suivi|takip etmek; izlemek
sauter|v|to jump||atlamak; zıplamak
tomber|v|to fall|tombé (être)|düşmek
# ---- core verbs ----
être|v|to be|été|olmak
avoir|v|to have|eu|sahip olmak
faire|v|to do; to make|fait|yapmak
dire|v|to say; to tell|dit|söylemek; demek
parler|v|to speak; to talk||konuşmak
raconter|v|to tell (a story)||anlatmak
demander|v|to ask||sormak; istemek
répondre|v|to answer|répondu|cevap vermek; yanıtlamak
savoir|v|to know (facts)|su|bilmek
connaître|v|to know (be familiar with)|connu|tanımak; bilmek
penser|v|to think||düşünmek
croire|v|to believe|cru|inanmak; sanmak
comprendre|v|to understand|compris|anlamak
vouloir|v|to want|voulu|istemek
pouvoir|v|can; to be able|pu|-ebilmek; yapabilmek
devoir|v|must; to have to|dû|zorunda olmak; -meli
falloir|v|to be necessary|fallu (il faut)|gerekmek
aimer|v|to love; to like||sevmek; hoşlanmak
adorer|v|to love; to adore||bayılmak; çok sevmek
détester|v|to hate||nefret etmek
préférer|v|to prefer||tercih etmek
voir|v|to see|vu|görmek
regarder|v|to look at; to watch||bakmak; izlemek
entendre|v|to hear|entendu|duymak; işitmek
écouter|v|to listen||dinlemek
lire|v|to read|lu|okumak
écrire|v|to write|écrit|yazmak
apprendre|v|to learn|appris|öğrenmek
étudier|v|to study||ders çalışmak; okumak (eğitim)
enseigner|v|to teach||öğretmek
travailler|v|to work||çalışmak
vivre|v|to live|vécu|yaşamak
jouer|v|to play||oynamak; çalmak (müzik)
donner|v|to give||vermek
prendre|v|to take|pris|almak
recevoir|v|to receive|reçu|almak (teslim); kabul etmek
acheter|v|to buy||satın almak
vendre|v|to sell|vendu|satmak
faire les courses|phr|to do the shopping||alışveriş yapmak
coûter|v|to cost||mal olmak; fiyatı olmak
ouvrir|v|to open|ouvert|açmak
fermer|v|to close||kapatmak
commencer|v|to begin||başlamak
finir|v|to finish|fini|bitirmek
arrêter|v|to stop||durdurmak; durmak
continuer|v|to continue||devam etmek
attendre|v|to wait|attendu|beklemek
trouver|v|to find||bulmak
perdre|v|to lose|perdu|kaybetmek
se souvenir|v|to remember|souvenu (être)|hatırlamak
se rappeler|v|to remember||hatırlamak
oublier|v|to forget||unutmak
aider|v|to help||yardım etmek
appeler|v|to call||çağırmak; aramak (telefonla)
téléphoner|v|to phone||telefon etmek
rencontrer|v|to meet||karşılaşmak; tanışmak
se retrouver|v|to meet up||buluşmak
montrer|v|to show||göstermek
expliquer|v|to explain||açıklamak
traduire|v|to translate|traduit|çevirmek; tercüme etmek
répéter|v|to repeat||tekrarlamak
envoyer|v|to send||göndermek
poser|v|to put down; to ask (a question)||koymak; (soru) sormak
s'asseoir|v|to sit down|assis (être)|oturmak
être assis|phr|to be sitting||oturuyor olmak
se tenir debout|phr|to stand||ayakta durmak
rester|v|to stay|resté (être)|kalmak
tenir|v|to hold|tenu|tutmak
sentir|v|to feel; to smell|senti|hissetmek; koklamak
se sentir|v|to feel (state)||kendini hissetmek
avoir peur|phr|to be afraid||korkmak
espérer|v|to hope||ummak; umut etmek
décider|v|to decide||karar vermek
résoudre|v|to solve|résolu|çözmek
rêver|v|to dream||hayal etmek; rüya görmek
rire|v|to laugh|ri|gülmek
sourire|v|to smile|souri|gülümsemek
pleurer|v|to cry||ağlamak
crier|v|to shout||bağırmak
chanter|v|to sing||şarkı söylemek
danser|v|to dance||dans etmek
dessiner|v|to draw||çizmek; resim çizmek
peindre|v|to paint|peint|boyamak; resim yapmak
se promener|v|to go for a walk||gezinmek; yürüyüşe çıkmak
s'intéresser|v|to be interested (in)||ilgilenmek; ilgi duymak
s'appeler|v|to be called||adı olmak; adı ... olmak
se marier|v|to get married||evlenmek
naître|v|to be born|né (être)|doğmak
mourir|v|to die|mort (être)|ölmek
grandir|v|to grow up||büyümek
changer|v|to change||değişmek; değiştirmek
construire|v|to build|construit|inşa etmek; yapmak
casser|v|to break||kırmak
réparer|v|to repair||tamir etmek; onarmak
jeter|v|to throw; to throw away||atmak; çöpe atmak
lever|v|to lift; to raise||kaldırmak
bouger|v|to move||kımıldamak; hareket etmek
être en retard|phr|to be late||geç kalmak
se dépêcher|v|to hurry||acele etmek
réussir|v|to succeed||başarmak
inviter|v|to invite||davet etmek
proposer|v|to suggest; to offer||önermek; teklif etmek
conseiller|v|to advise||tavsiye etmek; öğüt vermek
recommander|v|to recommend||tavsiye etmek
promettre|v|to promise|promis|söz vermek
permettre|v|to allow|permis|izin vermek
interdire|v|to forbid|interdit|yasaklamak
vérifier|v|to check||kontrol etmek; doğrulamak
choisir|v|to choose||seçmek
comparer|v|to compare||karşılaştırmak
compter|v|to count||saymak
calculer|v|to calculate||hesaplamak
utiliser|v|to use||kullanmak
se servir de|phr|to use||kullanmak
avoir besoin de|phr|to need||ihtiyacı olmak; ihtiyaç duymak
planifier|v|to plan||planlamak
organiser|v|to organise||düzenlemek; organize etmek
participer|v|to take part||katılmak
gagner|v|to win; to earn||kazanmak
se passer|v|to happen||olmak; meydana gelmek
arriver à|phr|to manage to||başarmak; -ebilmek
sembler|v|to seem||görünmek; gibi görünmek
signifier|v|to mean||anlamına gelmek; ifade etmek
vouloir dire|phr|to mean||demek istemek; anlamına gelmek
exister|v|to exist||var olmak
suffire|v|to be enough|suffi|yetmek; yeterli olmak
appartenir|v|to belong|appartenu|ait olmak
laisser|v|to let; to leave||bırakmak; izin vermek
quitter|v|to leave (a place or person)||terk etmek; ayrılmak
visiter|v|to visit (a place)||ziyaret etmek; gezmek
rendre visite à|phr|to visit (a person)||ziyaret etmek (birini)
saluer|v|to greet||selamlamak
dire au revoir|phr|to say goodbye||vedalaşmak; hoşça kal demek
remercier|v|to thank||teşekkür etmek
s'excuser|v|to apologise||özür dilemek
se réjouir|v|to be glad||sevinmek
s'énerver|v|to get annoyed||sinirlenmek
s'inquiéter|v|to worry||endişelenmek
se plaindre|v|to complain|plaint|şikayet etmek; yakınmak
se disputer|v|to argue||tartışmak; kavga etmek
discuter|v|to discuss||tartışmak; sohbet etmek
être d'accord|phr|to agree||aynı fikirde olmak; hemfikir olmak
refuser|v|to refuse||reddetmek
faire attention|phr|to pay attention||dikkat etmek
remarquer|v|to notice||fark etmek
décrire|v|to describe|décrit|tanımlamak; betimlemek
se présenter|v|to introduce oneself||kendini tanıtmak
imaginer|v|to imagine||hayal etmek; tasavvur etmek
dépendre|v|to depend|dépendu|bağlı olmak
influencer|v|to influence||etkilemek
développer|v|to develop||geliştirmek
protéger|v|to protect||korumak
détruire|v|to destroy|détruit|yok etmek; yıkmak
économiser|v|to save (money)||para biriktirmek; tasarruf etmek
dépenser|v|to spend (money)||para harcamak
mériter|v|to deserve||hak etmek
démissionner|v|to resign||istifa etmek
diriger|v|to lead; to manage||yönetmek; yönlendirmek
fumer|v|to smoke||sigara içmek
maigrir|v|to lose weight||zayıflamak; kilo vermek
grossir|v|to gain weight||kilo almak; şişmanlamak
soigner|v|to treat; to look after||tedavi etmek; bakmak
guérir|v|to cure; to recover||iyileştirmek; iyileşmek
# ---- adjectives ----
grand|adj|big; tall||büyük; uzun boylu
petit|adj|small; little||küçük
bon|adj|good||iyi
mauvais|adj|bad||kötü
nouveau|adj|new|nouvelle (f), nouveaux (pl)|yeni
vieux|adj|old|vieille (f)|yaşlı; eski
jeune|adj|young||genç
beau|adj|beautiful; handsome|belle (f), beaux (pl)|güzel; yakışıklı
joli|adj|pretty||güzel; hoş
laid|adj|ugly||çirkin
intelligent|adj|intelligent; clever||zeki; akıllı
bête|adj|stupid||aptal
gentil|adj|kind; nice||nazik; kibar
sympathique|adj|nice; friendly||sempatik; cana yakın
méchant|adj|mean; nasty||kötü; huysuz
drôle|adj|funny||komik
triste|adj|sad||üzgün
heureux|adj|happy||mutlu
content|adj|pleased; glad||memnun; hoşnut
intéressant|adj|interesting||ilginç
ennuyeux|adj|boring||sıkıcı
important|adj|important||önemli
difficile|adj|difficult||zor
facile|adj|easy||kolay
simple|adj|simple||basit
compliqué|adj|complicated||karmaşık
cher|adj|expensive; dear||pahalı; sevgili
bon marché|adj|cheap||ucuz
riche|adj|rich||zengin
pauvre|adj|poor||fakir; zavallı
fort|adj|strong||güçlü; kuvvetli
faible|adj|weak||zayıf
haut|adj|high; tall||yüksek; uzun
bas|adj|low||alçak; düşük
long|adj|long|longue (f)|uzun
court|adj|short||kısa
large|adj|wide||geniş
étroit|adj|narrow||dar
gros|adj|big; fat||iri; şişman
mince|adj|thin; slim||ince; zayıf
épais|adj|thick||kalın
lourd|adj|heavy||ağır
léger|adj|light (weight)||hafif
chaud|adj|hot; warm||sıcak
froid|adj|cold||soğuk
tiède|adj|lukewarm||ılık
rapide|adj|fast||hızlı
lent|adj|slow||yavaş
bruyant|adj|noisy||gürültülü
calme|adj|calm; quiet||sakin
propre|adj|clean; own||temiz; kendi
sale|adj|dirty||kirli
clair|adj|light; clear||açık; aydınlık
sombre|adj|dark||karanlık; koyu
plein|adj|full||dolu
vide|adj|empty||boş
ouvert|adj|open||açık
fermé|adj|closed||kapalı
libre|adj|free||özgür; boş
occupé|adj|busy; occupied||meşgul; dolu
prêt|adj|ready||hazır
juste|adj|correct; fair||doğru; adil
faux|adj|wrong; false|fausse (f)|yanlış; sahte
vrai|adj|true; real||doğru; gerçek
possible|adj|possible||mümkün
impossible|adj|impossible||imkânsız
nécessaire|adj|necessary||gerekli
même|adj|same; even||aynı
différent|adj|different||farklı
autre|adj|other||başka; diğer
prochain|adj|next||gelecek; sonraki
précédent|adj|previous||önceki
seul|adj|alone; only||yalnız; tek
ensemble|adv|together||birlikte
entier|adj|whole; entire||bütün; tüm
confortable|adj|comfortable||rahat; konforlu
dangereux|adj|dangerous||tehlikeli
sûr|adj|sure; safe||emin; güvenli
honnête|adj|honest||dürüst
poli|adj|polite||kibar; nazik
sérieux|adj|serious||ciddi
mouillé|adj|wet||ıslak
sec|adj|dry|sèche (f)|kuru
doux|adj|soft; gentle; sweet|douce (f)|yumuşak; tatlı
dur|adj|hard||sert
rond|adj|round||yuvarlak
vivant|adj|alive; lively||canlı
mort|adj|dead||ölü
célèbre|adj|famous||ünlü
populaire|adj|popular||popüler
moderne|adj|modern||modern
connu|adj|known; well-known||bilinen; tanınmış
étranger|adj|foreign||yabancı
français|adj|French||Fransız; Fransızca
anglais|adj|English||İngiliz; İngilizce
turc|adj|Turkish|turque (f)|Türk; Türkçe
allemand|adj|German||Alman; Almanca
russe|adj|Russian||Rus; Rusça
travailleur|adj|hard-working||çalışkan
paresseux|adj|lazy||tembel
nerveux|adj|nervous||gergin; sinirli
fou|adj|crazy|folle (f)|deli; çılgın
fatigant|adj|tiring||yorucu
gratuit|adj|free of charge||ücretsiz; bedava
# ---- colours ----
couleur|n f|colour||renk
blanc|adj|white|blanche (f)|beyaz
noir|adj|black||siyah
rouge|adj|red||kırmızı
bleu|adj|blue||mavi
vert|adj|green||yeşil
jaune|adj|yellow||sarı
orange|adj|orange||turuncu
marron|adj|brown||kahverengi
gris|adj|grey||gri
rose|adj|pink||pembe
violet|adj|purple||mor
# ---- adverbs / prepositions / conjunctions ----
très|adv|very||çok
trop|adv|too; too much||fazla; çok fazla
presque|adv|almost||neredeyse
seulement|adv|only||sadece; yalnızca
aussi|adv|also; too||de/da; ayrıca
même|adv|even||bile; hatta
environ|adv|approximately||yaklaşık
exactement|adv|exactly||tam olarak
vraiment|adv|really||gerçekten
naturellement|adv|naturally||doğal olarak; tabii ki
probablement|adv|probably||muhtemelen
certainement|adv|certainly||kesinlikle
malheureusement|adv|unfortunately||ne yazık ki; maalesef
heureusement|adv|fortunately||neyse ki
surtout|adv|especially; above all||özellikle; her şeyden önce
assez|adv|enough; rather||yeterince; oldukça
plutôt|adv|rather||daha çok; daha ziyade
pas du tout|phr|not at all||hiç de değil
en fait|phr|actually; in fact||aslında
au fait|phr|by the way||bu arada
donc|conj|so; therefore||öyleyse; dolayısıyla
alors|adv|then; so||o zaman; öyleyse
pourtant|adv|however; yet||yine de; ancak
quand même|phr|anyway; all the same||yine de; her şeye rağmen
sinon|conj|otherwise||yoksa; aksi takdirde
d'ailleurs|adv|besides; moreover||ayrıca; zaten
cependant|adv|however||ancak; bununla birlikte
c'est-à-dire|phr|that is to say||yani
ne … pas|phr|not||değil; -me/-ma
ne … plus|phr|no longer||artık değil
ne … jamais|phr|never||asla; hiç
et|conj|and||ve
ou|conj|or||veya; ya da
mais|conj|but||ama; fakat
car|conj|because; for||çünkü; zira
parce que|conj|because||çünkü
que|conj|that||ki; -diği
si|conj|if||eğer; -se/-sa
bien que|conj|although||her ne kadar; -e rağmen
pour que|conj|so that||-mesi için; diye
avant que|conj|before||-meden önce
après que|conj|after||-dikten sonra
pendant que|conj|while||-ken; -diği sırada
depuis|prep|since; for||-den beri; -dir
jusqu'à|prep|until; up to||-e kadar
dans|prep|in; into||-de/-da; içinde
à|prep|to; at; in||-e/-a; -de/-da
sur|prep|on||üzerinde; üstünde
sous|prep|under||altında
au-dessus de|prep|above||üstünde; yukarısında
devant|prep|in front of||önünde
derrière|prep|behind||arkasında
à côté de|prep|next to||yanında
entre|prep|between||arasında
avec|prep|with||ile; -le/-la
sans|prep|without||-sız/-siz; olmadan
pour|prep|for; in order to||için
contre|prep|against||karşı
vers|prep|towards; around (time)||-e doğru; sularında
par|prep|by; through||tarafından; -den geçerek
de|prep|of; from||-in/-ın; -den/-dan
sauf|prep|except||hariç; dışında
à cause de|prep|because of||yüzünden; nedeniyle
grâce à|prep|thanks to||sayesinde
malgré|prep|despite||-e rağmen
au lieu de|prep|instead of||yerine
le long de|prep|along||boyunca
en face de|prep|opposite||karşısında
pendant|prep|during||sırasında; boyunca
# ---- education / language ----
langue|n f|language; tongue||dil
mot|n m|word||kelime; sözcük
phrase|n f|sentence||cümle
alphabet|n m|alphabet||alfabe
grammaire|n f|grammar||dil bilgisi; gramer
dictionnaire|n m|dictionary||sözlük
vocabulaire|n m|vocabulary||kelime hazinesi; sözcük dağarcığı
cours|n m|course; lesson; class||kurs; ders
leçon|n f|lesson||ders
classe|n f|class||sınıf
examen|n m|exam||sınav
note|n f|grade; mark; note||not
erreur|n f|mistake||hata
faute|n f|mistake; fault||hata; kusur
question|n f|question||soru
réponse|n f|answer||cevap; yanıt
règle|n f|rule; ruler||kural; cetvel
exemple|n m|example||örnek
exercice|n m|exercise||alıştırma; egzersiz
devoirs|n m pl|homework||ev ödevi
texte|n m|text||metin
histoire|n f|story; history||hikâye; tarih
littérature|n f|literature||edebiyat
mathématiques|n f pl|mathematics||matematik
physique|n f|physics||fizik
chimie|n f|chemistry||kimya
biologie|n f|biology||biyoloji
géographie|n f|geography||coğrafya
science|n f|science||bilim
sens|n m|meaning; sense; direction||anlam; duyu; yön
traduction|n f|translation||çeviri
prononciation|n f|pronunciation||telaffuz
mémoire|n f|memory||hafıza; bellek
attention|n f|attention||dikkat
connaissance|n f|knowledge; acquaintance||bilgi; tanışıklık
expérience|n f|experience; experiment||deneyim; deney
récréation|n f|break (school)||teneffüs
diplôme|n m|diploma; degree||diploma
formation|n f|training; education||eğitim; yetiştirme
# ---- money / shopping ----
prix|n m|price; prize||fiyat; ödül
euro|n m|euro||euro
centime|n m|cent||sent
caisse|n f|cash desk; checkout||kasa
monnaie|n f|change; currency||bozuk para; para birimi
réduction|n f|discount||indirim
promotion|n f|special offer||kampanya; promosyon
magasin|n m|shop||mağaza; dükkân
boutique|n f|shop; boutique||dükkân; butik
supermarché|n m|supermarket||süpermarket
marché|n m|market||pazar; çarşı
centre commercial|n m|shopping centre||alışveriş merkezi
grand magasin|n m|department store||büyük mağaza
marchandise|n f|goods||mal; ticari eşya
produit|n m|product||ürün
qualité|n f|quality||kalite
carte bancaire|n f|bank card||banka kartı
compte|n m|account||hesap
dette|n f|debt||borç
impôt|n m|tax||vergi
assurance|n f|insurance||sigorta
# ---- communication / technology ----
internet|n m|internet||internet
site|n m|website; site||web sitesi; site
courriel|n m|e-mail||e-posta
e-mail|n m|e-mail||e-posta
message|n m|message||mesaj
numéro|n m|number||numara
appel|n m|call||arama; çağrı
connexion|n f|connection||bağlantı
information|n f|information||bilgi
nouvelles|n f pl|news||haberler
programme|n m|programme||program
application|n f|application; app||uygulama
écran|n m|screen||ekran
touche|n f|key (keyboard)||tuş
clavier|n m|keyboard||klavye
souris|n f|mouse (animal); mouse (computer)||fare
fichier|n m|file||dosya
dossier|n m|folder; file||klasör; dosya
mot de passe|n m|password||şifre; parola
imprimante|n f|printer||yazıcı
radio|n f|radio||radyo
musique|n f|music||müzik
chanson|n f|song||şarkı
film|n m|film; movie||film
série|n f|series||dizi
jeu|n m jeux|game||oyun
appareil photo|n m|camera||fotoğraf makinesi
batterie|n f|battery||batarya; pil
pile|n f|battery (disposable)||pil
recharger|v|to recharge||şarj etmek
allumer|v|to switch on; to light||açmak (cihaz); yakmak
éteindre|v|to switch off|éteint|kapatmak (cihaz); söndürmek
télécharger|v|to download||indirmek (internetten)
imprimer|v|to print||yazdırmak
enregistrer|v|to save; to record||kaydetmek
supprimer|v|to delete||silmek
# ---- nature / weather ----
nature|n f|nature||doğa
météo|n f|weather forecast||hava durumu
soleil|n m|sun||güneş
lune|n f|moon||ay
étoile|n f|star||yıldız
ciel|n m|sky||gökyüzü
nuage|n m|cloud||bulut
pluie|n f|rain||yağmur
neige|n f|snow||kar
vent|n m|wind||rüzgâr
orage|n m|thunderstorm||fırtına; gök gürültülü fırtına
brouillard|n m|fog||sis
gel|n m|frost||don
chaleur|n f|heat||sıcaklık
degré|n m|degree||derece
terre|n f|earth; land; soil||yeryüzü; toprak; kara
monde|n m|world||dünya
air|n m|air||hava
mer|n f|sea||deniz
lac|n m|lake||göl
fleuve|n m|river (to the sea)||nehir; ırmak
rivière|n f|river||nehir; akarsu
plage|n f|beach||plaj; kumsal
île|n f|island||ada
montagne|n f|mountain||dağ
forêt|n f|forest||orman
champ|n m|field||tarla
arbre|n m|tree||ağaç
fleur|n f|flower||çiçek
herbe|n f|grass||ot; çimen
feuille|n f|leaf; sheet||yaprak; kâğıt yaprağı
pierre|n f|stone||taş
sable|n m|sand||kum
animal|n m animaux|animal||hayvan
chien|n m|dog||köpek
chat|n m|cat||kedi
cheval|n m chevaux|horse||at
vache|n f|cow||inek
cochon|n m|pig||domuz
oiseau|n m oiseaux|bird||kuş
ours|n m|bear||ayı
loup|n m|wolf||kurt
renard|n m|fox||tilki
lapin|n m|rabbit||tavşan
serpent|n m|snake||yılan
insecte|n m|insect||böcek
il pleut|phr|it is raining||yağmur yağıyor
il neige|phr|it is snowing||kar yağıyor
il fait froid|phr|it is cold||hava soğuk
il fait chaud|phr|it is hot||hava sıcak
il fait beau|phr|the weather is nice||hava güzel
ensoleillé|adj|sunny||güneşli
nuageux|adj|cloudy||bulutlu
# ---- sport / leisure ----
sport|n m|sport||spor
football|n m|football||futbol
tennis|n m|tennis||tenis
échecs|n m pl|chess||satranç
piscine|n f|swimming pool||yüzme havuzu
stade|n m|stadium||stadyum
équipe|n f|team||takım
match|n m|match||maç
entraînement|n m|training||antrenman
victoire|n f|victory||zafer; galibiyet
passe-temps|n m|hobby||hobi
loisirs|n m pl|leisure||boş zaman etkinlikleri
concert|n m|concert||konser
exposition|n f|exhibition||sergi
spectacle|n m|show; performance||gösteri
fêter|v|to celebrate||kutlamak
club|n m|club||kulüp
# ---- feelings / abstract ----
vie|n f|life||hayat; yaşam
amour|n m|love||aşk; sevgi
amitié|n f|friendship||dostluk; arkadaşlık
bonheur|n m|happiness||mutluluk
joie|n f|joy||sevinç
peur|n f|fear||korku
espoir|n m|hope||umut
rêve|n m|dream||rüya; hayal
vérité|n f|truth||gerçek; hakikat
mensonge|n m|lie||yalan
pensée|n f|thought||düşünce
idée|n f|idea||fikir
avis|n m|opinion||görüş; kanı
opinion|n f|opinion||görüş; fikir
sentiment|n m|feeling||duygu; his
humeur|n f|mood||ruh hali; keyif
souhait|n m|wish||dilek
envie|n f|desire; wish||istek; arzu
intérêt|n m|interest||ilgi; çıkar
liberté|n f|freedom||özgürlük
droit|n m|right; law||hak; hukuk
loi|n f|law||yasa; kanun
ordre|n m|order||düzen; emir
choix|n m|choice||seçim; tercih
possibilité|n f|possibility||olasılık; imkân
raison|n f|reason||neden; akıl
conséquence|n f|consequence||sonuç
cas|n m|case||durum; vaka
manière|n f|manner; way||tarz; biçim
façon|n f|way; manner||şekil; tarz
condition|n f|condition||koşul; şart
différence|n f|difference||fark
partie|n f|part; game||bölüm; parti (oyun)
fin|n f|end||son
début|n m|beginning||başlangıç
milieu|n m|middle; environment||orta; çevre
lieu|n m lieux|place||yer
endroit|n m|place||yer
côté|n m|side||taraf; yan
forme|n f|form; shape||biçim; şekil
nombre|n m|number||sayı
quantité|n f|quantity||miktar
poids|n m|weight||ağırlık
état|n m|state; condition||durum; devlet
gouvernement|n m|government||hükûmet
guerre|n f|war||savaş
paix|n f|peace||barış
police|n f|police||polis
culture|n f|culture||kültür
art|n m|art||sanat
religion|n f|religion||din
problème|n m|problem||sorun; problem
solution|n f|solution||çözüm
succès|n m|success||başarı
but|n m|goal; aim||amaç; hedef
projet|n m|project||proje
résultat|n m|result||sonuç
environnement|n m|environment||çevre
avenir|n m|future||gelecek
futur|n m|future||gelecek
passé|n m|past||geçmiş
présent|n m|present||şimdiki zaman; bugün
événement|n m|event||olay
situation|n f|situation||durum
relation|n f|relationship||ilişki
responsabilité|n f|responsibility||sorumluluk
sécurité|n f|safety; security||güvenlik; emniyet
"""
