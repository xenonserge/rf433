def binary_to_raw(binary_message, output_filename="raw_data.txt"):
    """
    si changement d'etat alors impulsion longue.
    si aucun changement alors impulsion courte
    A chaque changement on prend l'etat précedent et on inverse
    """

    previous_state = "1"  # État initial a 1
    raw_values = []
    raw_values.append(550)  # valeur de la premiere impulsion pour la mise en forme du raw - valur a 550 mais qui pourrait etre plus longue

    for i in range(0, len(binary_message), 1):
        if i + 1 < len(binary_message):
            bit = binary_message[i]
            if bit == previous_state:
                # si valeur identique a precedente, alors pas de changement
                print("Pas de changement", bit,  previous_state)
                if previous_state == "1":
                    raw_values.append(-430)
                    raw_values.append(550)
                elif previous_state == "0":
                    raw_values.append(550)
                    raw_values.append(-430)
            elif bit != previous_state:
                # changement d'etat donc impulsion longue
                print("Changement", bit,  previous_state)
                if previous_state == "1":
                    raw_values.append(-920)
                elif previous_state == "0":
                    raw_values.append(1030)

            #sauvegarde de la valeur precedente de la valeur binaire
            previous_state = bit
    
    with open(output_filename, "w") as f:
        f.write("RAW_Data: " + " ".join(map(str, raw_values)))

# binary message
binary_input  = "11111111111111111111111101011111000101000010100111101000100000010100010000000110101000100101001010010101"

# Nom du fichier de sortie
nom_fichier_sortie = "raw_data_output_serge.txt"

# Exécuter la conversion et l'enregistrement
binary_to_raw(binary_input, nom_fichier_sortie)

print(f"Le fichier '{nom_fichier_sortie}' a été créé avec les données RAW.")
