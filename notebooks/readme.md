# 📂 Notebooks Folder Guide

Bu bo'limda loyihada ishlatilgan barcha Jupyter Notebook fayllari
mavzularga bo'lingan holda jamlangan. Quyidagi yo'riqnoma har bir papka
va uning maqsadini tushunishga yordam beradi.

------------------------------------------------------------------------

## 🧩 1. FeatureEngineering/

Bu papkada xususiyatlarni yasash va tanlashga oid ishlanmalar mavjud.

-   **embedded.ipynb** --- Embedded usullar (masalan, Tree-based) orqali
    feature importance aniqlash.
-   **filter.ipynb** --- Korrelatsiya, chi² kabi filter metodlari bilan
    feature selection.
-   **without_fs.ipynb** --- Hech qanday feature selection qilmasdan
    model qurilgan variant.

------------------------------------------------------------------------

## 🧪 2. Multi_Class/

Turli multiclass strategiyalarni sinovdan o'tkazgan notebooklar.

-   **OVO.ipynb** --- One-vs-One strategiyasi bilan multiclass
    classification.
-   **OVR.ipynb** --- One-vs-Rest (One-vs-All) yondashuvi bilan model
    qurish.

------------------------------------------------------------------------

## 🔄 3. OverSampling/

Imbalanced datasetlarni balanslash uchun ishlatilgan metodlar.

-   **smote.ipynb** --- SMOTE yordamida sun'iy namunalar generatsiyasi
    va modelga ta'siri.

------------------------------------------------------------------------

## 🎯 4. Tuning/

Model parametrlari qidiruvi.

-   **bayesian_optimization.ipynb** --- Bayesian Optimization yordamida
    optimal hyperparameter qidirish.
-   **manual_search.ipynb** --- Qo'l bilan parametrlarga asoslangan
    tuning.
-   **random_search.ipynb** --- Random Search yordamida tuning.

------------------------------------------------------------------------

## 📊 5. Analysis/

Ma'lumot, model va xususiyatlarni chuqur tahlil qiluvchi notebooklar.

-   **data_analysis.ipynb** --- Datasetning umumiy statistikasi,
    taqsimotlar, korelyatsiya va vizuallar.
-   **error_analysis.ipynb** --- Model xatolarini tahlil qilish,
    noto'g'ri prediksiyalarni o'rganish.
-   **feature_analysis.ipynb** --- Feature'larning modelga ta'siri,
    muhimlik darajasi, tahliliy graflar.
-   **shap_values.ipynb** --- Model prediksiyalarini SHAP orqali
    izohlash, global va lokal interpretatsiya.

------------------------------------------------------------------------

## ⚙️ 6. base_model_training.ipynb

Modelning boshlang'ich versiyasini train qilish va asosiy natijalarni
olish jarayonlari.

------------------------------------------------------------------------

## 🧪 7. offline_testing.ipynb

Modelni offline tarzda test qilish, prediksiyalar va real natijalar
bilan taqqoslash.

------------------------------------------------------------------------

## 👀 8. show_dataset.ipynb

Datasetni vizual ko'rib chiqish, statistikalar, missing value tahlili va
umumiy struktura.

------------------------------------------------------------------------

Agar kodlar bo'yicha qo'shimcha izoh yoki optimizatsiya kerak bo'lsa ---
bemalol ayt 😉
