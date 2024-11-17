# Creació de grups basada en coneixement, regles, i centrada en interpretabilitat
## Introducció
En aquest projecte hem intentat desviar-nos de la solució habitual de clústering, mètodes no supervisats, o altres caixes negres (o intents d'interpretabilitat) que s'acostumen a utilitzar en la resolució de problemes com aquest. 

Com a estudiants d'IA que sóm, sabem perfectament que la IA i el ML en general és una eina molt potent, però també que pot ser una caixa negra molt difícil de desxifrar, i sovint sobre-utilitzada, especialment en els últims anys. 
Per això hem decidit implementar una solució que combina la millor part dels sistemes tradicionals de recomanació basats en coneixement, amb la flexibilitat i adaptabilitat dels sistemes de recomanació basats en ML.

A través del coneixement que tenim sobre el domini amb el treballem, podem fer abstraccions i derivar regles que són absolutament clares per a un humà, i interpretables. 
Després, podem fer servir el que hem obtingut d'aquestes regles i explicar-ho a través d'un model de ML, que ens fa de pont entre aquest coneixement i el llenguatge natural, alhora que ens permet obtenir informació de manera molt més flexible i convenient que amb els sistemes tradicionals. 

## Organització dels fitxers
Hem dividit el projecte en dues parts principalment: una part més enfocada a fer una demostració de com funcionaria el sistema en un cas real, per a la qual hem fet servir Flask per al backend, i a través de la qual poden interactuar vàries persones alhora com ho farien en el sistema acabat. D'altra banda, tenim una part més enfocada a la implementació del sistema en si, on fem servir el dataset que se'ns ha donat per a veure com funcionaria el sistema de recomanació a un nivell més massiu. 

Així doncs, el fitxer de Server juntament amb el main_app.py contenen tot allò relacionat amb la demostració, mentre que la resta de carpetes i fitxers -utils, api_handler.py, participant, participant abstract...- van més enfocades a la implementació del sistema en si. Altres fitxers com el de heatmap.py són per a obtenir representacions visuals dels resultats obtinguts.

