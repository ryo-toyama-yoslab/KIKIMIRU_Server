<?php 
ini_set('display_errors', "On"); //php実行時のエラー確認用
date_default_timezone_set('Asia/Tokyo');
ini_set('log_errors', '1'); // エラーログの有効化
$log_path = './log/save_log.txt'; // エラーログのファイルパスを指定して保存
ini_set('error_log', $log_path); // エラーログのファイルパスを指定して保存
$error_log_data = date('Y-m-d H:i:s') . ' : ' . 'save_log' . "\n";

// POSTされた画像データの取得
$log= $_POST["log"];

// マイクロ秒現在時刻
$dt =date("YmdHis").substr(explode(".", (microtime(true) . ""))[1], 0, 3);

// 0欠損を補完
$dtStr = str_pad($dt, 17, 0, STR_PAD_RIGHT);

// ヘッダに「data:image/png;base64,」が付いているので、それは外す
//$log = str_replace('data:image/jpg;base64,', '', $log);
//$log = str_replace(' ', '+', $log);

//　ログとして保存
file_put_contents('./detection-results/Application_log/'.$dtStr.'.txt', $log);

//パーミッションを変更
//chmod('./img_file/'.$dtStr.'.jpg', 0777);

echo $dtStr;
?>