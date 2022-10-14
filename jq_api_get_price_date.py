# -*- coding: utf-8 -*-
# 2022.10.14 coded by yo.
# MIT License
# Python 3.6.8 / centos7.4

import urllib3
import requests
import datetime
import json
import sys




# J-Quants API 株価情報取得項目
# 
#  0 変数名	説明	型	例
#  1 Code	銘柄コード	String	86970
#  2 Date	日付	String	20170113
#  3 Open	始値（調整前）	Number	1683
#  4 Close	終値（調整前）	Number	1692
#  5 Low	安値（調整前）	Number	1673
#  6 High	高値（調整前）	Number	1704
#  7 Volume	取引高（調整前）	Number	1646200
#  8 TurnoverValue	取引代金	Number	2778858800
#  9 AdjustmentFactor	調整係数	Number	0.5（株式分割1:2の例）
# 10 AdjustmentOpen	調整済み始値	Number	841.5
# 11 AdjustmentClose	調整済み終値	Number	846
# 12 AdjustmentLow	調整済み安値	Number	836.5
# 13 AdjustmentHigh	調整済み高値	Number	852
# 14 AdjustmentVolume	調整済み取引高	Number	3292400








# ---------------------------------------------
# 機能: コマンドライン入力のパラメーターをチェックする。
# 引数1: コマンドライン入力のパラメーター（list型）
# 引数2: 出力ファイル名（string型）
# 返値: なし
# ---------------------------------------------
def func_parse_parameter(sys_argv):
    if len(sys_argv) == 2 :
        if sys_argv[1] == '-h' \
            or sys_argv[1] == '--help':
            print(sys_argv[0], ' date=[yyyymmdd]')
            print()
            exit()
        else :
            pass
        
    elif len(sys_argv) == 1 or len(sys_argv) > 5 :
        print('入力パラメーターが正しくありません。')
        print(sys_argv[0], ' date=[yyyymmdd]')
        exit()
    else:
        pass


# ---------------------------------------------
# 機能: コマンドライン入力のパラメーターを取得する。
# 引数1: コマンドライン入力のパラメーター（list型）
#
# 返値: 引数セット（辞書型）
# ---------------------------------------------
def func_get_parameter(sys_argv) :
    str_code = ''
    str_date = ''
    str_start = ''
    str_end = ''
    date_start = ''
    date_end = '' 
    for i in range(len(sys_argv)) :
        if i > 0 :
            if sys_argv[i][:5] == 'date=' :
                if len(sys_argv[i][5:]) == 8 :
                    str_date = sys_argv[i][5:]
                else :
                    print('日付は、8桁yyyymmddで指定して下さい。')
                    print(sys_argv[0], 'date=[yyyymmdd]')
                    print('例: date=20221014')
                    exit()
            else :
                print('入力パラメーターの形式が正しくありません。')
                print('sys_rgv[', i,']:', sys.argv[i])
                print('日付け指定のみできます。')
                print(sys_argv[0], 'date=[yyyymmdd]')
                print('例: date=20221014')
                exit()
    if len(str_date) == 8 :
        date_date = datetime.datetime.strptime(str_date, '%Y%m%d')
    else :
        print('入力パラメーターの形式が正しくありません。')
        print('sys_rgv[', i,']:', sys.argv[i])
        print(sys_argv[0], 'date=[yyyymmdd]')
        print('例: date=20221014')
        exit()
    
    dic_argv = {'code=':str_code, 'from=':date_start, 'to=':date_end, 'date=':str_date}
    return dic_argv



# ---------------------------------------------
# 機能 : 起動したディレクトリでファイルに書き込む。
# 引数1: 出力ファイル名（string型）
# 引数2: 出力文字列（string型）
# 返値 : 無し
# ---------------------------------------------
def func_read_from_file(str_fname):
    str_read = ''
    try:
        with open(str_fname, 'r', encoding = 'utf_8') as fin:
            while True:
                line = fin.readline()
                if not len(line):
                    break
                str_read = str_read + line
        return str_read

    except IOError as e:
        print('Can not read!!!')
        print(type(e))



# ---------------------------------------------
# 機能 : 起動したディレクトリでファイルに書き込む。
# 引数1: 出力ファイル名（string型）
# 引数2: 出力文字列（string型）
# 返値 : 無し
# ---------------------------------------------
def func_write_to_file(str_fname_output, str_text):
    try:
        with open(str_fname_output, 'w', encoding = 'utf_8') as fout:
            fout.write(str_text)     

    except IOError as e:
        print('Can not write!!!')
        print(type(e))




# ---------------------------------------------
# 機能 : ファイルに保存してあるIDトークンを読み出す。
# 引数1: IDトークン保存ファイル名（string型）
# 返値 : IDトークン（string型）
# 備考 : IDトークン保存ファイルのデータ形式は、
#   {"time_idtoken":"value","idToken":"value"}
# ---------------------------------------------
def func_read_idtoken(str_fname_idtoken):
    # ＩＤトークンの読み出し
    str_id_json = func_read_from_file(str_fname_idtoken)

    dic_idtoken = json.loads(str_id_json)
    str_idtoken = dic_idtoken.get('idToken')
    # ＩＤトークンを取得できない場合
    if str_idtoken is None :
        print('ＩＤトークンが取得できません。')
        quit()

    # ＩＤトークンの取得時間を表示
    str_time_idtoken = dic_idtoken.get('time_idToken')
    time_idtoken = datetime.datetime.strptime(str_time_idtoken, '%Y-%m-%d %H:%M:%S.%f')
    print('[ id token ]')
    print('time stamp :', time_idtoken)

    # ＩＤトークンの有効期限を表示（有効期限24時間）
    span_expire = datetime.timedelta(days=1)
    time_expire = time_idtoken + span_expire
    print('expiry date:', time_expire)
    time_remain = time_expire - datetime.datetime.now()
    print('remaining time:', time_remain)
    if time_remain > datetime.timedelta(days=0) :
        print('IDトークンの有効期間は２４時間です。')
    else :
        print('IDトークンは、無効です。有効期間を過ぎました。')
        
    print()
    return str_idtoken





# ---------------------------------------------
# 機能 : 出力ファイルにタイトル行を書き込む。
# 引数1: 出力ファイル名（string型）
# 返値 : 無し
# ---------------------------------------------
def func_write_title(str_fname_output):
    # csvで保存
    try:
        with open(str_fname_output, 'w', encoding = 'utf_8') as fout:
            # 1行目 タイトル行
            str_text = ''
            str_text = str_text + '"' + '銘柄コード' + '"' + ','	# 1
            str_text = str_text + '"' + '日付' + '"' + ','	# 2
            str_text = str_text + '"' + '始値（調整前）' + '"' + ','	# 3
            str_text = str_text + '"' + '終値（調整前）' + '"' + ','	# 4
            str_text = str_text + '"' + '安値（調整前）' + '"' + ','	# 5
            str_text = str_text + '"' + '高値（調整前）' + '"' + ','	# 6
            str_text = str_text + '"' + '取引高（調整前）' + '"' + ','	# 7
            str_text = str_text + '"' + '取引代金' + '"' + ','	# 8
            str_text = str_text + '"' + '調整係数' + '"' + ','	# 9
            str_text = str_text + '"' + '調整済み始値' + '"' + ','	# 10
            str_text = str_text + '"' + '調整済み終値' + '"' + ','	# 11
            str_text = str_text + '"' + '調整済み安値' + '"' + ','	# 12
            str_text = str_text + '"' + '調整済み高値' + '"' + ','	# 13
            str_text = str_text + '"' + '調整済み取引高' + '"' + '\n'	# 14

            # タイトル２行目 英文        
            str_text = str_text + '"' + 'Code' + '"' + ','	# 
            str_text = str_text + '"' + 'Date' + '"' + ','	# 
            str_text = str_text + '"' + 'Open' + '"' + ','	# 
            str_text = str_text + '"' + 'Close' + '"' + ','	# 
            str_text = str_text + '"' + 'Low' + '"' + ','	# 
            str_text = str_text + '"' + 'High' + '"' + ','	# 
            str_text = str_text + '"' + 'Volume' + '"' + ','	# 
            str_text = str_text + '"' + 'TurnoverValue' + '"' + ','	# 
            str_text = str_text + '"' + 'AdjustmentFactor' + '"' + ','	# 
            str_text = str_text + '"' + 'AdjustmentOpen' + '"' + ','	# 
            str_text = str_text + '"' + 'AdjustmentClose' + '"' + ','	# 
            str_text = str_text + '"' + 'AdjustmentLow' + '"' + ','	# 
            str_text = str_text + '"' + 'AdjustmentHigh' + '"' + ','	# 
            str_text = str_text + '"' + 'AdjustmentVolume' + '"' + '\n'	# 
            
            fout.write(str_text)
            fout.close

    except IOError as e:
        print('Can not write!!!')
        print(type(e))



# ---------------------------------------------
# 機能 : J-Quants API に株価情報、財務情報を問い合わせる。
# 引数1: IDトークンの値（string型）
# 引数1: 問合せURL（string型）
# 返値 : 財務データ（List型）
# ---------------------------------------------
def func_query_api(str_idToken, str_url):
    headers = {'Authorization': 'Bearer {}'.format(str_idToken)}
    resp = requests.get(str_url, headers=headers)
    dic_resp = json.loads(resp.text)
    if resp.status_code == 200 :
        # 正常に銘柄情報を取得
        return resp
    else :
        # 正しく取得できなかった場合
        # --- Message -----------------------------2022.10.03--
        # エラーで、403の場合のmessageは'M'と大文字になっているので注意。
        # エラーは400,401,403と3種類有る
        # 400: 未確認。これは何で起こるのしょう。
        # 401: {"message":"The incoming token has expired"}
        # 403: {"Message":"Access Denied"}
        # -----------------------------------------
        print('status_code:', resp.status_code)
        if resp.status_code == 400 or resp.status_code == 401 :
            print('message    :', dic_resp.get('message'))
        elif resp.status_code == 403 :
            print('message    :', dic_resp.get('Message'))
            print(resp.text)
        else :
            print(resp.text)
        quit()  # 終了




# =============================================
# 機能 : 保存してあるIDトークンを使い、銘柄指定で株価情報を取得し、保存する。
# 引数1: 開始日 書式 code=[12345] 
# 引数1: 開始日 書式 from=[yyyymmdd] 
# 引数3: 終了日 書式 to=[yyyymmdd] 
# 返値 : 無し
# 備考 : 出力のファイル名、IDトークンを保存してあるファイル名は適宜変更してください。
#       1銘柄ごとの取得になります。
#       財務データが複数返されます（複数ある場合）。
# ---------------------------------------------

# ＩＤトークン保存ファイル名
str_fname_idtoken = 'jq_idtoken.json'


# 入力パラメーターの書き出し
for i in range(len(sys.argv)):
    print('sys.argv[', i,']:', sys.argv[i])
print()

# パラメーターチェック
func_parse_parameter(sys.argv)

dic_argv = func_get_parameter(sys.argv)
str_code = dic_argv.get('code=')
str_date = dic_argv.get('date=')
date_from = dic_argv.get('from=')
date_to = dic_argv.get('to=')


# ＩＤトークンの読み出し
str_idtoken = func_read_idtoken(str_fname_idtoken)
# IDトークン保存ファイルのデータ形式は、
#   {"time_idtoken":"value","idToken":"value"}


# 出力ファイル名
str_fname_output = 'jq_price_' + str_date + '.csv'

# ファイルにタイトル行を書き込む
func_write_title(str_fname_output)

# 財務情報取得
str_parameter = 'date=' + str_date
str_url = 'https://api.jpx-jquants.com/v1/prices/daily_quotes?' + str_parameter #+ '"'
resp = func_query_api(str_idtoken, str_url)
dic_resp = json.loads(resp.text)    # jsonをパースして辞書型に変換
list_resp = dic_resp.get('daily_quotes')       # valueを取り出す。リスト型。

# 日付順にソート
list_resp = sorted(list_resp, key=lambda x:x['Code'])

try :
    if len(list_resp) > 0 :
        with open(str_fname_output, 'a', encoding = 'utf_8') as fout:
            # データ行
            for i in range(len(list_resp)):
                str_text = ''
                str_text = str_text + '"' + list_resp[i].get('Code') + '",'	# 
                str_text = str_text + '"' + list_resp[i].get('Date') + '",'	# 
                str_text = str_text + '"' + str(list_resp[i].get('Open')) + '",'	# 
                str_text = str_text + '"' + str(list_resp[i].get('Close')) + '",'	# 
                str_text = str_text + '"' + str(list_resp[i].get('Low')) + '",'	# 
                str_text = str_text + '"' + str(list_resp[i].get('High')) + '",'	# 
                str_text = str_text + '"' + str(list_resp[i].get('Volume')) + '",'	# 
                str_text = str_text + '"' + str(list_resp[i].get('TurnoverValue')) + '",'	# 
                str_text = str_text + '"' + str(list_resp[i].get('AdjustmentFactor')) + '",'	# 
                str_text = str_text + '"' + str(list_resp[i].get('AdjustmentOpen')) + '",'	# 
                str_text = str_text + '"' + str(list_resp[i].get('AdjustmentClose')) + '",'	# 
                str_text = str_text + '"' + str(list_resp[i].get('AdjustmentLow')) + '",'	# 
                str_text = str_text + '"' + str(list_resp[i].get('AdjustmentHigh')) + '",'	# 
                str_text = str_text + '"' + str(list_resp[i].get('AdjustmentVolume')) + '"\n'	# 

                fout.write(str_text)     
        fout.close
        print('outpu file:', str_fname_output)
        print(str_parameter,' data数:', i + 1 )  # 0からカウントしているので1加算
    else :
        print(str_parameter,' data数: 0')
              
except IOError as e:
    print('Can not write!!!')
    print(type(e))
    #print(line)

