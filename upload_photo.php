<?php
require_once 'config.php';
session_start();
$error = '';
if (!isset($_SESSION['registro_temp'])) {
    header("Location: register.php");
    exit;
}
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['submit_photo'])) {
    $conn = new mysqli(DB_HOST, DB_USER, DB_PASS, DB_NAME);
    if ($conn->connect_error) die("Error: " . $conn->connect_error);
    $data = $_SESSION['registro_temp'];
    $foto_nombre = null;
    if (isset($_FILES['foto']) && $_FILES['foto']['error'] === UPLOAD_ERR_OK) {
        $foto_tmp = $_FILES['foto']['tmp_name'];
        $foto_nombre = uniqid() . '.' . pathinfo($_FILES['foto']['name'], PATHINFO_EXTENSION);
        $destino = UPLOAD_DIR . $foto_nombre;
        if (!is_dir(UPLOAD_DIR)) mkdir(UPLOAD_DIR, 0777, true);
        if (move_uploaded_file($foto_tmp, $destino)) {
            $stmt = $conn->prepare("INSERT INTO usuarios (nombre, apellido, email, telefono, direccion, estado, permiso_trabajo, password, foto) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)");
            $stmt->bind_param("sssssssss", $data['nombre'], $data['apellido'], $data['email'], $data['telefono'], $data['direccion'], $data['estado'], $data['permiso_trabajo'], $data['password'], $foto_nombre);
            if ($stmt->execute()) {
                $_SESSION['user_id'] = $conn->insert_id;
                $_SESSION['es_admin'] = 0;
                unset($_SESSION['registro_temp']);
                header("Location: final.php");
                exit;
            } else {
                $error = "Error al guardar: " . $conn->error;
            }
        } else {
            $error = "Error al subir la foto.";
        }
    } else {
        $error = "Por favor, sube una foto válida.";
    }
    $stmt->close();
    $conn->close();
}
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CleanSpace - Subir Foto</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        html { font-family: 'Inter', sans-serif; }
        body { background-color: #1a1a1a; padding: 1rem; }
        .main-container { background-color: #0d0d0d; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5); }
        .left-panel { background-image: url('images/background.png'); background-size: cover; background-position: center; position: relative; }
        .left-panel::before { content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0; background-color: rgba(0, 0, 0, 0.6); z-index: 1; }
        .left-panel > * { position: relative; z-index: 2; }
        .right-panel { background: linear-gradient(to bottom, #1a1a1a, #0d0d0d); color: white; }
        .input-custom { background-color: transparent; border: 1px solid rgba(255, 255, 255, 0.3); color: white; transition: all 0.3s ease; padding: 0.75rem 1rem; font-size: 1rem; border-radius: 9999px; outline: none; width: 100%; }
        .input-custom:focus { border-color: white; }
        .input-custom::placeholder { color: rgba(255, 255, 255, 0.5); }
        .btn-submit { background-color: white; color: #0d0d0d; font-weight: 600; transition: all 0.3s ease; }
        .btn-submit:hover { background-color: #e0e0e0; }
        .btn-upload { background-color: transparent; border: 1px solid white; color: white; font-weight: 600; transition: all 0.3s ease; padding: 0.75rem 2rem; border-radius: 9999px; }
        .btn-upload:hover { background-color: rgba(255, 255, 255, 0.1); }
    </style>
</head>
<body class="flex items-center justify-center min-h-screen p-4">
    <div class="main-container w-full max-w-5xl h-[600px] md:h-[700px] rounded-3xl flex flex-col md:flex-row overflow-hidden">
        <div class="left-panel w-full md:w-1/3 flex items-center justify-center p-8">
            <div class="text-center">
                <img src="images/1logo_clean.png" alt="CleanSpace Logo" class="h-24 w-24 mx-auto">
            </div>
        </div>
        <div class="right-panel w-full md:w-2/3 flex flex-col items-center justify-center p-8 space-y-8">
            <h2 class="text-2xl font-semibold text-white mb-4">Subir Foto</h2>
            <?php if ($error): ?>
                <p class="text-red-500"><?php echo $error; ?></p>
            <?php endif; ?>
            <div class="flex flex-col md:flex-row items-center md:items-start space-y-8 md:space-y-0 md:space-x-12">
                <div class="flex-shrink-0">
                    <img src="images/face_example.png" alt="Foto" class="rounded-full w-40 h-40 object-cover">
                </div>
                <div class="text-white text-sm space-y-2">
                    <p class="font-semibold">La foto debe cumplir los siguientes requerimientos:</p>
                    <ul class="list-disc list-inside ml-4">
                        <li>DEBE TENER BUENA ILUMINACIÓN</li>
                        <li>DEBE SER TOMADA DESDE EL FRENTE</li>
                        <li>TRATAR DE NO INCLUIR GORRO Y LENTES</li>
                        <li>EL ROSTRO DEBE SER 100% VISIBLE</li>
                    </ul>
                </div>
            </div>
            <form method="POST" action="upload_photo.php" enctype="multipart/form-data" class="flex flex-col space-y-4 mt-8">
                <input type="file" name="foto" accept="image/*" class="input-custom" required>
                <button type="submit" name="submit_photo" class="btn-submit w-64 py-3 rounded-full text-lg font-semibold text-center">Enviar</button>
            </form>
        </div>
    </div>
</body>
</html>