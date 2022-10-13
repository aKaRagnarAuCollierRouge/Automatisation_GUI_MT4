

# création des variables qu'on va utiliser pour les passer à la fonctions changer style pour qu'on puisse changer le style
# des widgets  facilement et pour désemcombrer la fenêtre principale


#style principale des QPushButton
style_main_QPushButton="""QPushButton{background-color: black;
    color:white;
    border-style: outset;
    border-width: 2px;
    border-radius: 10px;
    border-color: beige;
    font: bold 14px;
    min-width: 10em;
    padding: 6px}
"""

# style main QLabel
style_main_QLabel="""QLabel{color:black;font-family: "Fira Sans", Arial, sans-serif;font-size: 15px;}"""
style_main_QMessageBox="""QLabel{color:red;font-family: "Fira Sans", Arial, sans-serif;font-size: 15px;}
                            QPushButton{background-color:green;border-color:red;border-style:outset;border-width: 2px;border-radius: 10px}
                            QString{color:yellow}"""
#changer la couleur des labels, ou d'autres widgets

style_black_label="""color:black"""
style_white_label="""color:white"""


# STYLE THEME DE BASE:


#---------------------------->>>>THEME NATURE<<<<<--------------------
theme_nature_background="""background-color: #307e65 """
theme_nature_widgets="""QPushButton{background-color: white;
                                color:black;
                                border-style: outset;
                                border-width: 2px;
                                border-radius: 10px;
                                border-color: beige;
                                font: bold 14px;
                                min-width: 10em;
                                padding: 6px}
                            QLabel{color:black}
                            QRadioButton{color:white}"""

#Label en fonction style de widget Label" theme nature"
style_label_obligatoire_nature="""color:red"""
style_label_facultatif_nature="""color:blue"""
style_label_vérification_nature="""color:black"""
style_label_neutre_nature="""color:black"""
style_label_OK_nature="""color:blue"""

# --------------->>>>>THEME SOMBRE<<<<<<----------------
theme_sombre_background="""background-color:black"""
theme_sombre_widgets="""QPushButton{background-color: black;
                        color:white;
                        border-style: outset;
                        border-width: 2px;
                        border-radius: 10px;
                        border-color: beige;
                        font: bold 14px;
                        min-width: 10em;
                        padding: 6px}
                    QLabel{color:white}
                    QRadioButton{color:white}
                    QSpinBox{color:white}
                    QDoubleSpinBox{color:white}
                    QComboBox{color:white;border-color:white}
                    """
#Label en fonction style de widget Label" theme dark"
style_label_obligatoire_sombre="""color:red"""
style_label_facultatif_sombre="""color:green"""
style_label_vérification_sombre="""color:purple"""
style_label_neutre_sombre="""color:white"""
style_label_OK_sombre="""color:green"""


#------------>>THEME CLAIRE<<<-----

theme_clair_widgets="""QPushButton{background-color: white;
                        color:black;
                        border-style: outset;
                        border-width: 2px;
                        border-radius: 10px;
                        border-color: beige;
                        font: bold 14px;
                        min-width: 10em;
                        padding: 6px}
                    QLabel{color:black}
                    QRadioButton{color:black}
                    QRadioButton{color:black}
                    QSpinBox{color:black}
                    QDoubleSpinBox{color:black}
                    QComboBox{color:black}

                     """

theme_clair_background="""background-color:white"""



#Label en fonction style de widget Label" theme claire"
style_label_obligatoire_clair="""color:red"""
style_label_facultatif_clair="""color:green"""
style_label_vérification_clair="""color:purple"""
style_label_neutre_clair="""color:black"""
style_label_OK_clair="""color:green"""