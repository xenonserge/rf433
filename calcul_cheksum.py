def calculate_thgr810_checksum(hex_data):
    """
    Calcule le checksum (avant swap) pour les données hexadécimales d'une sonde THGR810.

    Args:
        hex_data: La chaîne hexadécimale des données.

    Returns:
        La chaîne hexadécimale du checksum calculé (avant swap).
    """
    sum_of_nibbles = 0
    for char in hex_data:
        nibble = int(char, 16)
        sum_of_nibbles += nibble

    calculated_checksum = sum_of_nibbles & 0xFF
    calculated_checksum_hex = "{:02X}".format(calculated_checksum)
    return calculated_checksum_hex

# Les données hexadécimales du message (sans le checksum)
#data_hex = "F82497118210654"
#data_hex = "F82499710090214"
data_hex = "F82497118210654"



# Calcul du checksum
checksum = calculate_thgr810_checksum(data_hex)

print(f"Données (hex): {data_hex}")
print(f"Checksum calculé (avant swap): {checksum}")

# Si tu avais un message complet avec le checksum swappé, tu pourrais faire la comparaison comme ceci:
def verify_checksum_with_message(hex_message):
    if len(hex_message) >= 17:
        data_for_checksum = hex_message[:15]
        print(data_for_checksum)
        received_checksum_swapped = hex_message[15:17]
        print(received_checksum_swapped)
        calculated_checksum_unswapped = calculate_thgr810_checksum(data_for_checksum)
        received_checksum_unswapped_high = received_checksum_swapped[1]
        received_checksum_unswapped_low = received_checksum_swapped[0]
        received_checksum_unswapped = received_checksum_unswapped_high + received_checksum_unswapped_low

        if calculated_checksum_unswapped == received_checksum_unswapped:
            print("Checksum vérifié et valide.")
        else:
            print("Erreur de checksum lors de la vérification.")
    else:
        print("Message trop court pour la vérification complète du checksum.")

# Exemple de vérification (si tu avais le message complet)
full_message = "F8249711821065494"
verify_checksum_with_message(full_message)
