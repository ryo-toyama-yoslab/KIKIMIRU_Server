<?php 
ini_set('display_errors', "On"); //php実行時のエラー確認用
date_default_timezone_set('Asia/Tokyo');
ini_set('log_errors', '1'); // エラーログの有効化
$log_path = './log/getImage_error_log.txt'; // エラーログのファイルパスを指定して保存
ini_set('error_log', $log_path); // エラーログのファイルパスを指定して保存


// POSTされた画像データの取得
$img= $_POST["img"];

// マイクロ秒現在時刻
$dt =date("YmdHis").substr(explode(".", (microtime(true) . ""))[1], 0, 3);

// 0欠損を補完
$dtStr = str_pad($dt, 17, 0, STR_PAD_RIGHT);

// 画像保存先パス
$abs_path = dirname(__FILE__);
$path =  dirname(dirname($abs_path))."\n";
$folderToSave = $path . '/image_dir/' . $dtStr.'.jpg';#$_SERVER['HOME'] . '/image_dir/' . $dtStr.'.jpg'; #移動先ファイル
$error_log_data = $folderToSave . "\n";


error_log($error_log_data);
// ヘッダに「data:image/png;base64,」が付いているので、それは外す
$img = str_replace('data:image/jpg;base64,', '', $img);
$img = str_replace(' ', '+', $img);

// 残りのデータはbase64エンコードされているので、デコードする
$fileData= base64_decode($img);

// 画像として保存
try:
    #move_uploaded_file($fileData, $folderToSave);
catch(Exception $e):
    $error_log_data += date('Y-m-d H:i:s') . $e->getMessage() . "\n";
//パーミッションを変更
//chmod('./img_file/'.$dtStr.'.jpg', 0777);

error_log($error_log_data);
?>