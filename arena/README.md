# Arena Pass — Entradas 3D para el Amerant Bank Arena

Sitio de venta de entradas en 3D para el **Amerant Bank Arena** (Sunrise, FL — área de Fort Lauderdale).
Es un sitio estático (HTML + CSS + JS con Three.js desde CDN); no necesita PHP ni base de datos.

## Cómo verlo

```bash
cd arena
python3 -m http.server 8000
# abre http://localhost:8000
```

(Hay que servirlo por HTTP; abrir `index.html` directo con `file://` no carga los módulos.)

## Qué incluye

- **Vista aérea** del arena con estacionamientos, palmeras, lago y autopista; gira sola.
- **~18.000 asientos individuales** (Nivel 100, Nivel 300) y **16 suites** del nivel club.
- Pasa el mouse por una sección → precio y disponibilidad. Clic → la cámara vuela a la sección.
- Clic en un asiento → lo selecciona (máx. 8) y muestra **la vista real desde ese asiento**.
- **"Ver en 3D"** lleva la cámara a la altura de los ojos en ese asiento (arrastra para mirar alrededor).
- **Suites VIP** con su propia tarjeta y vista.
- 3 configuraciones según el evento: **hockey** (pista de hielo), **concierto** (escenario + sillas en la pista,
  secciones detrás del escenario bloqueadas) y **baloncesto** (cancha + courtside).
- Filtro de precio máximo, carrito, checkout con cargos e impuesto de FL (7%) y entradas con QR.

> Demo: los eventos, precios y disponibilidad son de ejemplo y no se procesa ningún pago.
> Para venta real habría que conectar el inventario y una pasarela de pago (p. ej. Stripe) en el backend.
