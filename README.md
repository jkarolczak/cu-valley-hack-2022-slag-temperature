# cu-valley-hack-2022

## Inferencja

1. Przygotowanie repozytorium:
    1. Sklonuj to
       repozytorium <br> ```git clone https://github.com/jkarolczak/cu-valley-hack-2022-slag-temperature.git```
    2. Przejdź do sklonowanego repozytorium <br> ```cd cu-valley-hack-2022-slag-temperature```
2. Przygotuj środowisko wykonawcze:
    1. Utwórz środowisko przy użyciu menedźera Conda uruchamiając
       polecenie <br>```conda env create -f environment.yml```
    2. Aktywuj utworzone środowisko wykonując polecenie <br>```conda activate cu-valley-slag```
3. Przygotowanie danych:
    1. Skopiuj archiwum zawierające dane do przeprowadzenia inferencji do
       repozytorium <br> ```mv <path-to-archive.zip> data.zip```
4. Przeprowadzenie inferencji:
    1. Uruchom polecenie <br> ```python scripts/inference_pipeline.py --archive <archive-name.zip>``` <br> Jeśli
       archiwum z danymi nazywa się `data.zip`, argument --archive może zostać pominięty, gdyż `data.zip` jest jego
       domyślną wartością. W takim przypadku wystarczy uruchomić
       polecenie <br> ```python scripts/inference_pipeline.py``` <br>
    2. Wyniki inferencji znajdują się w pliku `predictions.csv`, który znajduje się w katalogu, w którym obecnie się
       znajdujesz.

## Panel kontrolny

Aby uruchomić panel kontrolny należy wykonać następujące polecenie:

```
streamlit run app.py
```

Działające demo znajduje się na stronie [miedziaki.tech](http://miedziaki.tech)
Przygotowany mockup imituje panel kontrolny operatora pieca zawiesinowego w KGHM Hucie Miedzi “Głogów II”. Panel ten
pokazuje jak w prosty sposób nasze rozwiązanie może zostać zintegrowane z już istniejącymi oraz wdrożonymi systemami.
Dzięki takiej integracji operatorzy powinni łatwo zaadaptować nowe informacje. Prezentacja czynników wpływających na
predykcję zwraca uwagę operatora na istotne zmiany parametrów procesowych. Co za tym idzie ryzyko błędu ludzkiego jest
znacząco redukowane.

## Trenowanie modelu oraz eksperymentowanie

W celu trenowania modelu oraz eksperymentowania (porównywania modeli, optymalizacji hiperparametrów itp.), w
katalogu `scripts` zostały przygotowane następujące skypty:

- `parse_data.py` - skrypt parsujący dane wejściowe, agregujący je dla odpowieniego okna czasu przy użyciu różnych
  statystyk oraz zapisujący przygotowane dane do pliku
- `variable_selection.py` - skrypt ograniczający liczbę zmiennych w pliku do tych uprzednio zdefiniowanych
- `data_split.py` - skrypt dzielący zbiór danych na zbiory testowy, treningowy oraz holdout
- `train_model.py` - skrypt tworzący oraz trenujący nowy model
- `infer_model.py` - skrypt służący ewaluacji modelu
- `inference_pipeline.py` - skrypt służący przygotowaniu predykcji w sposób kompleksowy, przygotowany na potrzeby
  ewaluacji modelu przez organizatorów hackathonu. Więcej infomracji dostępncyh jest w sekcji powyżej (Inferencja).

Wszystkie skrypty są konfigurowane plikami konfiguracyjnymi, które znajdują się w katalogu `resources/cfg`. Takie
rozwiazanie umożliwia orkiestrację całego procesu eksperymentowania oraz ułatwia proces tworzenia modelu przez
użytkownika.

## Analiza danych

Proces analizy oraz jego rezultaty znajdują się pliku `analysis.ipynb`
