# Prediksi Jumlah Pelanggan Rental Sepeda

## Latar Belakang
### Tren Bersepeda
Sepeda memang beberapa tahun terakhir sudah menjadi tren di Indonesia sejak program Bike To Work. Tetapi belakangan ini saat era New Normal diberlakukan bersepeda menjadi salah satu olahraga yang digemari oleh semua kalangan. Sebelum era New Normal sepeda hanya digandrungi oleh komunitas atau kelompok sepeda, tetapi sekarang hampir semua kalangan melakukan olahraga bersepeda. Bahkan di era New Normal jumlah pesepeda mengalami peningkatan yang cukup signifikan dibandingkan saat New Normal belum diterapkan.
### Faktor Meningkatnya Jumlah Pesepeda Saat New Normal
- Khawatir jika menggunakan transportasi umum.
- Pembatasan kendaraan baik umum atau pribadi.
- Mulai sadar akan pentingnya olahraga untuk menginkatkan imunitas tubuh.
- Olahraga yang tidak kontak langsung dengan orang lain.
- Bertepatan dengan musim kemarau.
- Semakin banyaknya ruas jalur khusus pesepeda. 
- Ingin mengikuti tren saat ini.
### Akibat Meningkatnya Jumlah Pesepeda Saat New Normal
Akibat dari  meningkatknya jumlah orang yang bersepeda harga sepeda naik hampir 2x dari harga biasanya bahkan harga sepeda bekas pun harga jualnya lebih mahal dari pada saat sepeda tersebut pertama dibeli. Selain itu stok sepeda di toko-toko pun mulai kehabisan hingga kita harus memesan terlebih dahulu jika ingin membeli sepeda. Karena hal-hal tersebut tentunya tidak semua orang bisa membeli sepeda, namun karena ingin mengikuti tren banyak yang ingin tetap bersepeda, tetapi bagaimana caranya? Tentunya dengan cara rental sepeda.
### Bisnis Rental Sepeda
Bisnis rental sepeda merupakan jasa untuk peminjaman sepeda kepada perorangan atau kelompok, dan biasanya disewakan dalam hitungan per jam atau bahkan per hari. Makin maraknya pesepeda pada era New Normal seperti saat ini, bisnis rental sepeda menjadi salah satu bisnis yang mulai dilirik. Bahkan penyedia jasa wisata, tempat wisata dan Event Organizer mulai melirik bisnis rental sepeda karena potensi bisnis dikala tren sepeda saat ini. Pelaku bisnis yang sudah menjalankan bisnis rental sepeda bahkan mengaku slot penyewaan sepeda selalu penuh bahkan harus booking terlebih dahulu agar mendapat antrian. Tentunya hal tersebut cukup disayangkan karena bisa jadi orang pindah tempat penyewaan dan kita tidak dapat memperoleh keuntungan yang maksimal. Selain itu para pelaku bisnis rental sepeda pun ingin armada yang tersedia dapat dimanfaatkan secara maksimal atau terpakai seluruhnya.
### Problem
Bagaimana cara menentukkan atau memprediksi berapa jumlah pelanggan yang akan melakukan penyewaan sepeda agar dapat menentukkan jumlah sepeda yang akan dikerahkan atau dapat memaksimalkan jumlah sepeda yang dikerahkan agar memperoleh keuntungan yang maksimal?
### Goals
Dapat memprediksi atau menentukkan jumlah pelanggan yang akan menggunakan jasa rental sepeda untuk dapat menentukkan jumlah sepeda yang dikerahkan agar jumlah sepeda yang dikerahkan tidak kekurangan dan dapat memaksimalkan jumlah sepeda yang ada agar memperoleh keuntungan yang maksimal.

Data yang digunakan didapatkan atau diperoleh dari Kaggle bisa klik [di sini](https://www.kaggle.com/hmavrodiev/london-bike-sharing-dataset).

## Data Pre-Processing
- Melakukan pengecekan data apakah terdapat data yang masih bernilai Nan atau tidak.
- Mengubah atau membagi waktu menjadi tahun, bulan, tanggal, hari, dan jam untuk membantu dalam data analisis dan pembuatan model.
- Describe data untuk melihat nilai maksimal, minimal dan lain-lain pada setiap kolom.

## Exploratory Data Analysis
Pada EDA ini dilakukan data analisis pada data untuk melihat pengaruh dan korelasi dari setiap kolom pada kolom target yaitu jumlah pelanggan rental sepeda untuk membantu nantinya saat pembuatan model, selain itu juga untuk mendapatkan intisari dari data tersebut untuk memberi masukkan pada pelaku bisnis rental sepeda agar dapat memperoleh keuntungan yang maksimal.

## Handling Outlier
Dilakukan pengecekan pada data apakah terdapat outlier atau tidak dan apakah outlier tersebut akan digunakan atau tidak. Dalam kasus ini kita tetap akan menggunakan outlier tersebut untuk pembuatan model karena tujuan dari Final Project ini adalah untuk memperoleh kuntungan yang maksimal.

## Machine Learning Model
Selanjutnya dari data yang sebelumnya telah dilakukan _feature engeneering_ dan _feature selection_ akan dibuatkan model dengan membandingkan algoritma mana yang terbaik. Algoritma yang digunakan adalah _Linear Regression_, _ElasticNet_, _Random Forest Regressor_, dan _XGBoost Regressor_. Dari keempat algoritma tersebut diperoleh MAE, MSE, RMSE, dan R square sebagai berikut:

*| **Linear Regression** | **ElasticNet** | **Random Forest Regressor** | **XGBoost Regressor** 
------|------|------|------|------
**MAE**|501.413|609.363|338.262|341.404
**MSE**|511689.122|719971.162|339097.414|323570.247
**RMSE**|715.324|848.511|582.32|568.832
**R square**|0.599|0.437|0.734|0.747

Algoritma terbaik dengan parameter default adalah _XGBoost Regressor_. Selanjutnya dilakukan _hyper parameter tunning_ untuk memperoleh model yang lebih baik.

### Hyper Parameter Tunning
Algoirtma yang akan dilakukan _hyper parameter tunning_ adalah _ElasticNet_, _Random Forest Regressor_, dan _XGBoost Regressor_ dengan parameter yang akan ditunning sebagai berikut:
- _ElasticNet_
```python
paramsE = {
            "alpha": [1,0.1,0.01,0.001],
            "l1_ratio" : [0.1,0.3,0.5,0.7,0.9]
             }
```
- _Random Forest Regressor_
```python
paramsRF = {
            "n_estimators" : [100,120,140,160,180,200],
            "min_samples_split": np.arange(2,16,2),
            "min_samples_leaf": [1,3,5,7],
            "max_depth": ['None',8,9,10,11,12,13,14],
            "max_features":['auto',0.2,0.4,0.5,0.8]
             }
```
- _XGBoost Regressor_
```python
paramsX = {
            'max_depth': np.arange(1,7,1),
            'learning_rate': [0.001,0.01,0.1,0.3,0.5,0.7,0.9],
            'n_estimators': [100,120,140,160,180,200],
            'subsample': [0.2,0.4,0.6,0.8,1],
            'gamma': np.arange(0,10,2),
            'colsample_bytree': [0.2,0.4,0.6,0.8,1],
            'reg_alpha': np.logspace(-3,0,15),
            'reg_lambda': np.logspace(-3,0,15)
            }
```
Diperoleh MAE, MSE, RMSE, dan R square sebagai berikut:

*| **ElasticNet** | **Random Forest Regressor** | **XGBoost Regressor** 
------|------|------|------
**MAE**|501.299|323.014|322.7
**MSE**|511619.969|299387.766|295982.403
**RMSE**|715.276|547.163|544.042
**R square**|0.599|0.765|0.768


## Kesimpulan
Untuk memprediksi berapa jumlah pelanggan yang akan menyewa sepeda model yang terbaik adalah dengan menggunakan _XGBoost Regressor_ karena memiliki R square tertinggi dan memiliki MAE, MSE, dan RMSE terendah. Diharapkan dengan menggunakan model yang telah dibuat ini dapat membantu pelaku bisnis rental sepeda dalam memprediksi berapa jumlah pelanggan sepeda yang akan melakukan penyewaan agar dapat menentukkan jumlah sepeda yang akan dikerahkan, menentukkan harga, dan apakah sepeda yang tersedia akan terpakai secara maksimal atau tidak untuk memperoleh keuntungan yang maksimal.