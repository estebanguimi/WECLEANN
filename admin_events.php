<?php
require_once 'config.php';
session_start();
if (!isset($_SESSION['user_id']) || !$_SESSION['es_admin']) {
    header("Location: index.php");
    exit;
}
$conn = new mysqli(DB_HOST, DB_USER, DB_PASS, DB_NAME);
if ($conn->connect_error) die("Error: " . $conn->connect_error);

// Agregar nuevo evento
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['add_event'])) {
    $fecha = $_POST['event-date'];
    $nombre = $_POST['event-name'];
    $hora_inicio = $_POST['event-start-time'];
    $hora_fin = $_POST['event-end-time'];
    $turno = $_POST['event-turno'] ?: null;
    $restriccion = isset($_POST['event-restriction']) ? 1 : 0;
    $ubicacion = $_POST['event-location'] ?: null;
    $estado_publicacion = $_POST['estado_publicacion'] ?: 'borrador';
    $descripcion = $_POST['event-description'] ?: null;
    $query = "INSERT INTO eventos (fecha, nombre, hora_inicio, hora_fin, turno, restriccion, ubicacion, estado_publicacion, descripcion) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)";
    $stmt = $conn->prepare($query);
    $stmt->bind_param("ssssssiss", $fecha, $nombre, $hora_inicio, $hora_fin, $turno, $restriccion, $ubicacion, $estado_publicacion, $descripcion);
    $stmt->execute();
    $stmt->close();
}

// Editar evento existente
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['edit_event'])) {
    $id = $_POST['event_id'];
    $fecha = $_POST['event-date'];
    $nombre = $_POST['event-name'];
    $hora_inicio = $_POST['event-start-time'];
    $hora_fin = $_POST['event-end-time'];
    $turno = $_POST['event-turno'] ?: null;
    $restriccion = isset($_POST['event-restriction']) ? 1 : 0;
    $ubicacion = $_POST['event-location'] ?: null;
    $estado_publicacion = $_POST['estado_publicacion'] ?: 'borrador';
    $descripcion = $_POST['event-description'] ?: null;
    $query = "UPDATE eventos SET fecha = ?, nombre = ?, hora_inicio = ?, hora_fin = ?, turno = ?, restriccion = ?, ubicacion = ?, estado_publicacion = ?, descripcion = ? WHERE id = ?";
    $stmt = $conn->prepare($query);
    $stmt->bind_param("ssssssissi", $fecha, $nombre, $hora_inicio, $hora_fin, $turno, $restriccion, $ubicacion, $estado_publicacion, $descripcion, $id);
    $stmt->execute();
    $stmt->close();
}

// Eliminar evento
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['delete_event'])) {
    $id = $_POST['event_id'];
    $query = "DELETE FROM eventos WHERE id = ?";
    $stmt = $conn->prepare($query);
    $stmt->bind_param("i", $id);
    $stmt->execute();
    $stmt->close();
}

// Obtener eventos
$query = "SELECT * FROM eventos";
$result = $conn->query($query);
$events = [];
while ($row = $result->fetch_assoc()) {
    $events[] = $row;
}
$conn->close();
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CleanSpace - Gestión de Eventos</title>
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
        .btn-remove { background-color: #550000; color: white; padding: 0.4rem 0.8rem; font-size: 0.875rem; }
        .btn-remove:hover { background-color: #770000; }
        .btn-edit { background-color: #FFD700; color: #0d0d0d; }
        .btn-edit:hover { background-color: #e6c200; }
        .event-list-item { background-color: #1a1a1a; border-radius: 0.75rem; padding: 1rem 1.5rem; display: flex; align-items: center; justify-content: space-between; color: white; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2); }
        .event-list-item-info { flex-grow: 1; }
        .event-list-item-name { font-weight: 600; font-size: 1.1rem; }
        .event-list-item-details { font-size: 0.9rem; opacity: 0.7; }
        .event-list-item-details span { margin-right: 0.5rem; }
        .event-list-item-details .restriction-note { color: #FFD700; font-style: italic; }
        .edit-form { display: none; margin-top: 1rem; }
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
            <h2 class="text-white text-2xl font-bold mb-6 text-center">Gestión de Eventos</h2>
            <div class="bg-[#222222] p-6 rounded-xl mb-8 w-full max-w-md mx-auto">
                <h3 class="text-white text-lg font-semibold mb-4 text-center">Agregar Nuevo Evento</h3>
                <form method="POST" action="admin_events.php">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                        <input type="text" name="event-date" placeholder="Fecha (Ej: Agosto 2)" class="input-custom col-span-full" required>
                        <input type="text" name="event-name" placeholder="Nombre Evento (Ej: Turno 1)" class="input-custom col-span-full" required>
                        <input type="text" name="event-start-time" placeholder="Hora Inicio (Ej: 13:00)" class="input-custom" required>
                        <input type="text" name="event-end-time" placeholder="Hora Fin (Ej: 18:00)" class="input-custom" required>
                        <input type="text" name="event-turno" placeholder="Turno (1, 2, 3)" class="input-custom">
                        <input type="text" name="event-location" placeholder="Ubicación" class="input-custom col-span-full">
                        <textarea name="event-description" placeholder="Descripción" class="input-custom col-span-full h-24 resize-none"></textarea>
                        <div class="col-span-full flex items-center justify-center">
                            <input type="checkbox" name="event-restriction" id="event-restriction" class="mr-2">
                            <label for="event-restriction" class="text-white text-sm opacity-75">¿Tiene restricción de turno?</label>
                        </div>
                        <select name="estado_publicacion" class="input-custom col-span-full">
                            <option value="borrador">Borrador</option>
                            <option value="publicado">Publicado</option>
                        </select>
                    </div>
                    <button type="submit" name="add_event" class="btn-action btn-add w-full py-3">Agregar Evento</button>
                </form>
            </div>
            <div class="w-full max-w-md mx-auto">
                <h3 class="text-white text-lg font-semibold mb-4 text-center">Eventos Actuales</h3>
                <div id="events-list-container" class="flex flex-col gap-3">
                    <?php if (empty($events)): ?>
                        <p class="text-white opacity-75 text-center">No hay eventos para mostrar.</p>
                    <?php else: ?>
                        <?php foreach ($events as $event): ?>
                            <div class="event-list-item">
                                <div class="event-list-item-info">
                                    <div class="event-list-item-name"><?php echo $event['nombre']; ?></div>
                                    <div class="event-list-item-details">
                                        <span><?php echo $event['fecha']; ?></span> | <span><?php echo $event['hora_inicio'] . ' - ' . $event['hora_fin'] . ' PM'; ?></span>
                                        <?php if ($event['turno']): ?><span>Turno: <?php echo $event['turno']; ?></span><?php endif; ?>
                                        <?php if ($event['restriccion']): ?><span class="restriction-note">(Con restricción)</span><?php endif; ?>
                                        <?php if ($event['ubicacion']): ?><span>Ubicación: <?php echo $event['ubicacion']; ?></span><?php endif; ?>
                                        <span>Estado: <?php echo $event['estado_publicacion']; ?></span>
                                    </div>
                                </div>
                                <div>
                                    <form method="POST" action="admin_events.php" class="inline">
                                        <input type="hidden" name="event_id" value="<?php echo $event['id']; ?>">
                                        <button type="submit" name="delete_event" class="btn-action btn-remove mr-2">Eliminar</button>
                                    </form>
                                    <button type="button" class="btn-action btn-edit mr-2" onclick="toggleEditForm(<?php echo $event['id']; ?>)">Editar</button>
                                </div>
                            </div>
                            <!-- Formulario de edición -->
                            <div id="edit-form-<?php echo $event['id']; ?>" class="edit-form">
                                <form method="POST" action="admin_events.php">
                                    <input type="hidden" name="event_id" value="<?php echo $event['id']; ?>">
                                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                                        <input type="text" name="event-date" value="<?php echo $event['fecha']; ?>" class="input-custom col-span-full" required>
                                        <input type="text" name="event-name" value="<?php echo $event['nombre']; ?>" class="input-custom col-span-full" required>
                                        <input type="text" name="event-start-time" value="<?php echo $event['hora_inicio']; ?>" class="input-custom" required>
                                        <input type="text" name="event-end-time" value="<?php echo $event['hora_fin']; ?>" class="input-custom" required>
                                        <input type="text" name="event-turno" value="<?php echo $event['turno']; ?>" class="input-custom">
                                        <input type="text" name="event-location" value="<?php echo $event['ubicacion']; ?>" class="input-custom col-span-full">
                                        <textarea name="event-description" class="input-custom col-span-full h-24 resize-none"><?php echo $event['descripcion']; ?></textarea>
                                        <div class="col-span-full flex items-center">
                                            <input type="checkbox" name="event-restriction" id="edit-restriction-<?php echo $event['id']; ?>" <?php if ($event['restriccion']) echo 'checked'; ?> class="mr-2">
                                            <label for="edit-restriction-<?php echo $event['id']; ?>" class="text-white text-sm opacity-75">¿Tiene restricción de turno?</label>
                                        </div>
                                        <select name="estado_publicacion" class="input-custom col-span-full">
                                            <option value="borrador" <?php if ($event['estado_publicacion'] == 'borrador') echo 'selected'; ?>>Borrador</option>
                                            <option value="publicado" <?php if ($event['estado_publicacion'] == 'publicado') echo 'selected'; ?>>Publicado</option>
                                        </select>
                                    </div>
                                    <button type="submit" name="edit_event" class="btn-action btn-add w-full py-3">Guardar Cambios</button>
                                </form>
                            </div>
                        <?php endforeach; ?>
                    <?php endif; ?>
                </div>
            </div>
        </div>
    </div>
    <script>
        function toggleEditForm(id) {
            const form = document.getElementById(`edit-form-${id}`);
            form.style.display = form.style.display === 'none' ? 'block' : 'none';
        }
    </script>
</body>
</html>