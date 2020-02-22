# Microservice

## Apa ini?
Microservice untuk mendapatkan keypoints dari artikel.

## Base URL
http://13.250.46.91:3000

## API Documentation
---
**POST** `/`

Header: `none`

Body:
```json
{
  "isi_artikel": String
}
```

Response:

**200 OK**

```json
[String]
```

**500 Internal Server Error**
```html
some html page explaining what's wrong...
```
---
**GET** `/`

Header: `none`

Body: `none`

Response:

**200 OK**

```json
hello
```
---
**GET** `/test`

Header: `none`

Body: `none`

Response:

**200 OK**

```json
{
  "result": [
    "Mahfud juga menyebut hal tersebut ancaman terhadap teritori Indonesia.",
    "Pertama, kata dia, ancaman di Laut Natuna Utara atau Laut China Selatan.",
    "Dia pun mengingatkan ancaman China tidak bisa dihadapi dengan adu kekuatan.",
    "Secara hitungan matematis, jika perang fisik dengan China terjadi, dipastikan Indonesia akan kalah.",
    "\"Karena di situ ada klaim dari China yang di dalam konteks hukum internasional itu tidak ada."
  ],
  "url": "https://nasional.kompas.com/read/2020/02/21/13444071/mahfud-ungkap-2-ancaman-kedaulatan-indonesia-berdasarkan-analisis-prabowo"
}
```