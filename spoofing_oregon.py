#!/usr/bin/python3

# -*- coding: utf-8 -*-
def calculate_thgr810_checksum(hex_data):
    sum_of_nibbles = sum(int(char, 16) for char in hex_data)
    return "{:02X}".format(sum_of_nibbles & 0xFF)

def encode_temperature(temp):
    positive = temp >= 0
    temp_val = int(round(abs(temp) * 10))  # 22.8 -> 228
    temp_digits = list("{:03d}".format(temp_val))  # 3 digits only
    temp_nibbles = temp_digits[::-1] + ['0' if positive else '1']
    return temp_nibbles

def encode_humidity(humidity):
    hum_digits = list("{:02d}".format(humidity))  # 2 digits
    return hum_digits[::-1]  # Reversed

def swap_crc(crc_hex):
    return crc_hex[1] + crc_hex[0]  # Swap the two chars

def reverse_bits_in_nibble(nibble):
    return format(int(nibble, 16), '04b')[::-1]

def hex_to_bitstream(hex_string):
    # Invert bits in each nibble before generating bitstream
    bitstream = []
    for hex_char in hex_string:
        reversed_bits = reverse_bits_in_nibble(hex_char)
        bitstream.extend(int(bit) for bit in reversed_bits)
    return bitstream

def bitstream_to_symbols(bitstream):
    symbols = []
    prev = bitstream[0]
    symbols.append('S')  # First bit assumed to be '1'
    for bit in bitstream[1:]:
        symbols.append('S' if bit == prev else 'L')
        prev = bit
    return ''.join(['SS' if s == 'S' else 'L' for s in symbols])  # S = short = SS



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
                #print("Pas de changement", bit,  previous_state)
                if previous_state == "1":
                    raw_values.append(-430)
                    raw_values.append(550)
                elif previous_state == "0":
                    raw_values.append(550)
                    raw_values.append(-430)
            elif bit != previous_state:
                # changement d'etat donc impulsion longue
                #print("Changement", bit,  previous_state)
                if previous_state == "1":
                    raw_values.append(-920)
                elif previous_state == "0":
                    raw_values.append(1030)

            #sauvegarde de la valeur precedente de la valeur binaire
            previous_state = bit
        header = f"""Filetype: Flipper SubGhz RAW File
Version: 1
# generated with https://github.com/Dicalius/RF-433
# Auto-generated on transmission
Frequency: 433920000
Preset: FuriHalSubGhzPresetOok650Async
Protocol: RAW
RAW_Data: {" ".join(map(str, raw_values))}
"""
    with open(output_filename, "w") as f:
        f.write(header)
    
    print(f"\n✅ Fichier .sub généré : {output_filename}")



def main():
    sensors = {
        1: ("THGR810", "F824"),
        2: ("THGN123N", "1D20"),
        3: ("THWR288A", "EA4C"),
    }

    print("Quel capteur souhaitez-vous simuler ?")
    for i, (name, _) in sensors.items():
        print(f"{i}. {name}")

    choice = int(input("Entrez le numéro du capteur : "))
    if choice not in sensors:
        print("Capteur non valide.")
        return

    sensor_name, sensor_code = sensors[choice]
    temp = float(input("Entrez la température (ex: 22.8): "))
    humidity = int(input("Entrez l'humidité (ex: 56): "))

    # Demander le channel (1-9)
    channel = int(input("Entrez le channel (1-9) : "))
    if not (1 <= channel <= 9):
        print("Channel invalide.")
        return

    rolling_code = ['7', '1']
    sign_bit = ['1' if temp >= 0 else '0']
    temp_nibbles = encode_temperature(temp)
    hum_nibbles = encode_humidity(humidity)
    constant = ['4']
    end_const = ['9', 'A']

    print("\n--- RÉCAPITULATIF ---")
    print(f"Capteur sélectionné : {sensor_name} ({sensor_code})")
    print(f"Canal utilisé       : {channel}")
    print(f"Rolling code        : {''.join(rolling_code)}")
    print(f"Température         : {temp} °C ({'positive' if temp >= 0 else 'négative'})")
    print(f"Humidité            : {humidity} %")

    data_nibbles = list(sensor_code) + [str(channel)] + rolling_code + sign_bit + temp_nibbles + hum_nibbles + constant
    crc_input = ''.join(data_nibbles)
    crc = calculate_thgr810_checksum(crc_input)
    crc_swapped = swap_crc(crc)

    full_nibbles = data_nibbles + list(crc_swapped) + end_const
    hex_string = ''.join(full_nibbles)

    full_hex = "FFFFFFA" + hex_string

    print("\nChaîne hexadécimale complète :")
    print(full_hex)

    bitstream = hex_to_bitstream(full_hex)
    print("\nBitstream :")
    binary_input = (''.join(str(bit) for bit in bitstream))
    print(binary_input)

    # Nom du fichier de sortie
    nom_fichier_sortie = "raw_data_output_serge.sub"

    # Exécuter la conversion et l'enregistrement
    binary_to_raw(binary_input, nom_fichier_sortie)

if __name__ == "__main__":
    main()
