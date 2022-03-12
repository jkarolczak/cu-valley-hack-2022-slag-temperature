# cu-valley-hack-2022

## Inferencja

1. Przygotowanie repozytorium:
    1. Sklonuj to repozytorium (`git clone https://github.com/jkarolczak/cu-valley-hack-2022-slag-temperature.git`)
    2. Przejdź do sklonowanego repozytorium (`cd cu-valley-hack-2022-slag-temperature`)
2. Przygotuj środowisko wykonawcze:
    1. Utwórz środowisko przy użyciu menedźera Conda uruchamiając polecenie `conda env create environment.yaml`
    2. Aktywuj utworzone środowisko wykonując polecenie `conda activate cu-valley-slag`
3. Przygotowanie danych:
    1. Skopiuj archiwum zawierające dane do przeprowadzenia inferencji do
       repozytorium (`mv <path-to-archive.zip> data.zip`)
4. Przeprowadzenie inferencji:
    1. Uruchom polecenie `python scripts/inference_pipeline.py --archive <archive-name.zip>`<br> Jeśli archiwum z danymi
       nazywa się `data.zip`, argument --archive może zostać pominięty, gdyż `data.zip` jest jego domyślną wartością. W
       takim przypadku wystarczy uruchomić polecenie `python scripts/inference_pipeline.py`
    2. Wyniki inferencji znajdują się w pliku `predictions.csv`, który znajduje się w katalogu, w którym obecnie się
       znajdujesz.
