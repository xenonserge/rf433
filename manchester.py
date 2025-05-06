def coder_manchester(binaire):
    """
    Code une chaîne binaire en une séquence Manchester.

    Args:
        binaire (str): La chaîne binaire d'entrée.

    Returns:
        str: La séquence Manchester correspondante ('L' pour long, 'S' pour short).
    """
    if not binaire:
        return ""

    manchester = ""
    etat_precedent = binaire[0]

    for bit in binaire:
        if bit == etat_precedent:
            manchester += "S"
        else:
            manchester += "L"
            etat_precedent = bit

    return manchester

# Exemple d'utilisation
entree_binaire = "1111111111111111111111110101111100010100001010011110"
sequence_manchester = coder_manchester(entree_binaire)
print(f"L'entrée binaire : {entree_binaire}")
print(f"La séquence Manchester : {sequence_manchester}")