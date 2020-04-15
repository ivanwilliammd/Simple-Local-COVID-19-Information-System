#!/usr/bin/env python
# Created by Ivan William Harsono, MD, MCs (dr. Ivan William Harsono, MTI)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

import urllib.parse
import os
import pandas as pd
import datetime as dt

def ensure_folder(dir_path):
	if not os.path.exists(dir_path):
		os.makedirs(dir_path)

def create_msg_link(namaODP, current_dir, telpODP, linkWA):
	ensure_folder(os.path.join(current_dir, 'Message Text'))
	for file in os.listdir(os.path.join(current_dir, 'Message Text')):
		if file.endswith(".txt"):
			phone_number = telpODP[1:]
			msg_path = os.path.join(current_dir, 'Message Text', file)
			nama_link = file[:-4]
			with open(msg_path, 'r', encoding="utf-8") as file:
				data = file.read()
				data = data.replace("[]", namaODP)
			txt_msg = urllib.parse.quote(data)
		linkWA.write('\t\t\t<td align="center" width="250", cellpadding="10">\t\t<a href="https://api.whatsapp.com/send?phone=62{}&text={}" target="_blank">{}</a>\t\t</td>\n'.format(phone_number,txt_msg,nama_link))
		print('{} - {} - {} Berhasil Terexport'.format(namaODP, telpODP, nama_link))
	return print('Seluruh link {} Berhasil Terexport'.format(namaODP))

def move_old_html(current_dir):
	ensure_folder(os.path.join(current_dir, 'Previous html'))
	for file in os.listdir(current_dir):
		if file.endswith(".html"):
			os.replace(os.path.join(current_dir, file), os.path.join(current_dir, 'Previous html', file))
	return print('Successfully moving {} to "Previous html" folder'.format(file))



current_dir = os.getcwd()
move_old_html(current_dir)
current_date = dt.date.today()

linkWA = open('WA hyperlink ({}-{}).html'.format(str(current_date)[5:7], str(current_date)[8:]), 'w+')

count_txt = 0
for file in os.listdir(os.path.join(current_dir, 'Message Text')):
	count_txt = count_txt+1


linkWA.write('<html>\n')
linkWA.write('\t<head>\n')
linkWA.write('\t<title>ClickWA Pantau ODP dan Kontak Erat PKM XXXXXXXXX v.2.0</title>\n')
linkWA.write('\t<style>')
# linkWA.write('\t\ttable {border-collapse: collapse}')
linkWA.write('\t\ttable, th, td {border: 1px solid black;}')
linkWA.write('\t\tth {text-align: center;}')
linkWA.write('\t\ttr:hover {background-color: #FFB6C1}')
linkWA.write('\t</style>')
linkWA.write('\t</head>\n')
linkWA.write('\t<body>\n')
linkWA.write('\t<link rel="stylesheet" href="css/bootstrap.min.css">')
linkWA.write('\t<h1 align="center">ClickWA Puskesmas XXXXXXXXX {}</h1>\n'.format(current_date))
linkWA.write('\t<div class="container">')
linkWA.write('\t<div class="table-condensed">')
linkWA.write('\t\t<table align="center" class="table">\n')
linkWA.write('\t\t<tr>\n')
linkWA.write('\t\t\t<th>No</th>\n')
linkWA.write('\t\t\t<th>Nama Pasien</th>\n')
linkWA.write('\t\t\t<th>Telp</th>\n')
linkWA.write('\t\t\t<th colspan="{}">Link to WA</th>\n'.format(count_txt))
linkWA.write('\t\t</tr>\n')

phonebook_excel = os.path.join(current_dir, 'Phonebook.xlsx')
df_phonebook = pd.read_excel(phonebook_excel, sheet_name='Sheet1')
nama_pasien = []
telp_pasien = []

print("Sedang membaca data Phonebook dari Excel....................\n")

for jlh_pasien in range(len(df_phonebook)):
	nama_pasien.append(df_phonebook.iloc[jlh_pasien].values[0])
	telp_pasien.append(df_phonebook.iloc[jlh_pasien].values[1])

print("Selesai membaca data Phonebook dari Excel...................\n")

if len(nama_pasien)==len(telp_pasien):
	print("Menyatukan pesan dengan nomor telepon pasien................\n")
	for urutan_pasien in range(len(nama_pasien)):
		namaODP = nama_pasien[urutan_pasien]
		telpODP = str(telp_pasien[urutan_pasien])

		linkWA.write('\t\t<tr>\n')
		linkWA.write('\t\t\t<td align="right" cellpadding="10">{}.</td>\n'.format(urutan_pasien+1))
		linkWA.write('\t\t\t<td align="left" cellpadding="30">{}</td>\n'.format(namaODP))
		linkWA.write('\t\t\t<td align="left" cellpadding="20">{}</td>\n'.format(telpODP))
		if telpODP[0:2]=='08':
			telpODP = telpODP
			create_msg_link(namaODP, current_dir, telpODP, linkWA)
		elif telpODP[0]=='8':
			telpODP = '0' + telpODP
			create_msg_link(namaODP, current_dir, telpODP, linkWA)
		else:
			telpODP = "Invalid"
			linkWA.write('\t\t\t<td colspan="{}"></th>\n'.format(count_txt))
		linkWA.write('\t\t</tr>\n')
else:
	print('Jumlah kolom nama tidak sama dengan kolom telepon, pastikan kolom anda sudah benar')

linkWA.write('\t\t</table>\n')
linkWA.write('\t\t</div>\n')
linkWA.write('\t\t</div>\n')
linkWA.write('\t<p align="center">Created by Ivan William Harsono - Github: @ivanwilliammd</p>\n')
linkWA.write('\t</body>\n')
linkWA.write('</html>\n')
linkWA.close()

print('All {} phone number already exported to WA link'.format(len(nama_pasien)))