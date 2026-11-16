// Arena Pass — 3D ticketing for Amerant Bank Arena (Sunrise, FL · Fort Lauderdale area)
// Units: 1 world unit = 1 foot. Rink centred at the origin, long axis on X.
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';

const TAU = Math.PI * 2;
const $ = (s) => document.querySelector(s);
const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
const fmt = (n) => '$' + Math.round(n).toLocaleString('en-US');
const round5 = (n) => Math.round(n / 5) * 5;
const easeInOut = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
function mulberry(seed) {
  return () => {
    seed |= 0; seed = (seed + 0x6d2b79f5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

// ------------------------------------------------------------------ events
const EVENTS = [
  { id: 'hk1', type: 'hockey', title: 'Hockey profesional', sub: 'Temporada regular · Noche de rivalidad', date: 'Sáb 21 Nov 2026', short: 'Sáb 21 Nov', time: '7:00 PM', base: 95, seed: 11 },
  { id: 'cn1', type: 'concert', title: 'Noche Latina — Gira 2026', sub: 'Concierto · Escenario al fondo este', date: 'Vie 4 Dic 2026', short: 'Vie 4 Dic', time: '8:00 PM', base: 120, seed: 23 },
  { id: 'bb1', type: 'basketball', title: 'Showcase de Baloncesto', sub: 'Universitario · Doble cartelera', date: 'Sáb 12 Dic 2026', short: 'Sáb 12 Dic', time: '6:30 PM', base: 70, seed: 37 },
  { id: 'hk2', type: 'hockey', title: 'Hockey · Especial Fin de Año', sub: 'Temporada regular', date: 'Mié 30 Dic 2026', short: 'Mié 30 Dic', time: '7:30 PM', base: 110, seed: 51 },
];
const MAX_TICKETS = 8;

// ------------------------------------------------------------------ bowl geometry
// The bowl is a family of offset rounded rectangles around the rink (200 x 85 ft, 28 ft corners).
// pt(d, t): point at offset d (ft from the boards) and parameter t ∈ [0,1).
// t is arc-length at a reference offset, split per piece, so equal t at any d lies on the same normal
// line — aisles come out radial, like a real bowl.
const RA = 100, RB = 42.5, RR = 28, SA = RA - RR, SB = RB - RR, DREF = 45;
const PIECES = (() => {
  const q = (Math.PI / 2) * (RR + DREF);
  const L = [SB, q, 2 * SA, q, 2 * SB, q, 2 * SA, q, SB];
  const tot = L.reduce((a, b) => a + b);
  let acc = 0;
  return L.map((l) => { const p = { t0: acc / tot, t1: (acc + l) / tot }; acc += l; return p; });
})();
function pt(d, t) {
  t = ((t % 1) + 1) % 1;
  let i = 0;
  while (i < 8 && t > PIECES[i].t1) i++;
  const f = (t - PIECES[i].t0) / (PIECES[i].t1 - PIECES[i].t0);
  const A = RA + d, B = RB + d, R = RR + d;
  const arc = (cx, cz, a0) => { const a = a0 + f * Math.PI / 2, c = Math.cos(a), s = Math.sin(a); return { x: cx + R * c, z: cz + R * s, nx: c, nz: s }; };
  switch (i) {
    case 0: return { x: A, z: f * SB, nx: 1, nz: 0 };
    case 1: return arc(SA, SB, 0);
    case 2: return { x: SA - f * 2 * SA, z: B, nx: 0, nz: 1 };
    case 3: return arc(-SA, SB, Math.PI / 2);
    case 4: return { x: -A, z: SB - f * 2 * SB, nx: -1, nz: 0 };
    case 5: return arc(-SA, -SB, Math.PI);
    case 6: return { x: -SA + f * 2 * SA, z: -B, nx: 0, nz: -1 };
    case 7: return arc(SA, -SB, 1.5 * Math.PI);
    default: return { x: A, z: -SB + f * SB, nx: 1, nz: 0 };
  }
}
function zAtX(d, x) { // |z| of the offset curve at a given x (upper half)
  x = Math.abs(x);
  if (x <= SA) return RB + d;
  const R = RR + d;
  return SB + Math.sqrt(Math.max(0, R * R - (x - SA) * (x - SA)));
}
const T_TOP = (PIECES[2].t0 + PIECES[2].t1) / 2;

function loop(d, n = 300) { const a = []; for (let i = 0; i <= n; i++) a.push(pt(d, i / n)); return a; }
function makeGeo(pos, uv) {
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
  if (uv) g.setAttribute('uv', new THREE.Float32BufferAttribute(uv, 2));
  g.computeVertexNormals();
  return g;
}
function wallGeo(d, y0, y1, uLen = 0) {
  const L = loop(d), pos = [], uv = [];
  let acc = 0;
  for (let i = 0; i < L.length - 1; i++) {
    const p = L[i], q = L[i + 1], seg = Math.hypot(q.x - p.x, q.z - p.z);
    const u0 = uLen ? acc / uLen : i / (L.length - 1), u1 = uLen ? (acc + seg) / uLen : (i + 1) / (L.length - 1);
    acc += seg;
    pos.push(p.x, y0, p.z, q.x, y0, q.z, q.x, y1, q.z, p.x, y0, p.z, q.x, y1, q.z, p.x, y1, p.z);
    uv.push(u0, 0, u1, 0, u1, 1, u0, 0, u1, 1, u0, 1);
  }
  return makeGeo(pos, uv);
}
function ringGeo(d0, d1, y) {
  const A = loop(d0), B = loop(d1), pos = [];
  for (let i = 0; i < A.length - 1; i++) {
    const a = A[i], b = A[i + 1], c = B[i + 1], e = B[i];
    pos.push(a.x, y, a.z, b.x, y, b.z, c.x, y, c.z, a.x, y, a.z, c.x, y, c.z, e.x, y, e.z);
  }
  return makeGeo(pos);
}
function discGeo(d, y) {
  const shape = new THREE.Shape(loop(d, 200).map((p) => new THREE.Vector2(p.x, -p.z)));
  const g = new THREE.ShapeGeometry(shape, 4);
  g.rotateX(-Math.PI / 2);
  g.translate(0, y, 0);
  return g;
}
function planarUV(g, x0, z0, w, h) {
  const p = g.attributes.position, uv = [];
  for (let i = 0; i < p.count; i++) uv.push((p.getX(i) - x0) / w, 1 - (p.getZ(i) - z0) / h);
  g.setAttribute('uv', new THREE.Float32BufferAttribute(uv, 2));
  return g;
}

// ------------------------------------------------------------------ renderer / scene
const canvas = $('#scene');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, powerPreference: 'high-performance' });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.05;
renderer.outputColorSpace = THREE.SRGBColorSpace;

const scene = new THREE.Scene();
scene.background = (() => {
  const c = document.createElement('canvas'); c.width = 4; c.height = 512;
  const g = c.getContext('2d'), gr = g.createLinearGradient(0, 0, 0, 512);
  gr.addColorStop(0, '#2f6fc4'); gr.addColorStop(0.55, '#8cc0ec'); gr.addColorStop(1, '#e6f0f7');
  g.fillStyle = gr; g.fillRect(0, 0, 4, 512);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
})();
scene.fog = new THREE.Fog(0xd5e6f3, 1900, 5600);

const camera = new THREE.PerspectiveCamera(42, 1, 1, 9000);
camera.position.set(1500, 1100, 1700);
const controls = new OrbitControls(camera, canvas);
controls.enableDamping = true;
controls.dampingFactor = 0.08;

scene.add(new THREE.HemisphereLight(0xdcecff, 0x5b6b3c, 1.15));
const sun = new THREE.DirectionalLight(0xfff1dc, 2.3);
sun.position.set(380, 720, 300);
sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048);
Object.assign(sun.shadow.camera, { left: -340, right: 340, top: 340, bottom: -340, near: 200, far: 1600 });
sun.shadow.bias = -0.0004;
sun.shadow.normalBias = 0.6;
scene.add(sun);

const MAT = {
  concrete: new THREE.MeshStandardMaterial({ color: 0x8b9199, roughness: 0.92, side: THREE.DoubleSide }),
  floor: new THREE.MeshStandardMaterial({ color: 0x23262d, roughness: 0.85 }),
  ledge: new THREE.MeshStandardMaterial({ color: 0x3a3f48, roughness: 0.8, side: THREE.DoubleSide }),
  rim: new THREE.MeshStandardMaterial({ color: 0xd9dde3, roughness: 0.55, metalness: 0.25, side: THREE.DoubleSide }),
  steel: new THREE.MeshStandardMaterial({ color: 0xf2f4f7, roughness: 0.4, metalness: 0.5 }),
  white: new THREE.MeshStandardMaterial({ color: 0xf5f7fa, roughness: 0.5, side: THREE.DoubleSide }),
  dark: new THREE.MeshStandardMaterial({ color: 0x15181d, roughness: 0.7 }),
  seat: new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.55 }),
  glass: new THREE.MeshStandardMaterial({ color: 0xcfe7ff, transparent: true, opacity: 0.16, roughness: 0.05, depthWrite: false, side: THREE.DoubleSide }),
  hit: new THREE.MeshBasicMaterial({ visible: false }),
};

// ------------------------------------------------------------------ canvas textures
function canvasTex(w, h, draw, opts = {}) {
  const c = document.createElement('canvas'); c.width = w; c.height = h;
  draw(c.getContext('2d'), w, h);
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  t.anisotropy = 8;
  if (opts.repeat) { t.wrapS = THREE.RepeatWrapping; t.wrapT = THREE.RepeatWrapping; }
  t.userData.canvas = c;
  return t;
}
function noise(g, w, h, n, a, colors) {
  const r = mulberry(7);
  for (let i = 0; i < n; i++) { g.fillStyle = colors[(r() * colors.length) | 0]; g.globalAlpha = a * r(); g.fillRect(r() * w, r() * h, 1 + r() * 3, 1 + r() * 3); }
  g.globalAlpha = 1;
}

const iceTex = canvasTex(2000, 850, (g) => {
  const X = (x) => (x + 100) * 10, Z = (z) => (z + 42.5) * 10;
  g.fillStyle = '#eef5fb'; g.fillRect(0, 0, 2000, 850);
  noise(g, 2000, 850, 9000, 0.25, ['#d6e4f1', '#ffffff', '#c9dbeb']);
  const line = (x, w, c) => { g.fillStyle = c; g.fillRect(X(x) - w * 5, 0, w * 10, 850); };
  line(0, 1, '#c8102e'); line(-25, 1, '#0b3d91'); line(25, 1, '#0b3d91');
  line(-89, 0.25, '#c8102e'); line(89, 0.25, '#c8102e');
  const circle = (x, z, r, c, lw) => { g.beginPath(); g.arc(X(x), Z(z), r * 10, 0, TAU); g.strokeStyle = c; g.lineWidth = lw; g.stroke(); };
  const dot = (x, z, r, c) => { g.beginPath(); g.arc(X(x), Z(z), r * 10, 0, TAU); g.fillStyle = c; g.fill(); };
  circle(0, 0, 15, '#0b3d91', 3); dot(0, 0, 0.5, '#0b3d91');
  for (const sx of [-1, 1]) for (const sz of [-1, 1]) { circle(sx * 69, sz * 22, 15, '#c8102e', 3); dot(sx * 69, sz * 22, 1, '#c8102e'); dot(sx * 20, sz * 22, 1, '#c8102e'); }
  for (const sx of [-1, 1]) { // creases
    g.beginPath(); g.moveTo(X(sx * 89), Z(-4)); g.arc(X(sx * 89), Z(0), 60, sx > 0 ? Math.PI / 2 : -Math.PI / 2, sx > 0 ? 1.5 * Math.PI : Math.PI / 2, false);
    g.closePath(); g.fillStyle = '#7fb2e6'; g.fill(); g.strokeStyle = '#c8102e'; g.lineWidth = 2; g.stroke();
  }
  // centre-ice emblem (generic)
  g.save(); g.translate(X(0), Z(0));
  g.beginPath(); g.arc(0, 0, 120, 0, TAU); g.fillStyle = 'rgba(224,34,58,.85)'; g.fill();
  g.beginPath(); g.arc(0, 0, 104, 0, TAU); g.strokeStyle = '#ffc53d'; g.lineWidth = 6; g.stroke();
  g.fillStyle = '#fff'; g.font = '800 46px Inter, sans-serif'; g.textAlign = 'center'; g.textBaseline = 'middle';
  g.fillText('SUNRISE', 0, -12); g.font = '700 22px Inter, sans-serif'; g.fillText('FLORIDA', 0, 30);
  g.restore();
});

const courtTex = canvasTex(1880, 1000, (g, w, h) => {
  const X = (x) => (x + 47) * 20, Z = (z) => (z + 25) * 20;
  for (let i = 0; i < 50; i++) { g.fillStyle = i % 2 ? '#d7a46a' : '#cf9c60'; g.fillRect(0, i * 20, w, 20); }
  noise(g, w, h, 12000, 0.18, ['#b98546', '#e6b67c']);
  g.strokeStyle = '#fff'; g.lineWidth = 5;
  g.strokeRect(6, 6, w - 12, h - 12);
  g.beginPath(); g.moveTo(X(0), 0); g.lineTo(X(0), h); g.stroke();
  g.beginPath(); g.arc(X(0), Z(0), 120, 0, TAU); g.fillStyle = '#e0223a'; g.fill(); g.stroke();
  for (const s of [-1, 1]) {
    const bx = s * 41.75; // basket
    g.fillStyle = 'rgba(224,34,58,.9)';
    const kx0 = s > 0 ? X(47 - 19) : X(-47), kw = 19 * 20;
    g.fillRect(kx0, Z(-8), kw, 16 * 20); g.strokeRect(kx0, Z(-8), kw, 16 * 20);
    g.beginPath(); g.arc(X(s * 28), Z(0), 120, 0, TAU); g.stroke();
    g.beginPath(); // 3-pt line
    g.moveTo(X(s * 47), Z(-22)); g.lineTo(X(s * 33), Z(-22));
    g.arc(X(bx), Z(0), 23.75 * 20, s > 0 ? Math.PI + 1.18 : -1.18 + 0, s > 0 ? Math.PI - 1.18 : 1.18, s > 0);
    g.lineTo(X(s * 47), Z(22)); g.stroke();
  }
  g.fillStyle = 'rgba(255,255,255,.95)'; g.font = '800 64px Inter, sans-serif'; g.textAlign = 'center'; g.textBaseline = 'middle';
  g.fillText('SUNRISE', X(0), Z(0));
});

const ribbonTex = canvasTex(2048, 64, (g, w, h) => {
  const segs = [['#e0223a', '#fff', 'AMERANT BANK ARENA'], ['#0d1220', '#ffc53d', 'SUNRISE · FLORIDA'], ['#ffffff', '#0d1220', 'ARENA PASS'], ['#0d1220', '#ffffff', 'FORT LAUDERDALE']];
  const sw = w / segs.length;
  segs.forEach(([bg, fg, txt], i) => {
    g.fillStyle = bg; g.fillRect(i * sw, 0, sw, h);
    g.fillStyle = fg; g.font = '800 38px Inter, sans-serif'; g.textAlign = 'center'; g.textBaseline = 'middle';
    g.fillText(txt, i * sw + sw / 2, h / 2 + 2);
  });
}, { repeat: true });
const ribbonMat = new THREE.MeshStandardMaterial({ map: ribbonTex, emissive: 0xffffff, emissiveMap: ribbonTex, emissiveIntensity: 0.9, side: THREE.DoubleSide });

const facadeTex = canvasTex(512, 512, (g, w, h) => {
  const gr = g.createLinearGradient(0, 0, 0, h);
  gr.addColorStop(0, '#dfe3e8'); gr.addColorStop(0.22, '#c5cbd3'); gr.addColorStop(0.24, '#273548'); gr.addColorStop(1, '#16202e');
  g.fillStyle = gr; g.fillRect(0, 0, w, h);
  g.fillStyle = 'rgba(160,200,240,.18)';
  for (let y = 140; y < h; y += 70) g.fillRect(0, y, w, 4);
  g.fillStyle = '#9aa4b1';
  for (let x = 0; x < w; x += 64) g.fillRect(x, 120, 4, h);
  g.fillStyle = '#e0223a'; g.fillRect(0, 118, w, 8);
}, { repeat: true });

function screenTex(lines, w = 640, h = 360, bg = ['#0b1430', '#3a0d18']) {
  return canvasTex(w, h, (g) => {
    const gr = g.createLinearGradient(0, 0, w, h); gr.addColorStop(0, bg[0]); gr.addColorStop(1, bg[1]);
    g.fillStyle = gr; g.fillRect(0, 0, w, h);
    g.textAlign = 'center'; g.textBaseline = 'middle';
    lines.forEach(([txt, size, color, y]) => { g.fillStyle = color; g.font = `800 ${size}px Inter, sans-serif`; g.fillText(txt, w / 2, y * h); });
  });
}

// ------------------------------------------------------------------ static world: ground, plaza, lots, palms
const world = new THREE.Group(); scene.add(world);
{
  const ground = new THREE.Mesh(new THREE.PlaneGeometry(12000, 12000), new THREE.MeshStandardMaterial({ color: 0x7ea65a, roughness: 1 }));
  ground.rotation.x = -Math.PI / 2; ground.receiveShadow = true; world.add(ground);

  const plaza = new THREE.Mesh(ringGeo(150, 202, 0.15), new THREE.MeshStandardMaterial({ color: 0xd8d2c4, roughness: 0.95, side: THREE.DoubleSide }));
  plaza.receiveShadow = true; world.add(plaza);
  const road = new THREE.Mesh(ringGeo(202, 232, 0.2), new THREE.MeshStandardMaterial({ color: 0x41454c, roughness: 0.9, side: THREE.DoubleSide }));
  road.receiveShadow = true; world.add(road);
  world.add(new THREE.Mesh(ringGeo(216.6, 217.4, 0.26), new THREE.MeshBasicMaterial({ color: 0xf2c94c, side: THREE.DoubleSide })));
  const inner = new THREE.Mesh(discGeo(150, 0.1), MAT.floor); inner.receiveShadow = true; world.add(inner);

  // parking lots + cars
  const carGeo = (() => { const b = new THREE.BoxGeometry(6, 3.4, 14.5); b.translate(0, 2.2, 0); const c = new THREE.BoxGeometry(5.4, 2.2, 7.5); c.translate(0, 4.9, -0.5); return mergeGeometries([b, c]); })();
  const carCols = ['#f4f4f4', '#1d1f24', '#9aa1aa', '#c9ccd1', '#b3202b', '#24427a', '#3d4a3e', '#e7e2d6'].map((c) => new THREE.Color(c));
  const carMats = [];
  function lot(cx, cz, w, h, seed) {
    const r = mulberry(seed);
    const tex = canvasTex(Math.round(w * 2), Math.round(h * 2), (g, W, H) => {
      g.fillStyle = '#3c4047'; g.fillRect(0, 0, W, H);
      noise(g, W, H, 6000, 0.25, ['#2f3238', '#4a4f57']);
      g.fillStyle = '#e9e9e9';
      for (let m = 0; 12 + m * 60 + 60 < h; m++) {
        const y0 = 12 + m * 60;
        for (const [a, b] of [[y0, y0 + 18], [y0 + 42, y0 + 60]]) for (let x = 10; x <= w - 10; x += 9) g.fillRect(x * 2, a * 2, 1.5, (b - a) * 2);
      }
    });
    const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshStandardMaterial({ map: tex, roughness: 0.95 }));
    m.rotation.x = -Math.PI / 2; m.position.set(cx, 0.12, cz); m.receiveShadow = true; world.add(m);
    for (let mm = 0; 12 + mm * 60 + 60 < h; mm++) {
      const y0 = 12 + mm * 60;
      for (const zc of [y0 + 9, y0 + 51]) for (let x = 14.5; x < w - 10; x += 9) if (r() < 0.62) carMats.push([cx - w / 2 + x, cz - h / 2 + zc, carCols[(r() * carCols.length) | 0]]);
    }
  }
  lot(0, -470, 820, 340, 3); lot(0, 470, 820, 340, 4); lot(-540, 0, 340, 600, 5);
  const cars = new THREE.InstancedMesh(carGeo, new THREE.MeshStandardMaterial({ roughness: 0.35, metalness: 0.4 }), carMats.length);
  const o = new THREE.Object3D();
  carMats.forEach(([x, z, c], i) => { o.position.set(x, 0, z); o.rotation.set(0, 0, 0); o.updateMatrix(); cars.setMatrixAt(i, o.matrix); cars.setColorAt(i, c); });
  cars.castShadow = true; world.add(cars);

  // lake (east) and highway (north)
  const lakeShape = new THREE.Shape();
  for (let i = 0; i <= 64; i++) { const a = i / 64 * TAU, rr = 1 + 0.12 * Math.sin(a * 3) + 0.06 * Math.cos(a * 5); const px = 560 + 170 * rr * Math.cos(a), pz = 40 + 260 * rr * Math.sin(a); i ? lakeShape.lineTo(px, -pz) : lakeShape.moveTo(px, -pz); }
  const lakeG = new THREE.ShapeGeometry(lakeShape); lakeG.rotateX(-Math.PI / 2); lakeG.translate(0, 0.3, 0);
  world.add(new THREE.Mesh(lakeG, new THREE.MeshStandardMaterial({ color: 0x3f8db3, roughness: 0.12, metalness: 0.2 })));
  const hwTex = canvasTex(512, 160, (g, W, H) => { g.fillStyle = '#383c42'; g.fillRect(0, 0, W, H); g.fillStyle = '#eee'; for (const y of [38, 58, 102, 122]) for (let x = 0; x < W; x += 64) g.fillRect(x, y, 32, 3); g.fillStyle = '#f2c94c'; g.fillRect(0, 78, W, 4); }, { repeat: true });
  hwTex.repeat.set(40, 1);
  const hw = new THREE.Mesh(new THREE.PlaneGeometry(8000, 90), new THREE.MeshStandardMaterial({ map: hwTex, roughness: 0.9 }));
  hw.rotation.x = -Math.PI / 2; hw.position.set(0, 0.2, -820); world.add(hw);
  // distant low-rise buildings
  const r = mulberry(99), bGeo = new THREE.BoxGeometry(1, 1, 1); bGeo.translate(0, 0.5, 0);
  const blds = new THREE.InstancedMesh(bGeo, new THREE.MeshStandardMaterial({ color: 0xe9e6df, roughness: 0.8 }), 70);
  for (let i = 0; i < 70; i++) {
    let x, z; do { x = (r() - 0.5) * 4200; z = (r() - 0.5) * 4200; } while (Math.abs(x) < 900 && Math.abs(z) < 900 || Math.abs(z + 820) < 80);
    o.position.set(x, 0, z); o.rotation.set(0, r() * 0.4, 0); o.scale.set(80 + r() * 220, 20 + r() * 50, 60 + r() * 160); o.updateMatrix();
    blds.setMatrixAt(i, o.matrix); blds.setColorAt(i, new THREE.Color().setHSL(0.08, 0.08, 0.78 + r() * 0.15));
  }
  world.add(blds);
  o.scale.set(1, 1, 1);

  // palms
  const trunk = new THREE.CylinderGeometry(0.55, 0.95, 1, 6); trunk.translate(0, 0.5, 0);
  const leaves = [];
  for (let k = 0; k < 9; k++) { const g = new THREE.ConeGeometry(1.7, 14, 4, 1); g.rotateX(Math.PI / 2); g.scale(1, 0.22, 1); g.translate(0, 0, 7); g.rotateX(0.3 + (k % 2) * 0.3); g.rotateY((k / 9) * TAU); leaves.push(g); }
  const frondGeo = mergeGeometries(leaves);
  const spots = [];
  loop(178, 70).slice(0, 70).forEach((p) => spots.push([p.x, p.z]));
  loop(250, 56).slice(0, 56).forEach((p) => { if (Math.abs(p.x) > 330 || Math.abs(p.z) > 270 || true) spots.push([p.x, p.z]); });
  for (let x = -400; x <= 400; x += 50) { spots.push([x, -285]); spots.push([x, 285]); spots.push([x, -655]); spots.push([x, 655]); }
  for (let i = 0; i < 46; i++) { const a = (i / 46) * TAU; spots.push([560 + 215 * Math.cos(a), 40 + 305 * Math.sin(a)]); }
  for (let i = 0; i < 60; i++) { const a = r() * TAU, d = 720 + r() * 600; spots.push([Math.cos(a) * d, Math.sin(a) * d * 0.8]); }
  const trunks = new THREE.InstancedMesh(trunk, new THREE.MeshStandardMaterial({ color: 0x8a7254, roughness: 1 }), spots.length);
  const fronds = new THREE.InstancedMesh(frondGeo, new THREE.MeshStandardMaterial({ color: 0x3f7d2e, roughness: 0.9, side: THREE.DoubleSide }), spots.length);
  spots.forEach(([x, z], i) => {
    const h = 22 + r() * 14, s = 0.85 + r() * 0.4;
    o.position.set(x, 0, z); o.rotation.set((r() - 0.5) * 0.08, 0, (r() - 0.5) * 0.08); o.scale.set(s, h, s); o.updateMatrix(); trunks.setMatrixAt(i, o.matrix);
    o.position.set(x, h, z); o.rotation.set(0, r() * TAU, 0); o.scale.set(s, s, s); o.updateMatrix(); fronds.setMatrixAt(i, o.matrix);
    fronds.setColorAt(i, new THREE.Color().setHSL(0.27 + r() * 0.05, 0.5, 0.28 + r() * 0.08));
  });
  trunks.castShadow = fronds.castShadow = true;
  world.add(trunks, fronds);
}
// moving highway traffic
const traffic = (() => {
  const g = new THREE.BoxGeometry(14, 5, 6); g.translate(0, 2.5, 0);
  const m = new THREE.InstancedMesh(g, new THREE.MeshStandardMaterial({ roughness: 0.4, metalness: 0.3 }), 44);
  const r = mulberry(5), cols = ['#ffffff', '#1d1f24', '#b3202b', '#24427a', '#9aa1aa'];
  const cars = [];
  for (let i = 0; i < 44; i++) { const lane = i % 4; cars.push({ x: (r() - 0.5) * 5000, z: -820 + [-32, -12, 12, 32][lane], v: (lane < 2 ? -1 : 1) * (70 + r() * 40) }); m.setColorAt(i, new THREE.Color(cols[i % cols.length])); }
  world.add(m);
  const o = new THREE.Object3D();
  return (dt) => {
    cars.forEach((c, i) => { c.x += c.v * dt; if (c.x > 2600) c.x = -2600; if (c.x < -2600) c.x = 2600; o.position.set(c.x, 0.2, c.z); o.updateMatrix(); m.setMatrixAt(i, o.matrix); });
    m.instanceMatrix.needsUpdate = true;
  };
})();

// ------------------------------------------------------------------ the arena shell
const arena = new THREE.Group(); scene.add(arena);
const LOWER = { tier: 'lower', rows: 22, d0: 16, dd: 2.75, y0: 4.5, dy: 1.3, frontBase: 0, backH: 2.7 };
const UPPER = { tier: 'upper', rows: 18, d0: 96, dd: 2.6, y0: 50, dy: 1.62, frontBase: 34.5, backH: 6.7 };
const NSEC = 34;
const lowerBack = LOWER.d0 + (LOWER.rows - 1) * LOWER.dd + LOWER.dd / 2;   // 75.1
const upperFront = UPPER.d0 - UPPER.dd / 2;                               // 94.7
const upperBack = UPPER.d0 + (UPPER.rows - 1) * UPPER.dd + UPPER.dd / 2;   // 141.5
const ROOF_Y = UPPER.y0 + (UPPER.rows - 1) * UPPER.dy + UPPER.backH;       // ~84.2
const FACADE = 152;
{
  const add = (geo, mat, cast = true) => { const m = new THREE.Mesh(geo, mat); m.castShadow = cast; m.receiveShadow = true; arena.add(m); return m; };
  add(ringGeo(lowerBack, upperFront, 34.5), MAT.ledge);
  const rb1 = add(wallGeo(lowerBack, 34.5, 37.6, 96), ribbonMat, false);
  const rb2 = add(wallGeo(upperFront - 0.15, 45.4, 48.6, 96), ribbonMat, false);
  rb1.userData.ribbon = rb2.userData.ribbon = true;
  add(ringGeo(upperBack, FACADE + 0.6, ROOF_Y), MAT.rim);
  const fac = add(wallGeo(FACADE, 0, ROOF_Y, 42), new THREE.MeshStandardMaterial({ map: facadeTex, roughness: 0.35, metalness: 0.25, side: THREE.DoubleSide }));
  fac.material.map.repeat.set(1, 1);
  // flip v so the silver band is at the top
  const uv = fac.geometry.attributes.uv; for (let i = 0; i < uv.count; i++) uv.setY(i, uv.getY(i)); facadeTex.flipY = true;
  add(wallGeo(FACADE + 0.6, ROOF_Y - 1, ROOF_Y + 3), MAT.rim);
  add(wallGeo(upperBack, ROOF_Y, ROOF_Y + 3), MAT.rim);

  // exterior signage on both sidelines
  const signTex = canvasTex(2048, 200, (g, w, h) => { g.fillStyle = 'rgba(0,0,0,0)'; g.clearRect(0, 0, w, h); g.fillStyle = '#ffffff'; g.font = '800 150px Inter, sans-serif'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText('AMERANT BANK ARENA', w / 2, h / 2 + 8); });
  for (const s of [1, -1]) {
    const sign = new THREE.Mesh(new THREE.PlaneGeometry(190, 18.5), new THREE.MeshStandardMaterial({ map: signTex, transparent: true, emissive: 0xffffff, emissiveMap: signTex, emissiveIntensity: 0.35 }));
    sign.position.set(0, ROOF_Y - 11, s * (RB + FACADE + 0.9));
    if (s < 0) sign.rotation.y = Math.PI;
    arena.add(sign);
  }
  // entrance canopies at the four "gates"
  for (const [x, z, ry] of [[0, RB + FACADE + 12, 0], [0, -(RB + FACADE + 12), 0], [RA + FACADE + 12, 0, Math.PI / 2], [-(RA + FACADE + 12), 0, Math.PI / 2]]) {
    const c = new THREE.Mesh(new THREE.BoxGeometry(90, 2, 26), MAT.rim); c.position.set(x, 22, z); c.rotation.y = ry; c.castShadow = true; arena.add(c);
    const red = new THREE.Mesh(new THREE.BoxGeometry(90.4, 1.2, 26.4), new THREE.MeshStandardMaterial({ color: 0xe0223a, emissive: 0xe0223a, emissiveIntensity: 0.4 })); red.position.set(x, 20.6, z); red.rotation.y = ry; arena.add(red);
  }

  // roof arches + spine (open "cutaway" roof frame)
  const zmaxAt = (x) => zAtX(FACADE - 4, x);
  for (const x of [-170, -110, -50, 50, 110, 170]) {
    const zm = zmaxAt(x), pts = [];
    for (let i = 0; i <= 24; i++) { const z = -zm + (2 * zm * i) / 24; pts.push(new THREE.Vector3(x, ROOF_Y + 2 + 28 * (1 - (z / zm) ** 2), z)); }
    const tube = new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 48, 1.5, 6), MAT.steel);
    tube.castShadow = true; arena.add(tube);
  }
  const spine = []; for (let i = 0; i <= 24; i++) { const x = -235 + (470 * i) / 24; spine.push(new THREE.Vector3(x, ROOF_Y + 2 + 28 * (1 - (x / 245) ** 2), 0)); }
  const sp = new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(spine), 64, 1.8, 6), MAT.steel); sp.castShadow = true; arena.add(sp);
}

// centre-hung video board
const jumbo = (() => {
  const g = new THREE.Group();
  const mats = { main: new THREE.MeshStandardMaterial({ emissive: 0xffffff, emissiveIntensity: 1, color: 0x000000 }), side: new THREE.MeshStandardMaterial({ emissive: 0xffffff, emissiveIntensity: 1, color: 0x000000 }) };
  const box = new THREE.Mesh(new THREE.BoxGeometry(30, 18, 40), [mats.side, mats.side, MAT.dark, MAT.dark, mats.main, mats.main]);
  box.castShadow = true; g.add(box);
  const ring = new THREE.Mesh(new THREE.BoxGeometry(32, 3, 42), ribbonMat); ring.position.y = -11; g.add(ring);
  const top = new THREE.Mesh(new THREE.BoxGeometry(31, 2, 41), MAT.dark); top.position.y = 10; g.add(top);
  for (const [x, z] of [[-12, -16], [12, -16], [-12, 16], [12, 16]]) {
    const len = ROOF_Y + 30 - 70;
    const cab = new THREE.Mesh(new THREE.CylinderGeometry(0.25, 0.25, len, 4), MAT.dark); cab.position.set(x * 0.6, 11 + len / 2, z * 0.2); g.add(cab);
  }
  g.position.set(0, 60, 0);
  arena.add(g);
  return { group: g, mats };
})();

// ------------------------------------------------------------------ seat geometry
const seatGeo = (() => {
  const cush = new THREE.BoxGeometry(1.55, 0.3, 1.35); cush.translate(0, 1.45, 0.12);
  const back = new THREE.BoxGeometry(1.55, 1.75, 0.22); back.rotateX(-0.12); back.translate(0, 2.35, -0.62);
  const leg = new THREE.BoxGeometry(0.2, 1.3, 0.2); leg.translate(0, 0.65, 0);
  return mergeGeometries([cush, back, leg]);
})();

// ------------------------------------------------------------------ sections (static bowl)
function rowSeats(d, t0, t1, aisle = 1.7, pitch = 1.9) {
  const K = 48, P = [], cum = [0];
  for (let k = 0; k <= K; k++) P.push(pt(d, t0 + ((t1 - t0) * k) / K));
  for (let k = 1; k <= K; k++) cum.push(cum[k - 1] + Math.hypot(P[k].x - P[k - 1].x, P[k].z - P[k - 1].z));
  const usable = cum[K] - 2 * aisle, n = Math.max(0, Math.floor(usable / pitch)), out = [];
  if (!n) return out;
  const spc = usable / n;
  let k = 0;
  for (let i = 0; i < n; i++) {
    const s = aisle + spc * (i + 0.5);
    while (k < K - 1 && cum[k + 1] < s) k++;
    const f = (s - cum[k]) / (cum[k + 1] - cum[k] || 1), a = P[k], b = P[k + 1];
    const nx = a.nx + (b.nx - a.nx) * f, nz = a.nz + (b.nz - a.nz) * f, l = Math.hypot(nx, nz) || 1;
    out.push({ x: a.x + (b.x - a.x) * f, z: a.z + (b.z - a.z) * f, nx: nx / l, nz: nz / l });
  }
  return out;
}

function labelSprite(text, scale = 1, bg = 'rgba(10,13,20,.82)', fg = '#fff') {
  const tex = canvasTex(160, 72, (g, w, h) => {
    g.fillStyle = bg; g.beginPath(); g.roundRect(4, 4, w - 8, h - 8, 18); g.fill();
    g.fillStyle = fg; g.font = '800 40px Inter, sans-serif'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText(text, w / 2, h / 2 + 2);
  });
  const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: tex, depthWrite: false }));
  s.scale.set(8 * scale, 3.6 * scale, 1);
  return s;
}

const labels = new THREE.Group(); scene.add(labels);
const compass = (x, z) => (Math.abs(z) / (RB + 60) > Math.abs(x) / (RA + 60) ? (z < 0 ? 'Norte' : 'Sur') : x > 0 ? 'Este' : 'Oeste');

const BOWL = [];
for (const spec of [LOWER, UPPER]) {
  for (let k = 0; k < NSEC; k++) {
    const t0 = T_TOP + (k - 0.5) / NSEC, t1 = t0 + 1 / NSEC, tc = t0 + 0.5 / NSEC;
    // stepped concrete
    const pos = [], K = 12;
    const P = (d, t, y) => { const p = pt(d, t); return [p.x, y, p.z]; };
    const quad = (a, b, c, d) => pos.push(...a, ...b, ...c, ...a, ...c, ...d);
    const layout = [];
    for (let r = 0; r < spec.rows; r++) {
      const d = spec.d0 + r * spec.dd, y = spec.y0 + r * spec.dy, dF = d - spec.dd / 2, dB = d + spec.dd / 2;
      const yPrev = r === 0 ? spec.frontBase : y - spec.dy;
      for (let j = 0; j < K; j++) {
        const ta = t0 + ((t1 - t0) * j) / K, tb = t0 + ((t1 - t0) * (j + 1)) / K;
        quad(P(dF, ta, y), P(dF, tb, y), P(dB, tb, y), P(dB, ta, y));
        quad(P(dF, ta, yPrev), P(dF, tb, yPrev), P(dF, tb, y), P(dF, ta, y));
        if (r === spec.rows - 1) quad(P(dB, ta, y), P(dB, tb, y), P(dB, tb, y + spec.backH), P(dB, ta, y + spec.backH));
      }
      const seats = rowSeats(d, t0, t1);
      seats.forEach((s, i) => layout.push({ row: String(r + 1), r, rows: spec.rows, num: seats.length - i, x: s.x, y, z: s.z, rot: Math.atan2(-s.nx, -s.nz) }));
    }
    const mesh = new THREE.Mesh(makeGeo(pos), MAT.concrete);
    mesh.castShadow = true; mesh.receiveShadow = true;
    arena.add(mesh);
    const midR = Math.floor(spec.rows / 2), midD = spec.d0 + midR * spec.dd, cp = pt(midD, tc);
    const name = String((spec.tier === 'lower' ? 100 : 300) + k + 1);
    const center = new THREE.Vector3(cp.x, spec.y0 + midR * spec.dy, cp.z);
    const side = clamp(1 - Math.abs(cp.x) / (RA + midD));
    const lp = pt(spec.d0 - 4.5, tc), lbl = labelSprite(name, spec.tier === 'lower' ? 0.9 : 1.1);
    lbl.position.set(lp.x, spec.y0 + 1.6, lp.z); labels.add(lbl);
    const ap = pt(spec.d0 + (spec.rows - 1) * spec.dd, tc);
    const sec = {
      id: name, name: `Sección ${name}`, tier: spec.tier, level: spec.tier === 'lower' ? 'Nivel 100' : 'Nivel 300',
      zone: side >= 0.45 ? 'Lateral' : 'Fondo / esquina', side, center, inward: new THREE.Vector3(-cp.nx, 0, -cp.nz),
      anchor: new THREE.Vector3(ap.x, spec.y0 + (spec.rows - 1) * spec.dy + 6, ap.z), gate: compass(cp.x, cp.z), layout, hit: mesh, k,
    };
    mesh.userData.sec = sec;
    BOWL.push(sec);
  }
}

// ------------------------------------------------------------------ suites
const SUITES = [];
{
  const suiteMat = { wall: new THREE.MeshStandardMaterial({ color: 0x2b313b, roughness: 0.7 }), floor: new THREE.MeshStandardMaterial({ color: 0x6b4f3a, roughness: 0.8 }), chair: new THREE.MeshStandardMaterial({ color: 0x14161a, roughness: 0.4 }), light: new THREE.MeshStandardMaterial({ color: 0xfff1d0, emissive: 0xffe2a8, emissiveIntensity: 1.2 }) };
  let n = 1;
  for (const s of [1, -1]) {
    for (let k = 0; k < 8; k++) {
      const x = s > 0 ? 63 - k * 18 : -63 + k * 18;
      const zf = s * (RB + 78.6), zb = s * (RB + 91.6), zc = (zf + zb) / 2, w = 17.2, depth = 13, y0 = 34.5, h = 10;
      const g = new THREE.Group(); g.position.set(x, y0, zc);
      const add = (geo, mat, px, py, pz) => { const m = new THREE.Mesh(geo, mat); m.position.set(px, py, pz); m.castShadow = true; m.receiveShadow = true; g.add(m); return m; };
      add(new THREE.BoxGeometry(w, 0.4, depth), suiteMat.floor, 0, 0.2, 0);
      add(new THREE.BoxGeometry(w + 0.6, 0.7, depth + 0.6), MAT.rim, 0, h, 0);
      add(new THREE.BoxGeometry(w, h, 0.4), suiteMat.wall, 0, h / 2, (s * depth) / 2);
      add(new THREE.BoxGeometry(0.4, h, depth), suiteMat.wall, -w / 2, h / 2, 0);
      add(new THREE.BoxGeometry(0.4, h, depth), suiteMat.wall, w / 2, h / 2, 0);
      add(new THREE.BoxGeometry(w - 2, 0.2, 2), suiteMat.light, 0, h - 0.5, s * 2);
      const glass = new THREE.Mesh(new THREE.PlaneGeometry(w, h - 1), MAT.glass); glass.position.set(0, h / 2 + 0.3, (-s * depth) / 2); g.add(glass);
      add(new THREE.BoxGeometry(w - 1.5, 3, 0.8), suiteMat.wall, 0, 1.5, (-s * depth) / 2 + s * 0.8); // ledge counter
      for (let row = 0; row < 2; row++) for (let c = 0; c < 4; c++) {
        const ch = new THREE.Mesh(seatGeo, suiteMat.chair); ch.position.set(-5.4 + c * 3.6, 0.4 + row * 1.1, (-s * depth) / 2 + s * (3 + row * 3.2)); ch.rotation.y = s > 0 ? Math.PI : 0; ch.scale.setScalar(1.25); g.add(ch);
      }
      const lbl = labelSprite(`Suite ${n}`, 0.85, 'rgba(255,197,61,.95)', '#1b1300'); lbl.position.set(0, h + 2.6, 0); g.add(lbl);
      const hit = new THREE.Mesh(new THREE.BoxGeometry(w, h, depth), MAT.hit); hit.position.set(0, h / 2, 0); g.add(hit);
      arena.add(g);
      const suite = {
        id: n, name: `Suite ${n}`, side: s, group: g, hit, capacity: 16,
        center: new THREE.Vector3(x, y0 + h / 2, zc), inward: new THREE.Vector3(0, 0, -s),
        eye: new THREE.Vector3(x, y0 + 5.4, zf - s * 3), anchor: new THREE.Vector3(x, y0 + h + 4, zc), gate: s > 0 ? 'Sur · Club' : 'Norte · Club',
      };
      hit.userData.suite = suite;
      SUITES.push(suite);
      n++;
    }
  }
}

// ------------------------------------------------------------------ event-specific floors
const floors = { hockey: new THREE.Group(), basketball: new THREE.Group(), concert: new THREE.Group() };
Object.values(floors).forEach((g) => { g.visible = false; arena.add(g); });
{ // hockey
  const g = floors.hockey;
  const ice = new THREE.Mesh(planarUV(discGeo(0, 0.25), -100, -42.5, 200, 85), new THREE.MeshStandardMaterial({ map: iceTex, roughness: 0.12, metalness: 0.05 }));
  ice.receiveShadow = true; g.add(ice);
  const boards = new THREE.Mesh(wallGeo(0, 0, 3.6), MAT.white); boards.castShadow = true; g.add(boards);
  g.add(new THREE.Mesh(wallGeo(-0.05, 0.25, 0.9), new THREE.MeshStandardMaterial({ color: 0xffc53d, side: THREE.DoubleSide })));
  g.add(new THREE.Mesh(ringGeo(0, 0.7, 3.62), new THREE.MeshStandardMaterial({ color: 0x1d3b8a, side: THREE.DoubleSide })));
  g.add(new THREE.Mesh(wallGeo(0.35, 3.6, 10), MAT.glass));
  for (const x of [-26, 26]) { const b = new THREE.Mesh(new THREE.BoxGeometry(24, 3, 7), MAT.dark); b.position.set(x, 1.5, -(RB + 6)); g.add(b); }
  for (const x of [-8, 8]) { const b = new THREE.Mesh(new THREE.BoxGeometry(10, 3, 6), MAT.dark); b.position.set(x, 1.5, RB + 6); g.add(b); }
  for (const s of [-1, 1]) { // goals
    const net = new THREE.Mesh(new THREE.BoxGeometry(3.4, 4, 6), new THREE.MeshStandardMaterial({ color: 0xffffff, transparent: true, opacity: 0.55 }));
    net.position.set(s * 90.7, 2.25, 0); g.add(net);
    const pipe = new THREE.Mesh(new THREE.BoxGeometry(0.3, 4.1, 6.2), new THREE.MeshStandardMaterial({ color: 0xc8102e })); pipe.position.set(s * 89, 2.3, 0); g.add(pipe);
  }
}
{ // basketball
  const g = floors.basketball;
  g.add(new THREE.Mesh(discGeo(0, 0.2), MAT.floor));
  const apron = new THREE.Mesh(new THREE.PlaneGeometry(116, 70), new THREE.MeshStandardMaterial({ color: 0x1c2333, roughness: 0.7 })); apron.rotation.x = -Math.PI / 2; apron.position.y = 0.28; apron.receiveShadow = true; g.add(apron);
  const court = new THREE.Mesh(new THREE.PlaneGeometry(94, 50), new THREE.MeshStandardMaterial({ map: courtTex, roughness: 0.35 })); court.rotation.x = -Math.PI / 2; court.position.y = 0.32; court.receiveShadow = true; g.add(court);
  for (const s of [-1, 1]) {
    const pole = new THREE.Mesh(new THREE.BoxGeometry(1, 11, 1), MAT.dark); pole.position.set(s * 50, 5.5, 0); g.add(pole);
    const arm = new THREE.Mesh(new THREE.BoxGeometry(4.5, 0.6, 0.6), MAT.dark); arm.position.set(s * 47.8, 11, 0); g.add(arm);
    const board = new THREE.Mesh(new THREE.BoxGeometry(0.2, 3.5, 6), MAT.glass); board.position.set(s * 45.5, 11.5, 0); g.add(board);
    const rim = new THREE.Mesh(new THREE.TorusGeometry(0.75, 0.06, 6, 20), new THREE.MeshStandardMaterial({ color: 0xff6a00 })); rim.rotation.x = Math.PI / 2; rim.position.set(s * 44.6, 10, 0); g.add(rim);
  }
  const table = new THREE.Mesh(new THREE.BoxGeometry(36, 3, 3), new THREE.MeshStandardMaterial({ color: 0x0d1220, emissive: 0xe0223a, emissiveIntensity: 0.25 })); table.position.set(0, 1.5, -29); g.add(table);
}
{ // concert
  const g = floors.concert;
  const cover = new THREE.Mesh(discGeo(14, 0.2), new THREE.MeshStandardMaterial({ color: 0x2a2d34, roughness: 0.9 })); cover.receiveShadow = true; g.add(cover);
  const stage = new THREE.Mesh(new THREE.BoxGeometry(38, 6, 72), new THREE.MeshStandardMaterial({ color: 0x111317, roughness: 0.6 })); stage.position.set(92, 3, 0); stage.castShadow = stage.receiveShadow = true; g.add(stage);
  const runway = new THREE.Mesh(new THREE.BoxGeometry(18, 5, 8), stage.material); runway.position.set(64, 2.5, 0); g.add(runway);
  const led = new THREE.Mesh(new THREE.PlaneGeometry(68, 30), new THREE.MeshStandardMaterial({ color: 0x000000, emissive: 0xffffff, emissiveMap: screenTex([['NOCHE LATINA', 74, '#ffffff', 0.42], ['GIRA 2026', 40, '#ffc53d', 0.66]], 1024, 452, ['#4b0f6b', '#e0223a']) }));
  led.position.set(110.5, 23, 0); led.rotation.y = -Math.PI / 2; g.add(led);
  for (const s of [-1, 1]) {
    const scr = new THREE.Mesh(new THREE.PlaneGeometry(22, 13), led.material); scr.position.set(98, 28, s * 47); scr.rotation.y = -Math.PI / 2 + s * 0.35; g.add(scr);
    const tower = new THREE.Mesh(new THREE.BoxGeometry(2, 44, 2), MAT.dark); tower.position.set(104, 22, s * 38); g.add(tower);
  }
  const truss = new THREE.Mesh(new THREE.BoxGeometry(3, 3, 80), MAT.dark); truss.position.set(94, 44, 0); g.add(truss);
  const beamMat = new THREE.MeshBasicMaterial({ color: 0xffd6f0, transparent: true, opacity: 0.09, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide });
  for (let i = 0; i < 7; i++) {
    const cone = new THREE.Mesh(new THREE.ConeGeometry(9, 44, 16, 1, true), beamMat);
    cone.position.set(88, 22, -30 + i * 10); cone.rotation.z = -0.25; g.add(cone);
  }
  const foh = new THREE.Mesh(new THREE.BoxGeometry(14, 6, 14), MAT.dark); foh.position.set(-60, 3, 0); foh.castShadow = true; g.add(foh);
}

// floor & courtside sections (only active for their event type)
function floorBlock(id, x0, x1, z0, z1, extra) {
  const layout = [], rows = Math.floor((x1 - x0) / 3.2) + 1, letters = 'ABCDEFGHJKLMNPQRSTUV';
  for (let r = 0; r < rows; r++) {
    const x = x1 - r * 3.2, n = Math.floor((z1 - z0) / 1.85);
    for (let i = 0; i < n; i++) layout.push({ row: letters[r], r, rows, num: i + 1, x, y: 0.2, z: z0 + 1 + i * 1.85, rot: Math.PI / 2 });
  }
  const cx = (x0 + x1) / 2, cz = (z0 + z1) / 2;
  const carpet = new THREE.Mesh(new THREE.PlaneGeometry(x1 - x0 + 4, z1 - z0 + 2), new THREE.MeshStandardMaterial({ color: 0x3a1f28, roughness: 0.95 }));
  carpet.rotation.x = -Math.PI / 2; carpet.position.set(cx, 0.24, cz); floors.concert.add(carpet);
  const hit = new THREE.Mesh(new THREE.BoxGeometry(x1 - x0 + 4, 4, z1 - z0 + 2), MAT.hit); hit.position.set(cx, 2, cz); floors.concert.add(hit);
  const lbl = labelSprite(id, 1.1, 'rgba(224,34,58,.95)'); lbl.position.set(x1 + 4, 5, cz); floors.concert.add(lbl);
  const sec = { id, name: `Piso ${id}`, tier: 'floor', level: 'Piso', zone: 'Frente al escenario', side: 1, center: new THREE.Vector3(cx, 0, cz), inward: new THREE.Vector3(1, 0, 0), anchor: new THREE.Vector3(cx, 7, cz), gate: 'Oeste · Piso', layout, hit, ...extra };
  hit.userData.sec = sec;
  return sec;
}
const FLOOR_SECS = [floorBlock('A', 22, 58, 2.5, 36, { front: true }), floorBlock('B', 22, 58, -36, -2.5, { front: true }), floorBlock('C', -24, 16, 2.5, 36), floorBlock('D', -24, 16, -36, -2.5)];
const COURT_SECS = [1, -1].map((s) => {
  const layout = [];
  for (let r = 0; r < 2; r++) for (let i = 0; i < 40; i++) layout.push({ row: 'AB'[r], r, rows: 2, num: i + 1, x: -38 + i * 1.95, y: 0.3 + r * 0.9, z: s * (30.5 + r * 2.6), rot: s > 0 ? Math.PI : 0 });
  const hit = new THREE.Mesh(new THREE.BoxGeometry(82, 5, 6), MAT.hit); hit.position.set(0, 2.5, s * 31.8); floors.basketball.add(hit);
  const riser = new THREE.Mesh(new THREE.BoxGeometry(82, 0.9, 2.6), MAT.dark); riser.position.set(0, 0.45, s * 33.1); floors.basketball.add(riser);
  const id = s > 0 ? 'CS-Sur' : 'CS-Norte';
  const sec = { id, name: `Courtside ${s > 0 ? 'Sur' : 'Norte'}`, tier: 'courtside', level: 'Courtside', zone: 'A pie de cancha', side: 1, center: new THREE.Vector3(0, 0, s * 31), inward: new THREE.Vector3(0, 0, -s), anchor: new THREE.Vector3(0, 6, s * 32), gate: s > 0 ? 'Sur · VIP' : 'Norte · VIP', layout, hit };
  hit.userData.sec = sec;
  return sec;
});

// ------------------------------------------------------------------ state
const state = {
  ev: null, mode: 'overview', focus: null, prevMode: null, hoverSec: null, hoverSeat: -1,
  cart: [], suiteCart: [], preview: null, maxPrice: Infinity, priceMin: 0, priceMax: 0,
  tip: null,
};
let SECTIONS = [], SEATS = [], seatMesh = null, hitTargets = [], LOOK = new THREE.Vector3();

const COL = {
  free: new THREE.Color('#e0223a'), freeHi: new THREE.Color('#ff7a8a'), taken: new THREE.Color('#22345f'),
  blocked: new THREE.Color('#33363d'), sel: new THREE.Color('#ffc53d'), hover: new THREE.Color('#ffffff'), over: new THREE.Color('#5a2a34'),
};
const _c = new THREE.Color();
function seatColor(i) {
  const s = SEATS[i];
  if (s.sel) return _c.copy(COL.sel);
  if (i === state.hoverSeat) return _c.copy(COL.hover);
  if (s.status === 'blocked') _c.copy(COL.blocked);
  else if (s.status === 'taken') _c.copy(COL.taken);
  else if (s.price > state.maxPrice) _c.copy(COL.over);
  else _c.copy(state.mode === 'overview' && state.hoverSec === s.sec ? COL.freeHi : COL.free);
  if (state.mode !== 'overview' && state.focus && s.sec !== state.focus) _c.multiplyScalar(0.5);
  return _c;
}
function recolor(list) {
  if (!seatMesh) return;
  if (list) list.forEach((i) => seatMesh.setColorAt(i, seatColor(i)));
  else for (let i = 0; i < SEATS.length; i++) seatMesh.setColorAt(i, seatColor(i));
  seatMesh.instanceColor.needsUpdate = true;
}

// ------------------------------------------------------------------ event setup
function setupEvent(ev) {
  state.ev = ev;
  const wasAway = state.mode !== 'overview';
  state.mode = 'overview';
  state.cart = []; state.suiteCart = []; state.preview = null; state.focus = null; state.hoverSec = null; state.hoverSeat = -1;
  for (const k in floors) floors[k].visible = k === ev.type;
  LOOK.set(...(ev.type === 'concert' ? [92, 16, 0] : [0, 3, 0]));

  // jumbotron content
  const t = ev.type === 'hockey' ? '🏒' : ev.type === 'basketball' ? '🏀' : '🎤';
  jumbo.mats.main.emissiveMap = screenTex([[t, 70, '#fff', 0.24], [ev.title.toUpperCase(), ev.title.length > 20 ? 34 : 44, '#ffffff', 0.52], [`${ev.short.toUpperCase()} · ${ev.time}`, 28, '#ffc53d', 0.74], ['BIENVENIDOS · AMERANT BANK ARENA', 18, '#9fb4d9', 0.9]]);
  jumbo.mats.side.emissiveMap = screenTex([['ARENA PASS', 52, '#ffffff', 0.45], ['¡A tu asiento!', 30, '#ffc53d', 0.68]], 480, 320, ['#e0223a', '#3a0d18']);
  jumbo.mats.main.needsUpdate = jumbo.mats.side.needsUpdate = true;
  jumbo.group.visible = ev.type !== 'concert';

  SECTIONS = [...BOWL, ...(ev.type === 'concert' ? FLOOR_SECS : []), ...(ev.type === 'basketball' ? COURT_SECS : [])];
  SECTIONS.forEach((s) => {
    s.blocked = ev.type === 'concert' && (s.tier === 'lower' || s.tier === 'upper') && s.center.x > 0 && Math.atan2(Math.abs(s.center.z), s.center.x) < 0.5;
    s.seatIdx = [];
  });

  // seats
  const rnd = mulberry(ev.seed);
  SEATS = [];
  SECTIONS.forEach((sec, si) => {
    sec.layout.forEach((L) => {
      const rowF = 1 - L.r / Math.max(1, L.rows - 1);
      let price, pTake;
      if (sec.tier === 'lower') { price = ev.base * (0.95 + 1.35 * sec.side) * (1 + 0.55 * rowF); pTake = 0.32 + 0.25 * sec.side; }
      else if (sec.tier === 'upper') { price = ev.base * 0.42 * (1 + 0.6 * sec.side) * (1 + 0.22 * rowF); pTake = 0.22 + 0.15 * sec.side; }
      else if (sec.tier === 'floor') { price = ev.base * (sec.front ? 2.6 : 1.9) * (1 + 0.4 * rowF); pTake = 0.42; }
      else { price = ev.base * (L.r === 0 ? 11 : 8); pTake = 0.55; }
      const cluster = Math.sin(L.r * 0.9 + si * 2.1 + ev.seed) * Math.cos(L.num * 0.35 + ev.seed * 0.7);
      const taken = rnd() < clamp(pTake + 0.22 * cluster, 0.04, 0.95);
      const idx = SEATS.length;
      SEATS.push({ idx, sec, row: L.row, num: L.num, x: L.x, y: L.y, z: L.z, rot: L.rot, price: round5(price), status: sec.blocked ? 'blocked' : taken ? 'taken' : 'free', sel: false });
      sec.seatIdx.push(idx);
    });
  });
  SECTIONS.forEach((s) => {
    const free = s.seatIdx.map((i) => SEATS[i]).filter((x) => x.status === 'free');
    s.available = free.length; s.total = s.seatIdx.length;
    s.minPrice = free.length ? Math.min(...free.map((x) => x.price)) : 0;
    s.maxPrice = free.length ? Math.max(...free.map((x) => x.price)) : 0;
  });
  SUITES.forEach((s, i) => { s.price = Math.round((ev.base * (32 + (i % 8 > 1 && i % 8 < 6 ? 6 : 0))) / 25) * 25; s.sold = rnd() < 0.45; });

  if (seatMesh) { arena.remove(seatMesh); seatMesh.dispose(); }
  seatMesh = new THREE.InstancedMesh(seatGeo, MAT.seat, SEATS.length);
  const o = new THREE.Object3D();
  SEATS.forEach((s, i) => { o.position.set(s.x, s.y, s.z); o.rotation.set(0, s.rot, 0); o.updateMatrix(); seatMesh.setMatrixAt(i, o.matrix); });
  seatMesh.receiveShadow = true;
  arena.add(seatMesh);
  recolor();

  hitTargets = [...SECTIONS.filter((s) => !s.blocked).map((s) => s.hit), ...SUITES.map((s) => s.hit)];
  BOWL.forEach((s) => (s.hit.material = s.blocked ? blockedMat : MAT.concrete));

  // price filter
  const prices = SEATS.filter((s) => s.status === 'free').map((s) => s.price);
  state.priceMin = Math.min(...prices); state.priceMax = Math.max(...prices); state.maxPrice = Infinity;
  const slider = $('#maxPrice');
  slider.min = state.priceMin; slider.max = state.priceMax; slider.value = state.priceMax;
  $('#maxPriceLabel').textContent = 'sin límite';

  renderEvents(); renderPanel(); renderCart(); updatePins();
  if (wasAway) goOverview();
}
const blockedMat = new THREE.MeshStandardMaterial({ color: 0x4d5158, roughness: 0.95, side: THREE.DoubleSide });

// ------------------------------------------------------------------ camera flights & modes
let flight = null;
function flyTo(pos, target, dur = 1500, lift = 0) {
  flight = { p0: camera.position.clone(), t0: controls.target.clone(), p1: pos.clone(), t1: target.clone(), start: performance.now(), dur, lift };
  controls.enabled = false;
}
function setControls(mode) {
  controls.autoRotate = mode === 'overview';
  controls.autoRotateSpeed = 0.35;
  controls.enableZoom = mode !== 'seat';
  controls.enablePan = mode === 'section';
  controls.rotateSpeed = mode === 'seat' ? -0.35 : 0.6;
  controls.minDistance = mode === 'seat' ? 0.01 : mode === 'overview' ? 220 : 25;
  controls.maxDistance = mode === 'seat' ? 2 : mode === 'overview' ? 1300 : 320;
  controls.maxPolarAngle = mode === 'seat' ? Math.PI * 0.85 : mode === 'overview' ? 1.32 : 1.5;
  controls.minPolarAngle = mode === 'seat' ? 0.25 : 0;
}
const OVERVIEW_POS = new THREE.Vector3(430, 380, 560), OVERVIEW_TGT = new THREE.Vector3(0, 10, 0);

function goOverview() {
  state.mode = 'overview'; state.focus = null; state.hoverSeat = -1;
  setControls('overview');
  flyTo(OVERVIEW_POS, OVERVIEW_TGT, 1600, 80);
  recolor(); renderPanel(); updateBack();
}
function focusSection(sec, fly = true) {
  state.mode = 'section'; state.focus = sec; state.hoverSec = null; state.hoverSeat = -1;
  setControls('section');
  if (fly) {
    const dist = sec.tier === 'upper' ? 75 : sec.tier === 'lower' ? 64 : 52, up = sec.tier === 'upper' ? 20 : sec.tier === 'lower' ? 30 : 40;
    const pos = sec.center.clone().addScaledVector(sec.inward, dist).add(new THREE.Vector3(0, up, 0));
    flyTo(pos, sec.center.clone().add(new THREE.Vector3(0, 3, 0)), 1500, 30);
  }
  recolor(); renderPanel(); updateBack();
}
function focusSuite(suite) {
  state.mode = 'section'; state.focus = null; state.hoverSeat = -1;
  state.preview = { kind: 'suite', suite };
  setControls('section');
  const pos = suite.center.clone().addScaledVector(suite.inward, 46).add(new THREE.Vector3(suite.center.x > 0 ? -14 : 14, 3, 0));
  flyTo(pos, suite.center, 1500, 30);
  recolor(); renderPanel(); updateBack(); renderThumbSoon();
}
function eyeFor(p) {
  if (p.kind === 'suite') return { eye: p.suite.eye.clone(), look: LOOK.clone() };
  const s = SEATS[p.idx];
  const eye = new THREE.Vector3(s.x, s.y + 4.0, s.z);
  eye.add(new THREE.Vector3(Math.sin(s.rot), 0, Math.cos(s.rot)).multiplyScalar(0.25));
  return { eye, look: LOOK.clone() };
}
function viewFrom(p) {
  state.prevMode = { focus: state.focus };
  state.mode = 'seat';
  setControls('seat');
  const { eye, look } = eyeFor(p);
  const tgt = eye.clone().add(look.sub(eye).normalize().multiplyScalar(0.5));
  flyTo(eye, tgt, 1800, 25);
  recolor(); renderPanel(); updateBack();
}
function goBack() {
  if (state.mode === 'seat') {
    const f = state.prevMode?.focus;
    if (f) focusSection(f);
    else if (state.preview?.kind === 'suite') focusSuite(state.preview.suite);
    else goOverview();
  } else if (state.mode === 'section') { state.preview = null; goOverview(); }
}
function updateBack() {
  const b = $('#back');
  b.classList.toggle('hidden', state.mode === 'overview');
  b.textContent = state.mode === 'seat' ? (state.prevMode?.focus ? `← ${state.prevMode.focus.name}` : '← Volver') : '← Vista del arena';
}

// ------------------------------------------------------------------ selection
function toast(msg) {
  const t = $('#toast'); t.textContent = msg; t.classList.remove('hidden');
  clearTimeout(toast._t); toast._t = setTimeout(() => t.classList.add('hidden'), 2200);
}
function ticketCount() { return state.cart.length + state.suiteCart.reduce((a, s) => a + s.capacity, 0); }
function toggleSeat(i) {
  const s = SEATS[i];
  if (s.sel) {
    s.sel = false; state.cart = state.cart.filter((x) => x !== i);
    if (state.preview?.kind === 'seat' && state.preview.idx === i) state.preview = state.cart.length ? { kind: 'seat', idx: state.cart[state.cart.length - 1] } : null;
  } else {
    if (s.status !== 'free') return toast('Ese asiento ya está vendido');
    if (s.price > state.maxPrice) return toast('Ese asiento está por encima de tu precio máximo');
    if (state.cart.length >= MAX_TICKETS) return toast(`Máximo ${MAX_TICKETS} entradas por compra`);
    s.sel = true; state.cart.push(i); state.preview = { kind: 'seat', idx: i };
  }
  recolor([i]); updatePins(); renderPanel(); renderCart(); renderThumbSoon();
}
function toggleSuite(suite) {
  if (state.suiteCart.includes(suite)) state.suiteCart = state.suiteCart.filter((x) => x !== suite);
  else if (suite.sold) return toast('Esa suite ya está reservada');
  else state.suiteCart.push(suite);
  renderPanel(); renderCart();
}

// gold pins above selected seats
const pins = [];
{
  const geo = mergeGeometries([new THREE.ConeGeometry(1.1, 2.6, 16).rotateX(Math.PI).translate(0, 1.3, 0), new THREE.SphereGeometry(1.5, 16, 12).translate(0, 3.3, 0)]);
  const mat = new THREE.MeshStandardMaterial({ color: 0xffc53d, emissive: 0xffb000, emissiveIntensity: 0.6, roughness: 0.3 });
  for (let i = 0; i < MAX_TICKETS; i++) { const m = new THREE.Mesh(geo, mat); m.visible = false; scene.add(m); pins.push(m); }
}
function updatePins() {
  pins.forEach((p, i) => {
    const idx = state.cart[i];
    p.visible = idx !== undefined;
    if (p.visible) { const s = SEATS[idx]; p.userData.base = s.y + 5; p.position.set(s.x, s.y + 5, s.z); }
  });
}

// ------------------------------------------------------------------ "your view" thumbnail
const thumbCanvas = document.createElement('canvas');
thumbCanvas.width = 640; thumbCanvas.height = 360;
const thumbCam = new THREE.PerspectiveCamera(62, 16 / 9, 0.5, 9000);
let thumbPending = false;
function renderThumbSoon() { thumbPending = true; }
// Renders the seat's point of view with the main renderer, copies it into the 2D card canvas,
// then the caller re-renders the normal view in the same frame (no second WebGL context).
function renderThumb() {
  thumbPending = false;
  if (!state.preview) return;
  const { eye, look } = eyeFor(state.preview);
  const W = canvas.width, H = canvas.height;
  thumbCam.aspect = W / H; thumbCam.updateProjectionMatrix();
  thumbCam.position.copy(eye); thumbCam.lookAt(look);
  const vis = pins.map((p) => p.visible); pins.forEach((p) => (p.visible = false));
  const lv = labels.visible; labels.visible = false;
  renderer.render(scene, thumbCam);
  let cw = W, ch = (W * 9) / 16;
  if (ch > H) { ch = H; cw = (H * 16) / 9; }
  thumbCanvas.getContext('2d').drawImage(canvas, (W - cw) / 2, (H - ch) / 2, cw, ch, 0, 0, 640, 360);
  pins.forEach((p, i) => (p.visible = vis[i]));
  labels.visible = lv;
}

// ------------------------------------------------------------------ UI: events, panel, cart
function renderEvents() {
  $('#events').innerHTML = EVENTS.map((e) => `<button class="event-chip ${e === state.ev ? 'active' : ''}" data-ev="${e.id}" type="button"><b>${e.title}</b><small>${e.short} · ${e.time}</small></button>`).join('');
}
$('#events').addEventListener('click', (e) => {
  const b = e.target.closest('[data-ev]'); if (!b) return;
  const ev = EVENTS.find((x) => x.id === b.dataset.ev);
  if (ev === state.ev) return;
  if (state.cart.length || state.suiteCart.length) toast('Cambiaste de evento: se vació tu selección');
  setupEvent(ev);
});

function zonesFor() {
  const z = new Map();
  const add = (key, label, sub, sec, min, avail) => {
    if (!z.has(key)) z.set(key, { key, label, sub, secs: [], min: Infinity, avail: 0 });
    const e = z.get(key); if (sec) e.secs.push(sec); if (avail) { e.min = Math.min(e.min, min); e.avail += avail; }
  };
  SECTIONS.filter((s) => !s.blocked).forEach((s) => {
    const key = `${s.level}·${s.zone}`;
    const sub = s.tier === 'floor' ? 'Sillas numeradas en la pista' : s.tier === 'courtside' ? 'Primera fila, acceso VIP' : s.tier === 'lower' ? (s.zone === 'Lateral' ? 'La mejor vista del juego' : 'Cerca de la acción') : (s.zone === 'Lateral' ? 'Vista completa, gran precio' : 'La opción más económica');
    add(key, `${s.level} · ${s.zone}`, sub, s, s.minPrice, s.available);
  });
  const freeSuites = SUITES.filter((s) => !s.sold);
  z.set('suites', { key: 'suites', label: 'Suites premium', sub: '16 personas · catering · baño privado', secs: [], min: Math.min(...freeSuites.map((s) => s.price)), avail: freeSuites.length, suites: true });
  const order = ['Courtside', 'Piso', 'Nivel 100', 'suites', 'Nivel 300'];
  return [...z.values()].sort((a, b) => order.findIndex((o) => a.key.startsWith(o)) - order.findIndex((o) => b.key.startsWith(o)) || b.min - a.min);
}

function seatCardHTML(i) {
  const s = SEATS[i];
  return `<div class="card">
    <div class="thumb-slot"><span class="tag">👁 Tu vista desde el asiento</span></div>
    <div class="card-body">
      <div class="card-grid"><div><small>Sección</small><b>${s.sec.id}</b></div><div><small>Fila</small><b>${s.row}</b></div><div><small>Asiento</small><b>${s.num}</b></div></div>
      <div class="price-big"><b>${fmt(s.price)}</b><span>Entrada ${s.gate || s.sec.gate} · por persona</span></div>
      <div class="btn-row">
        ${state.mode === 'seat' ? '' : `<button class="btn" data-act="view" data-idx="${i}">Ver en 3D</button>`}
        <button class="btn" data-act="toggle" data-idx="${i}">Quitar</button>
      </div>
    </div></div>`;
}
function suiteCardHTML(su) {
  const inCart = state.suiteCart.includes(su);
  return `<div class="card">
    <div class="thumb-slot"><span class="tag">👁 Tu vista desde la suite</span></div>
    <div class="card-body">
      <div class="card-grid"><div><small>Nivel</small><b>Club</b></div><div><small>Personas</small><b>${su.capacity}</b></div><div><small>Tipo</small><b>VIP</b></div></div>
      <ul class="perks"><li>Catering y bebidas incluidos</li><li>Baño privado y TV</li><li>Entrada y estacionamiento VIP</li></ul>
      <div class="price-big"><b>${su.sold ? 'Reservada' : fmt(su.price)}</b><span>${su.sold ? 'No disponible' : 'precio total de la suite'}</span></div>
      <div class="btn-row">
        ${state.mode === 'seat' ? '' : `<button class="btn" data-act="view-suite">Ver vista</button>`}
        ${su.sold ? '' : `<button class="btn ${inCart ? '' : 'gold'}" data-act="suite-toggle">${inCart ? 'Quitar suite' : 'Elegir esta suite'}</button>`}
      </div>
    </div></div>`;
}

function renderPanel() {
  const ev = state.ev, p = $('#panel');
  let html = '';
  if (state.mode === 'overview') {
    const free = SEATS.filter((s) => s.status === 'free').length;
    html = `<div class="eyebrow">${ev.date} · ${ev.time}</div>
      <h2>${ev.title}</h2>
      <p class="muted">${ev.sub}<br>Amerant Bank Arena · 1 Panther Pkwy, Sunrise, FL 33323</p>
      <div class="stats"><div class="stat"><b>${free.toLocaleString('en-US')}</b><span>disponibles</span></div><div class="stat"><b>${fmt(state.priceMin)}</b><span>desde</span></div><div class="stat"><b>${SUITES.filter((s) => !s.sold).length}</b><span>suites libres</span></div></div>
      <h3>Elige una zona</h3>
      ${zonesFor().map((z) => `<button class="zone" data-act="zone" data-zone="${z.key}"><span><b>${z.label}</b><small>${z.sub}</small></span><span class="from">${z.avail ? fmt(z.min) : 'Agotado'}<small>${z.avail} ${z.suites ? 'suites' : 'disp.'}</small></span></button>`).join('')}
      <div class="hint">Toca una sección en el mapa 3D para acercarte y ver cada asiento. Arrastra para girar el arena.</div>`;
  } else if (state.preview?.kind === 'suite' && !state.focus) {
    const su = state.preview.suite;
    html = `<div class="eyebrow">Nivel Club · Entrada ${su.gate}</div><h2>${su.name}</h2>
      <p class="muted">Suite privada con vista al centro ${ev.type === 'concert' ? 'del show' : 'de la pista'}.</p>
      ${suiteCardHTML(su)}`;
  } else {
    const sec = state.focus;
    const mine = state.cart.filter((i) => SEATS[i].sec === sec || state.mode === 'seat');
    const idx = SECTIONS.indexOf(sec);
    const nav = sec.tier === 'lower' || sec.tier === 'upper';
    const nb = (d) => { const list = BOWL.filter((s) => s.tier === sec.tier && !s.blocked); const j = list.indexOf(sec); return list[(j + d + list.length) % list.length]; };
    html = `<div class="eyebrow">${sec.level} · ${sec.zone} · Entrada ${sec.gate}</div>
      <h2>${sec.name}</h2>
      <div class="stats"><div class="stat"><b>${sec.available}</b><span>de ${sec.total} libres</span></div><div class="stat"><b>${sec.available ? fmt(sec.minPrice) : '—'}</b><span>desde</span></div><div class="stat"><b>${sec.available ? fmt(sec.maxPrice) : '—'}</b><span>hasta</span></div></div>
      ${nav ? `<div class="sec-nav"><button data-act="sec" data-id="${nb(-1).id}">‹ Sección ${nb(-1).id}</button><button data-act="sec" data-id="${nb(1).id}">Sección ${nb(1).id} ›</button></div>` : ''}
      ${state.preview?.kind === 'seat' ? seatCardHTML(state.preview.idx) : state.preview?.kind === 'suite' ? suiteCardHTML(state.preview.suite) : `<div class="hint">Toca los asientos <b style="color:#ff6b7d">rojos</b> para elegirlos (hasta ${MAX_TICKETS}). Los azules ya están vendidos.</div>`}
      ${state.cart.length ? `<h3>Tus asientos (${state.cart.length})</h3><ul class="sel-list">${state.cart.map((i) => { const s = SEATS[i]; return `<li><span><b>Sec ${s.sec.id}</b> · Fila ${s.row} · Asiento ${s.num}</span><span>${fmt(s.price)} <button data-act="toggle" data-idx="${i}" aria-label="Quitar">✕</button></span></li>`; }).join('')}</ul>` : ''}`;
    void idx;
  }
  p.innerHTML = html;
  const slot = p.querySelector('.thumb-slot');
  if (slot) { slot.prepend(thumbCanvas); renderThumbSoon(); }
}
$('#panel').addEventListener('click', (e) => {
  const b = e.target.closest('[data-act]'); if (!b) return;
  const act = b.dataset.act;
  if (act === 'zone') {
    const z = zonesFor().find((x) => x.key === b.dataset.zone);
    if (z.suites) { const su = SUITES.filter((s) => !s.sold).sort((a, c) => Math.abs(a.center.x) - Math.abs(c.center.x))[0]; if (su) focusSuite(su); return; }
    const best = z.secs.filter((s) => s.available).sort((a, c) => c.available - a.available)[0];
    if (best) { state.preview = null; focusSection(best); }
  } else if (act === 'sec') { state.preview = null; focusSection(SECTIONS.find((s) => s.id === b.dataset.id)); }
  else if (act === 'toggle') toggleSeat(+b.dataset.idx);
  else if (act === 'view') { state.preview = { kind: 'seat', idx: +b.dataset.idx }; viewFrom(state.preview); }
  else if (act === 'view-suite') viewFrom(state.preview);
  else if (act === 'suite-toggle') toggleSuite(state.preview.suite);
});
$('#back').addEventListener('click', goBack);

function subtotal() { return state.cart.reduce((a, i) => a + SEATS[i].price, 0) + state.suiteCart.reduce((a, s) => a + s.price, 0); }
function renderCart() {
  const bar = $('#cartbar');
  const n = state.cart.length + state.suiteCart.length;
  bar.classList.toggle('hidden', !n);
  if (!n) return;
  const parts = [];
  if (state.cart.length) parts.push(`${state.cart.length} entrada${state.cart.length > 1 ? 's' : ''}`);
  if (state.suiteCart.length) parts.push(`${state.suiteCart.length} suite${state.suiteCart.length > 1 ? 's' : ''}`);
  bar.innerHTML = `<div class="ci"><b>${parts.join(' + ')} · ${fmt(subtotal())}</b><small>${state.ev.short} · ${state.ev.time} · antes de cargos</small></div><button class="btn primary" data-act="checkout">Confirmar entradas →</button>`;
}
$('#cartbar').addEventListener('click', (e) => { if (e.target.closest('[data-act="checkout"]')) openCheckout(); });

// ------------------------------------------------------------------ checkout
function totals() {
  const sub = subtotal(), tickets = ticketCount();
  const service = sub * 0.12, facility = tickets * 4.5, tax = sub * 0.07;
  return { sub, service, facility, tax, total: sub + service + facility + tax, tickets };
}
function openCheckout() {
  const t = totals(), ev = state.ev, m = $('#modal');
  const lines = [
    ...state.cart.map((i) => { const s = SEATS[i]; return `<li><span>Sec ${s.sec.id} · Fila ${s.row} · Asiento ${s.num}</span><span>${fmt(s.price)}</span></li>`; }),
    ...state.suiteCart.map((s) => `<li><span>${s.name} · ${s.capacity} pases</span><span>${fmt(s.price)}</span></li>`),
  ].join('');
  m.innerHTML = `<div class="sheet">
    <button class="close" data-act="close" aria-label="Cerrar">✕</button>
    <div class="eyebrow">${ev.date} · ${ev.time}</div>
    <h2>${ev.title}</h2>
    <p class="muted">Amerant Bank Arena · Sunrise, FL</p>
    <ul class="lines">${lines}
      <li class="sub"><span>Subtotal</span><span>${fmt(t.sub)}</span></li>
      <li class="sub"><span>Cargo por servicio (12%)</span><span>$${t.service.toFixed(2)}</span></li>
      <li class="sub"><span>Cargo de instalación ($4.50 × ${t.tickets})</span><span>$${t.facility.toFixed(2)}</span></li>
      <li class="sub"><span>Impuesto de ventas FL (7%)</span><span>$${t.tax.toFixed(2)}</span></li>
      <li class="total"><span>Total</span><span>$${t.total.toFixed(2)}</span></li>
    </ul>
    <form class="form" id="payForm">
      <label>Nombre<input name="name" required autocomplete="name" placeholder="Nombre y apellido"></label>
      <label>Email<input name="email" type="email" required autocomplete="email" placeholder="tu@email.com"></label>
      <label class="full">Tarjeta<input name="card" inputmode="numeric" value="4242 4242 4242 4242" required></label>
      <label>Vence<input name="exp" value="12/29" required></label>
      <label>CVC<input name="cvc" value="123" required></label>
      <button class="btn primary block" style="grid-column:1/-1;margin-top:6px" type="submit">Pagar $${t.total.toFixed(2)}</button>
    </form>
    <p class="disclaimer">Demo: no se procesa ningún pago. Sitio independiente, no afiliado oficialmente al Amerant Bank Arena.</p>
  </div>`;
  m.classList.remove('hidden');
  m.querySelector('#payForm').addEventListener('submit', (e) => { e.preventDefault(); completePurchase(new FormData(e.target)); });
}
$('#modal').addEventListener('click', (e) => {
  if (e.target === e.currentTarget || e.target.closest('[data-act="close"]')) $('#modal').classList.add('hidden');
});
function qr(canvas, seed) {
  const g = canvas.getContext('2d'), N = 25, s = canvas.width / N, r = mulberry(seed);
  g.fillStyle = '#fff'; g.fillRect(0, 0, canvas.width, canvas.height); g.fillStyle = '#0d1220';
  for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) if (r() < 0.48) g.fillRect(x * s, y * s, s, s);
  for (const [fx, fy] of [[0, 0], [N - 7, 0], [0, N - 7]]) {
    g.fillStyle = '#fff'; g.fillRect((fx - 0) * s, (fy - 0) * s, 8 * s, 8 * s);
    g.fillStyle = '#0d1220'; g.fillRect(fx * s, fy * s, 7 * s, 7 * s);
    g.fillStyle = '#fff'; g.fillRect((fx + 1) * s, (fy + 1) * s, 5 * s, 5 * s);
    g.fillStyle = '#0d1220'; g.fillRect((fx + 2) * s, (fy + 2) * s, 3 * s, 3 * s);
  }
}
function completePurchase(fd) {
  const ev = state.ev, order = 'AP-' + Math.random().toString(36).slice(2, 8).toUpperCase();
  const items = [
    ...state.cart.map((i) => { const s = SEATS[i]; return { title: `Sección ${s.sec.id}`, cols: [['Fila', s.row], ['Asiento', s.num], ['Entrada', s.sec.gate]] }; }),
    ...state.suiteCart.map((s) => ({ title: s.name, cols: [['Pases', s.capacity], ['Nivel', 'Club'], ['Entrada', s.gate]] })),
  ];
  // mark as sold
  state.cart.forEach((i) => { SEATS[i].status = 'taken'; SEATS[i].sel = false; });
  state.suiteCart.forEach((s) => (s.sold = true));
  SECTIONS.forEach((s) => { const free = s.seatIdx.map((i) => SEATS[i]).filter((x) => x.status === 'free'); s.available = free.length; s.minPrice = free.length ? Math.min(...free.map((x) => x.price)) : 0; s.maxPrice = free.length ? Math.max(...free.map((x) => x.price)) : 0; });
  state.cart = []; state.suiteCart = []; state.preview = null;
  recolor(); updatePins(); renderCart();

  const name = String(fd.get('name') || '').replace(/[<>&"]/g, '');
  $('#modal').innerHTML = `<div class="sheet">
    <button class="close" data-act="close" aria-label="Cerrar">✕</button>
    <div class="eyebrow" style="color:var(--ok)">✓ Compra confirmada · ${order}</div>
    <h2>¡Nos vemos en el arena${name ? ', ' + name.split(' ')[0] : ''}!</h2>
    <p class="muted">${ev.title} · ${ev.date} · ${ev.time}. Las puertas abren 1 hora antes. Presenta el código QR en la entrada indicada.</p>
    <div class="tickets">${items.map((it, k) => `<div class="ticket"><div><h4>${it.title}</h4><div class="tmeta">${ev.title} · ${ev.short} · ${ev.time}</div><div class="tseat">${it.cols.map(([a, b]) => `<div><small>${a}</small><b>${b}</b></div>`).join('')}</div></div><canvas width="200" height="200" data-qr="${k}"></canvas></div>`).join('')}</div>
    <button class="btn primary block" style="margin-top:16px" data-act="close">Volver al arena</button>
    <p class="disclaimer">Entradas de demostración — no válidas para ingresar.</p>
  </div>`;
  $('#modal').querySelectorAll('canvas[data-qr]').forEach((c, k) => qr(c, order.charCodeAt(3) * 131 + k * 17 + 7));
  renderPanel();
}

// ------------------------------------------------------------------ price filter
$('#maxPrice').addEventListener('input', (e) => {
  const v = +e.target.value;
  state.maxPrice = v >= state.priceMax ? Infinity : v;
  $('#maxPriceLabel').textContent = state.maxPrice === Infinity ? 'sin límite' : fmt(v);
  cancelAnimationFrame(recolor._raf); recolor._raf = requestAnimationFrame(() => recolor());
});

// ------------------------------------------------------------------ picking / hover / click
const ray = new THREE.Raycaster(), ndc = new THREE.Vector2();
function pick(cx, cy) {
  const r = canvas.getBoundingClientRect();
  ndc.set(((cx - r.left) / r.width) * 2 - 1, -((cy - r.top) / r.height) * 2 + 1);
  ray.setFromCamera(ndc, camera);
  const targets = state.mode === 'overview' ? hitTargets : [seatMesh, ...hitTargets];
  for (const h of ray.intersectObjects(targets, false)) {
    if (h.object === seatMesh) return { seat: h.instanceId };
    if (h.object.userData.suite) return { suite: h.object.userData.suite };
    if (h.object.userData.sec) return { sec: h.object.userData.sec };
  }
  return null;
}
const tip = $('#tooltip');
function setTip(anchor, html, sold = false) {
  if (!anchor) { state.tip = null; tip.classList.add('hidden'); return; }
  state.tip = anchor; tip.innerHTML = html; tip.classList.toggle('sold', sold); tip.classList.remove('hidden');
}
function hover(p) {
  const prevSec = state.hoverSec, prevSeat = state.hoverSeat;
  state.hoverSec = null; state.hoverSeat = -1;
  let anchor = null, html = '', sold = false;
  if (p?.seat !== undefined && state.mode !== 'overview') {
    const s = SEATS[p.seat];
    if (s.sec === state.focus || state.mode === 'seat') {
      state.hoverSeat = s.status === 'free' && !s.sel ? p.seat : -1;
      anchor = new THREE.Vector3(s.x, s.y + 4.5, s.z);
      sold = s.status !== 'free';
      html = `<b>Fila ${s.row} · Asiento ${s.num}</b><span class="tp-price">${sold ? 'Vendido' : fmt(s.price)}</span><small>${s.sec.name}${s.sel ? ' · en tu selección' : ''}</small>`;
    } else {
      anchor = s.sec.anchor; html = `<b>${s.sec.name}</b><span class="tp-price">desde ${fmt(s.sec.minPrice)}</span><small>Toca para ir a esta sección</small>`;
    }
  } else if (p?.sec) {
    const s = p.sec;
    if (state.mode === 'overview') state.hoverSec = s;
    anchor = s.anchor;
    sold = !s.available;
    html = `<b>${s.name}</b><span class="tp-price">${s.available ? 'desde ' + fmt(s.minPrice) : 'Agotada'}</span><small>${s.level} · ${s.zone} · ${s.available} disponibles</small>`;
  } else if (p?.suite) {
    const s = p.suite; anchor = s.anchor; sold = s.sold;
    html = `<b>${s.name}</b><span class="tp-price">${s.sold ? 'Reservada' : fmt(s.price)}</span><small>Nivel Club · ${s.capacity} personas · VIP</small>`;
  }
  setTip(anchor, html, sold);
  canvas.style.cursor = p ? 'pointer' : 'grab';
  if (prevSec !== state.hoverSec) recolor([...(prevSec?.seatIdx || []), ...(state.hoverSec?.seatIdx || [])]);
  if (prevSeat !== state.hoverSeat) recolor([prevSeat, state.hoverSeat].filter((i) => i >= 0));
}
function click(p) {
  if (!p) return;
  if (p.suite) return focusSuite(p.suite);
  if (p.seat !== undefined && state.mode !== 'overview') {
    const s = SEATS[p.seat];
    if (s.sec !== state.focus && state.mode !== 'seat') { state.preview = null; return focusSection(s.sec); }
    return toggleSeat(p.seat);
  }
  if (p.sec) {
    if (p.sec === state.focus && state.mode === 'section') return;
    if (state.mode === 'seat') return;
    state.preview = null; focusSection(p.sec);
  }
}
let down = null, moveRaf = 0, lastMove = null;
canvas.addEventListener('pointerdown', (e) => { down = { x: e.clientX, y: e.clientY, t: performance.now() }; });
canvas.addEventListener('pointermove', (e) => {
  if (e.pointerType !== 'mouse') return;
  lastMove = e;
  if (!moveRaf) moveRaf = requestAnimationFrame(() => { moveRaf = 0; if (!flight && !(down && e.buttons)) hover(pick(lastMove.clientX, lastMove.clientY)); });
});
canvas.addEventListener('pointerleave', () => hover(null));
canvas.addEventListener('pointerup', (e) => {
  if (!down) return;
  const moved = Math.hypot(e.clientX - down.x, e.clientY - down.y);
  down = null;
  if (moved > 6 || flight) return;
  const p = pick(e.clientX, e.clientY);
  if (e.pointerType !== 'mouse') hover(p);
  click(p);
});
window.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') { if (!$('#modal').classList.contains('hidden')) $('#modal').classList.add('hidden'); else goBack(); }
});
let idleTimer = 0;
controls.addEventListener('start', () => { controls.autoRotate = false; clearTimeout(idleTimer); });
controls.addEventListener('end', () => { clearTimeout(idleTimer); idleTimer = setTimeout(() => { if (state.mode === 'overview') controls.autoRotate = true; }, 7000); });

// ------------------------------------------------------------------ main loop
function resize() {
  const w = window.innerWidth, h = window.innerHeight;
  renderer.setSize(w, h, false);
  camera.aspect = w / h;
  camera.fov = w < 760 ? 55 : 42;
  camera.updateProjectionMatrix();
}
window.addEventListener('resize', resize);
resize();

const clock = new THREE.Clock();
const _v = new THREE.Vector3();
function tick() {
  const dt = Math.min(clock.getDelta(), 0.05), now = performance.now();
  if (flight) {
    const k = clamp((now - flight.start) / flight.dur), e = easeInOut(k);
    camera.position.lerpVectors(flight.p0, flight.p1, e);
    camera.position.y += Math.sin(Math.PI * e) * flight.lift;
    controls.target.lerpVectors(flight.t0, flight.t1, e);
    camera.lookAt(controls.target);
    if (k >= 1) { flight = null; controls.enabled = true; }
  }
  if (!flight) controls.update();
  ribbonTex.offset.x = (ribbonTex.offset.x + dt * 0.06) % 1;
  traffic(dt);
  pins.forEach((p, i) => { if (p.visible) { p.position.y = p.userData.base + Math.sin(now / 300 + i) * 0.6; p.rotation.y += dt * 2; } });
  if (thumbPending && !flight) renderThumb();
  labels.visible = state.mode !== 'seat';
  renderer.render(scene, camera);
  if (state.tip) {
    _v.copy(state.tip).project(camera);
    if (_v.z > 1) tip.style.opacity = 0;
    else { tip.style.opacity = 1; tip.style.left = ((_v.x + 1) / 2) * window.innerWidth + 'px'; tip.style.top = ((1 - _v.y) / 2) * window.innerHeight + 'px'; }
  }
  requestAnimationFrame(tick);
}

setupEvent(EVENTS[0]);
setControls('overview');
controls.target.copy(OVERVIEW_TGT);
flyTo(OVERVIEW_POS, OVERVIEW_TGT, 2600, 0);
requestAnimationFrame(tick);
requestAnimationFrame(() => setTimeout(() => $('#loader').classList.add('done'), 150));
window.__arena = { state, SECTIONS: () => SECTIONS, SEATS: () => SEATS, SUITES, focusSection, focusSuite, toggleSeat, viewFrom, goOverview, setupEvent, EVENTS };
