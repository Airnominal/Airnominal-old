# Upravljanje platform

## Registracija platforme

Spletna stran ima nek form, kjer lahko registriraš svojo merilno napravo.
**Request:**

```http
POST /platforms/new
{
    "Podatki o platformi": "Karkoli je pač potrebno (recimo ime, mogoče opis, seznam podprtih senzorjev/meritev...?)"
}
```

```python
#sledi shemi
schema = Schema({
                "name": str,
                "platform": str,
                "sensors": [
                    {
                        "name": str,
                        "mes_type": str,
                    }
                ],
            })
```

**Response:**

```json5
{
    "success": true, // Ker zakaj pa nebi tega poslal?
    "id": "123" // ID nove platforme. Sicer dvomim, da ga bom rabil takoj, ampak za vsak slučaj.
    "key": "0868e3eb4a2353d960b61537b547ba5d" //neki takega tudi
}
HTTP 200 OK
```

V kolikor je šlo kaj narobe, dobiš ta dva responsa

```json5
{
    "success": false,
    "error" : "schema not validated"
}
HTTP 400
```

oz.

```json5
{
    "success": false,
    "error": "Raca measurement type does not exist"
}
HTTP 400
```

v kolirko je measurement type še ne obstaja, se ga da dobiti tako

```json5
POST /platforms/new/type
{
    "name": "weight",
    "unit": "kg"
}
```

kjer je respons potem

```json5
{
    "success": true
}
HTTP 200 OK
```

oziroma

```json5
{
    "success": false,
    "error" : "schema not validated"
}
HTTP 400
```

oziroma

```json5
{
    "success": false,
    "error" : "already exists"
}
```

Erorji bodo tudi na splošno human readable, tko da jih ni treba neki parsat, sam displajat jih je treba.

## Urejanje platforme

Recimo nek `/platforms/edit` pa `/platforms/remove`, samo tega še ni treba zdaj.

# Prikazovanje podatkov

## Step 1: Pridobivanje podatkov o platformah

Spletna stran najprej dobi podatke o vseh registriranih platformah.
Trenutno bom verjetno rabil samo ID pa recimo ime, v prihodnosti pa mogoče tudi kaj drugega.
Glede na to da je varnost prva prioriteta (/s), ni treba nobene avtentikacije in samo vrne podatke o vseh platformah.
**Request:**

```http
GET /platforms
```

**Response:**

```json5
[
    { // Isti podatki, kot pri registraciji, pa še IDji zraven.
        "id": "AAAAAA",
        "name": "Nekaj",
        "description": "Nekaj",
        "...": "..." // Ostale stvari, recimo podprte meritve/senzorji in njihove enote
    }
]
```

## Step 2: Izbiranje vrste prikaza podatkov

Uporabnik se nekako odloči, katere podatke želi gledati. Recimo po lokaciji, posamezni vrsti meritve...
Za zečetek pa lahko rečemo, da gleda vse podatke iz vseh naprav.

## Step 3: Pridobivanje podatkov

Spletna stran vsakih `n` sekund naredi request na API za pridobivanje podatkov.
Ob prvem requestu izpusti `from` parameter, tako da dobi vse podatke za nazaj, ob vsakem naslednjem requestu pa `from` nastavi na čas prejšnjega.
Ostalih parametrov trenutno še ne bom rabil, ampak bi bilo fino, če so implementirani za prihodnost.
**Request:**

```http
GET /measurements?platform=AAAAAA,BBBBBB&measurements=temperature,humidity,pm10,nox&from=2022-02-24T14:00:20&to=2022-02-24T14:00:30
```

- `platform`: ID posamezne merilne naprave/platforme/Arduina (karkoli pač temu rečemo). Lahko jih je več, en alpa noben. Če ID ni podan, vrne meritve od vseh platform, ki jih ima.

- `measurements`: Katere tipe meritve želi dobiti (temperature, humidity, pm10, nox ...). Lahko jih je več, en alpa noben. Če ni podan, vrne vse meritve, ki jih ima.

- `from`: Od kdaj naprej naj bodo meritve, v ISO formatu (datetime.fromisoformat). Če ni podan, vrne vse, kar ima.

- `to`: Do kdaj naj bodo meritve, isto ISO format. Če ni podan, vrne vse, kar ima.
  **Response:**
  
  ```json5
  [ // Seznam vseh meritev/skupin meritev, ki ustrezajo pogojem iz requesta
    {
        "hash": "AAAAAAAAAAAAAAAA", // Nek hash meritve, da lahko ugotovim če je slučajno kaj podvojenega. Kaj točno hashat se ti odloči, samo vsak ta objekt mora met svoj hash.
        "timestamp": "2022-02-24T14:06:29.789987", // Tisto kar dobiš v Pythonu z datetime.isoformat() - https://docs.python.org/3/library/datetime.html#datetime.datetime.isoformat
        "platform": "AAAAA", // ID platforme. Pač ista stvar kot v requestu.
        "coordinates": [12.345, 54.321], // Trenutna lokacija platforme, če jo je treba met.
        "data": { // Dejanske meritve
            "name": "temperature",
            "unit": "°C",
            "value": 20,
        }
    }
  ]
  ```
  
  ## Step 4: Shranjevanje in prikazovanje podatkov
  
  Iz pridobljenih podatkov odstrani vse podvojene (če bi slučajno večkrat naredil isti request ali pa kaj takega), jih shrani (verjetno v `localStorage`) in jih prikaže na grafih.d
  
  # Pošiljanje podatkov iz arduina
  
  ```json5
  {
      "k": "aRKJDFNA23546" //key, po nove v base 64 da vzame manj placa
      "iST": "H3" // id Station, zapisano v base 64 da vzame manj placa
      "iSE": "T4" // id Senzorja, spet v base 64
      "v": 33.2 // value, kjer postaja je
      "lat": 56.4 // latitude
      "lon" : 33.6 // longitude
      "uT" : 15982374592873 // unixTime epcho
  }
  ```
