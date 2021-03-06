"Sallii ohjelman käytön komennolla `python -m pakkaus`."
import sys
import os

from pakkaus import huffman
from pakkaus import lzw


def get_help():
    print("Käyttö:")
    print("  python -m pakkaus (huffman|lzw) (compress|uncompress) filename compressed_filename")
    print()
    sys.exit()


if __name__ == "__main__":
    if sys.argv[2] in ["-h", "--help"]:
        get_help()
    elif sys.argv[2] in ["c", "compress", "pakkaus", "pakkaa"]:
        source_file = sys.argv[3]
        destination_file = sys.argv[4]

        print("Pakataan...")

        if sys.argv[1] in ["h", "huf", "huffman"]:
            huffman.pack_file(source_file, destination_file)
        elif sys.argv[1] in ["lzw", "lempel-ziv-welch"]:
            lzw.compress_file(source_file, destination_file)
        else:
            get_help()

        print("Pakattu")

        source_size = os.path.getsize(source_file)
        destination_size = os.path.getsize(destination_file)
        print(
            f"Alkuperäisen koko: {source_size} tavua, pakatun koko: {destination_size} tavua, pakkaussuhde: {(destination_size/source_size)*100}%."
        )

    elif sys.argv[2] in ["u", "uncompress", "purku", "pura"]:
        source_file = sys.argv[3]
        destination_file = sys.argv[4]
        print("Puretaan...")

        if sys.argv[1] in ["h", "huf", "huffman"]:
            huffman.unpack_file(source_file, destination_file)
        if sys.argv[1] in ["lzw", "lempel-ziv-welch"]:
            lzw.uncompress_file(source_file, destination_file)
        else:
            get_help()

        print("Purettu")
    else:
        get_help()
