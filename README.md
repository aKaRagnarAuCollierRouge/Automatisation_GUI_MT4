# Automatisation_GUI_MT4 OU "GEAR SECONDO" pour la vitesse

Theme: trading

But du projet: - faciliter mes prises de positions en trading notamment pour calculer le lot et diviser mon lot pour prendre de multiple position rapidement et 
pouvoir mettre un TP et SL différents sur chaque position au besoin pour manager mon risque de façon optimale. 
=> automatisation du GUI dans la partie ("rentrer_position_partiel.py)
-mettre en place une stratégie de Draw down qui s'appliquera automatiquement en fonction de la somme d'argent sur le compte lorsque je calcul le lot.
-avoir des alertes des prochaines annonces pour que je n'ai pas à me prendre la tête à aller sur les sites tout les jours ainsi que des signaux sonores de 
leur approche pour ne pas se faire surprendre et me le rapeler qu'une annonce importante est en approche.



Les différents onglets :
Ce projet a pour but d'automatiser le calcul de lot en fonction de la commission, valeur pip qui dépend de la paire de trader, du risque et d'autres parametres






----------------------------------PLAN DE GUI_partiel_automatisation.py-----------------------
ALLUMAGE DE L'APPLICATION
169->creation des widget onglet 1 Entrée directe
221-> creation widgets onglet 2 Entrée différée
274-> creation widgets onglet 3 Calcul de lot
342-> creation wisget onglet 4 Manger Trade
378->creation des widget onglet 5 Calcul Dradown Strategie
470-> creation widgets onglet 2 Entrée différée:(487-> Suppression annonce dépassé ,triage,ajout des annonces dans self.table_annonce(QTableView),532-> chrono de l'annonce mise en marche intervalle 1seconde)
549-> modification label OK pour strategie DD pas important
617-> on modifie les label qui infore du % de DD et du pallier qu'on a atteint 
640-> on change les widgets et on en cache certains en fonction de si dans les parametres par default on utilise la plateforme metatrader 4 ou 5.

677-> Barre d'outils
#parametres permet de changer:-"d'ajouter une paire" de devise(ex:XXX/JPY
                              -"modifier la valeur du pip" des différentes paires
                              -"supprimer des paires"
                              -"modifier des parametres par default" qui vont etre appliquer au démarrage (commission , risque, montant du compte, paire, nombre de partiel,stop loss/entrée(ces2 parametres sont inutiles en realité), la version de metatrader utiliait de base
#DrawDown permet  de : - "modifier l'activation palliers" , leur risque manuellement
                      -"remettre strategie DD à zero" permet de remettre le DD à 0 et de remettre le risque de base(pallier0)
                      -Desativer/Activer strategie de DD, cache les labels de DD et ne change plus automatiquement le risque ou inversement
#changer visuel: permet de selectionner un style particulier de l'application
#Manager Trade change les parametres par default de manager trade mais un peu nul j'avoue
#Actualiser , lorsque l'on change des parametres par default pour les appliquer il est 
nécessaire d'appuyer sur actualiser pour que ces changements soient appliqués
#Rollback ancienne strategie DD: permet de rollback l'ancienne strategie de DD mise en place 
#arrêter musique: arrête la musique des annonces mais n'arrête pas le Timer
774-> reliage des différents widgets à des fonctions en fonction de signaux (connexion signaux)

->833 ajout des différents widgets dans les layouts

-> 1030 1)ajout des différents styles de bases au différents layouts 
2) personalisation en fonctiondes labels qui sont obligatoires/facultatifs/vérification/OK et application du style choisis par default par l'utilisateur (changer visuel dans l'appli)
A NOTER : pour changer les styles , les fonctions utilisait viennent de style_widgets/style_général.py

--Methodes--
1105->fonction changant titre window en fct chgt onglet
1109-> passe un ordre direct d'achat ,=> relié à l'onglet entrée direct(btn achat); va chercher la fct qui passe l'odre d'achat dans le fichier 
rentrer_position_partiel.py
1137-> passe un ordre direct de vente(btn vente
1156-> passe un ordre position différé (cest à dire que la plateforme attend un signal, un niveau de prix pour placer l'ordre sur le marché 
1257-> calcul le lot dans l'onglet calcul lot(btn calcul lot) et applique le lot calculer directement dans les onglets ventes et achat pour facliter
1333 à 1357-> change les valeurs de certains widget (spinbox) qui sont les mêmes pour certains onglets(SL,TP,Entree....)
1367-1392 contient les fonctions qui ouvre les fenetres du boutons parametres dans la barre d'outils
1394-> fonction qui permet d'activer ou non le son des annonces, lorsque que l'on clique sur le bouton activermusqiue/desactiver musique
1413-> fonction qui permet d'actualiser l'application lorsque l'on change des parametres par default(''> d'ailleur il serait bien que je le mette dans un autre Thread)
1512 -> permet de changer la valeur du pip automatiquement lorsque l'on change de paire dans l'onglet calcul de lot
1518-> permet d'operer tout les changements de l'application lorsque l'on change les boutons radios MT
1661->change les ordres qu'on peut passer dans l'onglet ordre différée car il faut savoir qu'on peut passer + d'ordre différé sur MT5 que sur MT4
1672-> permet  d'ouvrir la fenetre qui permet de changer les palliers de DD quand on appuie sur le bouton "DrawDown dans la barre d'outils
1678-> calcul le DD et appelle la fonction permettant de changer label qui indique le dd  en fonction du DD
1751-> fct changeant le label en fonction du DD
1792->Activate ou desactive strategie DD lorsque l'on appuie sur le bouton"Activer/Desactiver strategie drawdown" dans la barre d'outils
1813-> remet à 0% le DD
1829 -> fcts permettant de changer le style de l'appli lorsque l'on clique sur le bouton changer visuel de la barre d'outils
1879-> calcul activation , montant du compte dans l'onglet de calcul de strategie DD
1923->applique la strategie calculer au prealable lorsque l'on est dans l'onglet strategie DD(bouton "Appliquer strategie")
2033-> juste changement des labels OK pour dire que le champs est bien remplit
2104-> fonction qui sert à revenir à la derniere strategie de DD si on a fait une erreur dans la barre d'outils
2240->







A venir: mettre en place une fonction de web scrapping qui prends directement du site et me les insère dans mon tableau directement pour que je n'ai pas à le rentrer
manuellement parce que c'est chiant.



->



