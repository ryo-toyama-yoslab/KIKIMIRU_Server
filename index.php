<?php
date_default_timezone_set('Asia/Tokyo');
ini_set('display_errors', "On"); //php実行時のエラー確認用
ini_set('log_errors', '1'); // エラーログの有効化
$log_path = './log/error_log.txt'; // エラーログのファイルパスを指定して保存
ini_set('error_log', $log_path); // エラーログのファイルパスを指定して保存
$error_log_data = date('Y-m-d H:i:s') . ' : ' . 'error_log' . "\n";

$error_log_data = 'run index.php\n';

// ランダムな少数値を返す
function randomFloat($min = 0, $max = 1) {
    return $min + mt_rand() / mt_getrandmax() * ($max - $min);
}

//画像移動処理
$stackImgfolder = "./img_file/";# 移動元ファイル

$folderToSave = "/home/toyama/image_dir/";#$_SERVER['HOME'] . "/image_dir/"; #移動先ファイル
foreach (glob($stackImgfolder.'*.jpg') as $stackImgfile) {
    echo($folderToSave.basename($stackImgfile));
    $success = copy($stackImgfile, $folderToSave.basename($stackImgfile));

    if ($success) {
        $error_log_data += "移動成功". $stackImgfile ."\n";
    }else{
        $error_log_data += "移動失敗". $stackImgfile ."\n";
    }
    usleep(randomFloat(500000, 1500000)); #マイクロ秒単位でスリープ
}

error_log($error_log_data);
?>