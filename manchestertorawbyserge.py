def manchester_to_raw(manchester_code, output_filename="raw_data.txt"):
    """
        
    short  c'est obligatoirement 1 transition donc deux impulsions et l'etat précédent est conservé
    long veut dire qu'il y a un changement d'etat
    """

    binary_sequence = "1"

    previous_state = 1  # État initial a 1

    raw_values = []
    raw_values.append(550)  # Transition pour le Manchester


    for i in range(0, len(manchester_code), 1):
        if i + 1 < len(manchester_code):
            pair = manchester_code[i]
            if pair == "S":
                # si Short alors on conserve l'état precedent
                print("short")
                if previous_state == 1:
                    raw_values.append(-430)
                    raw_values.append(550)
                    binary_sequence += "1"
                elif previous_state == 0:
                    raw_values.append(550)
                    raw_values.append(-430)
                    binary_sequence += "0"

                #previous_state = 1 - previous_state # Inversion de l'état
            elif pair == "L":
                # Si long alors changement d'etat
                if previous_state == 1:
                    raw_values.append(-920)
                    binary_sequence += "0"
                elif previous_state == 0:
                    raw_values.append(1030)
                    binary_sequence += "1"
                #on change le previous_state var changement d'etat
                previous_state = 1 - previous_state # Inversion de l'état

    print(binary_sequence)
    
    with open(output_filename, "w") as f:
        f.write("RAW_Data: " + " ".join(map(str, raw_values)))

# Votre code Manchester
manchester_input = "SSSSSSSSSSSSSSSSSSSSSSSLLLLSSSSLSSLLLLSSSLLLLSLSSSLLLSSLLSSSSSLLLLSSLLSSSSSSLSLLLLLSSLLSLLLLSLLLLSLLLLL"

# Nom du fichier de sortie
nom_fichier_sortie = "raw_data_output_serge.txt"

# Exécuter la conversion et l'enregistrement
manchester_to_raw(manchester_input, nom_fichier_sortie)

print(f"Le fichier '{nom_fichier_sortie}' a été créé avec les données RAW.")
