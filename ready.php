<?php
date_default_timezone_set('Asia/Tokyo');
ini_set('display_errors', "On"); //php実行時のエラー確認用
ini_set('log_errors', '1'); // エラーログの有効化
$log_path = './log/ready_log.txt'; // エラーログのファイルパスを指定して保存
ini_set('error_log', $log_path); // エラーログのファイルパスを指定して保存
$error_log_data = date('Y-m-d H:i:s') . ' : ' . 'ready_log' . "\n";

//画像認識結果(単体画像の結果)のテキストファイルを初期化
file_put_contents("./detection-results/recognition_result.txt",'');

//10枚の画像認識結果からの医療行為特定結果のテキストファイルを初期化
file_put_contents("./detection-results/post_result.txt",'');

//画像消去処理
try {
    foreach ( glob('./img_file/*.jpg') as $detectionImgfile ) {
        unlink($detectionImgfile);
    }
} catch (Exception $e) {
    $error_log_data += $e->getMessage() . "\n";
}

//画像消去処理
try {
    foreach ( glob('./img_file/detectionFolder/*.jpg') as $detectionImgfile ) {
        unlink($detectionImgfile);
    }
} catch (Exception $e) {
    $error_log_data += $e->getMessage() . "\n";
}

error_log($error_log_data);
?>