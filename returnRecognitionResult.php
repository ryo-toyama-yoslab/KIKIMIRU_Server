<?php
ini_set('display_errors', "On"); //php実行時のエラー確認用
date_default_timezone_set('Asia/Tokyo');
ini_set('log_errors', '1'); // エラーログの有効化
$log_path = './log/returnRecoginionResult_error_log.txt'; // エラーログのファイルパスを指定して保存
ini_set('error_log', $log_path); // エラーログのファイルパスを指定して保存
$error_log_data = date('Y-m-d H:i:s') . ' : ' . 'returnRecoginionResult_error_log' . "\n";

// ./img_file/recognitionFolderフォルダ内の画像枚数をカウント
// マイクロ秒現在時刻
//$dtStr =date("YmdHis") . substr(explode(".", (microtime(true) . ""))[1], 0, 3);

//認識結果が出力されていればその結果をアプリに返送 & 該当結果は削除(仮保存データ)
$result = file("./detection-results/post_result.txt", FILE_SKIP_EMPTY_LINES | FILE_IGNORE_NEW_LINES);
if(!empty($result)){
    $post_result = $result[0];
    // 1行目(認識するフォルダパス)を削除
    unset($result[0]);
    //上書き
    file_put_contents("./detection-results/post_result.txt", implode(PHP_EOL,$result));
    echo $post_result;
}else{
    echo "null";
    //テスト用
    //file_put_contents("./detection-results/log.txt","youtui "."-time:".$time."\n", FILE_APPEND);
    //echo "blood";s
}

error_log($error_log_data);
?>