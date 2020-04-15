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
import numpy as np

def convert_score(kat_data):
    if kat_data=="Kontak Erat ODP":
        score=1
    elif kat_data=="Kontak Erat PDP":
        score=2
    elif kat_data=="ODP":
        score=3
    elif kat_data=="PDP":
        score=4
    elif kat_data=="Positif COVID":
        score=5
    elif kat_data=="Sehat":
        score=6
    elif kat_data=="Meninggal":
        score=7
    else:
        score=0
    return score

def compare_score(jumlah_pasien, df_data_trimmed, Kategori, df_awal, Kategori_Awal, df_akhir, Kategori_Akhir):
    print('Comparing patient scoring based on their category {} with {} to create new column {}.......'.format(Kategori_Awal, Kategori_Akhir, Kategori))
    for urutan_pasien in range(jumlah_pasien):
        score_awal = convert_score(df_awal[Kategori_Awal].iloc[urutan_pasien])
        score_akhir = convert_score(df_akhir[Kategori_Akhir].iloc[urutan_pasien])
        if score_akhir>score_awal:
            df_data_trimmed.at[urutan_pasien,Kategori] = df_akhir[Kategori_Akhir].iloc[urutan_pasien]
        else:
            continue

Current_directory = os.getcwd()
df_combi=pd.DataFrame()
for file in os.listdir(os.path.join(Current_directory, 'Laporan Kunjungan Pasien ePus')):
    if file.endswith(".xlsx"):
        print('Reading {} and adding it to address book......'.format(file))
        df_epus_alamat =  pd.read_excel(os.path.join(Current_directory, 'Laporan Kunjungan Pasien ePus', file), sheet_name='Sheet1')
        df_dropped_na = df_epus_alamat.dropna(axis=0, how='any', thresh=10, subset=None, inplace=False)
        df_fixed_header= df_dropped_na.rename(columns=df_dropped_na.iloc[0]).drop(df_dropped_na.index[0])
        df_alamat = df_fixed_header.fillna('-')
        df_combi = df_combi.append(df_alamat,ignore_index=True)

df_rebuild = pd.DataFrame()
df_rebuild['Nama'] = df_combi['Nama Pasien']
df_rebuild['Alamat'] = df_combi['Alamat'] + ' , ' + df_combi['Kelurahan']

df_trimmed_combi = pd.DataFrame()
for file in os.listdir(os.path.join(Current_directory, 'Data Pasien Tanpa Alamat')):
    if file.endswith(".xlsx"):
        print('Reading {} and finding suitable address......'.format(file))
        df_data_pasien_odp = pd.read_excel(os.path.join(Current_directory, 'Data Pasien Tanpa Alamat', file), sheet_name='Sheet1')
        df_data_trimmed = pd.DataFrame()
        df_data_trimmed['Nama Lengkap'] = df_data_pasien_odp['Nama_Lengkap'].str.upper()
        df_data_trimmed['Jenis Kelamin'] = df_data_pasien_odp['Jenis_Kelamin']
        df_data_trimmed['Umur'] = df_data_pasien_odp['Umur']
        df_data_trimmed['HP'] = df_data_pasien_odp['HP'].fillna('')
        df_data_trimmed['HP'] = '0'+ df_data_trimmed['HP'].astype(str)
        df_data_trimmed['HP'] = df_data_trimmed['HP'].str.rstrip('.0')
        df_data_trimmed['Kategori'] = df_data_pasien_odp['Kategori_Awal']

        jumlah_pasien = len(df_data_trimmed)
        compare_score(jumlah_pasien, df_data_trimmed, 'Kategori', df_data_pasien_odp, 'Kategori_Awal', df_data_pasien_odp, 'Kategori_Akhir')

        df_data_trimmed['Hasil Pemantauan'] = df_data_pasien_odp['Pemantauan'].fillna('')
        df_data_trimmed['Hasil Pemantauan'] = df_data_trimmed['Hasil Pemantauan'].str.split().str.get(0)
        df_data_trimmed['Kategori Akhir'] = df_data_trimmed['Kategori']

        compare_score(jumlah_pasien, df_data_trimmed, 'Kategori Akhir', df_data_trimmed, 'Kategori',  df_data_trimmed, 'Hasil Pemantauan')
#         for urutan_pasien in range(jumlah_pasien):
#             score_diag = convert_score(df_data_trimmed['Kategori'].iloc[urutan_pasien])
#             score_pemantauan = convert_score(df_data_trimmed['Hasil Pemantauan'].iloc[urutan_pasien])
#             if score_pemantauan>score_diag:
#                 df_data_trimmed.at[urutan_pasien,'Kategori Akhir'] = df_data_trimmed['Hasil Pemantauan'].iloc[urutan_pasien]
#             else:
#                 continue

        df_data_trimmed['Alamat'] = df_data_pasien_odp['Alamat']
        df_data_trimmed['Alamat'] = df_data_trimmed['Alamat'].fillna('-')

        for urutan_pasien in range(jumlah_pasien):
            if df_data_trimmed['Alamat'].iloc[urutan_pasien]=='-':
                if len(df_rebuild['Alamat'][df_rebuild['Nama']==df_data_trimmed['Nama Lengkap'].iloc[urutan_pasien]])>0:
                    df_data_trimmed.at[urutan_pasien,'Alamat'] = df_rebuild['Alamat'][df_rebuild['Nama']==df_data_trimmed['Nama Lengkap'].iloc[urutan_pasien]].values[0]
        df_trimmed_combi = df_trimmed_combi.append(df_data_trimmed,ignore_index=True)

enter_name = input("Please a name for your exported Excel file\n(Please enter the name without adding .xlsx):\n")        
df_trimmed_combi.to_excel(os.path.join(Current_directory, 'Result', '{}.xlsx'.format(enter_name)), sheet_name = "Sheet1")