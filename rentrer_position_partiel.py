
import pyautogui
#fonction permettant de prendre des positions et partielles très rapidement en execution direct
def execution_direct(lot,SL,nb_partiel,vente_ou_achat,TP):
    pyautogui.click(1261, 22)
    taille_position = round(lot / nb_partiel, 2)

    for i in range(nb_partiel):
        pyautogui.hotkey('fn','f9')
        pyautogui.press('tab')

        pyautogui.write(str(taille_position))
        pyautogui.press('tab')
        if SL:
            pyautogui.write(str(SL))
        pyautogui.press('tab')
        if TP:
            pyautogui.write(str(TP))
        pyautogui.press('tab',presses=3)
        if vente_ou_achat=='vente':
            pyautogui.press('space')
        elif vente_ou_achat=='achat':
            pyautogui.press('tab')
            pyautogui.press('space')
        pyautogui.press('alt')
        pyautogui.press('up',presses=2)
        pyautogui.press('enter')


#fonction permettant de prendre des positions très rapidement en position différé
def execution_différé(lot, entrée, nb_partiel, SL, TP, type_ordre) :
    pyautogui.click(1261,22)
    taille_position=round(lot/nb_partiel,2)

    for i in range(nb_partiel):
        pyautogui.hotkey('fn', 'f9')
        pyautogui.press('tab')
        pyautogui.write(str(taille_position))
        pyautogui.press('tab')
        if SL!=0:
            pyautogui.write(str(SL))
        pyautogui.press('tab')
        if TP!=0:
            pyautogui.write(str(TP))
        pyautogui.press('tab',presses=2)
        pyautogui.press('down')
        pyautogui.press('tab')
        if type_ordre=='Buy Limit':
            pass
        elif type_ordre=="Sell Limit":
            pyautogui.press('down')
        elif type_ordre=="Buy Stop":
            pyautogui.press('down' ,presses=2)

        elif type_ordre=='Sell Stop':
            pyautogui.press("down",presses=3)
        pyautogui.press("tab")
        pyautogui.write(str(entrée))
        pyautogui.press("tab",presses=2)
        pyautogui.press('space')
        pyautogui.press('alt')
        pyautogui.press('up',presses=2)
        pyautogui.press('enter')






