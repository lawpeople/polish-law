#!/usr/bin/env python3

import argparse
import re
import sys

replacements = {
    "-\n": "",
    '"Art': "Art",
    "<": "c",
    ". *": ".",
    "'": "",
    "*/,": "%",
    "l-ym": "1-ym",
    "iub": "lub",
    "urzęlowy": "urzędowy",
    "[zby": "Izby",
    "(lrzędnik": "Urzędnik",
    "(rzędnik": "Urzędnik",
    "(irzędnik": "Urzędnik",
    "(lrzędów": "Urzędów",
    "Ulrzędy": "Urzędy",
    "Ulrzędom": "Urzędom",
    "Ulrzędów": "Urzędów",
    "Ulrzędach": "Urzędach",
    "Połskiemu": "Polskiemu",
    "TYTGŁ": "TYTUŁ",
    "Art..": "Art. ",
    "orzeczenie": "orzeczenie",
    " łub ": " lub ",
    "ewentualnegc": "ewentualnego",
    "saniej": "samej",
    "wożźnych": "woźnych",
    "(lrz.": "Urz.",
    "(lrzędami": "Urzędami",
    "(lstawy": "Ustawy",
    "Regen<yjna": "Regencyjna",
    "Przzes": "Prezes",
    "prżez": "przez",
    "Presze": "Prezes",
    "Żiemskich": "Ziemskich",
    "jeśłi": "jeśli",
    "chwiii": "chwili",
    "chwiłi": "chwili",
    "jlości": "ilości",
    "llość": "Ilość",
    "siużby": "służby",
    "koinisja": "komisja",
    ". (l": ". U",
    "ałbo": "albo",
    "sivój": "swój",
    "kraowej": "krajowej",
    "obewiązku": "obowiązku",
    "lstniejący": "Istniejący",
    "Alcksander": "Aleksander",
    "Kakpwski": "Kakowski",
    "£nglich": "Englich",
    "posedanie": "posiadanie",
    "kiłku": "kilku",
    "uchyłone": "uchylone",
    "płastycznych": "plastycznych",
    "kołumny": "kolumny",
    "podłega": "podlega",
    "spcsób": "sposób",
    "Mnistra": "Ministra",
    "zajrożonego": "zagrożonego",
    "przeciko": "przeciwko",
    "zarząau": "zarządu",
    "uehwali": "uchwali",
    "ucrnwalony": "uchwalony",
    "Ulstawodawczego": "Ustawodawczego",
    "listawodawczego": "Ustawodawczego",
    "(lstawodawczego": "Ustawodawczego",
    "drożyżniany": "drożyźniany",
    "łączmie": "łącznie",
    "głósowania": "głosowania",
    "podsektetarzy": "podsekretarzy",
    "oktegu": "okręgu",
    "ogloszenia": "ogłoszenia",
    "egłoszenia": "ogłoszenia",
    "bądzie": "będzie",
    "urzęcowania": "urzędowania",
    "urzędowenia": "urzędowania",
    "rozporzadzeń": "rozporządzeń",
    "wewnetrznych": "wewnętrznych",
    "zawiacomienia": "zawiadomienia",
    "kontrołą": "kontrolą",
    "członkow": "członków",
    "czionków": "członków",
    "członkówie": "członkowie",
    "rażie": "razie",
    "Rekląmacje": "Reklamacje",
    "mieiscowej": "miejscowej",
    "pismiennie": "piśmiennie",
    "póżniej": "później",
    " byc ": " być ",
    "kandyddtów": "kandydatów",
    "protokwłu": "protokułu",
    "lokału": "lokalu",
    "lokaiu": "lokalu",
    "wydałić": "wydalić",
    "płacu": "placu",
    "giosowania": "głosowania",
    "głósowania": "głosowania",
    "okołiczności": "okoliczności",
    "oddała": "oddala",
    "główmą": "główną",
    "obywateł": "obywatel",
    "pogwałcenią": "pogwałcenia",
    "Hajwyższy": "Najwyższy",
    "Majwyższy": "Najwyższy",
    "Członkcwie": "Członkowie",
    "uwolnienłe": "uwolnienie",
    "Krółestwa": "Królestwa",
    "wzgiędna": "względna",
    "połeca": "poleca",
    "cełu": "celu",
    "wogóla": "wogóle",
    "personeł": "personel",
    "tyłko": "tylko",
    "potskich": "polskich",
    "połskich": "polskich",
    "wołno": "wolno",
    "sima": "sama",
    "dałsze": "dalsze",
    "gininom": "gminom",
    "naieżna": "należna",
    "poiera": "pobiera",
    "wriosek": "wniosek",
    "przysłaguje": "przysługuje",
    "sprawiedliwaści": "sprawiedliwości",
    "wykształcemiem": "wykształceniem",
    "przedstawicieł": "przedstawiciel",
    "Powiaowy": "Powiatowy",
    "Rozdzielczęgo": "Rozdzielczego",
    "posiadafą": "posiadają",
    "Milicjj": "Milicji",
    "Gchyla": "Uchyla",
    "dałej": "dalej",
    "ułegnie": "ulegnie",
    "(lrzędowego": "Urzędowego",
    "właściwosci": "właściwości",
    "swoicn": "swoich",
    "kusztach": "kosztach",
    "Ulstawy": "Ustawy",
    "Thuguit": "Thugutt",
    "Thugult": "Thugutt",
    "Pilsudski": "Piłsudski",
    "lzby": "Izby",
    "dnią": "dnia",
    "$$": "§§",
    " Ne ": " № ",
    "\x0c": "",
}

FIRST_PAGE_STARTS = [
    "Rada Regencyjna do Narodu Polskiego",
    "Do Naczelnego Dowódcy Wojsk Polskich",
    "DEKRET",
    "USTAWA",
    "ROZPORZĄDZENIE",
    "Przepisy",
]


def print_refined_ocr(is_first_page: bool) -> None:
    output_lines: list[str] = []
    # Fix most frequent mistakes in the OCR-ed line
    for line in sys.stdin:
        for bad, good in replacements.items():
            line = line.replace(bad, good)
        output_lines.append(line)

    output = ""
    # First page
    if is_first_page:
        content_started = False
        for line in output_lines:
            if any([p in line for p in FIRST_PAGE_STARTS]):
                content_started = True

            if content_started:
                output += line
    else:
        content_started = False
        whitespace_started = False
        for line in output_lines:
            if not content_started and line == "\n":
                whitespace_started = True

            if not content_started and whitespace_started and line != "\n":
                content_started = True
                line = line.lstrip()

            if content_started:
                output += line

    output = re.sub(
        r"\n(?:rt|Ft|Fert|Firt|Hrt|Prt|Rrt|Frt)\.? ?(\d+)", r"\nArt. \1", output
    )
    output = re.sub(r"\n© ", r"\no ", output)
    output = re.sub(r"\n©\) ", r"\nc) ", output)
    output = re.sub(r",{2,}", r",", output)
    output = re.sub(r"([\w,\.]+)\n([\w ]{2,})", r"\1 \2", output)
    output = re.sub(r"Art. (\d)\d ", r"Art. \1. ", output)
    output = re.sub(r"Art. (\d+)[\.,]+", r"Art. \1.", output)
    output = re.sub(r"! ([a-z])", r" \1", output)
    output = re.sub(r"(\d) 1 (\d)", r"\1 i \2", output)
    output = re.sub(r"\n(\d)([\.\)])", r"\n\1\2", output)
    output = re.sub(r"\w? ?Aleksander Kakowski", "† Aleksander Kakowski", output)
    output = re.sub(r"\n{3,}", r"\n\n", output)
    # Provide proper markdown whitespacing
    output = output.strip()
    output = (
        output.replace("\n\n", "EOPAR").replace("\n", "  \n").replace("EOPAR", "\n\n")
    )

    print(output, end="")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Refine OCR result")
    parser.add_argument("--first-page", action="store_true")
    args = parser.parse_args()
    print_refined_ocr(is_first_page=args.first_page)
