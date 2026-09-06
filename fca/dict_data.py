"""Built-in French <-> English core dictionary (A1-B1, ~900 entries).

Line format:  headword|pos [gender] [plural]|english; english 2[|note]
Nouns carry their gender (m / f / mf / pl) and an irregular plural when needed
(``n m yeux``). Irregular verb notes go into the optional fourth field.
"""

DATA = r"""
# ---- greetings / politeness ----
bonjour|int|hello; good morning
bonsoir|int|good evening
bonne nuit|phr|good night
salut|int|hi; bye (informal)
au revoir|phr|goodbye
à bientôt|phr|see you soon
à plus tard|phr|see you later
à demain|phr|see you tomorrow
merci|int|thank you
merci beaucoup|phr|thank you very much
s'il vous plaît|phr|please (formal)
s'il te plaît|phr|please (informal)
de rien|phr|you are welcome
je vous en prie|phr|you are welcome (formal)
pardon|int|sorry; excuse me
excusez-moi|phr|excuse me
désolé|adj|sorry
oui|part|yes
non|part|no
si|part|yes (contradicting a negative); if
d'accord|phr|okay; agreed
bien sûr|phr|of course
peut-être|adv|maybe; perhaps
bienvenue|int|welcome
félicitations|int|congratulations
bonne chance|phr|good luck
bon appétit|phr|enjoy your meal
santé|int|cheers
à vos souhaits|phr|bless you
joyeux anniversaire|phr|happy birthday
comment allez-vous|phr|how are you (formal)
comment ça va|phr|how are you (informal)
ça va|phr|I am fine; how are you
comment vous appelez-vous|phr|what is your name (formal)
je m'appelle|phr|my name is
je viens de|phr|I come from
je ne comprends pas|phr|I do not understand
je ne sais pas|phr|I do not know
parlez-vous anglais|phr|do you speak English
pouvez-vous répéter|phr|can you repeat
combien ça coûte|phr|how much does it cost
où est|phr|where is
je voudrais|phr|I would like
il y a|phr|there is; there are
qu'est-ce que c'est|phr|what is it
# ---- question words ----
qui|pron|who
que|pron|what; that
quoi|pron|what
où|adv|where
quand|adv|when
pourquoi|adv|why
comment|adv|how
quel|pron|which; what
combien|adv|how much; how many
lequel|pron|which one
# ---- pronouns / articles ----
je|pron|I
tu|pron|you (singular, informal)
il|pron|he; it
elle|pron|she; it
on|pron|one; we (informal); people
nous|pron|we; us
vous|pron|you (plural or formal)
ils|pron|they (masculine)
elles|pron|they (feminine)
me|pron|me; myself
te|pron|you; yourself
se|pron|oneself; himself; herself
le|art|the (masculine); him; it
la|art|the (feminine); her; it
les|art|the (plural); them
un|art|a; an (masculine); one
une|art|a; an (feminine)
des|art|some (plural)
du|art|some (masculine); of the
de la|art|some (feminine)
mon|pron|my (masculine)
ma|pron|my (feminine)
mes|pron|my (plural)
ton|pron|your (masculine, informal)
ta|pron|your (feminine, informal)
son|pron|his; her; its (masculine)
sa|pron|his; her; its (feminine)
notre|pron|our
votre|pron|your (formal or plural)
leur|pron|their; to them
ce|pron|this; that; it
cette|pron|this; that (feminine)
ces|pron|these; those
celui|pron|the one; this one
tout|pron|all; everything
tous|pron|all; everyone
chaque|pron|each; every
quelque chose|phr|something
quelqu'un|pron|someone
rien|pron|nothing
personne|pron|nobody; person
lui|pron|him; to him; to her
eux|pron|them (masculine)
moi|pron|me (stressed)
toi|pron|you (stressed)
y|pron|there; to it
en|pron|of it; some; in
# ---- numbers ----
zéro|num|zero
un|num|one
deux|num|two
trois|num|three
quatre|num|four
cinq|num|five
six|num|six
sept|num|seven
huit|num|eight
neuf|num|nine
dix|num|ten
onze|num|eleven
douze|num|twelve
treize|num|thirteen
quatorze|num|fourteen
quinze|num|fifteen
seize|num|sixteen
dix-sept|num|seventeen
dix-huit|num|eighteen
dix-neuf|num|nineteen
vingt|num|twenty
vingt et un|num|twenty-one
trente|num|thirty
quarante|num|forty
cinquante|num|fifty
soixante|num|sixty
soixante-dix|num|seventy
quatre-vingts|num|eighty
quatre-vingt-dix|num|ninety
cent|num|hundred
mille|num|thousand
million|n m|million
premier|num|first
deuxième|num|second
troisième|num|third
dernier|adj|last
moitié|n f|half
demi|adj|half
fois|n f|time (occasion)
beaucoup|adv|much; many; a lot
peu|adv|little; few
plusieurs|pron|several
quelques|pron|some; a few
un peu|phr|a little
# ---- time ----
temps|n m|time; weather
heure|n f|hour; o'clock
minute|n f|minute
seconde|n f|second
jour|n m|day
journée|n f|day (duration)
nuit|n f|night
matin|n m|morning
après-midi|n m|afternoon
soir|n m|evening
soirée|n f|evening (duration); party
semaine|n f|week
week-end|n m|weekend
mois|n m|month
an|n m|year
année|n f|year (duration)
siècle|n m|century
aujourd'hui|adv|today
demain|adv|tomorrow
hier|adv|yesterday
après-demain|adv|the day after tomorrow
avant-hier|adv|the day before yesterday
maintenant|adv|now
tout de suite|phr|right away
bientôt|adv|soon
plus tard|phr|later
avant|prep|before
après|prep|after
tôt|adv|early
tard|adv|late
toujours|adv|always; still
jamais|adv|never
parfois|adv|sometimes
souvent|adv|often
rarement|adv|rarely
d'habitude|phr|usually
déjà|adv|already
encore|adv|still; again; more
pas encore|phr|not yet
d'abord|adv|first; at first
puis|adv|then
ensuite|adv|then; next
enfin|adv|finally
soudain|adv|suddenly
longtemps|adv|for a long time
lundi|n m|Monday
mardi|n m|Tuesday
mercredi|n m|Wednesday
jeudi|n m|Thursday
vendredi|n m|Friday
samedi|n m|Saturday
dimanche|n m|Sunday
janvier|n m|January
février|n m|February
mars|n m|March
avril|n m|April
mai|n m|May
juin|n m|June
juillet|n m|July
août|n m|August
septembre|n m|September
octobre|n m|October
novembre|n m|November
décembre|n m|December
printemps|n m|spring
été|n m|summer
automne|n m|autumn
hiver|n m|winter
fête|n f|party; holiday; festival
vacances|n f pl|holidays; vacation
anniversaire|n m|birthday; anniversary
rendez-vous|n m|appointment; date
calendrier|n m|calendar
date|n f|date
# ---- family / people ----
homme|n m|man
femme|n f|woman; wife
enfant|n mf|child
garçon|n m|boy; waiter
fille|n f|girl; daughter
bébé|n m|baby
famille|n f|family
parents|n m pl|parents
mère|n f|mother
père|n m|father
maman|n f|mom
papa|n m|dad
fils|n m|son
frère|n m|brother
sœur|n f|sister
grand-mère|n f|grandmother
grand-père|n m|grandfather
grands-parents|n m pl|grandparents
petit-fils|n m|grandson
petite-fille|n f|granddaughter
oncle|n m|uncle
tante|n f|aunt
cousin|n m|cousin (male)
cousine|n f|cousin (female)
mari|n m|husband
époux|n m|husband; spouse
ami|n m|friend (male)
amie|n f|friend (female)
copain|n m|friend; boyfriend
copine|n f|friend; girlfriend
voisin|n m|neighbour
invité|n m|guest
collègue|n mf|colleague
patron|n m|boss
monsieur|n m|Mr; sir; gentleman
madame|n f|Mrs; madam
mademoiselle|n f|Miss
nom|n m|name; surname
prénom|n m|first name
âge|n m|age
adulte|n mf|adult
adolescent|n m|teenager
personne|n f|person
gens|n m pl|people
peuple|n m|people; nation
# ---- jobs ----
travail|n m|work; job
métier|n m|profession; trade
médecin|n m|doctor
professeur|n m|teacher; professor
élève|n mf|pupil
étudiant|n m|student
ingénieur|n m|engineer
informaticien|n m|computer scientist; IT specialist
vendeur|n m|shop assistant; seller
cuisinier|n m|cook; chef
serveur|n m|waiter
chauffeur|n m|driver
policier|n m|police officer
journaliste|n mf|journalist
artiste|n mf|artist
musicien|n m|musician
acteur|n m|actor
écrivain|n m|writer
avocat|n m|lawyer
boulanger|n m|baker
coiffeur|n m|hairdresser
infirmier|n m|nurse (male)
infirmière|n f|nurse (female)
ouvrier|n m|worker
mécanicien|n m|mechanic
secrétaire|n mf|secretary
fonctionnaire|n mf|civil servant
entrepreneur|n m|entrepreneur
scientifique|n mf|scientist
traducteur|n m|translator
entreprise|n f|company; enterprise
société|n f|company; society
bureau|n m|office; desk
usine|n f|factory
salaire|n m|salary
client|n m|customer
réunion|n f|meeting
contrat|n m|contract
candidature|n f|application (job)
CV|n m|CV; résumé
poste|n m|position; job
chômage|n m|unemployment
carrière|n f|career
# ---- home ----
maison|n f|house
appartement|n m|flat; apartment
pièce|n f|room; piece; coin
chambre|n f|bedroom; room
cuisine|n f|kitchen; cooking
salon|n m|living room
salle de bains|n f|bathroom
toilettes|n f pl|toilet
couloir|n m|corridor
balcon|n m|balcony
jardin|n m|garden
cave|n f|cellar
toit|n m|roof
étage|n m|floor; storey
escalier|n m|stairs
ascenseur|n m|lift; elevator
porte|n f|door
fenêtre|n f|window
mur|n m|wall
sol|n m|floor; ground
plafond|n m|ceiling
meuble|n m|piece of furniture
table|n f|table
chaise|n f|chair
fauteuil|n m|armchair
canapé|n m|sofa
lit|n m|bed
armoire|n f|wardrobe
étagère|n f|shelf
miroir|n m|mirror
lampe|n f|lamp
lumière|n f|light
tapis|n m|carpet; rug
tableau|n m tableaux|painting; board; blackboard; table (chart)
frigo|n m|fridge
réfrigérateur|n m|refrigerator
cuisinière|n f|cooker; stove
four|n m|oven
machine à laver|n f|washing machine
télévision|n f|television
clé|n f|key
poubelle|n f|bin; trash can
loyer|n m|rent
quartier|n m|neighbourhood; district
ranger|v|to tidy up; to put away
nettoyer|v|to clean
laver|v|to wash
cuisiner|v|to cook
habiter|v|to live (in a place)
déménager|v|to move (house)
louer|v|to rent
# ---- everyday objects ----
chose|n f|thing
objet|n m|object
sac|n m|bag
sac à dos|n m|backpack
valise|n f|suitcase
portefeuille|n m|wallet
argent|n m|money; silver
portable|n m|mobile phone; laptop
téléphone|n m|telephone
ordinateur|n m|computer
lunettes|n f pl|glasses
parapluie|n m|umbrella
livre|n m|book
cahier|n m|notebook; exercise book
stylo|n m|pen
crayon|n m|pencil
papier|n m|paper
lettre|n f|letter (mail); letter (alphabet)
journal|n m journaux|newspaper; diary
magazine|n m|magazine
photo|n f|photo
cadeau|n m cadeaux|present; gift
jouet|n m|toy
ballon|n m|ball; balloon
montre|n f|watch
carte|n f|card; map; menu
boîte|n f|box; can; nightclub
bouteille|n f|bottle
# ---- clothing ----
vêtement|n m|piece of clothing
robe|n f|dress
chemise|n f|shirt
t-shirt|n m|T-shirt
pantalon|n m|trousers; pants
jean|n m|jeans
jupe|n f|skirt
manteau|n m manteaux|coat
veste|n f|jacket
costume|n m|suit; costume
pull|n m|sweater
bonnet|n m|beanie; cap
chapeau|n m chapeaux|hat
écharpe|n f|scarf
gant|n m|glove
chaussette|n f|sock
chaussure|n f|shoe
botte|n f|boot
basket|n f|sneaker
taille|n f|size; waist; height
mettre|v|to put; to put on|mis
enlever|v|to take off; to remove
porter|v|to wear; to carry
essayer|v|to try; to try on
# ---- body / health ----
corps|n m|body
tête|n f|head
visage|n m|face
œil|n m yeux|eye
oreille|n f|ear
nez|n m|nose
bouche|n f|mouth
dent|n f|tooth
cheveux|n m pl|hair
cou|n m|neck
gorge|n f|throat
épaule|n f|shoulder
bras|n m|arm
main|n f|hand
doigt|n m|finger
jambe|n f|leg
pied|n m|foot
genou|n m genoux|knee
dos|n m|back
ventre|n m|belly; stomach
cœur|n m|heart
sang|n m|blood
peau|n f|skin
santé|n f|health
en bonne santé|phr|healthy
malade|adj|ill; sick
maladie|n f|illness; disease
douleur|n f|pain
mal de tête|n m|headache
fièvre|n f|fever
rhume|n m|cold (illness)
toux|n f|cough
médicament|n m|medicine; drug
comprimé|n m|tablet; pill
pharmacie|n f|pharmacy
hôpital|n m hôpitaux|hospital
cabinet|n m|doctor's office
urgences|n f pl|emergency room
accident|n m|accident
fatigué|adj|tired
dormir|v|to sleep|dormi
s'endormir|v|to fall asleep
se réveiller|v|to wake up
se lever|v|to get up
se reposer|v|to rest
avoir mal|phr|to hurt; to be in pain
# ---- food / drink ----
nourriture|n f|food
repas|n m|meal
petit déjeuner|n m|breakfast
déjeuner|n m|lunch
dîner|n m|dinner
pain|n m|bread
beurre|n m|butter
fromage|n m|cheese
lait|n m|milk
œuf|n m|egg
viande|n f|meat
poulet|n m|chicken
poisson|n m|fish
saucisse|n f|sausage
jambon|n m|ham
soupe|n f|soup
riz|n m|rice
pâtes|n f pl|pasta
pomme de terre|n f|potato
frites|n f pl|chips; French fries
légume|n m|vegetable
fruit|n m|fruit
pomme|n f|apple
poire|n f|pear
banane|n f|banana
orange|n f|orange
citron|n m|lemon
raisin|n m|grape
fraise|n f|strawberry
tomate|n f|tomato
concombre|n m|cucumber
oignon|n m|onion
ail|n m|garlic
salade|n f|salad; lettuce
carotte|n f|carrot
champignon|n m|mushroom
sel|n m|salt
sucre|n m|sugar
poivre|n m|pepper
huile|n f|oil
miel|n m|honey
gâteau|n m gâteaux|cake
biscuit|n m|biscuit; cookie
chocolat|n m|chocolate
glace|n f|ice cream; ice; mirror
bonbon|n m|sweet; candy
eau|n f eaux|water
thé|n m|tea
café|n m|coffee; cafe
jus|n m|juice
bière|n f|beer
vin|n m|wine
verre|n m|glass
tasse|n f|cup
assiette|n f|plate
cuillère|n f|spoon
fourchette|n f|fork
couteau|n m couteaux|knife
casserole|n f|saucepan
poêle|n f|frying pan
restaurant|n m|restaurant
boulangerie|n f|bakery
menu|n m|menu; set meal
addition|n f|bill (restaurant); addition
pourboire|n m|tip (money)
délicieux|adj|delicious
sucré|adj|sweet
salé|adj|salty
épicé|adj|spicy
frais|adj|fresh; cool
faim|n f|hunger
soif|n f|thirst
avoir faim|phr|to be hungry
avoir soif|phr|to be thirsty
manger|v|to eat
boire|v|to drink|bu
prendre le petit déjeuner|phr|to have breakfast
commander|v|to order
payer|v|to pay
goûter|v|to taste
# ---- city / transport ----
ville|n f|city; town
village|n m|village
pays|n m|country
capitale|n f|capital city
rue|n f|street
place|n f|square; place; seat
route|n f|road
chemin|n m|path; way
pont|n m|bridge
parc|n m|park
centre|n m|centre
centre-ville|n m|city centre
bâtiment|n m|building
immeuble|n m|apartment building
église|n f|church
musée|n m|museum
théâtre|n m|theatre
cinéma|n m|cinema
bibliothèque|n f|library
école|n f|school
lycée|n m|secondary school; high school
université|n f|university
banque|n f|bank
poste|n f|post office
hôtel|n m|hotel
gare|n f|railway station
arrêt|n m|stop (bus)
aéroport|n m|airport
métro|n m|metro; underground
bus|n m|bus
tramway|n m|tram
voiture|n f|car
taxi|n m|taxi
train|n m|train
avion|n m|plane
bateau|n m bateaux|boat; ship
vélo|n m|bicycle
billet|n m|ticket; banknote
ticket|n m|ticket (metro, bus)
passeport|n m|passport
carte d'identité|n f|ID card
frontière|n f|border
voyage|n m|journey; trip
excursion|n f|excursion
touriste|n mf|tourist
plan|n m|map (city); plan
adresse|n f|address
feu|n m feux|traffic light; fire
carrefour|n m|crossroads
coin|n m|corner
parking|n m|car park
station-service|n f|petrol station
embouteillage|n m|traffic jam
horaire|n m|timetable; schedule
départ|n m|departure
arrivée|n f|arrival
quai|n m|platform; quay
entrée|n f|entrance; starter
sortie|n f|exit
à droite|phr|on the right; to the right
à gauche|phr|on the left; to the left
tout droit|phr|straight ahead
loin|adv|far
près|adv|near
ici|adv|here
là|adv|there
là-bas|adv|over there
chez|prep|at the home of
à la maison|phr|at home
en haut|phr|upstairs; above
en bas|phr|downstairs; below
dedans|adv|inside
dehors|adv|outside
partout|adv|everywhere
nulle part|phr|nowhere
# ---- movement verbs ----
aller|v|to go|allé (être)
venir|v|to come|venu (être)
partir|v|to leave|parti (être)
arriver|v|to arrive; to happen|arrivé (être)
entrer|v|to enter|entré (être)
sortir|v|to go out|sorti (être)
monter|v|to go up; to get on|monté (être)
descendre|v|to go down; to get off|descendu (être)
rentrer|v|to return home|rentré (être)
revenir|v|to come back|revenu (être)
retourner|v|to return; to go back|retourné (être)
passer|v|to pass; to spend (time)
traverser|v|to cross
marcher|v|to walk; to work (function)
courir|v|to run|couru
voler|v|to fly; to steal
nager|v|to swim
conduire|v|to drive|conduit
voyager|v|to travel
apporter|v|to bring (a thing)
amener|v|to bring (a person)
emmener|v|to take (a person) along
chercher|v|to look for; to fetch
suivre|v|to follow|suivi
sauter|v|to jump
tomber|v|to fall|tombé (être)
# ---- core verbs ----
être|v|to be|été
avoir|v|to have|eu
faire|v|to do; to make|fait
dire|v|to say; to tell|dit
parler|v|to speak; to talk
raconter|v|to tell (a story)
demander|v|to ask
répondre|v|to answer|répondu
savoir|v|to know (facts)|su
connaître|v|to know (be familiar with)|connu
penser|v|to think
croire|v|to believe|cru
comprendre|v|to understand|compris
vouloir|v|to want|voulu
pouvoir|v|can; to be able|pu
devoir|v|must; to have to|dû
falloir|v|to be necessary|fallu (il faut)
aimer|v|to love; to like
adorer|v|to love; to adore
détester|v|to hate
préférer|v|to prefer
voir|v|to see|vu
regarder|v|to look at; to watch
entendre|v|to hear|entendu
écouter|v|to listen
lire|v|to read|lu
écrire|v|to write|écrit
apprendre|v|to learn|appris
étudier|v|to study
enseigner|v|to teach
travailler|v|to work
vivre|v|to live|vécu
jouer|v|to play
donner|v|to give
prendre|v|to take|pris
recevoir|v|to receive|reçu
acheter|v|to buy
vendre|v|to sell|vendu
faire les courses|phr|to do the shopping
coûter|v|to cost
ouvrir|v|to open|ouvert
fermer|v|to close
commencer|v|to begin
finir|v|to finish|fini
arrêter|v|to stop
continuer|v|to continue
attendre|v|to wait|attendu
trouver|v|to find
perdre|v|to lose|perdu
se souvenir|v|to remember|souvenu (être)
se rappeler|v|to remember
oublier|v|to forget
aider|v|to help
appeler|v|to call
téléphoner|v|to phone
rencontrer|v|to meet
se retrouver|v|to meet up
montrer|v|to show
expliquer|v|to explain
traduire|v|to translate|traduit
répéter|v|to repeat
envoyer|v|to send
poser|v|to put down; to ask (a question)
s'asseoir|v|to sit down|assis (être)
être assis|phr|to be sitting
se tenir debout|phr|to stand
rester|v|to stay|resté (être)
tenir|v|to hold|tenu
sentir|v|to feel; to smell|senti
se sentir|v|to feel (state)
avoir peur|phr|to be afraid
espérer|v|to hope
décider|v|to decide
résoudre|v|to solve|résolu
rêver|v|to dream
rire|v|to laugh|ri
sourire|v|to smile|souri
pleurer|v|to cry
crier|v|to shout
chanter|v|to sing
danser|v|to dance
dessiner|v|to draw
peindre|v|to paint|peint
se promener|v|to go for a walk
s'intéresser|v|to be interested (in)
s'appeler|v|to be called
se marier|v|to get married
naître|v|to be born|né (être)
mourir|v|to die|mort (être)
grandir|v|to grow up
changer|v|to change
construire|v|to build|construit
casser|v|to break
réparer|v|to repair
jeter|v|to throw; to throw away
lever|v|to lift; to raise
bouger|v|to move
être en retard|phr|to be late
se dépêcher|v|to hurry
réussir|v|to succeed
inviter|v|to invite
proposer|v|to suggest; to offer
conseiller|v|to advise
recommander|v|to recommend
promettre|v|to promise|promis
permettre|v|to allow|permis
interdire|v|to forbid|interdit
vérifier|v|to check
choisir|v|to choose
comparer|v|to compare
compter|v|to count
calculer|v|to calculate
utiliser|v|to use
se servir de|phr|to use
avoir besoin de|phr|to need
planifier|v|to plan
organiser|v|to organise
participer|v|to take part
gagner|v|to win; to earn
se passer|v|to happen
arriver à|phr|to manage to
sembler|v|to seem
signifier|v|to mean
vouloir dire|phr|to mean
exister|v|to exist
suffire|v|to be enough|suffi
appartenir|v|to belong|appartenu
laisser|v|to let; to leave
quitter|v|to leave (a place or person)
visiter|v|to visit (a place)
rendre visite à|phr|to visit (a person)
saluer|v|to greet
dire au revoir|phr|to say goodbye
remercier|v|to thank
s'excuser|v|to apologise
se réjouir|v|to be glad
s'énerver|v|to get annoyed
s'inquiéter|v|to worry
se plaindre|v|to complain|plaint
se disputer|v|to argue
discuter|v|to discuss
être d'accord|phr|to agree
refuser|v|to refuse
faire attention|phr|to pay attention
remarquer|v|to notice
décrire|v|to describe|décrit
se présenter|v|to introduce oneself
imaginer|v|to imagine
dépendre|v|to depend|dépendu
influencer|v|to influence
développer|v|to develop
protéger|v|to protect
détruire|v|to destroy|détruit
économiser|v|to save (money)
dépenser|v|to spend (money)
mériter|v|to deserve
démissionner|v|to resign
diriger|v|to lead; to manage
fumer|v|to smoke
maigrir|v|to lose weight
grossir|v|to gain weight
soigner|v|to treat; to look after
guérir|v|to cure; to recover
# ---- adjectives ----
grand|adj|big; tall
petit|adj|small; little
bon|adj|good
mauvais|adj|bad
nouveau|adj|new|nouvelle (f), nouveaux (pl)
vieux|adj|old|vieille (f)
jeune|adj|young
beau|adj|beautiful; handsome|belle (f), beaux (pl)
joli|adj|pretty
laid|adj|ugly
intelligent|adj|intelligent; clever
bête|adj|stupid
gentil|adj|kind; nice
sympathique|adj|nice; friendly
méchant|adj|mean; nasty
drôle|adj|funny
triste|adj|sad
heureux|adj|happy
content|adj|pleased; glad
intéressant|adj|interesting
ennuyeux|adj|boring
important|adj|important
difficile|adj|difficult
facile|adj|easy
simple|adj|simple
compliqué|adj|complicated
cher|adj|expensive; dear
bon marché|adj|cheap
riche|adj|rich
pauvre|adj|poor
fort|adj|strong
faible|adj|weak
haut|adj|high; tall
bas|adj|low
long|adj|long|longue (f)
court|adj|short
large|adj|wide
étroit|adj|narrow
gros|adj|big; fat
mince|adj|thin; slim
épais|adj|thick
lourd|adj|heavy
léger|adj|light (weight)
chaud|adj|hot; warm
froid|adj|cold
tiède|adj|lukewarm
rapide|adj|fast
lent|adj|slow
bruyant|adj|noisy
calme|adj|calm; quiet
propre|adj|clean; own
sale|adj|dirty
clair|adj|light; clear
sombre|adj|dark
plein|adj|full
vide|adj|empty
ouvert|adj|open
fermé|adj|closed
libre|adj|free
occupé|adj|busy; occupied
prêt|adj|ready
juste|adj|correct; fair
faux|adj|wrong; false|fausse (f)
vrai|adj|true; real
possible|adj|possible
impossible|adj|impossible
nécessaire|adj|necessary
même|adj|same; even
différent|adj|different
autre|adj|other
prochain|adj|next
précédent|adj|previous
seul|adj|alone; only
ensemble|adv|together
entier|adj|whole; entire
confortable|adj|comfortable
dangereux|adj|dangerous
sûr|adj|sure; safe
honnête|adj|honest
poli|adj|polite
sérieux|adj|serious
mouillé|adj|wet
sec|adj|dry|sèche (f)
doux|adj|soft; gentle; sweet|douce (f)
dur|adj|hard
rond|adj|round
vivant|adj|alive; lively
mort|adj|dead
célèbre|adj|famous
populaire|adj|popular
moderne|adj|modern
connu|adj|known; well-known
étranger|adj|foreign
français|adj|French
anglais|adj|English
turc|adj|Turkish|turque (f)
allemand|adj|German
russe|adj|Russian
travailleur|adj|hard-working
paresseux|adj|lazy
nerveux|adj|nervous
fou|adj|crazy|folle (f)
fatigant|adj|tiring
gratuit|adj|free of charge
# ---- colours ----
couleur|n f|colour
blanc|adj|white|blanche (f)
noir|adj|black
rouge|adj|red
bleu|adj|blue
vert|adj|green
jaune|adj|yellow
orange|adj|orange
marron|adj|brown
gris|adj|grey
rose|adj|pink
violet|adj|purple
# ---- adverbs / prepositions / conjunctions ----
très|adv|very
trop|adv|too; too much
presque|adv|almost
seulement|adv|only
aussi|adv|also; too
même|adv|even
environ|adv|approximately
exactement|adv|exactly
vraiment|adv|really
naturellement|adv|naturally
probablement|adv|probably
certainement|adv|certainly
malheureusement|adv|unfortunately
heureusement|adv|fortunately
surtout|adv|especially; above all
assez|adv|enough; rather
plutôt|adv|rather
pas du tout|phr|not at all
en fait|phr|actually; in fact
au fait|phr|by the way
donc|conj|so; therefore
alors|adv|then; so
pourtant|adv|however; yet
quand même|phr|anyway; all the same
sinon|conj|otherwise
d'ailleurs|adv|besides; moreover
cependant|adv|however
c'est-à-dire|phr|that is to say
ne … pas|phr|not
ne … plus|phr|no longer
ne … jamais|phr|never
et|conj|and
ou|conj|or
mais|conj|but
car|conj|because; for
parce que|conj|because
que|conj|that
si|conj|if
bien que|conj|although
pour que|conj|so that
avant que|conj|before
après que|conj|after
pendant que|conj|while
depuis|prep|since; for
jusqu'à|prep|until; up to
dans|prep|in; into
à|prep|to; at; in
sur|prep|on
sous|prep|under
au-dessus de|prep|above
devant|prep|in front of
derrière|prep|behind
à côté de|prep|next to
entre|prep|between
avec|prep|with
sans|prep|without
pour|prep|for; in order to
contre|prep|against
vers|prep|towards; around (time)
par|prep|by; through
de|prep|of; from
sauf|prep|except
à cause de|prep|because of
grâce à|prep|thanks to
malgré|prep|despite
au lieu de|prep|instead of
le long de|prep|along
en face de|prep|opposite
pendant|prep|during
# ---- education / language ----
langue|n f|language; tongue
mot|n m|word
phrase|n f|sentence
alphabet|n m|alphabet
grammaire|n f|grammar
dictionnaire|n m|dictionary
vocabulaire|n m|vocabulary
cours|n m|course; lesson; class
leçon|n f|lesson
classe|n f|class
examen|n m|exam
note|n f|grade; mark; note
erreur|n f|mistake
faute|n f|mistake; fault
question|n f|question
réponse|n f|answer
règle|n f|rule; ruler
exemple|n m|example
exercice|n m|exercise
devoirs|n m pl|homework
texte|n m|text
histoire|n f|story; history
littérature|n f|literature
mathématiques|n f pl|mathematics
physique|n f|physics
chimie|n f|chemistry
biologie|n f|biology
géographie|n f|geography
science|n f|science
sens|n m|meaning; sense; direction
traduction|n f|translation
prononciation|n f|pronunciation
mémoire|n f|memory
attention|n f|attention
connaissance|n f|knowledge; acquaintance
expérience|n f|experience; experiment
récréation|n f|break (school)
diplôme|n m|diploma; degree
formation|n f|training; education
# ---- money / shopping ----
prix|n m|price; prize
euro|n m|euro
centime|n m|cent
caisse|n f|cash desk; checkout
monnaie|n f|change; currency
réduction|n f|discount
promotion|n f|special offer
magasin|n m|shop
boutique|n f|shop; boutique
supermarché|n m|supermarket
marché|n m|market
centre commercial|n m|shopping centre
grand magasin|n m|department store
marchandise|n f|goods
produit|n m|product
qualité|n f|quality
carte bancaire|n f|bank card
compte|n m|account
dette|n f|debt
impôt|n m|tax
assurance|n f|insurance
# ---- communication / technology ----
internet|n m|internet
site|n m|website; site
courriel|n m|e-mail
e-mail|n m|e-mail
message|n m|message
numéro|n m|number
appel|n m|call
connexion|n f|connection
information|n f|information
nouvelles|n f pl|news
programme|n m|programme
application|n f|application; app
écran|n m|screen
touche|n f|key (keyboard)
clavier|n m|keyboard
souris|n f|mouse (animal); mouse (computer)
fichier|n m|file
dossier|n m|folder; file
mot de passe|n m|password
imprimante|n f|printer
radio|n f|radio
musique|n f|music
chanson|n f|song
film|n m|film; movie
série|n f|series
jeu|n m jeux|game
appareil photo|n m|camera
batterie|n f|battery
pile|n f|battery (disposable)
recharger|v|to recharge
allumer|v|to switch on; to light
éteindre|v|to switch off|éteint
télécharger|v|to download
imprimer|v|to print
enregistrer|v|to save; to record
supprimer|v|to delete
# ---- nature / weather ----
nature|n f|nature
météo|n f|weather forecast
soleil|n m|sun
lune|n f|moon
étoile|n f|star
ciel|n m|sky
nuage|n m|cloud
pluie|n f|rain
neige|n f|snow
vent|n m|wind
orage|n m|thunderstorm
brouillard|n m|fog
gel|n m|frost
chaleur|n f|heat
degré|n m|degree
terre|n f|earth; land; soil
monde|n m|world
air|n m|air
mer|n f|sea
lac|n m|lake
fleuve|n m|river (to the sea)
rivière|n f|river
plage|n f|beach
île|n f|island
montagne|n f|mountain
forêt|n f|forest
champ|n m|field
arbre|n m|tree
fleur|n f|flower
herbe|n f|grass
feuille|n f|leaf; sheet
pierre|n f|stone
sable|n m|sand
animal|n m animaux|animal
chien|n m|dog
chat|n m|cat
cheval|n m chevaux|horse
vache|n f|cow
cochon|n m|pig
oiseau|n m oiseaux|bird
ours|n m|bear
loup|n m|wolf
renard|n m|fox
lapin|n m|rabbit
serpent|n m|snake
insecte|n m|insect
il pleut|phr|it is raining
il neige|phr|it is snowing
il fait froid|phr|it is cold
il fait chaud|phr|it is hot
il fait beau|phr|the weather is nice
ensoleillé|adj|sunny
nuageux|adj|cloudy
# ---- sport / leisure ----
sport|n m|sport
football|n m|football
tennis|n m|tennis
échecs|n m pl|chess
piscine|n f|swimming pool
stade|n m|stadium
équipe|n f|team
match|n m|match
entraînement|n m|training
victoire|n f|victory
passe-temps|n m|hobby
loisirs|n m pl|leisure
concert|n m|concert
exposition|n f|exhibition
spectacle|n m|show; performance
fêter|v|to celebrate
club|n m|club
# ---- feelings / abstract ----
vie|n f|life
amour|n m|love
amitié|n f|friendship
bonheur|n m|happiness
joie|n f|joy
peur|n f|fear
espoir|n m|hope
rêve|n m|dream
vérité|n f|truth
mensonge|n m|lie
pensée|n f|thought
idée|n f|idea
avis|n m|opinion
opinion|n f|opinion
sentiment|n m|feeling
humeur|n f|mood
souhait|n m|wish
envie|n f|desire; wish
intérêt|n m|interest
liberté|n f|freedom
droit|n m|right; law
loi|n f|law
ordre|n m|order
choix|n m|choice
possibilité|n f|possibility
raison|n f|reason
conséquence|n f|consequence
cas|n m|case
manière|n f|manner; way
façon|n f|way; manner
condition|n f|condition
différence|n f|difference
partie|n f|part; game
fin|n f|end
début|n m|beginning
milieu|n m|middle; environment
lieu|n m lieux|place
endroit|n m|place
côté|n m|side
forme|n f|form; shape
nombre|n m|number
quantité|n f|quantity
poids|n m|weight
état|n m|state; condition
gouvernement|n m|government
guerre|n f|war
paix|n f|peace
police|n f|police
culture|n f|culture
art|n m|art
religion|n f|religion
problème|n m|problem
solution|n f|solution
succès|n m|success
but|n m|goal; aim
projet|n m|project
résultat|n m|result
environnement|n m|environment
avenir|n m|future
futur|n m|future
passé|n m|past
présent|n m|present
événement|n m|event
situation|n f|situation
relation|n f|relationship
responsabilité|n f|responsibility
sécurité|n f|safety; security
"""
