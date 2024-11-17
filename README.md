# Creació de grups basada en coneixement, regles, i centrada en interpretabilitat
## Introducció
En aquest projecte hem intentat desviar-nos de la solució habitual de clústering, mètodes no supervisats, o altres caixes negres (o intents d'interpretabilitat com XGboost) que s'acostumen a utilitzar en la resolució de problemes com aquest. Si bé alguns d'aquests models et permeten saber *com* afecta cada factor, no et saben dir *per què* ho fa.

Com a estudiants d'IA que sóm, sabem perfectament que la IA i el ML en general són una eina molt potent, però també que en pot ser una de molt difícil de desxifrar, i sovint sobre-utilitzada, especialment en els últims anys. 
Per això hem decidit implementar una solució que combina la millor part dels sistemes tradicionals de recomanació basats en coneixement, amb la flexibilitat i adaptabilitat dels sistemes de recomanació basats en ML.

A través del coneixement que tenim sobre el domini amb el treballem, podem fer abstraccions per a obtenir noves propietats de les que ja tenim, i derivar regles que són absolutament clares per a un humà, i interpretables (ja que la decisió es pot veure com una suma ponderada dels factors obtinguts a partir de les regles).
Després, podem fer servir el que hem obtingut d'aquestes regles i explicar-ho a través d'un model de ML, que ens fa de pont entre aquest coneixement i el llenguatge natural, alhora que ens permet obtenir informació de manera molt més flexible i convenient que amb els sistemes tradicionals. 

## Implementació
Hem dedicat un gran esforç a fer abstraccions de les característiques per a poder obtenir informació que va més enllà del que ja tenim, i dels mètodes habituals de combinació senzilla de variables. 
A partir d'aquestes, hem determinat vàries característiques per a les quals hem definit regles per poder derivar-ne els valors. Que ens permeten saber per a dos persones o dos conjunts d'aquestes, com d'aqueqüades són per a formar un grup, per quins motius, i (molt important també) per quins motius no. 
Per a obtenir les variables inicials, i per a explicar els resultats, hem fet ús d'una LLM que ens permet tractar amb llenguatge natural. 

## Organització dels fitxers
Hem dividit el projecte en dues parts principalment: una part més enfocada a fer una demostració de com funcionaria el sistema en un cas real, per a la qual hem fet servir Flask per al backend, i a través de la qual poden interactuar vàries persones alhora com ho farien en el sistema acabat. D'altra banda, tenim una part més enfocada a la implementació del sistema en si, on fem servir el dataset que se'ns ha donat per a veure com funcionaria el sistema de recomanació a un nivell més massiu. 

Així doncs, el fitxer de Server juntament amb el main_app.py contenen tot allò relacionat amb la demostració, mentre que la resta de carpetes i fitxers -utils, api_handler.py, participant, participant abstract...- van més enfocades a la implementació del sistema en si. Altres fitxers com el de heatmap.py són per a obtenir representacions visuals dels resultats obtinguts.

