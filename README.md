# 🛡️ Predicting CVE Type and CVSS Score

## 🧾 Project haqida

- bu dunyodagi dasturiy ta’minot va tizimlardagi zaifliklar ro‘yxati. Har bir CVE — bu ma’lum bir xavfsizlik kamchiligi yoki zaiflikni ifodalaydi.
- CVE datasetidagi turli atributlardan foydalangan holda `type` va `cvss_score` predict qilish.  
- Maqsad — multi-output classification model yordamida zaiflik turlarini va ularning xavf darajasini aniqlash.

* **Type:** Multi-Output Classification  
* **Target:** `type` va `cvss_score`  


## Loyihaning foydaliligi
- Cybersecurity mutaxassislari: zaifliklarni tez aniqlash va ularni tuzatish.
- Developerlar va IT companylar: uz dasturlarida mavjud xavfli zaifliklarni aniqlash va ularni oldindan tuzatish.

---

## 📊 Data Extraction

Loyihaning asosiy malumotlari NVDning rasmiy **CVE JSON Feed 2.0** manbasidan real-time tarzda yigib olindi.

2023–2025 yillar buyicha barcha feedlar tuliq parse qilinib, yakuniy dataset 102,963 ta CVE yozuvdan iborat buldi.

- URL: [NVD CVE JSON Feed](https://nvd.nist.gov/feeds/json/cve/2.0/)  
- Year: 2023, 2024, 2025  
- Dataset: 102,963   
- Features: `cve_id`, `description`, `cvss_score`, `cwe`, `vendor`, `product`, `publish_date`, `type`  

### 🧹 Data 


- Boshlanishida raw dataset juda notekis va kup redundant malumotlarga ega edi.  
- Data cleaning qilindi: Unnecessary columns olib tashlandi, text normalization amalga oshirildi.  
- Barcha yillardagi datasetlar birlashtirildi (merge qilindi), va model training uchun tayyor holatga keltirildi.

---

## ⚡ Base Model Training Comparison

Boshlangich natijalar (feature engineering, SMOTE/oversampling va hyperparameter tuning qilinmagan holat):

| Algorithm          | Type Acc | K-Fold Mean | K-Fold Std | cvss_score Acc | K-Fold Mean | K-Fold Std | Combined |
|--------------------|----------|-------------|------------|----------------|-------------|------------|----------|
| Bagging            | 0.87     | 0.78        | 0.01       | 0.62           | 0.52        | 0.01       | 0.75     |
| Bagged DT          | 0.87     | 0.78        | 0.01       | 0.62           | 0.52        | 0.01       | 0.75     |
| Stacking           | 0.84     | 0.70        | 0.01       | 0.64           | 0.49        | 0.01       | 0.74     |
| RandomForest       | 0.84     | 0.67        | 0.01       | 0.63           | 0.50        | 0.01       | 0.73     |
| GradientBoosting   | 0.85     | 0.76        | 0.01       | 0.60           | 0.42        | 0.01       | 0.72     |

## 🚀 Final Model Training

Keyin preprocessing, feature engineering, tuning, feature selection va SMOTE/oversampling ishlari amalga oshirildi,  
lekin natijalar **without tuning, without SMOTE, without feature selection** kursatildi.  

Keyin, shu optimization qilingan datasetni train qilish qaror qilindi va eng yaxshi natija **GradientBoosting** modeli bilan olindi.  

Natijalar:

## 🔧 Feature Engineering 

| Feature name                   | Type       | Description                                                                 |
|--------------------------------|------------|-----------------------------------------------------------------------------|
| cve_id                         | categorical| CVE identifikatori                                                          |
| description                    | categorical| Zaiflik tavsifi va xujum stsenariysi                                        |
| cvss_score                     | numerical  | CVE xavf darajasi (Common Vulnerability Scoring System)                     |
| cwe                            | categorical| CVE turining CWE kodi (Common Weakness Enumeration)                         |
| vendor                         | categorical| Zaiflik mavjud bo‘lgan kompaniya/vendor nomi                                |
| product                        | categorical| Zaiflik mavjud bo‘lgan mahsulot nomi                                        |
| publish_date                   | categorical| CVE e'lon qilingan sana                                                     |
| type                           | categorical| Zaiflik turi (XSS, DoS, RCE, Other, …)                                      |
| vendor_freq                    | numerical  | Vendor appearance frequency (datasetdagi chastota)                          |
| product_freq                   | numerical  | Product appearance frequency                                                |
| desc_len                       | numerical  | Description uzunligi (character count)                                      |
| desc_word_count                | numerical  | Descriptiondagi so‘zlar soni                                                |
| desc_num_count                 | numerical  | Descriptiondagi raqamlar soni                                               |
| desc_upper_ratio               | numerical  | Descriptiondagi katta harflar foizi                                         |
| desc_exclamation               | numerical  | Descriptiondagi `!` belgilar soni                                           |
| desc_question                  | numerical  | Descriptiondagi `?` belgilar soni                                           |
| vendor_product_interaction     | numerical  | Vendor va product o‘rtasidagi interaction score                             |
| XSS_score                      | numerical  | XSS vulnerability ehtimoli                                                  |
| SQLi_score                     | numerical  | SQL Injection ehtimoli                                                      |
| RCE_score                      | numerical  | Remote Code Execution ehtimoli                                              |
| DoS_score                      | numerical  | Denial of Service ehtimoli                                                  |
| CSRF_score                     | numerical  | Cross-Site Request Forgery ehtimoli                                         |
| AuthBypass_score               | numerical  | Authentication Bypass ehtimoli                                              |
| PrivEsc_score                  | numerical  | Privilege Escalation ehtimoli                                               |
| PathTraversal_score            | numerical  | Path Traversal ehtimoli                                                     |
| SSRF_score                     | numerical  | Server-Side Request Forgery ehtimoli                                        |
| InfoDisclosure_score           | numerical  | Information Disclosure ehtimoli                                             |
| Other_score                    | numerical  | Boshqa turdagi zaiflik ehtimoli                                             |
| cvss_keywords_score            | numerical  | Description matni asosida CVSS score ehtimoli                               |

---
