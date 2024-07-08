#################################################################
# IMPORT
#################################################################
import os
import time
import cv2
import re
import csv
# import sys

from src.loader import c_loader

import numpy as np
import pytesseract

from PIL import Image

pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract.exe'
# print(pytesseract.pytesseract.tesseract_cmd)


#################################################################
# GLB
#################################################################
GLB_COLUMN_PERSONNE_PHYSIQUE = ["Nom / Prénom", "Sexe", "Date de naissance", "Lieu de naissance", "Nom et prénom d'usage", "Droit", "Adresse des titulaires de droit", "Identifiant foncier"]
GLB_COLUMN_PERSONNE_MORALE = ["Raison sociale", "Numéro SIREN", "Sigle", "Droit", "Adresse des titulaires de droit", "Identifiant foncier"]


#################################################################
# CLASS
#################################################################
class cPersonne_physique:
    def __init__(self, nom_prenom, sexe, data_naissance, lieu_naissance, nom_prenom_usage, droit, adresse_titulaire_droit, adresse_fonciere, post_code, id_foncier):
        self.section_parcelle = ""
        self.parcelle = ""
        self.city = ""
        
        self.nom_prenom = nom_prenom 
        self.sexe = sexe  
        self.data_naissance = data_naissance  
        self.lieu_naissance = lieu_naissance  
        self.nom_prenom_usage = nom_prenom_usage  
        self.droit = droit  
        self.adresse_titulaire_droit = adresse_titulaire_droit  
        self.adresse_fonciere = adresse_fonciere
        self.post_code = post_code
        self.id_foncier = id_foncier         
     
    def set_section_parcelle(self, section_parcelle):
        self.section_parcelle = section_parcelle
        
    def set_parcelle(self, parcelle):
        self.parcelle = parcelle
      
    def set_city(self, city):
        self.city = city
     
    def get_csv_row(self, header):
        row = []
        for value in header:
            if(value == "Section Parcelle"):
                row.append(self.section_parcelle)
            elif(value == "Parcelle"):
                row.append(self.parcelle)
            elif(value == "Nom/Prenom"):
                row.append(self.nom_prenom_usage)
            elif(value == "Adresse Proprio"):
                row.append(self.adresse_fonciere)
            elif(value == "Code Postale"):
                row.append(self.post_code)
            elif(value == "Commune"):
                row.append(self.city)
            else:
                row.append(" ")
        
        return row
              
    def toString(self):
        print("------------- Personne Physique -------------")
        print(f"section parcelle: {self.section_parcelle}")
        print(f"parcelle: {self.parcelle}")
        print(f"city: {self.city}")
        print(f"nom_prenom: {self.nom_prenom}")
        print(f"sexe: {self.sexe}")
        print(f"data_naissance: {self.data_naissance}")
        print(f"lieu_naissance: {self.lieu_naissance}")
        print(f"nom_prenom_usage: {self.nom_prenom_usage}")
        print(f"droit: {self.droit}")
        print(f"adresse_titulaire_droit: {self.adresse_titulaire_droit}")
        print(f"id_foncier: {self.id_foncier}")
              
class cPersonne_morale:
    def __init__(self, raison_sociale, numero_siren, sigle, droit, adresse_titulaire_droit, adresse_fonciere, post_code, id_foncier):
        self.section_parcelle = ""
        self.parcelle = ""
        self.city = ""
        
        self.raison_sociale = raison_sociale
        self.numero_siren = numero_siren  
        self.sigle = sigle  
        self.droit = droit  
        self.adresse_titulaire_droit = adresse_titulaire_droit  
        self.adresse_fonciere = adresse_fonciere
        self.post_code = post_code
        self.id_foncier = id_foncier 
    
    def set_section_parcelle(self, section_parcelle):
        self.section_parcelle = section_parcelle
        
    def set_parcelle(self, parcelle):
        self.parcelle = parcelle
      
    def set_city(self, city):
        self.city = city
    
    def get_csv_row(self, header):
        row = []
        for value in header:
            if(value == "Section Parcelle"):
                row.append(self.section_parcelle)
            elif(value == "Parcelle"):
                row.append(self.parcelle)
            elif(value == "Nom/Prenom"):
                row.append(self.raison_sociale)
            elif(value == "Adresse Proprio"):
                row.append(self.adresse_fonciere)
            elif(value == "Code Postale"):
                row.append(self.post_code)
            elif(value == "Commune"):
                row.append(self.city)
            else:
                row.append(" ")
        
        return row
         
    def toString(self):
        print("------------- Personne Morale -------------")
        print(f"section parcelle: {self.section_parcelle}")
        print(f"parcelle: {self.parcelle}")
        print(f"city: {self.city}")
        print(f"raison_sociale: {self.raison_sociale}")
        print(f"numero_siren: {self.numero_siren}")
        print(f"sigle: {self.sigle}")
        print(f"droit: {self.droit}")
        print(f"adresse_titulaire_droit: {self.adresse_titulaire_droit}")
        print(f"id_foncier: {self.id_foncier}")


#################################################################
# FUNCTION
#################################################################

# -------------- On Image --------------
def get_bounding_boxes(file_path):
    if(not os.path.exists(file_path)):
        print("Error <get_bounding_boxes> file_path not found")
        return
    
    img = cv2.imread(file_path)
    
    # color to find
    lower = np.array([172, 172, 172])
    upper = np.array([174, 174, 174])
    mask = cv2.inRange(img, lower, upper)
    
    kernel = np.ones((2, 2), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=1)
    
    #apply mask
    result = cv2.bitwise_and(img, img, mask=mask)
    
    #transform to grey
    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    
    #remove bruit and get edge
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    
    # get contours
    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    bounding_boxes = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        if(not (x, y, w, h) in bounding_boxes):
            bounding_boxes.append((x, y, w, h))
            
    # print(f"bounding_boxes : {bounding_boxes}\n number: {len(bounding_boxes)}")
    
    bounding_boxes.reverse()
    bounding_boxes = bounding_boxes[:-1]
    
    
    # for boxe in bounding_boxes:
    #     x, y, w, h = boxe
    #     region_to_resize = img[y:y+h, x:x+w]


    #     cv2.imshow('Resized Image', region_to_resize)
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()
            
    
    return bounding_boxes



# -------------- On path -------------- 
def get_list_path(folder_path):
    list_files = os.listdir(folder_path)
    list_path = []
    for file in list_files:
        if(not file.endswith(".png")):
            print(f"Error <get_list_path> {file} wrong format")
            continue
        file_path = os.path.join(folder_path, file)
        list_path.append(file_path)     
        
    # list_path = [os.path.join(folder_path, file) for file in list_files]
    return list_path

def rename_files(folder_path, list_path):
    new_list_path = []
    for i in range(len(list_path)):
        old_name = list_path[i]
        new_name = "img_{:04d}.png".format(i+1)
        new_path = os.path.join(folder_path, new_name)
        if(not os.path.exists(new_path)):
            os.rename(old_name, new_path)
        new_list_path.append(new_path)

    return new_list_path    
    


# -------------- On text --------------
def get_city(text):
    if(not (("(" in text) and (")" in text))):
        return ""
        
    index_start = text.index("(")
    index_stop = text.index(")")
    
    city = text[index_start+1: index_stop]
    city_formated = get_text_formated(city)
    
    list_word = city_formated.split(";")
    if(len(list_word) != 2):
        return city_formated
        
    city_formated = list_word[-1] 
    return city_formated

def get_number_personne(text, indice):
    if(indice == None):
        return 0
    
    number_personne = text[indice+2]
    if(not number_personne.isdigit()):
        print(f"Error <get_number_personne> number invalid")
        return 0
    
    return int(number_personne)

def get_parcelle(text):
    match_parcelle = re.search(r"de la parcelle ", text)

    if(not match_parcelle):
        return "", ""
    else:
        indice_start = match_parcelle.end() 
        if(len(text) < (indice_start+7)):
            return "", ""
        
        section_parcelle = text[indice_start: indice_start+2]
        parcelle = text[indice_start+3: indice_start+7]
        
        return section_parcelle, parcelle  
   
def get_text(file_path, bounding_box, indice):
    x, y, w, h = bounding_box[indice]
        
    img = cv2.imread(file_path)
    region_to_resize = img[y:y+h, x:x+w]
    
    text = pytesseract.image_to_string(region_to_resize)  
    text_formated = get_text_formated(text)
    
    return text_formated

def get_text_formated(text):
    text_formated = text.replace('\n', ' ')
    text_formated = text_formated.strip()
    return text_formated
       
def get_type_personne(text):
    match_physical = re.search(r"personne(s)? physique(s)?", text)
    match_moral = re.search(r"personne(s)? morale(s)?", text)

    if match_physical:
        return (match_physical.end(), 0)
    elif match_moral:
        return (match_moral.end(), 1)
    else:
        print(f"Error <get_type_personne> personne unknown")
        return None, None
   
def format_adresse(text_adresse_titulaire_droit):
    list_word = text_adresse_titulaire_droit.split(" ")
    list_number = []
    for i in range(len(list_word)):
        word = list_word[i]
        if(not word.isdigit()):
            continue
        
        number = int(word)
        if((number > 10000) and (number < 100000)):
            list_number.append(word)
            

    if(len(list_number) != 1):
        return text_adresse_titulaire_droit, text_adresse_titulaire_droit
    
    index = list_word.index(list_number[0])
    
    adresse_fonciere = list_word[:index]
    post_code = list_word[index:]

    adresse_fonciere = " ".join(adresse_fonciere)
    post_code = " ".join(post_code)
      
    return  adresse_fonciere, post_code
    # print(f"text_adresse_titulaire_droit: {text_adresse_titulaire_droit}") 
    # print(f"adresse_fonciere: {adresse_fonciere}")
    # print(f"post_code: {post_code}")
    # print("------------------------")

    
# -------------- On class -------------- 
def set_city_information(list_personne, city):
    for personne in list_personne:
        personne.set_city(city)
 
def set_parcelle_information(list_personne, section_parcelle, parcelle):
    for personne in list_personne:
        personne.set_section_parcelle(section_parcelle)
        personne.set_parcelle(parcelle)
        

# -------------- On csv --------------
def create_csv(path, data):
    with open(path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        
        for row in data:
            writer.writerow(row)
    

# -------------- On csv data--------------
def format_data_csv(data):
    data_grouped_by_parcelle = group_data_by_parcelle(data)
    data_grouped_by_name = group_data_by_name(data_grouped_by_parcelle)
    
    
    sorted_data = sorted(data_grouped_by_name[1:], key=lambda x: (x[1], x[2]))
    sorted_data.insert(0, data_grouped_by_name[0])
    
    return sorted_data


def group_data_by_name(data):
    dict_data = {}
    for i in range(len(data)):
        if(i == 0 ):
            continue
        
        row = data[i]
        
        section_parcelle = row[1]
        parcelle = row[2]
        code = row[9]
        
        key = (section_parcelle, parcelle, code)
        if(key in dict_data):
            dict_data[key].append(i)
        else:
            dict_data[key] = [i]
        
    new_data = []
    new_data.append(data[0])
    
    for key in dict_data:
        array_indice = dict_data[key]
        
        size_array = len(array_indice)
        name = ""
        
        for i in range(size_array):
            indice = array_indice[i]
            row = data[indice]
            
            if(i < (size_array-1)):
                name += row[7]  + ", "
            else:
                name += row[7]
            
        row[7] = name
        new_data.append(row)
        
    return new_data
  

def group_data_by_parcelle(data):
    dict_data = {}
    for i in range(len(data)):
        if(i == 0 ):
            continue
        
        row = data[i]
        
        section_parcelle = row[1]
        name = row[7]
        code = row[9]
        
        key = (section_parcelle, name, code)
        if(key in dict_data):
            dict_data[key].append(i)
        else:
            dict_data[key] = [i]
        
    new_data = []
    new_data.append(data[0])
    
    for key in dict_data:
        array_indice = dict_data[key]
        
        size_array = len(array_indice)
        parcelle = ""
        
        for i in range(size_array):
            indice = array_indice[i]
            row = data[indice]
            
            if(i < (size_array-1)):
                parcelle += row[2]  + ", "
            else:
                parcelle += row[2]
            
        row[2] = parcelle
        new_data.append(row)
        
    return new_data
    

# -------------- Main function --------------
def get_list_information(list_path):
    list_personne_morale = []
    list_personne_physique = []
    
    list_error_personne_morale = []
    list_error_personne_physique = []
    
    list_error_parcelle = []
    list_error_city = []
    
    for i in range(len(list_path)):
        status = 0
        file_path = list_path[i]
        
        if(not os.path.exists(file_path)):
            list_error_personne_morale.append(file_path)
            continue
        
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)
        
        # get the informations on the 'pacerelle' 
        section_parcelle, parcelle = get_parcelle(text)
        if((section_parcelle == "") or (parcelle == "")):
            list_error_parcelle.append(file_path)
            
        # get the city
        city = get_city(text)
        if(city == ""):
            list_error_city.append(file_path)
        
        #get the type of personne  
        type_personne = get_type_personne(text)
        if(type_personne == (None, None)):
            print(f"<Error> type unknow in {file_path}")
            
        index, personne_type = type_personne
        # get the number of personne
        number_personne = get_number_personne(text, index)
        
        #split table on the picture to get each cells coordinates
        bounding_box = get_bounding_boxes(file_path)
        
        if(personne_type == 1):
            # create object that represent personne
            temp_list_personne_morale = create_personne_morale(file_path, bounding_box, number_personne) 
            
            #set informations taken before
            set_parcelle_information(temp_list_personne_morale, section_parcelle, parcelle)
            set_city_information(temp_list_personne_morale, city)
            
            # store data
            if(len(temp_list_personne_morale) == 0):
                list_error_personne_morale.append(file_path)
                status = 2
            else:
                list_personne_morale += temp_list_personne_morale
                status = 1
            
        elif(personne_type == 0):
            # create object that represent personne 
            temp_list_personne_physique = create_personne_physique(file_path, bounding_box, number_personne)
            
            #set informations taken before
            set_parcelle_information(temp_list_personne_physique, section_parcelle, parcelle)
            set_city_information(temp_list_personne_physique, city)
            
            # store data
            if(len(temp_list_personne_physique) == 0):
                list_error_personne_physique.append(file_path)
                status = 2
            else:
                list_personne_physique += temp_list_personne_physique  
                status = 1
         
        elif(personne_type == None):
            list_error_personne_morale.append(file_path)
            status = 2
                   
        percent = (i*100)/len(list_path)
        c_loader.step(percent, status)
                
                         
            
    # print(f"list_personne_morale : {len(list_personne_morale)}")
    # print(f"list_personne_physique : {len(list_personne_physique)}")
    
    # print(f"size list_error_personne_morale : {len(list_error_personne_morale)}")
    # print(f"size list_error_personne_physique : {len(list_error_personne_physique)}")
    
    # print(f"list_error_personne_morale : {list_error_personne_morale}")
    # print(f"list_error_personne_physique : {list_error_personne_physique}")
    
    # print(f"error pacerelle : {list_error_parcelle}")
    # print(f"error city : {list_error_city}")
    
    data = {
        "list_personne_morale":list_personne_morale,
        "list_personne_physique":list_personne_physique,
        "list_error_personne_morale":list_error_personne_morale,
        "list_error_personne_physique":list_error_personne_physique,
        "list_error_parcelle":list_error_parcelle,
        "list_error_city":list_error_city,
    }
        
    return data
 
  
def create_personne_morale(file_path, bounding_box, number_personne):
    list_personne_morale = []
    
    number_column = len(GLB_COLUMN_PERSONNE_MORALE)
    number_row = number_personne +1
    number_cells = number_column *  number_row

    if(len(bounding_box) != number_cells):
        print(f"Error <create_personne_morale> len(bounding_box) != number_cells) : {len(bounding_box) != number_cells}")
        return []
    
    #check header
    for i in range(number_column):
        text = get_text(file_path, bounding_box, i)
        
        if(text != GLB_COLUMN_PERSONNE_MORALE[i]):
            print(f"Error <create_personne_morale> text_formated != GLB_COLUMN_PERSONNE_MORALE[i] : {text} != {GLB_COLUMN_PERSONNE_MORALE[i]}")
            return []
    
    # rows
    for i in range(1, number_row, 1):
        indice_raison_sociale = (number_column*i)
        text_raison_sociale = get_text(file_path, bounding_box, indice_raison_sociale)
        
        # indice_numero_siren = 1 + (number_column*i)
        # text_numero_siren = get_text(file_path, bounding_box, indice_numero_siren)
        text_numero_siren = "UNUSED"
        
        # indice_sigle = 2 + (number_column*i)
        # text_sigle = get_text(file_path, bounding_box, indice_sigle)
        text_sigle ="UNUSED"
        
        # indice_droit = 3 + (number_column*i)
        # text_droit = get_text(file_path, bounding_box, indice_droit)
        text_droit = "UNUSED"
        
        indice_adresse_titulaire_droit = 4 + (number_column*i)
        text_adresse_titulaire_droit = get_text(file_path, bounding_box, indice_adresse_titulaire_droit)
        
        adresse_fonciere, post_code = format_adresse(text_adresse_titulaire_droit)
        
        # indice_id_foncier = 5 + (number_column*i)
        # text_id_foncier = get_text(file_path, bounding_box, indice_id_foncier)
        text_id_foncier = "UNUSED"
        
        c_personne_morale = cPersonne_morale(text_raison_sociale, text_numero_siren, text_sigle, text_droit, text_adresse_titulaire_droit, adresse_fonciere, post_code, text_id_foncier)
        # c_personne_morale.toString()
        list_personne_morale.append(c_personne_morale)
        
    return list_personne_morale
                          
def create_personne_physique(file_path, bounding_box, number_personne):
    list_personne_physique = []
    
    number_column = len(GLB_COLUMN_PERSONNE_PHYSIQUE)
    number_row = number_personne +1
    number_cells = number_column *  number_row

    if(len(bounding_box) != number_cells):
        print(f"Error <create_personne_physique> len(bounding_box) != number_cells) : {len(bounding_box) != number_cells}")
        return []
    
    #check header
    for i in range(number_column):
        text = get_text(file_path, bounding_box, i)
            
        if(text != GLB_COLUMN_PERSONNE_PHYSIQUE[i]):
            # weird case
            if((i == 0) and (text == "Nom/ Prénom")):
                continue
            print(f"Error <create_personne_physique> text_formated != GLB_COLUMN_PERSONNE_MORALE[i] : {text} != {GLB_COLUMN_PERSONNE_PHYSIQUE[i]}")
            return []
        
    
    # rows
    for i in range(1, number_row, 1):
        indice_nom_prenom = (number_column*i)
        text_nom_prenom = get_text(file_path, bounding_box, indice_nom_prenom)
        text_nom_prenom = "UNUSED"
        
        indice_sexe = 1 + (number_column*i)
        text_sexe = get_text(file_path, bounding_box, indice_sexe)
        
        # indice_date_naissance = 2 + (number_column*i)
        # text_date_naissance = get_text(file_path, bounding_box, indice_date_naissance)
        text_date_naissance = "UNUSED"
        
        # indice_lieu_naissance = 3 + (number_column*i)
        # text_lieu_naissance = get_text(file_path, bounding_box, indice_lieu_naissance)
        text_lieu_naissance = "UNUSED"
        
        indice_nom_prenom_usage = 4 + (number_column*i)
        text_nom_prenom_usage = get_text(file_path, bounding_box, indice_nom_prenom_usage)
        
        # indice_droit = 5 + (number_column*i)
        # text_droit = get_text(file_path, bounding_box, indice_droit)
        text_droit = "UNUSED"
        
        indice_adresse_titulaire_droit = 6 + (number_column*i)
        text_adresse_titulaire_droit = get_text(file_path, bounding_box, indice_adresse_titulaire_droit)
        adresse_fonciere, post_code = format_adresse(text_adresse_titulaire_droit)
        
        # indice_id_foncier = 7 + (number_column*i)
        # text_id_foncier = get_text(file_path, bounding_box, indice_id_foncier)
        text_id_foncier = "UNUSED"
        
        c_personne_physique = cPersonne_physique(text_nom_prenom, text_sexe, text_date_naissance, text_lieu_naissance, text_nom_prenom_usage, text_droit, text_adresse_titulaire_droit, adresse_fonciere, post_code, text_id_foncier)
        # c_personne_physique.toString()
        list_personne_physique.append(c_personne_physique)
        
    return list_personne_physique      



# -------------- OTHER --------------
# path = r"St etienne du rouvray - Copie\\img_1.png"
# get_bounding_boxes(path)
# img = cv2.imread(path)
# cv2.imshow('Image', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()



# file_path = r"St etienne du rouvray - Copie\\img_15.png"
# img = cv2.imread(file_path)
# boxes = pytesseract.image_to_boxes(img)  

  
# bounding_box = get_bounding_boxes(file_path)

# # for i in range(len(bounding_box)):
# for i in range(1):
#     x, y, w, h = bounding_box[2]
#     word = []
#     for b in boxes.splitlines():
#         b = b.split()
#         char, bx, by, bw, bh = b[0], int(b[1]), int(b[2]), int(b[3]), int(b[4])
#         by = img.shape[0] - by
#         bh = img.shape[0] - bh
        
#         if bx >= x and bw <= x + w and by >= y and bh <= y + h:
#             word.append(char)
        
#     print(word)
#     print(''.join(word))