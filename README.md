# Pakkaus-tira

Tiralabra 2021 Syksy

## Documentation

Ohjelmaa vaatii Pythonin. Itselläni käytössä on Python 3.9.4. Ohjelma voidaan suorittaa komennolla `python -m pakkaus`.  
Testit voidaan suorittaa komennolla `python -m unittest`. Testikattavuuteen käytetään moduulia pytest-cov, ja tyyppitarkastukseen  
käytetään mypy-moduulia. Koodin laatua voidaan tarkkailla moduulilla pylint, mutta pylint on usein erittäin tarkka, ja kaikki koodi on jo formatoitu black-työkalulla.

Hyvä tapa asentaa molemmat on tehdä uusi virtuaaliympäristö `python -m venv env` ja aktivoida se. (Luultavasti Linux: `source env/bin/activate` ja Windows `env/Scripts/Activate.ps1`) Tämän jälkeen tarvittavat pakkaukset voidaan asentaa komennolla `pip install mypy pytest pylint`
Testikattavuus saadann komennolla `pytest --cov-report term-missing --cov=pakkaus tests/`, laadun tarkastus komennolla `pylint pakkaus` ja tyyppitarkastus komennolla `mypy -m pakkaus`.

- [Määrittelydokumentti](docs/määrittelydokumentti.md)

- [Testausdokumentti](docs/testausdokumentti.md)

- [Toteutusdokumentti](docs/toteutusdokumentti.md)

<!-- - Käyttöohje -->

### Viikkoraportit

- [Viikko 1](docs/vk1_raportti.md)

- [Viikko 2](docs/vk2_raportti.md)

- [Viikko 3](docs/vk3_raportti.md)
