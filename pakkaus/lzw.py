"Tämä moduuli toteuttaa LZW-pakkausalgoritmin Tiralabraa varten."


# @dataclass
# class _TrieNode:
#     "Dataclass Trie-luokan solmuja varten."

#     children: dict[int, "_TrieNode"] = field(default_factory=dict)
#     value: Optional[bytes] = None


# class _TrieNode:
#     "class Trie-luokan solmuja varten."
#     __slots__ = "children", "value"

#     def __init__(self) -> None:
#         self.children: dict[int, _TrieNode] = dict()
#         self.value: Optional[bytes] = None


# class _Trie:
#     "Toteuttaa Trie-tietorakenteen LZW-algoritmia varten tupleja käyttäen."

#     def __init__(self) -> None:
#         # mypy ei taida tukea rekursiivisia tyyppejä
#         self.data: Any = [dict(), None]
#         self.size = 0

#     def __str__(self):
#         return str(self.data)

#     def get(self, key: bytes) -> bytes:
#         pair = self.data
#         for integer in key:
#             if integer in pair[0]:
#                 pair = pair[0][integer]
#             else:
#                 raise KeyError("Trie get() did not find key.")
#         # # mypy valittaa optionalista:
#         # if map.value is None:
#         #     raise ValueError()
#         return pair[1]

#     def __getitem__(self, item: bytes) -> bytes:
#         return self.get(item)

#     def __setitem__(self, key: bytes, value: bytes) -> None:
#         return self.insert(key, value)

#     def __contains__(self, item: bytes) -> bool:
#         pair = self.data
#         for integer in item:
#             if integer in pair[0]:
#                 pair = pair[0][integer]
#             else:
#                 return False
#         return True

#     def insert(self, key: bytes, value: bytes) -> None:
#         pair = self.data
#         for integer in key:
#             if integer not in pair[0]:
#                 pair[0][integer] = [dict(), None]
#             pair = pair[0][integer]
#         pair[1] = value
#         self.size += 1

#     def __len__(self):
#         return self.size


def compress(data: bytes) -> bytes:
    """
    Pakkaa annetun bytes-rakenteen LZW-algoritmilla.
    """

    # koska bytes konkatenaatio on hidasta,
    # käytetään bytearrayita

    DICTIONARY_MAX_SIZE = 2 ** 16
    # Testissä oli Trie tietorakenne hitauden selvittämiseksi
    # Se oli jotenkin vielä hitaampi kuin dict.
    # Luultavasti koska Pythonin oliot ovat erittäin hitaita ja
    # dict on osittain optimoitua C-koodia.
    # Myös Trie ilman luokkia on noin 2.5 kertaa hitaampi
    # kuin dict
    # dictionary = _Trie()
    dictionary = dict()

    # sanakirjan laitetaan kaikki yhden tavun koodit
    for i in range(0, 256):
        dictionary[i.to_bytes(1, "big")] = i.to_bytes(2, "big")

    # jostain syystä tämä on nopeampi kuin
    # len(dictionary), vaikka dict kyllä
    # pitää lukua itse
    dict_size = 256

    results: list[bytes] = list()

    # bytes() + bytes() konkatenaatio
    # pitäisi olla hidasta, mutta testauksen
    # mukaan se on nopeampaa kuin bytearray()
    word = bytes()

    # itse algoritmi
    for pointer, _ in enumerate(data):
        # sanakirja ei voi kasvaa loputtomasti, joten
        # se tyhjennetään. Sopivasti tämä rajoittaa
        # koodin pituuden kahteen tavuun
        if dict_size >= DICTIONARY_MAX_SIZE:
            del dictionary
            dict_size = 256
            # dictionary = _Trie()
            dictionary = dict()
            for i in range(0, 256):
                dictionary[i.to_bytes(1, "big")] = i.to_bytes(2, "big")

        byte = data[pointer : pointer + 1]

        # etsitään pisin merkkijono
        # joka on sanakirjassa
        if word + byte in dictionary:
            word = word + byte
        # kun pisin on löydetty, sen koodi tulostetaan
        else:
            results.append(dictionary[word])

            # sanakirjaan lisätään pisin merkkijono
            # plus seuraava symboli
            dictionary[word + byte] = dict_size.to_bytes(2, "big")

            dict_size += 1
            # aloitetaan uudelleen pisimmän merkkijonon haku
            word = byte

    results.append(dictionary[word])

    return b"".join(results)


def uncompress(data: bytes) -> bytes:
    """
    Purkaa annetun LZW-pakatun bytes rakenteen.
    Toisin kuin compress(), tämän funktion
    nopeus pitäisi olla hyväksyttävää.
    """

    # LZW:n purkaminen toimii, koska
    # koodeista voidaan rakentaa syöte
    # takaperin, kunhan käytetään tarkalleen
    # samaa tapaa kuin pakkauksessa

    DICTIONARY_MAX_SIZE = 2 ** 16

    # sanakirjana käytetään pelkkää listaa
    # itse alkusanakirja on sama kuin pakkauksessa
    dictionary: list[bytearray] = list()
    for i in range(0, 256):
        dictionary.append(i.to_bytes(1, "big"))

    output: list[bytearray] = list()

    # kahden tavun konkatenaatio
    last_code = (data[0] << 8) | data[1]
    code = last_code
    output.append(dictionary[last_code])

    for i in range(2, len(data) - 1, 2):

        code = (data[i] << 8) | data[i + 1]
        # koodit ovat samassa indeksissä kuin
        # niiden arvot listassa, joten
        # jos koodi on vähemmän kuin
        # listan pituus, se kuuluu siihen
        if code < len(dictionary):
            # kun ohjelma tulostaa merkkijonon,
            output.append(dictionary[code])
            # se konkatenoidaan seuraavan dekoodatun
            # merkkijonon ekalla merkillä ja lisätään
            # sanakirjaan
            dictionary.append(dictionary[last_code] + dictionary[code][0:1])
        # jos seuraavaa merkkijonoa ei voi dekoodata,
        # seuraavan on pakko olla tällä hetkellä dekoodattu merkkijono
        # joten sen ensimmäinen merkki on sama kuin
        # tämänhetkisen ensimmäinen merkki
        else:
            # mikä lisätään sanakirjaan
            dictionary.append(dictionary[last_code] + dictionary[last_code][0:1])
            output.append(dictionary[last_code] + dictionary[last_code][0:1])

        last_code = code

        # sanakirja myös tyhjennetään samassa kohdassa kuin pakkauksessa
        if len(dictionary) == DICTIONARY_MAX_SIZE:
            dictionary.clear()
            for i in range(0, 256):
                dictionary.append(i.to_bytes(1, "big"))

    return b"".join(output)


def compress_file(source_name: str, destination_name: str) -> None:
    """
    Avaa annetun tiedoston, lukee, pakkaa ja tallentaa sen.
    Pakatut tiedot tallennetaan toiseen annettuun tiedostoon.
    Pakkauksen tekee funktio compress().
    """

    with open(source_name, "rb") as f:
        data = f.read()

    compressed = compress(data)

    with open(destination_name, "wb") as f:
        f.write(compressed)


def uncompress_file(source_name: str, destination_name: str) -> None:
    """
    Avaa funktion pack_file() pakkaaman tiedoston, purkaa sen, ja kääntää sen.
    Lopuksi käännetty data tallennetaan toiseen annettuun tiedostoon.
    Purkamisen hoitaa uncompress().
    """

    with open(source_name, "rb") as f:
        data = f.read()

    uncompressed = uncompress(data)

    with open(destination_name, "wb") as f:
        f.write(uncompressed)
