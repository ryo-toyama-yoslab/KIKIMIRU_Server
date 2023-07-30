import re
from PIL import Image, ImageDraw, ImageFont
import os
import cv2



def crate_BBox(image, output):
    #ImageDrawオブジェクトの生成
    draw = ImageDraw.Draw(image)
    linewidth = 1 # 線の太さ
    rectcolor = 'red'
    textcolor = 'white'

    #画像の幅と高さ，チャネル数
    imw, imh = image.size

    #矩形描画
    draw.rectangle([(int(output[3]), int(output[2])), (int(output[5]), int(output[4]))], outline=rectcolor, width=linewidth)

    #認識結果の医療機器名を描画
    text = output[0] + " " + output[1]
    text_size = 15
    font = ImageFont.truetype('NimbusSansNarrow-Regular.t1', text_size)

    txw, txh = draw.textsize(text, font=font)#文字列"text"が占める領域のサイズを取得

    bboxw =int(output[5]) - int(output[3]) #BBoxの横幅
    bboxh =int(output[4]) - int(output[2]) #BBoxの縦幅

    t_bbox_difw = abs(txw - bboxw) #BBoxとテキスト横幅の差
    t_bbox_difh = abs(txh - bboxh) #BBoxとテキスト立幅の差

    # テキストの描画を開始する座標
    #右上に結果とスコア表示
    txpos_upperRight = (int(output[3]), int(output[2])-txh-linewidth*4) #左上座標
    typos_upperRight = (int(output[3])+txw+linewidth*4, int(output[2])) #右下座標

    #右下に結果とスコア表示
    txpos_lowerRight = (int(output[3]), int(output[4])) 
    typos_lowerRight = (int(output[3])+txw+linewidth*4, int(output[4])+txh+linewidth*4)

    #左下に結果とスコア表示
    txpos_lowerLeft = (int(output[5])-txw-linewidth*4, int(output[4])) #BBoxの左下に名前と信頼度スコア表示する場合の左上座標
    typos_lowerLeft = (int(output[5]), int(output[4])+txh+linewidth*4) #BBoxの左下に名前と信頼度スコア表示する場合の右下座標

    #左上に結果とスコア表示
    txpos_upperLeft = (int(output[5])-txw-linewidth*4, int(output[2])-txh-linewidth*4) #BBoxの左上に名前と信頼度スコア表示する場合の左上座標
    typos_upperLeft = (int(output[5]), int(output[4])) #BBoxの左上に名前と信頼度スコア表示する場合の右下座標


    # テキストを描画する領域を"rectcolor"で塗りつぶし,テキストをtextcolor(=白色)で描画
    if ((int(output[3]) < imw/2) and (int(output[2]) <= imh/2)): #認識位置が左上の場合
        draw.rectangle([txpos_lowerRight, typos_lowerRight], outline=rectcolor, fill=rectcolor, width=linewidth)
        draw.text((int(output[3]), int(output[4])), text, font=font, fill=textcolor)
    elif((int(output[3]) >= imw/2) and (int(output[2]) <= imh/2)): #認識位置が右上の場合
        draw.rectangle([txpos_lowerLeft, typos_lowerLeft], outline=rectcolor, fill=rectcolor, width=linewidth)
        draw.text((int(output[5])-txw, int(output[4])), text, font=font, fill=textcolor)
    elif((int(output[3]) < imw/2) and (int(output[2]) > imh/2)): #認識位置が左下の場合
        draw.rectangle([txpos_upperRight, typos_upperRight], outline=rectcolor, fill=rectcolor, width=linewidth)
        draw.text((int(output[3]), int(output[2])-txh+linewidth*4), text, font=font, fill=textcolor)
    elif((int(output[3]) >= imw/2) and (int(output[2]) > imh/2)): #認識位置が右下の場合
        draw.rectangle([txpos_upperLeft, typos_upperLeft], outline=rectcolor, fill=rectcolor, width=linewidth)
        draw.text((int(output[5])-txw, int(output[2])-txh+linewidth*4), text, font=font, fill=textcolor)

    return draw


'''
ログファイルにある画像フォルダの画像の読み込みとBoundingBoxの描画
'''
def read_imgFile(img_path, recognition_log, count):
    #画像ファイルのパス
    file_path = "../Storage_dir/" + img_path

    #画像保存用フォルダの作成
    file_forSave = '../Draw_recogniton_area/' + img_path
    os.makedirs(file_forSave, exist_ok=True)

    #画像の名前を番号に指定(同じ画像に対して複数の認識結果を保存するため)
    img_name = str(count)

    #重ね合わせ描画用 矩形オブジェクトのリスト
    bbox_list = []

    #重ね合わせ描画用 画像のリスト
    image = None
    image = Image.open(file_path + ".jpg") #画像を開く
    bbox_list.append(crate_BBox(image, recognition_log)) #BBoxの描画
    image.save(file_forSave + "/" + img_name + ".jpg") #通し番号で保存
    """
    if img_num == recognition_log[]:#同じ画像の結果なら描画オブジェクトのみ作成
        
    elif img_num == '0':#一番最初の画像を読み込んだ時
        
        
        bbox_list.append(crate_BBox(image, recognition_log))
    else:#別の画像になったら 前の画像の結果を保存 & 描画を行う
        #画像保存
        
        bbox_list = []
        img_num = output[6]
        image = Image.open(file_path + "/" + output[6] + ".jpg")
        bbox_list.append(crate_BBox(image, output))
    try:
        
    except FileNotFoundError:
        print("フォルダ名 : " + img_path + "は../Strage_dir/に存在しません")
        return
    """


   


'''
ログファイルを読み込む
'''
def read_logFile(log_path):
    f = open(log_path, 'r')
    log = f.read()
    img_path_list = re.findall(r'[0-9]{17}', log) #記録されている画像名リスト
    
    #画像ファイル名を取得(重複を外す)
    img_path_list = list(set(img_path_list)) #
    print("記録されている画像フォルダ数 : " + str(len(img_path_list)))

    #画像リストにある画像ごとに処理
    for img_path in img_path_list:
        count = 0
        #認識結果とBoundingBoxの座標を取得 正規表現 : 出力結果 信頼度スコア (左上y座標,左上x座標)(右下y座標,右下x座標) 画像ファイル名 
        pattern_str = re.compile(r"(.+) ([0-1]+.[0-9]+) \(([0-9]+),([0-9]+)\) \(([0-9]+),([0-9]+)\) " + (img_path))
        recognition_log = pattern_str.findall(log)
        print("画像ファイル名 : " + img_path)
        for img_log in recognition_log:
            """
            print(img_log[0]) #認識した医療機器名
            print(img_log[1]) #信頼度スコア
            print(img_log[2]) #BoundingBoxの左上y座標
            print(img_log[3]) #BoundingBoxの左上x座標
            print(img_log[4]) #BoundingBoxの右下y座標
            print(img_log[5]) #BoundingBoxの右下x座標
            """
            if(len(img_log) > 0):
                count += 1
                read_imgFile(img_path, img_log, count)

    f.close()




'''
実行コード
'''

print("認識結果の描画を開始します．")
print("描画結果は~toyama/public_html/Draw_recognition_area/ に保存されます．")

read_logFile('log.txt')
print("Complete")