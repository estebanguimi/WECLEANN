<?php
require_once 'config.php';
session_start();
if (!isset($_SESSION['user_id'])) {
    header("Location: index.php");
    exit;
}
$conn = new mysqli(DB_HOST, DB_USER, DB_PASS, DB_NAME);
if ($conn->connect_error) die("Error: " . $conn->connect_error);
$query = "SELECT e.nombre, e.fecha, CONCAT(e.hora_inicio, ' - ', e.hora_fin, ' PM') AS time FROM inscripciones i JOIN eventos e ON i.id_evento = e.id WHERE i.id_usuario = ? AND i.estado = 'pendiente'";
$stmt = $conn->prepare($query);
$stmt->bind_param("i", $_SESSION['user_id']);
$stmt->execute();
$result = $stmt->get_result();
$selected_events = [];
while ($row = $result->fetch_assoc()) {
    $selected_events[] = $row;
}
$stmt->close();
$conn->close();
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CleanSpace - Gracias por Completar</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        html { font-family: 'Inter', sans-serif; }
        body { background-color: #1a1a1a; padding: 1rem; }
        .main-container { background-color: #0d0d0d; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5); display: flex; flex-direction: column; align-items: center; }
        .header-image { width: 100%; height: 150px; object-fit: cover; object-position: center; border-top-left-radius: 1.5rem; border-top-right-radius: 1.5rem; position: relative; z-index: 1; background-size: cover; background-position: center; }
        .header-image::before { content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0; background-color: rgba(0, 0, 0, 0.6); z-index: 2; }
        .header-content { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 3; text-align: center; }
        .main-content-area { flex-grow: 1; width: 100%; padding: 2rem; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; background: linear-gradient(to bottom, #1a1a1a, #0d0d0d); border-bottom-left-radius: 1.5rem; border-bottom-right-radius: 1.5rem; }
        .btn-thank-you { background-color: transparent; border: 1px solid rgba(255, 255, 255, 0.3); color: white; padding: 0.75rem 2rem; border-radius: 9999px; font-weight: 600; transition: all 0.3s ease; }
        .btn-thank-you:hover { background-color: rgba(255, 255, 255, 0.1); border-color: white; }
        .btn-exit { background-color: transparent; color: rgba(255, 255, 255, 0.7); border: none; text-decoration: underline; transition: color 0.3s ease; }
        .btn-exit:hover { color: white; }
        @media (max-width: 768px) { .main-container { height: auto; } .header-image { height: 100px; } .main-content-area { padding: 1.5rem; } .btn-thank-you { padding: 0.6rem 1.5rem; font-size: 0.9rem; } .btn-exit { font-size: 0.9rem; } }
    </style>
</head>
<body class="flex items-center justify-center min-h-screen p-4">
    <div class="main-container w-full max-w-5xl h-[600px] md:h-[700px] rounded-3xl overflow-hidden">
        <div class="header-image" style="background-image: url('images/background.png');">
            <div class="header-content">
                <img src="images/1logo_clean.png" alt="CleanSpace Logo" class="h-24 w-24 mx-auto">
            </div>
        </div>
        <div class="main-content-area">
            <h2 class="text-white text-3xl font-bold mb-6">Gracias por Completar</h2>
            <p class="text-white text-base mb-4 max-w-md opacity-85">Eventos seleccionados:</p>
            <ul class="text-white text-sm mb-4 max-w-md">
                <?php foreach ($selected_events as $event): ?>
                    <li><?php echo "{$event['nombre']} - {$event['fecha']} ({$event['time']})"; ?></li>
                <?php endforeach; ?>
            </ul>
            <p class="text-white text-base mb-4 max-w-md opacity-85">
                Si no puedes asistir a alguno de los eventos, contacta a: 9548450289 - 9548454277
            </p>
            <p class="text-white text-sm mb-8 max-w-md opacity-75">
                Para inconvenientes con papeles o contacto, usa los números anteriores. Por favor, firma y sube los términos y condiciones aquí.
            </p>
            <a href="index.php" class="btn-exit text-lg">Salir</a>
        </div>
    </div>
</body>
</html>