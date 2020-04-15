# Simple Local COVID-19 Information System
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3753157.svg)](https://doi.org/10.5281/zenodo.3753157)

Simple mini-Python apps for "Simple Local COVID-19 Surveillance Information System in Primary Health Care" made during my medical doctor internsip practice at Public Health Care (Puskesmas) located in Tangerang City. Tangerang City Health System use online integrated medical record based on [ePuskesmas](epuskesmas.id) and [ePuskesmas Kota Tangerang](https://kotatangerang.epuskesmas.id/)

However, since COVID-19 outbreak, to ease surveillance process of people with respiratory symptoms, it is integrate specific apps in addition of standard technology provided to us by public health office (Dinas Kesehatan). This is some of apps, used in conjunction with Google Forms, Awesome Table, Google sheet, Google My Map, and ePuskesmas database.

Note: for data privacy, I will use dummy data in this repo as template table data

## Prerequisite 
- Python
- Jupyter notebook/IPython (Optional for ease debugging process)
- Pandas Library 
- Numpy, 
- Scikit tools, 
- Pyinstaller
- Whatsapp Desktop (Download it from Microsoft Store, NOT from whatsapp.com/web.whatsapp.com)

## Environment and Deployement
This code already tested and compiled into single .exe file and tested on Windows 10 using pyinstaller library (navigate first to each directory folder)
```
pyinstaller "ClickWA ODP COVID-19 v2.0.py" --onefile --icon="icon.ico"
```
```
pyinstaller "ePuskesmas Splitter v1.5.py" --onefile --icon="icon.ico"
```
```
pyinstaller "FindMyAddress.py" --onefile --icon="icon.ico"
```

This repository consist of:
## 1. ClickWA (v2.0)
This application are used to generate specific message Whatsapp (WA) hyperlink with many template text to multiple patients, which use Python programming apps, Pandas Library, HTML/CSS Bootstrap

Feature:
1. Able to convert Phonebook Name & Number into html link (Number format can start from zero '08XXXXXX' or missing out 0 number '8XXXXXXX')
2. "Previous html" folder that contains previous day ClickWA hyperlink
3. "Red highlight" will show on duplicate name entry on "Phonebook.xlsx"
4. Simple yet clean User Interface (UI) and User Experience (UX):
	- Added table border and container for better size on medium sized screen
	- Added mouse hover pink color to help visualization
5. Unlimited Custom Text Message by adding new .txt file on "Message Text" folder.
6. Automatic naming on WA Message by putting [] sign on .txt file
Note: please don't delete the hidden "css" folder

How to run:
1. Run "ClickWA ODP COVID-19 v2.0.py" on your conda environment (Alternatively, run the .exe file if you already compile it using pyinstaller)
2. Wait until the process finish
3. You will have "WA hyperlink ({month}-{date}).html" file generated in your directory [for example: "WA hyperlink (04-11).html"]
4. Open the html file generated on your browser (preferably Google Chrome)
5. Click the link provided (blue color) which named after your text message file (.txt) you previously put on "Message Text" folder
6. After you click the link, you will be asked to open "Whatsapp desktop app" --> Open it, and your text message already tailored for each patients


## 2. ePusSplitter (v1.5)
This application are used to split the patient I check during my PHC rotation, since there are 5 medical interns (include me), 5 doctor staffs checking patient on daily basis and input it on ePuskesmas (ePus for short), it is time consuming to manually split my patient especially when I want input patient name (using their initially of course), age, eRM number (e-medical record), anthopometric data, vital sign, and SOAP data (see [here](https://www.google.com/url?sa=i&url=https%3A%2F%2Fmusculoskeletalkey.com%2Ftreatment-notes-and-progress-notes-using-a-modified-soap-format%2F&psig=AOvVaw0f6efYNtK5C_vn29sg1ysQ&ust=1587049489716000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCJCh7Jna6ugCFQAAAAAdAAAAABAS) for example of SOAP format).

I create this apps to ease my work by running this apps on .xlsx monthly patient report generated by ePuskesmas web apps (stored in 'Excel ePus' folder), and automatically export any data entry which contain my name (ivan) for example: dr. Ivan/dr.ivan/ivan (able to search capital and non-capital letter) on "Keterangan" column.

The .xlsx spreadsheet containing separated and simplified data will be exported on 'Splitted Excel' folder and HTML file will be created on parent folder

Don't delete html_file folder as it will contain your subhtml file, or else, your html file will contain all dead link.


How to run:
1. Run "ePuskesmas Splitter v1.5.py" on your conda environment (Alternatively, run the .exe file if you already compile it using pyinstaller)
2. Wait until the process finish
3. You will have "ePus Hyperlink.html" file generated in your directory [for example: WA hyperlink (04-11).html]
4. Open the html file generated on your browser (preferably Google Chrome)
5. Click the link provided (blue color) which named besides your patient name 
6. The link will be opened on new tab, and you will get SOAP format like this

```
2020-03-26 07:59:27


Bpk. AC, 51 th, 10 bln, eRM XXXXXXX, BB 51 kg


S: RPS: meriang, demam, batuk, pilek ingus bening, tenggorokan gatal 2 hari
RPD: kegiatan di bandara


O: TD 110/70; HR 80; RR 20; T 36.5 C



A: Acute upper respiratory infections of multiple and unspecified sites (J06)


P:
Ambroksol tablet 30 mg, Signa : 3x1, Jumlah : 10.00
Klorfeniramin maleat (CTM) tablet 4 mg, Signa : 3x1, Jumlah : 10.00
Parasetamol tablet 500 mg, Signa : 3x1, Jumlah : 10.00
```


## 3. FindMyAddress (v1.0)
This apps are used to find patient address on ePus database by comparing patient's name with ePus database. First, prepare your excel datas which  still have missing "Alamat" data on "Data Pasien Tanpa Alamat" folder, by comparing it with "Laporan Kunjungan Pasien ePus" .xlsx file extracted from ePus report menu.

How to run:
1. Run "FindMyAddress.py" on your conda environment (Alternatively, run the .exe file if you already compile it using pyinstaller)
2. Wait until the process finish and input what filename of results you want (for example: doremi --> doremi.xlsx will be exported on "Result" folder)
3. Upload this file to google drive, then open Google My Map and import from spreadsheet and sort by address


Icon are acquired from: Google pictures and converted to .ico file using this [link](https://icoconvert.com/)
