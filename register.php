<?php
require_once 'config.php';
session_start();
$error = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $conn = new mysqli(DB_HOST, DB_USER, DB_PASS, DB_NAME);
    if ($conn->connect_error) die("Error: " . $conn->connect_error);
    $nombre = $_POST['nombre'];
    $apellido = $_POST['apellido'];
    $email = $_POST['email'];
    $telefono = $_POST['telefono'];
    $direccion = $_POST['direccion'];
    $estado = $_POST['estado'];
    $permiso_trabajo = $_POST['permiso_trabajo'];
    $password = password_hash($_POST['email'], PASSWORD_DEFAULT);
    $_SESSION['registro_temp'] = [
        'nombre' => $nombre,
        'apellido' => $apellido,
        'email' => $email,
        'telefono' => $telefono,
        'direccion' => $direccion,
        'estado' => $estado,
        'permiso_trabajo' => $permiso_trabajo,
        'password' => $password
    ];
    $stmt = $conn->prepare("INSERT INTO usuarios (nombre, apellido, email, telefono, direccion, estado, permiso_trabajo, password) VALUES (?, ?, ?, ?, ?, ?, ?, ?)");
    $stmt->bind_param("ssssssss", $nombre, $apellido, $email, $telefono, $direccion, $estado, $permiso_trabajo, $password);
    if ($stmt->execute()) {
        $_SESSION['user_id'] = $conn->insert_id;
        $_SESSION['es_admin'] = 0;
        header("Location: upload_photo.php");
        exit;
    } else {
        $error = "Error al registrar: " . $conn->error;
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
    <title>CleanSpace - Registro</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        html { font-family: 'Inter', sans-serif; }
        body { background-color: #1a1a1a; padding: 1rem; }
        .main-container { background-color: #0d0d0d; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5); }
        .left-panel { background-image: url('images/background.png'); background-size: cover; background-position: center; position: relative; }
        .left-panel::before { content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0; background-color: rgba(0, 0, 0, 0.6); z-index: 1; }
        .left-panel > * { position: relative; z-index: 2; }
        .right-panel { background: linear-gradient(to bottom, #1a1a1a, #0d0d0d); }
        .input-custom { background-color: transparent; border: 1px solid rgba(255, 255, 255, 0.3); color: white; transition: all 0.3s ease; padding: 0.75rem 1rem; font-size: 1rem; border-radius: 9999px; outline: none; width: 100%; }
        .input-custom:focus { border-color: white; }
        .input-custom::placeholder { color: rgba(255, 255, 255, 0.5); }
        .btn-submit { background-color: white; color: #0d0d0d; font-weight: 600; transition: all 0.3s ease; }
        .btn-submit:hover { background-color: #e0e0e0; }
    </style>
</head>
<body class="flex items-center justify-center min-h-screen p-4">
    <div class="main-container w-full max-w-5xl h-[600px] md:h-[700px] rounded-3xl flex flex-col md:flex-row overflow-hidden">
        <div class="left-panel w-full md:w-1/3 flex items-center justify-center p-8">
            <div class="text-center">
                <img src="images/1logo_clean.png" alt="CleanSpace Logo" class="h-24 w-24 mx-auto">
            </div>
        </div>
        <div class="right-panel w-full md:w-2/3 flex flex-col items-center justify-center p-8 space-y-4">
            <?php if ($error): ?>
                <p class="text-red-500"><?php echo $error; ?></p>
            <?php endif; ?>
            <form method="POST" action="register.php" class="grid grid-cols-1 md:grid-cols-2 gap-4 w-full max-w-xl">
                <input type="text" name="nombre" placeholder="Nombre" class="input-custom col-span-1" required>
                <input type="text" name="apellido" placeholder="Apellido" class="input-custom col-span-1" required>
                <input type="email" name="email" placeholder="Correo Electrónico" class="input-custom col-span-full" required>
                <input type="tel" name="telefono" placeholder="Teléfono" class="input-custom col-span-full" required>
                <input type="text" name="direccion" placeholder="Dirección" class="input-custom col-span-full">
                <input type="text" name="estado" placeholder="Estado" class="input-custom col-span-1">
                <input type="text" name="permiso_trabajo" placeholder="Permiso de trabajo (Papeles)" class="input-custom col-span-1">
                <button type="submit" class="btn-submit w-64 py-3 rounded-full text-lg font-semibold mt-6 col-span-full text-center">Siguiente</button>
            </form>
        </div>
    </div>
</body>
</html>