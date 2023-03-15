#GESTION DES FILIERE & GROUPES & STAGIAIRES
from PyQt5.QtWidgets import QApplication,QMessageBox,QTableWidgetItem
from PyQt5.uic import loadUi
import icon_load , icons
import sqlite3


# main app
app = QApplication([])

#load Ptqt5 Designer
login_space= loadUi('identification.ui')
window = loadUi("stagiaire.ui")

# setGeometry(left, top, width, height)
window.setGeometry(150, 100, 929, 490)

window.setMaximumWidth(929)
window.setMaximumHeight(490)
window.setMinimumWidth(929)
window.setMinimumHeight(490)

#Geomerty login_space
login_space.setGeometry(150, 100, 929, 490)

login_space.setMaximumWidth(929)
login_space.setMaximumHeight(490)
login_space.setMinimumWidth(929)
login_space.setMinimumHeight(490)

#
window.table_liste.verticalHeader().hide()
#DATABASE 

inscription=sqlite3.connect('inscription.db')

#FILIERE
inscription.execute('''create table if not exists filiere(
                                    code_filiere INTEGER PRIMARY KEY AUTOINCREMENT,
                                    nom_filiere text not null
                                    );''')
#
inscription.execute('''create table if not exists groupe(
                                    code_groupe INTEGER PRIMARY KEY AUTOINCREMENT,
                                    nom_groupe text not null,
                                    nom_filiere text not null
                                    );''')
inscription.execute('''create table if not exists stagiaire(
                                    code_de_stagiaire INTEGER primary key AUTOINCREMENT,
                                    nom text not null,
                                    prenom text not null,
                                    filiere text not null ,
                                    groupe text not null ,
                                    telephone text not null,
                                    adresse text not null);''')



#FUNCTIONS
def message(titre , message):
    msg=QMessageBox()
    msg.setText(f"{message}")
    msg.setIcon(QMessageBox.Information)
    msg.setWindowTitle(f"{titre}")
    msg.exec_()
def check():
    username = login_space.username.text()
    password = login_space.password.text()
    if (username == '' and password == '' ): 
        window.show()
        login_space.close()
    else :
        message("Erreur de connexion ", "Error : Nom d'utilisateur ou mot de passe incorrect ")
def ajouter_filiere():
    nom_filiere = window.Nom_filiere.text()

    if (check_filiere(nom_filiere.upper())):
        message("Ajouter Filière ", "Error : Cette Filiere déja existe ")
    else:
        inscription.execute("INSERT INTO filiere(nom_filiere) Values ('"+nom_filiere.upper()+"')")
        inscription.commit()
        print(nom_filiere)
        window.drop_filiere.addItems([nom_filiere.upper()])
        window.inscription_filiere.addItems([nom_filiere.upper()])
        message("Ajouter Filière ", "Bien Ajouter !")
    window.Nom_filiere.clear()
def ajouter_groupe():
    nom_groupe = window.Nom_groupe.text()
    filiere = window.drop_filiere.currentText()
    if (nom_groupe =='' or filiere=='Choisir une filiere'):
        message("Ajouter Groupe", "Error : remplir les champs ")

    else:
        if (check_groupe(nom_groupe.upper())):
            inscription.execute("INSERT INTO groupe(nom_groupe ,nom_filiere ) Values ('"+nom_groupe.upper()+"', '"+filiere+"')")
            inscription.commit()
            window.inscription_groupe.addItems([nom_groupe.upper()])
            message("Ajouter Groupe", "Bien Ajouter !")
            #clear
            window.Nom_groupe.clear()
        else : 
            message("Groupe", "Error : Cette Filiere déja existe ")


def ajouter_stg():
    nom=window.inscription_nom.text()
    prenom=window.inscription_prenom.text()
    filiere = window.inscription_filiere.currentText()
    groupe = window.inscription_groupe.currentText()
    adresse=window.inscription_adresse.text()
    telephone=window.inscription_telephone.text()
    if (nom=='' or prenom=='' or filiere =='Choisir une filiere' or groupe=="Choisir un groupe" or adresse=='' or telephone==''):
        message("Ajouter stagiaire ", "Error : remplir les champs ")
    else :
        inscription.execute("insert into stagiaire(nom ,prenom,filiere,groupe ,telephone ,adresse) values('"+nom.lower()+"','"+prenom.lower()+"','"+filiere+"','"+groupe+"' ,'"+telephone+"' ,'"+adresse+"');")
        inscription.commit()
        message("Ajouter stagiaire ", "Bien Ajouter !")
        window.inscription_nom.clear()
        window.inscription_prenom.clear()
        window.inscription_adresse.clear()
        window.inscription_telephone.clear()

    afficher(get_data_stg())
    #clear


def drop_filiere():
    list_filiere  = []
    mycursor = inscription.cursor()
    mycursor.execute("SELECT nom_filiere FROM filiere")
    list_filiere_disponible = mycursor.fetchall()
    for i in list_filiere_disponible :
        list_filiere.append(i[0])
    # print(list_filiere)
    
    window.drop_filiere.addItems(list_filiere)
    window.inscription_filiere.addItems(list_filiere)
   # print(list_filiere)
    print(window.inscription_groupe.currentText())

def Render_group():
    a = window.inscription_filiere.currentText()
    mycursor = inscription.cursor()
    mycursor.execute("SELECT nom_groupe FROM groupe Where nom_filiere='"+a+"' ")
    list_groupe_disponible = mycursor.fetchall()
    list_new= []
    for i in list_groupe_disponible:
        list_new.append(i[0])
    print(list_new)
    # return self.currentText()
    window.inscription_groupe.clear()
    window.inscription_groupe.addItems(list_new)



def drop_groupe():
    list_groupe  = []
    mycursor = inscription.cursor()
    mycursor.execute("SELECT nom_groupe FROM groupe Where '"+window.inscription_filiere.currentText()+"' ")
    list_groupe_disponible = mycursor.fetchall()
    for i in list_groupe_disponible :
        list_groupe.append(i[0])
    
    window.inscription_groupe.addItems(list_groupe)

def get_data_stg():
    mycursor = inscription.cursor()
    mycursor.execute("SELECT * FROM stagiaire")
    stgs = mycursor.fetchall()
    return stgs

def afficher(donne):
    list_general_stgs =  donne
    row = 0
    window.table_liste.setRowCount(len(list_general_stgs))

    for person in list_general_stgs :
        window.table_liste.setItem(row, 0,QTableWidgetItem(f"{person[0]}")) #Code
        window.table_liste.setItem(row, 1,QTableWidgetItem(person[1]))   #Nom
        window.table_liste.setItem(row, 2,QTableWidgetItem(person[2]))   #Prenom
        window.table_liste.setItem(row, 3,QTableWidgetItem(person[3]))   #filiere
        window.table_liste.setItem(row, 4,QTableWidgetItem(person[4]))   #groupe
        window.table_liste.setItem(row, 5,QTableWidgetItem(person[5]))   #tele
        window.table_liste.setItem(row, 6,QTableWidgetItem(person[6])) # adresse
        row+=1

def Chercher_name(name):#Cherche par nom dans Database 
    mycursor = inscription.cursor()
    mycursor.execute("SELECT * FROM stagiaire Where nom='"+name+"' ")
    result = mycursor.fetchall()
    return result

def Search_btn():
    valeur = window.Zone_search.text()
    if valeur:
        result = Chercher_name(valeur)
        afficher(result)
    else :
        afficher(get_data_stg())
    window.Zone_search.clear()

def Chercher_code(code):#Cherche par nom dans Database 
    result = []
    mycursor = inscription.cursor()
    mycursor.execute("SELECT * FROM stagiaire Where code_de_stagiaire='"+code+"' ")
    result = mycursor.fetchall()

    if len(result) == 0: 
        return False
    else :
        return True


def supp_stg():
    code_stg = window.zone_supp.text()
    if(code_stg != ''):
        if (Chercher_code(code_stg)):
            mycursor = inscription.cursor()
            mycursor.execute("DELETE FROM stagiaire WHERE code_de_stagiaire='"+code_stg+"';")
            message("supprimer stagiaire ", "Bien supprimer !")
        else:
            message("supprimer stagiaire ", "Le code n'existe pas")

    else : 
        message("supprimer stagiaire ", "Enter un Code Stagiaire")
    window.zone_supp.clear()
    inscription.commit()
    afficher(get_data_stg())


def check_filiere(filiere):
    filiere_ = []
    mycursor = mycursor = inscription.cursor()
    mycursor.execute(f"SELECT nom_filiere FROM filiere WHERE nom_filiere='{filiere}'")
    filiere_ = mycursor.fetchall()
    if filiere_:
        return True
    else :
        return False
def check_groupe(groupe):
    groupe_ = []
    mycursor = mycursor = inscription.cursor()
    mycursor.execute(f"SELECT nom_groupe FROM groupe WHERE nom_groupe='{groupe}'")
    groupe_ = mycursor.fetchall()
    if len(groupe_)==0:
        return True
    else :
        return False


afficher(get_data_stg())
drop_filiere()
drop_groupe()
get_data_stg()

window.refresh.clicked.connect(lambda :afficher(get_data_stg()))
window.delete_btn.clicked.connect(supp_stg)
window.search_btn.clicked.connect(Search_btn)
window.inscription_filiere.currentIndexChanged.connect(Render_group)
window.inscription_valider.clicked.connect(ajouter_stg)
window.groupe_valider.clicked.connect(ajouter_groupe)
window.filiere_valider.clicked.connect(ajouter_filiere)
login_space.connect.clicked.connect(check)

window.table_liste.setColumnWidth(6, 210)

login_space.show()
app.exit(app.exec_())





#################################################################
#################################################################
##########   PROJECT CREE PAR :                     #############
##########    LAHCEN AOUINA & HASSAN EL KABAIR      #############
#################################################################
#################################################################

