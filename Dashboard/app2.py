# Flask : library utama untuk membuat API
# render_template : agar dapat memberikan respon file html
# request : untuk membaca data yang diterima saat request datang
from flask import Flask, render_template, request
# plotly dan plotly.graph_objs : membuat plot
import plotly
import plotly.graph_objs as go
# pandas : untuk membaca csv dan men-generate dataframe
import pandas as pd
import json
from sqlalchemy import create_engine
import pickle
import pandas as pd

# untuk membuat route
app = Flask(__name__)

###################
## CATEGORY PLOT ##
###################

## IMPORT DATA USING pd.read_csv
df = pd.read_csv('df_clean.csv')



# category plot function
def category_plot(
    cat_plot = 'histplot',
    cat_x = 'is_holiday', cat_y = 'cnt',
    estimator = 'avg', hue = 'weather_code'):

    # generate dataframe tips.csv
    df = pd.read_csv('df_clean.csv')



    # jika menu yang dipilih adalah histogram
    if cat_plot == 'histplot':
        # siapkan list kosong untuk menampung konfigurasi hist
        data = []
        # generate config histogram dengan mengatur sumbu x dan sumbu y
        for val in df[hue].unique():
            hist = go.Histogram(
                x=df[df[hue]==val][cat_x],
                y=df[df[hue]==val][cat_y],
                histfunc=estimator,
                name=val
            )
            #masukkan ke dalam array
            data.append(hist)
        #tentukan title dari plot yang akan ditampilkan
        title='Histogram'
    elif cat_plot == 'boxplot':
        data = []

        for val in df[hue].unique():
            box = go.Box(
                x=df[df[hue] == val][cat_x], #series
                y=df[df[hue] == val][cat_y],
                name = val
            )
            data.append(box)
        title='Box'
    # menyiapkan config layout tempat plot akan ditampilkan
    # menentukan nama sumbu x dan sumbu y
    if cat_plot == 'histplot':
        layout = go.Layout(
            title=title,
            xaxis=dict(title=cat_x),
            yaxis=dict(title='jumlah'),
            # boxmode group digunakan berfungsi untuk mengelompokkan box berdasarkan hue
            boxmode = 'group'
        )
    else:
        layout = go.Layout(
            title=title,
            xaxis=dict(title=cat_x),
            yaxis=dict(title=cat_y),
            # boxmode group digunakan berfungsi untuk mengelompokkan box berdasarkan hue
            boxmode = 'group'
        )
    #simpan config plot dan layout pada dictionary
    result = {'data': data, 'layout': layout}

    #json.dumps akan mengenerate plot dan menyimpan hasilnya pada graphjson
    graphJSON = json.dumps(result, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

# akses halaman menuju route '/' untuk men-test
# apakah API sudah running atau belum
@app.route('/')
def index():

    plot = category_plot()
    # dropdown menu
    # kita lihat pada halaman dashboard terdapat menu dropdown
    # terdapat lima menu dropdown, sehingga kita mengirimkan kelima variable di bawah ini
    # kita mengirimnya dalam bentuk list agar mudah mengolahnya di halaman html menggunakan looping
    list_plot = [('histplot', 'Histogram'), ('boxplot', 'Box')]
    list_x = [('is_holiday', 'Is_holiday'), ('is_weekend', 'Is_weekend'), ('season', 'Season'), ('Hari', 'Hari'),('weather_code', 'Weather_code')]
    list_y = [('cnt', 'cnt')]
    list_est = [('avg', 'Average'),('count', 'Count'),  ('max', 'Max'), ('min', 'Min')]
    list_hue = [('is_holiday', 'Is_holiday'), ('is_weekend', 'Is_weekend'), ('season', 'Season'), ('Hari', 'Hari'),('weather_code', 'Weather_code')]

    return render_template(
        # file yang akan menjadi response dari API
        'category.html',
        # plot yang akan ditampilkan
        plot=plot,
        # menu yang akan tampil di dropdown 'Jenis Plot'
        focus_plot='histplot',
        # menu yang akan muncul di dropdown 'sumbu X'
        focus_x='is_holiday',

        # untuk sumbu Y tidak ada, nantinya menu dropdown Y akan di disable
        # karena pada histogram, sumbu Y akan menunjukkan kuantitas data

        # menu yang akan muncul di dropdown 'Estimator'
        focus_estimator='cnt',
        # menu yang akan tampil di dropdown 'Hue'
        focus_hue='weather_code',
        # list yang akan digunakan looping untuk membuat dropdown 'Jenis Plot'
        drop_plot= list_plot,
        # list yang akan digunakan looping untuk membuat dropdown 'Sumbu X'
        drop_x= list_x,
        # list yang akan digunakan looping untuk membuat dropdown 'Sumbu Y'
        drop_y= list_y,
        # list yang akan digunakan looping untuk membuat dropdown 'Estimator'
        drop_estimator= list_est,
        # list yang akan digunakan looping untuk membuat dropdown 'Hue'
        drop_hue= list_hue)

# ada dua kondisi di mana kita akan melakukan request terhadap route ini
# pertama saat klik menu tab (Histogram & Box)
# kedua saat mengirim form (saat merubah salah satu dropdown) 
@app.route('/cat_fn/<nav>')
def cat_fn(nav):

    # saat klik menu navigasi
    if nav == 'True':
        cat_plot = 'histplot'
        cat_x = 'is_holiday'
        cat_y = 'cnt'
        estimator = 'avg'
        hue = 'weather_code'
    
    # saat memilih value dari form
    else:
        cat_plot = request.args.get('cat_plot')
        cat_x = request.args.get('cat_x')
        cat_y = request.args.get('cat_y')
        estimator = request.args.get('estimator')
        hue = request.args.get('hue')

    # Dari boxplot ke histogram akan None
    if estimator == None:
        estimator = 'avg'
    
    # Saat estimator == 'count', dropdown menu sumbu Y menjadi disabled dan memberikan nilai None
    if cat_y == None:
        cat_y = 'cnt'

    # Dropdown menu
    list_plot = [('histplot', 'Histogram'), ('boxplot', 'Box')]
    list_x = [('is_holiday', 'Is_holiday'), ('is_weekend', 'Is_weekend'), ('season', 'Season'), ('Hari', 'Hari'),('weather_code', 'Weather_code')]
    list_y = [('cnt', 'cnt')]
    list_est = [ ('avg', 'Average'), ('count', 'Count'), ('max', 'Max'), ('min', 'Min')]
    list_hue = [('is_holiday', 'Is_holiday'), ('is_weekend', 'Is_weekend'), ('season', 'Season'), ('Hari', 'Hari'),('weather_code', 'Weather_code')]

    plot = category_plot(cat_plot, cat_x, cat_y, estimator, hue)
    return render_template(
        # file yang akan menjadi response dari API
        'category.html',
        # plot yang akan ditampilkan
        plot=plot,
        # menu yang akan tampil di dropdown 'Jenis Plot'
        focus_plot=cat_plot,
        # menu yang akan muncul di dropdown 'sumbu X'
        focus_x=cat_x,
        focus_y=cat_y,

        # menu yang akan muncul di dropdown 'Estimator'
        focus_estimator=estimator,
        # menu yang akan tampil di dropdown 'Hue'
        focus_hue=hue,
        # list yang akan digunakan looping untuk membuat dropdown 'Jenis Plot'
        drop_plot= list_plot,
        # list yang akan digunakan looping untuk membuat dropdown 'Sumbu X'
        drop_x= list_x,
        # list yang akan digunakan looping untuk membuat dropdown 'Sumbu Y'
        drop_y= list_y,
        # list yang akan digunakan looping untuk membuat dropdown 'Estimator'
        drop_estimator= list_est,
        # list yang akan digunakan looping untuk membuat dropdown 'Hue'
        drop_hue= list_hue
    )

##################
## SCATTER PLOT ##
##################

# scatter plot function
def scatter_plot(cat_x, cat_y, hue):


    data = []

    for val in df[hue].unique():
        scatt = go.Scatter(
            x = df[df[hue] == val][cat_x],
            y = df[df[hue] == val][cat_y],
            mode = 'markers',
            name = val
        )
        data.append(scatt)

    layout = go.Layout(
        title= 'Scatter',
        title_x= 0.5,
        xaxis=dict(title=cat_x),
        yaxis=dict(title=cat_y)
    )

    result = {"data": data, "layout": layout}

    graphJSON = json.dumps(result,cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

@app.route('/scatt_fn')
def scatt_fn():
    cat_x = request.args.get('cat_x')
    cat_y = request.args.get('cat_y')
    hue = request.args.get('hue')

    # WAJIB! default value ketika scatter pertama kali dipanggil
    if cat_x == None and cat_y == None and hue == None:
        cat_x = 't1'
        cat_y = 'cnt'
        hue = 'is_holiday'

    # Dropdown menu
    list_x = [('t1', 't1'), ('hum', 'hum'), ('wind_speed', 'wind_speed')]
    list_y = [('cnt', 'cnt')]
    list_hue = [('is_holiday', 'is_holiday'), ('is_weekend', 'is_weekend')]

    plot = scatter_plot(cat_x, cat_y, hue)

    return render_template(
        'scatter.html',
        plot=plot,
        focus_x=cat_x,
        focus_y=cat_y,
        focus_hue=hue,
        drop_x= list_x,
        drop_y= list_y,
        drop_hue= list_hue
    )

##############
## PIE PLOT ##
##############

def pie_plot(hue = 'is_holiday'):
    


    vcounts = df[hue].value_counts()

    labels = []
    values = []

    for item in vcounts.iteritems():
        labels.append(item[0])
        values.append(item[1])
    
    data = [
        go.Pie(
            labels=labels,
            values=values
        )
    ]

    layout = go.Layout(title='Pie', title_x= 0.48)

    result = {'data': data, 'layout': layout}

    graphJSON = json.dumps(result,cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

@app.route('/pie_fn')
def pie_fn():
    hue = request.args.get('hue')

    if hue == None:
        hue = 'is_holiday'

    list_hue = [('is_holiday', 'is_holiday'), ('is_weekend', 'is_weekend'), ('weather_code', 'weather_code')]

    plot = pie_plot(hue)
    return render_template('pie.html', plot=plot, focus_hue=hue, drop_hue= list_hue)


@app.route('/pred_lr')
def pred_lr():
    sqlengine = create_engine('mysql+mysqlconnector://admin:ember123!@localhost/final?host=localhost?port=3306')
    engine = sqlengine.raw_connection()
    cursor = engine.cursor()
    cursor.execute("SELECT * FROM raw_data")
    data = cursor.fetchall()
    return render_template('predict.html', data=data)

@app.route('/pred_result', methods=['POST', 'GET'])
def pred_result():

    if request.method == 'POST':
    ## Untuk Predict
        input = request.form
        
        suhu = float(input['t1'])
        hum = float(input['hum'])
        wind = float(input['wind'])


        if input['holiday'] == 'yes':
            holiday2 = 1
        else:
            holiday2 = 0


        if input['weekend'] == 'yes':
            weekend2 = 1
        else:
            weekend2 = 0

        if input['cuaca'] == "Cerah":
            cuaca_1 = 1
            cuaca_2 = 0
            cuaca_3 = 0
            cuaca_4 = 0
            cuaca_7 = 0
            cuaca_10 = 0
            cuaca_26 = 0
        elif input['cuaca'] == "Sedikit Berawan":
            cuaca_1 = 0
            cuaca_2 = 1
            cuaca_3 = 0
            cuaca_4 = 0
            cuaca_7 = 0
            cuaca_10 = 0
            cuaca_26 = 0
        elif input['cuaca'] == "Berawan Pecah-Pecah":
            cuaca_1 = 0
            cuaca_2 = 0
            cuaca_3 = 1
            cuaca_4 = 0
            cuaca_7 = 0
            cuaca_10 = 0
            cuaca_26 = 0
        elif input['cuaca'] == "Berawan":
            cuaca_1 = 0
            cuaca_2 = 0
            cuaca_3 = 0
            cuaca_4 = 1
            cuaca_7 = 0
            cuaca_10 = 0
            cuaca_26 = 0
        elif input['cuaca'] == "Hujan Ringan":
            cuaca_1 = 0
            cuaca_2 = 0
            cuaca_3 = 0
            cuaca_4 = 0
            cuaca_7 = 1
            cuaca_10 = 0
            cuaca_26 = 0
        elif input['cuaca'] == "Hujan Disertai Badai Petir":
            cuaca_1 = 0
            cuaca_2 = 0
            cuaca_3 = 0
            cuaca_4 = 0
            cuaca_7 = 0
            cuaca_10 = 1
            cuaca_26 = 0
        elif input['cuaca'] == "Hujan Salju":
            cuaca_1 = 0
            cuaca_2 = 0
            cuaca_3 = 0
            cuaca_4 = 0
            cuaca_7 = 0
            cuaca_10 = 0
            cuaca_26 = 1

        if input['bulan'] in ['maret','april','mei']:
            season_0 = 1
            season_1 = 0
            season_2 = 0
            season_3 = 0
        elif input['bulan'] in ['juni','juli','agustus']:
            season_0 = 0
            season_1 = 1
            season_2 = 0
            season_3 = 0
        elif input['bulan'] in ['september','oktober','november']:
            season_0 = 0
            season_1 = 0
            season_2 = 1
            season_3 = 0
        elif input['bulan'] in ['desember','januari','februari']:
            season_0 = 0
            season_1 = 0
            season_2 = 0
            season_3 = 1

        tanggal = int(input['tanggal'])
        if 1<= tanggal <=7:
            week_1 = 1
            week_2 = 0
            week_3 = 0
            week_4 = 0
        elif 8<= tanggal <=14:
            week_1 = 0
            week_2 = 1
            week_3 = 0
            week_4 = 0
        elif 15<= tanggal <=21:
            week_1 = 0
            week_2 = 0
            week_3 = 1
            week_4 = 0
        elif tanggal > 21:
            week_1 = 0
            week_2 = 0
            week_3 = 0
            week_4 = 1
        
        jam = int(input['jam'])
        if 0<= jam <= 5:
            dini_hari = 1
            pagi = 0
            siang = 0
            sore = 0
            malam = 0
        elif 6<= jam <=9:
            dini_hari = 0
            pagi = 1
            siang = 0
            sore = 0
            malam = 0
        elif 10<= jam <=15:
            dini_hari = 0
            pagi = 0
            siang = 1
            sore = 0
            malam = 0
        elif 16<= jam <=19:
            dini_hari = 0
            pagi = 0
            siang = 0
            sore = 1
            malam = 0
        else:
            dini_hari = 0
            pagi = 0
            siang = 0
            sore = 0
            malam = 1
        input_data = pd.DataFrame([[suhu,hum,wind,holiday2,weekend2,cuaca_1,cuaca_2,cuaca_3,cuaca_4,cuaca_7,cuaca_10,cuaca_26,season_0,season_1,season_2,season_3,week_1,week_2,week_3,week_4,dini_hari,malam,pagi,siang,sore]],
        columns=['t1', 'hum', 'wind_speed', 'is_holiday', 'is_weekend',
       'weather_code_1.0', 'weather_code_2.0', 'weather_code_3.0',
       'weather_code_4.0', 'weather_code_7.0', 'weather_code_10.0',
       'weather_code_26.0', 'season_0.0', 'season_1.0', 'season_2.0',
       'season_3.0', 'Tanggal_week_1', 'Tanggal_week_2', 'Tanggal_week_3',
       'Tanggal_week_4', 'Jam_ dini hari', 'Jam_malam', 'Jam_pagi',
       'Jam_siang', 'Jam_sore'])
        pred = Model.predict(input_data)[0]

        ## Untuk Isi Data
        holiday_dt = ''
        if input['holiday'] == 'yes':
            holiday_dt = 'Yes'
        else:
            holiday_dt = 'No'

        weekend_dt = ''
        if input['weekend'] == 'yes':
            weekend_dt = 'Yes'
        else:
            weekend_dt = 'No'

        jam_dt = ''
        if int(input['jam'])<10:
            jam_dt = f'0{int(input["jam"])}:00'
        else:
            jam_dt = f'{int(input["jam"])}:00'
        return render_template('result.html',
            suhu=float(input['t1']),
            hum=float(input['hum']),
            wind=float(input['wind']),
            holiday=holiday_dt,
            weekend=weekend_dt,
            cuaca=input['cuaca'],
            bulan=input['bulan'].capitalize(),
            tanggal=int(input['tanggal']),
            jam=jam_dt,
            prediksi=int(pred)
            )

if __name__ == '__main__':
    # ## Me-Load data dari Database
    # sqlengine = create_engine('mysql+pymysql://kal:s3cret123@127.0.0.1/flaskapp', pool_recycle=3605)
    # dbConnection = sqlengine.connect()
    # engine = sqlengine.raw_connection()
    # cursor = engine.cursor()
    # tips = pd.read_sql("select * from tips", dbConnection)
    
    ## Load Model
    with open('Model', 'rb') as model:
        Model = pickle.load(model)
    app.run(debug=True)