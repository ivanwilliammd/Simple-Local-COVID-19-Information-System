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

import os
import pandas as pd

def get_initials(fullname):
	name_list = fullname.split()
	initials = ""
	for name in name_list:  # go through each name
		initials += name[0].upper()  # append the initial
	return initials

def get_prefix(gender, age):
	age_front = age.split()[0]
	if int(age_front)<19:
		prefix = "An."
	else:
		if gender=="L":
			prefix = "Bpk."
		if gender=="P":
			prefix = "Ibu"
	return prefix

def get_obat(obat):
	obat_split = obat.split("+")
	return obat_split

linkePus = open('ePus Hyperlink.html', 'w+')
print('Creating ePus Hyperlink.html')
linkePus.write('<html>\n')
linkePus.write('\t<head>\n')
linkePus.write('\t<title>ePuskesmas Pasien dr. myname</title>\n')
linkePus.write('\t<body>\n')
linkePus.write('\t<h1>ePuskesmas dr. myname</h1>\n')
linkePus.write('\t\t<table>\n')
linkePus.write('\t\t<tr>\n')
linkePus.write('\t\t\t<th>No</th>\n')
linkePus.write('\t\t\t<th>Tanggal</th>\n')
linkePus.write('\t\t\t<th>Nama Pasien</th>\n')
linkePus.write('\t\t\t<th>eRM</th>\n')
linkePus.write('\t\t\t<th>Link</th>\n')
linkePus.write('\t\t\t<th>Diagnosa</th>\n')
linkePus.write('\t\t</tr>\n')
count_px = 0

# put your name on here (don't delete '' sign --> for example 'ivan')
myname = '' 

count_xlsx_file = 0
Current_directory = os.getcwd()
for file in os.listdir(os.path.join(Current_directory, 'Excel ePus')):
	if file.endswith(".xlsx"):
		count_xlsx_file = count_xlsx_file + 1
		df_epus_myname =  pd.read_excel(os.path.join(Current_directory, 'Excel ePus', file), sheet_name='Sheet1')
		df_dropped_na = df_epus_myname.dropna(axis=0, how='any', thresh=10, subset=None, inplace=False)
		df_fixed_header= df_dropped_na.rename(columns=df_dropped_na.iloc[0]).drop(df_dropped_na.index[0])
		df_myname = df_fixed_header[df_fixed_header.Keterangan.str.lower().str.contains(myname, na=False, regex=True)]
		df_myname = df_myname.fillna('--')

		df_rebuild = pd.DataFrame()
		df_rebuild['Date'] = df_myname['Tanggal']
		df_rebuild['Nama'] = df_myname['Nama Pasien']
		df_rebuild['eRM'] = df_myname['No. eRM']
		df_rebuild['JK'] = df_myname['Jenis Kelamin']
		df_rebuild['BB'] = df_myname['Berat Badan']
		df_rebuild['Umur'] = df_myname['Umur Tahun'].str.slice(0,-6) + str(' th, ') + df_myname['Umur Bulan'].str.slice(0,-6)+ str(' bln')
		df_rebuild['S1'] = df_myname['RPS'] 
		df_rebuild['S2']= df_myname['RPD']
		df_rebuild['TTV'] = str('TD ') + df_myname['Sistole'].str.slice(0,-3) + str('/') + df_myname['Diastole'].str.slice(0,-3) + str('; HR ') + df_myname['Detak Nadi'].str.slice(0,-7) + str('; RR ') + df_myname['Nafas'].str.slice(0,-7) + str('; T ') + df_myname['Suhu'] 
		df_rebuild['A'] = df_myname['Diagnosa 1'] + str(', ') + df_myname['Diagnosa 2'] + str(', ') + df_myname['Diagnosa 3']  + str(', ') + df_myname['Diagnosa 4'] + str(', ') + df_myname['Diagnosa 5'] 
		df_rebuild['A'] = df_rebuild['A'].str.replace(", --*", '')
		df_rebuild['P'] = df_myname['Resep'] + str(', ') + df_myname['Tindakan']
		df_rebuild['P'] = df_rebuild['P'].str.replace(", --*", '')
		df_rebuild['P'] = df_rebuild['P'].str.replace(", Racikan : -", '\n')

		df_rebuild.to_excel(os.path.join(Current_directory, 'Splitted Excel', file), sheet_name = "Sheet1")

		for urutan_pasien in range(len(df_rebuild)):
			count_px = count_px + 1
			linkePus.write('\t\t<tr>\n')
			linkePus.write('\t\t\t<td align="right" cellpadding="10">{}.</td>\n'.format(count_px))
			linkePus.write('\t\t\t<td align="left" cellpadding="30">{}</td>\n'.format(df_rebuild['Date'].iloc[urutan_pasien][:10]))
			linkePus.write('\t\t\t<td align="left" cellpadding="20">{}</td>\n'.format(df_rebuild['Nama'].iloc[urutan_pasien]))
			linkePus.write('\t\t\t<td align="left" cellpadding="20">{}</td>\n'.format(df_rebuild['eRM'].iloc[urutan_pasien]))
			linkePus.write('\t\t\t<td align="center" width="250", cellpadding="10">\t\t<a href="html_file/{}_{}.html" target="_blank">Lihat SOAP</a>\t\t</td>\n'.format(df_rebuild['Nama'].iloc[urutan_pasien], df_rebuild['Date'].iloc[urutan_pasien][:10]))
			linkePus.write('\t\t\t<td align="left" cellpadding="20">{}</td>\n'.format(df_rebuild['A'].iloc[urutan_pasien].split()[-1][1:-1]))

			print('Creating {}_{}.html'.format(df_rebuild['Nama'].iloc[urutan_pasien], df_rebuild['Date'].iloc[urutan_pasien][:10]))
			linkePasien = open('html_file/{}_{}.html'.format(df_rebuild['Nama'].iloc[urutan_pasien], df_rebuild['Date'].iloc[urutan_pasien][:10]), 'w+')
			linkePasien.write('<html>\n')
			linkePasien.write('\t<head>\n')
			linkePasien.write('\t<title>{}, eRM {}</title>\n'.format(df_rebuild['Nama'].iloc[urutan_pasien],df_rebuild['eRM'].iloc[urutan_pasien]))
			linkePasien.write('\t<body>\n')
			inisial = get_initials(df_rebuild['Nama'].iloc[urutan_pasien])
			prefix = get_prefix(df_rebuild['JK'].iloc[urutan_pasien], df_rebuild['Umur'].iloc[urutan_pasien])
			obat_split = get_obat(df_rebuild['P'].iloc[urutan_pasien])

			linkePasien.write('\t<p style="font-size:200%;">{}<br><br></p>'.format(df_rebuild['Date'].iloc[urutan_pasien]))
			linkePasien.write('\t<p style="font-size:200%;">{} {}, {}, eRM {}, BB {}<br><br></p>'.format(prefix, inisial, df_rebuild['Umur'].iloc[urutan_pasien], df_rebuild['eRM'].iloc[urutan_pasien], df_rebuild['BB'].iloc[urutan_pasien]))
			linkePasien.write('\t<p style="font-size:200%;">S:\nRPS: {}<br>'.format(df_rebuild['S1'].iloc[urutan_pasien]))
			linkePasien.write('RPD: {}<br><br></p>'.format(df_rebuild['S2'].iloc[urutan_pasien]))
			linkePasien.write('\t<p style="font-size:200%;">O: {}<br><br><br></p>'.format(df_rebuild['TTV'].iloc[urutan_pasien]))
			linkePasien.write('\t<p style="font-size:200%;">A: {}<br><br></p>'.format(df_rebuild['A'].iloc[urutan_pasien]))
			linkePasien.write('\t<p style="font-size:200%;">P:<br>')
			for obat in obat_split:
				linkePasien.write('{}<br>'.format(obat))
			linkePasien.write('\t</p>')
			linkePasien.write('\t</body>')
			linkePasien.write('</html>')
			linkePasien.close()

		linkePus.write('\t\t<tr>\n')

linkePus.write('\t\t</table>\n')
linkePus.write('\t<p>Created by Ivan William Harsono - Github: @mynamewilliammd</p>\n')
linkePus.write('\t</body>\n')
linkePus.write('</html>\n')
linkePus.close()
print('Finish appending {} patients to ePus Hyperlink.html\n'.format(count_px))
print('Closing apps.......')