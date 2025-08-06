<?php
require_once 'config.php';
session_start();
if (isset($_SESSION['user_id'])) {
    header("Location: " . ($_SESSION['es_admin'] ? "admin_events.php" : "events.php"));
    exit;
}
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CleanSpace - Ingreso</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        html { font-family: 'Inter', sans-serif; }
        body { background-color: #1a1a1a; }
        .main-container { background-color: #0d0d0d; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5); }
        .left-panel { background-image: url('images/background.png'); background-size: cover; background-position: center; position: relative; }
        .left-panel::before { content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0; background-color: rgba(0, 0, 0, 0.6); z-index: 1; }
        .left-panel > * { position: relative; z-index: 2; }
        .right-panel { background: linear-gradient(to bottom, #1a1a1a, #0d0d0d); }
        .btn-custom { background-color: transparent; border: 1px solid rgba(255, 255, 255, 0.3); color: white; transition: all 0.3s ease; }
        .btn-custom:hover { background-color: rgba(255, 255, 255, 0.1); border-color: white; }
    </style>
</head>
<body class="flex items-center justify-center min-h-screen p-4">
    <div class="main-container w-full max-w-5xl h-[600px] md:h-[700px] rounded-3xl flex flex-col md:flex-row overflow-hidden">
        <div class="left-panel w-full md:w-1/2 flex items-center justify-center p-8">
            <div class="text-center">
                <img src="images/1logo_clean.png" alt="CleanSpace Logo" class="h-24 w-24 mx-auto">
            </div>
        </div>
        <div class="right-panel w-full md:w-1/2 flex flex-col items-center justify-center p-8 space-y-6">
            <a href="login_form.php" class="btn-custom w-64 py-3 rounded-full text-lg font-semibold text-center">Ingreso</a>
            <a href="register.php" class="btn-custom w-64 py-3 rounded-full text-lg font-semibold text-center">Registro</a>
        </div>
    </div>
</body>
</html>