<?php
require_once 'config.php';
session_start();
if (!isset($_SESSION['user_id']) || !$_SESSION['es_admin']) {
    header("Location: index.php");
    exit;
}
require 'vendor/autoload.php';
use PHPMailer\PHPMailer\PHPMailer;
use Twilio\Rest\Client;
$conn = new mysqli(DB_HOST, DB_USER, DB_PASS, DB_NAME);
if ($conn->connect_error) die("Error: " . $conn->connect_error);
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $id_inscripcion = $_POST['id_inscripcion'];
    $estado = $_POST['estado'];
    $mensaje_personalizado = $_POST['mensaje_personalizado'] ?? '';
    $query = "UPDATE inscripciones SET estado = ?, mensaje_personalizado = ? WHERE id = ?";
    $stmt = $conn->prepare($query);
    $stmt->bind_param("ssi", $estado, $mensaje_personalizado, $id_inscripcion);
    $stmt->execute();
    $query = "SELECT u.email, u.telefono, u.nombre, e.nombre AS evento, e.fecha, e.hora_inicio FROM inscripciones i JOIN usuarios u ON i.id_usuario = u.id JOIN eventos e ON i.id_evento = e.id WHERE i.id = ?";
    $stmt = $conn->prepare($query);
    $stmt->bind_param("i", $id_inscripcion);
    $stmt->execute();
    $data = $stmt->get_result()->fetch_assoc();
    $mail = new PHPMailer(true);
    $mail->isSMTP();
    $mail->Host = 'smtp.gmail.com';
    $mail->SMTPAuth = true;
    $mail->Username = 'tuemail@gmail.com';
    $mail->Password = 'tuapppassword';
    $mail->SMTPSecure = 'tls';
    $mail->Port = 587;
    $mail->setFrom('tuemail@gmail.com', 'CleanSpace');
    $mail->addAddress($data['email']);
    $mail->Subject = 'Confirmación de Evento';
    $mail->Body = "Hola {$data['nombre']},\n\nEstás {$estado} para {$data['evento']} el {$data['fecha']} a las {$data['hora_inicio']}.\n{$mensaje_personalizado}";
    $mail->send();
    $twilio = new Client('tu_twilio_sid', 'tu_twilio_token');
    $twilio->messages->create($data['telefono'], [
        'from' => '+1234567890',
        'body' => "Hola {$data['nombre']}, estás {$estado} para {$data['evento']} el {$data['fecha']} a las {$data['hora_inicio']}. {$mensaje_personalizado}"
    ]);
    $stmt->close();
}
$query = "SELECT i.id, u.nombre, u.apellido, u.email, e.nombre AS evento, e.fecha, i.estado FROM inscripciones i JOIN usuarios u ON i.id_usuario = u.id JOIN eventos e ON i.id_evento = e.id";
$result = $conn->query($query);
$inscripciones = [];
while ($row = $result->fetch_assoc()) {
    $inscripciones[] = $row;
}
$conn->close();
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CleanSpace - Gestión de Inscritos</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        html { font-family: 'Inter', sans-serif; }
        body { background-color: #1a1a1a; padding: 1rem; }
        .main-container { background-color: #0d0d0d; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5); }
        .left-panel { background-image: url('images/background.png'); background-size: cover; background-position: center; position: relative; }
        .left-panel::before { content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0; background-color: rgba(0, 0, 0, 0.6); z-index: 1; }
        .left-panel > * { position: relative; z-index: 2; }
        .right-panel { background: linear-gradient(to bottom, #1a1a1a, #0d0d0d); overflow-y: auto; }
        .input-custom { background-color: transparent; border: 1px solid rgba(255, 255, 255, 0.3); color: white; transition: all 0.3s ease; padding: 0.75rem 1rem; font-size: 1rem; border-radius: 9999px; outline: none; width: 100%; }
        .input-custom:focus { border-color: white; }
        .input-custom::placeholder { color: rgba(255, 255, 255, 0.5); }
        .btn-action { border: 1px solid transparent; color: white; transition: all 0.3s ease; padding: 0.5rem 1.5rem; border-radius: 9999px; font-weight: 600; }
        .btn-action:hover { opacity: 0.9; }
        .btn-add { background-color: #0056D2; color: white; }
        .btn-add:hover { background-color: #0040a0; }
        table { border-collapse: collapse; width: 100%; }
        th, td { padding: 0.75rem; text-align: left; }
        th { background-color: #2a2a2a; color: white; }
        td { background-color: #1a1a1a; color: white; }
    </style>
</head>
<body class="flex items-center justify-center min-h-screen p-4">
    <div class="main-container w-full max-w-5xl h-[600px] md:h-[700px] rounded-3xl flex flex-col md:flex-row overflow-hidden">
        <div class="left-panel w-full md:w-1/3 flex items-center justify-center p-8">
            <div class="text-center">
                <img src="images/1logo_clean.png" alt="CleanSpace Logo" class="h-24 w-24 mx-auto">
                <h1 class="text-white text-4xl font-bold mt-4">CleanSpace</h1>
                <p class="text-white text-sm mt-2 opacity-75">Tu espacio, limpio y brillante.</p>
            </div>
        </div>
        <div class="right-panel w-full md:w-2/3 flex flex-col p-8">
            <h2 class="text-white text-2xl font-bold mb-6 text-center">Gestión de Inscritos</h2>
            <a href="admin_events.php" class="text-white text-sm mb-4">Volver a Gestión de Eventos</a>
            <table class="text-white w-full max-w-md mx-auto">
                <tr>
                    <th>Nombre</th>
                    <th>Evento</th>
                    <th>Fecha</th>
                    <th>Estado</th>
                    <th>Acciones</th>
                </tr>
                <?php foreach ($inscripciones as $inscripcion): ?>
                    <tr>
                        <td><?php echo "{$inscripcion['nombre']} {$inscripcion['apellido']}"; ?></td>
                        <td><?php echo $inscripcion['evento']; ?></td>
                        <td><?php echo $inscripcion['fecha']; ?></td>
                        <td><?php echo $inscripcion['estado']; ?></td>
                        <td>
                            <form method="POST" action="admin_users.php">
                                <input type="hidden" name="id_inscripcion" value="<?php echo $inscripcion['id']; ?>">
                                <select name="estado" class="input-custom">
                                    <option value="pendiente" <?php if ($inscripcion['estado'] == 'pendiente') echo 'selected'; ?>>Pendiente</option>
                                    <option value="aprobado" <?php if ($inscripcion['estado'] == 'aprobado') echo 'selected'; ?>>Aprobado</option>
                                    <option value="rechazado" <?php if ($inscripcion['estado'] == 'rechazado') echo 'selected'; ?>>Rechazado</option>
                                </select>
                                <input type="text" name="mensaje_personalizado" placeholder="Mensaje personalizado" class="input-custom">
                                <button type="submit" class="btn-action btn-add">Actualizar</button>
                            </form>
                        </td>
                    </tr>
                <?php endforeach; ?>
            </table>
        </div>
    </div>
</body>
</html>