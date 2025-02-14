<?php
session_start();
if (!isset($_SESSION['time_remaining'])) {
    $_SESSION['time_remaining'] = 900;  // 15분(초 단위)
}

$_SESSION['time_remaining']--;

$minutes = floor($_SESSION['time_remaining'] / 60);
$seconds = $_SESSION['time_remaining'] % 60;
?>

<!DOCTYPE html>
<html lang="ko">

<head>
    <title>PHP 타이머</title>
    <meta http-equiv="refresh" content="1">
</head>

<body>
    <h1> hi </h1>
    <p> 메롱 </p>
    <div style="font-size: 48px; font-weight: bold;">
        <?php echo sprintf("%02d:%02d", $minutes, $seconds); ?>
    </div>
</body>

</html>