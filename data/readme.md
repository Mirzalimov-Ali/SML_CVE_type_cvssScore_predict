# 📁 Data Folder Structure Guide

Quyida `data/` papkasidagi barcha bo'limlar va ularning vazifalari
chiroyli va tushunarli tarzda yoritilgan. Har bir qadam --- xom
ma'lumotdan to to'liq tayyor engineered datasetgacha bo'lgan jarayonni
aks ettiradi.

------------------------------------------------------------------------

## 🧪 1. engineering/

Model uchun yakuniy ishlov berilgan (engineered) dataset versiyasi.

-   **engineered_dataset.ipynb**\
    Feature engineering jarayonlari: yangi feature yasash, eskilarni
    o'zgartirish, normalizatsiya, encoding va boshqa ishlanmalar.

------------------------------------------------------------------------

## 🧩 2. filled/

Missing value'lar to'ldirilgan datasetlar.

-   **filled_dataset.ipynb**\
    NaN qiymatlarni to'g'rilash strategiyalari (mean, median, KNN
    imputer, model-based imputation va boshqalar).

------------------------------------------------------------------------

## 🛠️ 3. preprocessed/

Modelga berilishidan oldingi to'liq tayyorlangan datasetlar.

-   **preprocessed_dataset.ipynb**\
    Encoding, scaling, outlier removal, balancing kabi preprocess
    jarayonlari.

------------------------------------------------------------------------

## 🗂️ 4. raw/

Xom ma'lumotlar va ularga ishlov berilgan oraliq bosqichlar.

### 🔹 cleaned/

Tozalangan datasetlar (duplicate removal, formatting, unnecessary
columns removal, incorrect records cleanup).

-   **cleaned_cve_2023_dataset.csv**\
-   **cleaned_cve_2024_dataset.csv**\
-   **cleaned_cve_2025_dataset.csv**

### 🔹 extracted/

Original manbalardan to'g'ridan-to'g'ri olingan datasetlar (hali
tozalanmagan versiya).

-   **cve_2023_dataset.csv**\
-   **cve_2024_dataset.csv**\
-   **cve_2025_dataset.csv**

### 🔹 merged/

Yil bo'yicha datasetlar birlashtirilgan to'liq umumiy versiya.

-   **merged_dataset.csv**

------------------------------------------------------------------------

Agar istasang, shu bo'limni umumiy **project README** ichiga qo'shib
chiqib ham beraman 😉\
Yoki folder architecture diagrammasini grafik ko'rinishda ham chizib
berishim mumkin!
