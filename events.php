<?php
require_once 'config.php';
session_start();
if (!isset($_SESSION['user_id'])) {
    header("Location: index.php");
    exit;
}
$conn = new mysqli(DB_HOST, DB_USER, DB_PASS, DB_NAME);
if ($conn->connect_error) die("Error: " . $conn->connect_error);
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $selected_events = $_POST['events'] ?? [];
    foreach ($selected_events as $event_id) {
        $query = "INSERT INTO inscripciones (id_usuario, id_evento, estado) VALUES (?, ?, 'pendiente')";
        $stmt = $conn->prepare($query);
        $stmt->bind_param("ii", $_SESSION['user_id'], $event_id);
        $stmt->execute();
        $stmt->close();
    }
    header("Location: final.php");
    exit;
}
// Modificación: Solo eventos publicados
$query = "SELECT id, fecha, nombre, CONCAT(hora_inicio, ' - ', hora_fin, ' PM') AS time, turno, restriccion FROM eventos WHERE estado_publicacion = 'publicado'";
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
    <title>CleanSpace - Eventos Disponibles</title>
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
        .event-item { background-color: #1a1a1a; border-radius: 9999px; padding: 0.75rem 1.5rem; display: flex; align-items: center; justify-content: space-between; cursor: pointer; transition: background-color 0.2s ease-in-out, border-color 0.2s ease-in-out; border: 1px solid transparent; }
        .event-item:hover:not(.disabled) { background-color: #2a2a2a; }
        .event-item.selected { border-color: #ffffff; background-color: #2a2a2a; }
        .event-item.disabled { opacity: 0.5; cursor: not-allowed; }
        .event-item input[type="checkbox"] { display: none; }
        .event-info { flex-grow: 1; color: white; }
        .event-time { color: rgba(255, 255, 255, 0.7); font-size: 0.9rem; }
        .event-name { font-weight: 600; }
        .pagination-controls { display: flex; justify-content: center; align-items: center; margin-top: 1.5rem; color: white; }
        .pagination-button { background-color: transparent; border: 1px solid rgba(255, 255, 255, 0.3); color: white; padding: 0.5rem 1rem; border-radius: 0.5rem; cursor: pointer; transition: background-color 0.2s ease; }
        .pagination-button:hover:not(:disabled) { background-color: rgba(255, 255, 255, 0.1); }
        .pagination-button:disabled { opacity: 0.5; cursor: not-allowed; }
        .pagination-number { margin: 0 1rem; font-weight: 600; }
    </style>
</head>
<body class="flex items-center justify-center min-h-screen p-4">
    <div class="main-container w-full max-w-5xl h-[600px] md:h-[700px] rounded-3xl flex flex-col md:flex-row overflow-hidden">
        <div class="left-panel w-full md:w-1/3 flex items-center justify-center p-8">
            <div class="text-center">
                <img src="images/1logo_clean.png" alt="CleanSpace Logo" class="h-24 w-24 mx-auto">
            </div>
        </div>
        <div class="right-panel w-full md:w-2/3 flex flex-col items-center p-8">
            <h2 class="text-white text-2xl font-bold mb-2">Eventos Disponibles</h2>
            <p class="text-white text-sm opacity-75 mb-6 text-center">Seleccione a los que pueda Asistir.</p>
            <form method="POST" action="events.php">
                <div id="event-list" class="flex flex-col gap-3 w-full max-w-md">
                    <?php foreach ($events as $index => $event): ?>
                        <?php if ($event['restriccion'] && $event['fecha'] === 'Agosto 2'): ?>
                            <p class="text-white text-xs opacity-60 text-right mt-1 mb-4">Únicamente puede seleccionar el 1er y 3er turno el mismo día</p>
                        <?php endif; ?>
                        <label class="event-item" data-date="<?php echo $event['fecha']; ?>" <?php if ($event['turno']) echo "data-turno='{$event['turno']}'"; ?>>
                            <input type="checkbox" name="events[]" value="<?php echo $event['id']; ?>">
                            <div class="event-info">
                                <div class="event-name"><?php echo $event['nombre']; ?></div>
                                <div class="event-time"><?php echo $event['time']; ?></div>
                            </div>
                        </label>
                    <?php endforeach; ?>
                </div>
                <div class="pagination-controls">
                    <button type="button" id="prev-page" class="pagination-button"><</button>
                    <span id="page-number" class="pagination-number">1</span>
                    <button type="button" id="next-page" class="pagination-button">></button>
                </div>
                <button type="submit" class="btn-submit w-64 py-3 rounded-full text-lg font-semibold mt-6 text-center">Enviar</button>
            </form>
        </div>
    </div>
    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const events = <?php echo json_encode($events); ?>;
            const eventsPerPage = 5;
            let currentPage = 0;
            const totalPages = Math.ceil(events.length / eventsPerPage);
            const eventListContainer = document.getElementById('event-list');
            const pageNumberSpan = document.getElementById('page-number');
            const prevPageBtn = document.getElementById('prev-page');
            const nextPageBtn = document.getElementById('next-page');

            function renderEvents() {
                eventListContainer.innerHTML = '';
                const start = currentPage * eventsPerPage;
                const end = start + eventsPerPage;
                const itemsToRender = events.slice(start, end);
                itemsToRender.forEach((itemData, index) => {
                    if (itemData.fecha === 'Agosto 2' && itemData.restriccion) {
                        const note = document.createElement('p');
                        note.className = 'text-white text-xs opacity-60 text-right mt-1 mb-4';
                        note.textContent = 'Únicamente puede seleccionar el 1er y 3er turno el mismo día';
                        eventListContainer.appendChild(note);
                    }
                    const label = document.createElement('label');
                    label.className = 'event-item';
                    label.dataset.date = itemData.fecha;
                    if (itemData.turno) label.dataset.turno = itemData.turno;
                    const input = document.createElement('input');
                    input.type = 'checkbox';
                    input.name = `events[]`;
                    input.value = itemData.id;
                    input.addEventListener('change', () => {
                        label.classList.toggle('selected', input.checked);
                        applyAgosto2Restriction();
                    });
                    label.appendChild(input);
                    const eventInfoDiv = document.createElement('div');
                    eventInfoDiv.className = 'event-info';
                    eventInfoDiv.innerHTML = `<div class="event-name">${itemData.nombre}</div><div class="event-time">${itemData.time}</div>`;
                    label.appendChild(eventInfoDiv);
                    eventListContainer.appendChild(label);
                });
                updatePaginationControls();
                applyAgosto2Restriction();
            }

            function updatePaginationControls() {
                pageNumberSpan.textContent = currentPage + 1;
                prevPageBtn.disabled = currentPage === 0;
                nextPageBtn.disabled = currentPage === totalPages - 1;
            }

            prevPageBtn.addEventListener('click', () => {
                if (currentPage > 0) {
                    currentPage--;
                    renderEvents();
                }
            });

            nextPageBtn.addEventListener('click', () => {
                if (currentPage < totalPages - 1) {
                    currentPage++;
                    renderEvents();
                }
            });

            function applyAgosto2Restriction() {
                const agosto2Checkboxes = Array.from(eventListContainer.querySelectorAll('.event-item[data-date="Agosto 2"] input[type="checkbox"]'));
                if (agosto2Checkboxes.length > 0) {
                    const t1 = agosto2Checkboxes.find(cb => cb.closest('.event-item').dataset.turno === '1');
                    const t2 = agosto2Checkboxes.find(cb => cb.closest('.event-item').dataset.turno === '2');
                    const t3 = agosto2Checkboxes.find(cb => cb.closest('.event-item').dataset.turno === '3');
                    agosto2Checkboxes.forEach(cb => {
                        cb.disabled = false;
                        cb.closest('.event-item').classList.remove('disabled');
                    });
                    if (t1 && t2 && t3) {
                        const t1Checked = t1.checked;
                        const t2Checked = t2.checked;
                        const t3Checked = t3.checked;
                        if (t1Checked || t3Checked) {
                            t2.disabled = true;
                            t2.closest('.event-item').classList.add('disabled');
                            if (t2Checked) {
                                t2.checked = false;
                                t2.closest('.event-item').classList.remove('selected');
                            }
                        } else if (t2Checked) {
                            t1.disabled = true;
                            t1.closest('.event-item').classList.add('disabled');
                            t3.disabled = true;
                            t3.closest('.event-item').classList.add('disabled');
                            if (t1Checked) {
                                t1.checked = false;
                                t1.closest('.event-item').classList.remove('selected');
                            }
                            if (t3Checked) {
                                t3.checked = false;
                                t3.closest('.event-item').classList.remove('selected');
                            }
                        }
                    }
                }
            }
            renderEvents();
        });
    </script>
</body>
</html>