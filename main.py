from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uvicorn

app = FastAPI(title="App de Notas API", version="1.0.0")

# CRUD generico server-side (persistencia multi-dispositivo)
try:
    from app.routers import data as _data_router
    app.include_router(_data_router.router)
except Exception as _e:
    import logging; logging.getLogger('uvicorn').warning('data router: %s', _e)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Pydantic Schemas ─────────────────────────────────────────────────────────

class UsuarioCreate(BaseModel):
    nombre: str
    email: str
    avatar: Optional[str] = None

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[str] = None
    avatar: Optional[str] = None

class NotaCreate(BaseModel):
    titulo: str
    contenido: str
    usuario_id: int

class NotaUpdate(BaseModel):
    titulo: Optional[str] = None
    contenido: Optional[str] = None
    usuario_id: Optional[int] = None

class EtiquetaCreate(BaseModel):
    nombre: str
    color: str

class EtiquetaUpdate(BaseModel):
    nombre: Optional[str] = None
    color: Optional[str] = None

class NotaEtiquetaCreate(BaseModel):
    nota_id: int
    etiqueta_id: int

class NotaEtiquetaUpdate(BaseModel):
    nota_id: Optional[int] = None
    etiqueta_id: Optional[int] = None

# ─── Seed Data ────────────────────────────────────────────────────────────────

usuarios_db: List[dict] = [
    {"id": 1, "nombre": "Ana García",       "email": "ana.garcia@universidad.edu",      "avatar": "AG", "created_at": "2024-01-10T08:00:00"},
    {"id": 2, "nombre": "Carlos López",     "email": "carlos.lopez@universidad.edu",    "avatar": "CL", "created_at": "2024-01-15T10:30:00"},
    {"id": 3, "nombre": "María Rodríguez",  "email": "maria.rodriguez@universidad.edu", "avatar": "MR", "created_at": "2024-02-01T09:00:00"},
    {"id": 4, "nombre": "Pedro Martínez",   "email": "pedro.martinez@universidad.edu",  "avatar": "PM", "created_at": "2024-02-10T11:00:00"},
    {"id": 5, "nombre": "Lucía Fernández",  "email": "lucia.fernandez@universidad.edu", "avatar": "LF", "created_at": "2024-02-20T14:00:00"},
]

notas_db: List[dict] = [
    {
        "id": 1, "titulo": "Apuntes de Cálculo II",
        "contenido": "Las integrales dobles se calculan iterando integrales simples. El teorema de Fubini permite cambiar el orden de integración cuando la función es continua en el dominio rectangular. Es fundamental dominar el cambio de variable a coordenadas polares para regiones circulares.",
        "usuario_id": 1, "created_at": "2024-03-01T10:00:00", "updated_at": "2024-03-01T10:00:00",
    },
    {
        "id": 2, "titulo": "Historia de la Segunda Guerra Mundial",
        "contenido": "La Segunda Guerra Mundial comenzó en 1939 con la invasión de Polonia por parte de Alemania. Los principales aliados fueron Reino Unido, Francia, URSS y Estados Unidos. El conflicto terminó en 1945 con la rendición de Alemania y Japón.",
        "usuario_id": 1, "created_at": "2024-03-05T11:30:00", "updated_at": "2024-03-06T09:00:00",
    },
    {
        "id": 3, "titulo": "Programación Orientada a Objetos",
        "contenido": "Los cuatro pilares de la POO son: Encapsulación, Herencia, Polimorfismo y Abstracción. En Python se definen clases con la palabra reservada 'class'. La herencia múltiple está disponible aunque se recomienda usar composición cuando sea posible.",
        "usuario_id": 2, "created_at": "2024-03-10T14:00:00", "updated_at": "2024-03-10T14:00:00",
    },
    {
        "id": 4, "titulo": "Química Orgánica – Hidrocarburos",
        "contenido": "Los hidrocarburos son compuestos formados exclusivamente por carbono e hidrógeno. Se clasifican en alcanos (enlaces simples), alquenos (doble enlace) y alquinos (triple enlace). Los aromáticos como el benceno poseen un sistema conjugado de electrones π.",
        "usuario_id": 2, "created_at": "2024-03-12T09:00:00", "updated_at": "2024-03-12T09:00:00",
    },
    {
        "id": 5, "titulo": "Macroeconomía – Política Fiscal",
        "contenido": "La política fiscal es el conjunto de medidas que adopta el gobierno en relación con el gasto público y los impuestos. Busca influir en la actividad económica, controlar el ciclo económico y redistribuir la renta. El multiplicador keynesiano explica el efecto amplificado del gasto.",
        "usuario_id": 3, "created_at": "2024-03-15T16:00:00", "updated_at": "2024-03-16T10:00:00",
    },
    {
        "id": 6, "titulo": "Anatomía del Sistema Nervioso",
        "contenido": "El sistema nervioso central está compuesto por el encéfalo y la médula espinal. El sistema nervioso periférico incluye los nervios craneales y espinales. Las neuronas transmiten impulsos eléctricos a través de sinapsis químicas mediadas por neurotransmisores.",
        "usuario_id": 3, "created_at": "2024-03-18T08:30:00", "updated_at": "2024-03-18T08:30:00",
    },
    {
        "id": 7, "titulo": "Derecho Constitucional – Derechos Fundamentales",
        "contenido": "La Constitución es la norma fundamental del ordenamiento jurídico. Establece los derechos fundamentales de los ciudadanos y organiza los poderes del Estado. Los derechos se dividen en civiles, políticos, económicos, sociales y culturales.",
        "usuario_id": 4, "created_at": "2024-03-20T13:00:00", "updated_at": "2024-03-21T11:00:00",
    },
    {
        "id": 8, "titulo": "Física Cuántica – Principio de Incertidumbre",
        "contenido": "El principio de incertidumbre de Heisenberg establece que no es posible conocer simultáneamente con precisión arbitraria la posición y el momento lineal de una partícula. Matemáticamente: Δx·Δp ≥ ℏ/2. Esto tiene profundas implicaciones en la naturaleza de la realidad.",
        "usuario_id": 4, "created_at": "2024-03-22T15:00:00", "updated_at": "2024-03-22T15:00:00",
    },
]

etiquetas_db: List[dict] = [
    {"id": 1, "nombre": "Matemáticas",  "color": "#3B82F6"},
    {"id": 2, "nombre": "Historia",     "color": "#EF4444"},
    {"id": 3, "nombre": "Ciencias",     "color": "#10B981"},
    {"id": 4, "nombre": "Programación", "color": "#8B5CF6"},
    {"id": 5, "nombre": "Química",      "color": "#F59E0B"},
    {"id": 6, "nombre": "Economía",     "color": "#06B6D4"},
    {"id": 7, "nombre": "Medicina",     "color": "#EC4899"},
    {"id": 8, "nombre": "Derecho",      "color": "#6B7280"},
]

nota_etiquetas_db: List[dict] = [
    {"id": 1,  "nota_id": 1, "etiqueta_id": 1},
    {"id": 2,  "nota_id": 1, "etiqueta_id": 3},
    {"id": 3,  "nota_id": 2, "etiqueta_id": 2},
    {"id": 4,  "nota_id": 3, "etiqueta_id": 4},
    {"id": 5,  "nota_id": 3, "etiqueta_id": 3},
    {"id": 6,  "nota_id": 4, "etiqueta_id": 5},
    {"id": 7,  "nota_id": 4, "etiqueta_id": 3},
    {"id": 8,  "nota_id": 5, "etiqueta_id": 6},
    {"id": 9,  "nota_id": 6, "etiqueta_id": 7},
    {"id": 10, "nota_id": 6, "etiqueta_id": 3},
    {"id": 11, "nota_id": 7, "etiqueta_id": 8},
    {"id": 12, "nota_id": 8, "etiqueta_id": 1},
    {"id": 13, "nota_id": 8, "etiqueta_id": 3},
]

_counters = {"usuario": 6, "nota": 9, "etiqueta": 9, "nota_etiqueta": 14}

def next_id(entity: str) -> int:
    val = _counters[entity]
    _counters[entity] += 1
    return val

# ─── Health Check ─────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {
        "app": "App de Notas API",
        "version": "1.0.0",
        "status": "running",
        "entities": {
            "usuarios": len(usuarios_db),
            "notas": len(notas_db),
            "etiquetas": len(etiquetas_db),
            "nota_etiquetas": len(nota_etiquetas_db),
        },
        "endpoints": ["/usuarios", "/notas", "/etiquetas", "/nota-etiquetas"],
    }

# ─── CRUD Usuarios ────────────────────────────────────────────────────────────

@app.get("/usuarios")
def get_usuarios():
    return usuarios_db

@app.get("/usuarios/{usuario_id}")
def get_usuario(usuario_id: int):
    usuario = next((u for u in usuarios_db if u["id"] == usuario_id), None)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@app.post("/usuarios", status_code=201)
def create_usuario(data: UsuarioCreate):
    if next((u for u in usuarios_db if u["email"] == data.email), None):
        raise HTTPException(status_code=409, detail="Ya existe un usuario con ese email")
    nuevo = {
        "id": next_id("usuario"),
        "nombre": data.nombre,
        "email": data.email,
        "avatar": data.avatar if data.avatar else data.nombre[:2].upper(),
        "created_at": datetime.now().isoformat(),
    }
    usuarios_db.append(nuevo)
    return nuevo

@app.put("/usuarios/{usuario_id}")
def update_usuario(usuario_id: int, data: UsuarioUpdate):
    usuario = next((u for u in usuarios_db if u["id"] == usuario_id), None)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if data.nombre is not None:
        usuario["nombre"] = data.nombre
    if data.email is not None:
        if next((u for u in usuarios_db if u["email"] == data.email and u["id"] != usuario_id), None):
            raise HTTPException(status_code=409, detail="Ya existe un usuario con ese email")
        usuario["email"] = data.email
    if data.avatar is not None:
        usuario["avatar"] = data.avatar
    return usuario

@app.delete("/usuarios/{usuario_id}")
def delete_usuario(usuario_id: int):
    global usuarios_db
    if not next((u for u in usuarios_db if u["id"] == usuario_id), None):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usuarios_db = [u for u in usuarios_db if u["id"] != usuario_id]
    return {"message": "Usuario eliminado correctamente", "id": usuario_id}

# ─── CRUD Notas ───────────────────────────────────────────────────────────────

@app.get("/notas")
def get_notas(
    usuario_id: Optional[int] = Query(default=None),
    etiqueta_id: Optional[int] = Query(default=None),
    q: Optional[str] = Query(default=None, description="Búsqueda en título o contenido"),
):
    result = list(notas_db)
    if usuario_id is not None:
        result = [n for n in result if n["usuario_id"] == usuario_id]
    if etiqueta_id is not None:
        ids_con_etiqueta = {ne["nota_id"] for ne in nota_etiquetas_db if ne["etiqueta_id"] == etiqueta_id}
        result = [n for n in result if n["id"] in ids_con_etiqueta]
    if q:
        ql = q.lower().strip()
        result = [n for n in result if ql in n["titulo"].lower() or ql in n["contenido"].lower()]
    return result

@app.get("/notas/{nota_id}")
def get_nota(nota_id: int):
    nota = next((n for n in notas_db if n["id"] == nota_id), None)
    if not nota:
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    etiquetas_ids = [ne["etiqueta_id"] for ne in nota_etiquetas_db if ne["nota_id"] == nota_id]
    etiquetas = [e for e in etiquetas_db if e["id"] in etiquetas_ids]
    return {**nota, "etiquetas": etiquetas}

@app.post("/notas", status_code=201)
def create_nota(data: NotaCreate):
    if not next((u for u in usuarios_db if u["id"] == data.usuario_id), None):
        raise HTTPException(status_code=404, detail="El usuario_id especificado no existe")
    now = datetime.now().isoformat()
    nueva = {
        "id": next_id("nota"),
        "titulo": data.titulo,
        "contenido": data.contenido,
        "usuario_id": data.usuario_id,
        "created_at": now,
        "updated_at": now,
    }
    notas_db.append(nueva)
    return nueva

@app.put("/notas/{nota_id}")
def update_nota(nota_id: int, data: NotaUpdate):
    nota = next((n for n in notas_db if n["id"] == nota_id), None)
    if not nota:
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    if data.titulo is not None:
        nota["titulo"] = data.titulo
    if data.contenido is not None:
        nota["contenido"] = data.contenido
    if data.usuario_id is not None:
        if not next((u for u in usuarios_db if u["id"] == data.usuario_id), None):
            raise HTTPException(status_code=404, detail="El usuario_id especificado no existe")
        nota["usuario_id"] = data.usuario_id
    nota["updated_at"] = datetime.now().isoformat()
    return nota

@app.delete("/notas/{nota_id}")
def delete_nota(nota_id: int):
    global notas_db, nota_etiquetas_db
    if not next((n for n in notas_db if n["id"] == nota_id), None):
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    notas_db = [n for n in notas_db if n["id"] != nota_id]
    nota_etiquetas_db = [ne for ne in nota_etiquetas_db if ne["nota_id"] != nota_id]
    return {"message": "Nota eliminada correctamente", "id": nota_id}

# ─── CRUD Etiquetas ───────────────────────────────────────────────────────────

@app.get("/etiquetas")
def get_etiquetas():
    return [
        {**e, "conteo_notas": sum(1 for ne in nota_etiquetas_db if ne["etiqueta_id"] == e["id"])}
        for e in etiquetas_db
    ]

@app.get("/etiquetas/{etiqueta_id}")
def get_etiqueta(etiqueta_id: int):
    etiqueta = next((e for e in etiquetas_db if e["id"] == etiqueta_id), None)
    if not etiqueta:
        raise HTTPException(status_code=404, detail="Etiqueta no encontrada")
    notas_ids = [ne["nota_id"] for ne in nota_etiquetas_db if ne["etiqueta_id"] == etiqueta_id]
    notas = [n for n in notas_db if n["id"] in notas_ids]
    return {**etiqueta, "notas": notas}

@app.post("/etiquetas", status_code=201)
def create_etiqueta(data: EtiquetaCreate):
    if next((e for e in etiquetas_db if e["nombre"].lower() == data.nombre.lower()), None):
        raise HTTPException(status_code=409, detail="Ya existe una etiqueta con ese nombre")
    nueva = {"id": next_id("etiqueta"), "nombre": data.nombre, "color": data.color}
    etiquetas_db.append(nueva)
    return nueva

@app.put("/etiquetas/{etiqueta_id}")
def update_etiqueta(etiqueta_id: int, data: EtiquetaUpdate):
    etiqueta = next((e for e in etiquetas_db if e["id"] == etiqueta_id), None)
    if not etiqueta:
        raise HTTPException(status_code=404, detail="Etiqueta no encontrada")
    if data.nombre is not None:
        if next((e for e in etiquetas_db if e["nombre"].lower() == data.nombre.lower() and e["id"] != etiqueta_id), None):
            raise HTTPException(status_code=409, detail="Ya existe una etiqueta con ese nombre")
        etiqueta["nombre"] = data.nombre
    if data.color is not None:
        etiqueta["color"] = data.color
    return etiqueta

@app.delete("/etiquetas/{etiqueta_id}")
def delete_etiqueta(etiqueta_id: int):
    global etiquetas_db, nota_etiquetas_db
    if not next((e for e in etiquetas_db if e["id"] == etiqueta_id), None):
        raise HTTPException(status_code=404, detail="Etiqueta no encontrada")
    etiquetas_db = [e for e in etiquetas_db if e["id"] != etiqueta_id]
    nota_etiquetas_db = [ne for ne in nota_etiquetas_db if ne["etiqueta_id"] != etiqueta_id]
    return {"message": "Etiqueta eliminada correctamente", "id": etiqueta_id}

# ─── CRUD NotaEtiqueta ────────────────────────────────────────────────────────

@app.get("/nota-etiquetas")
def get_nota_etiquetas(
    nota_id: Optional[int] = Query(default=None),
    etiqueta_id: Optional[int] = Query(default=None),
):
    result = list(nota_etiquetas_db)
    if nota_id is not None:
        result = [ne for ne in result if ne["nota_id"] == nota_id]
    if etiqueta_id is not None:
        result = [ne for ne in result if ne["etiqueta_id"] == etiqueta_id]
    return result

@app.get("/nota-etiquetas/{nota_etiqueta_id}")
def get_nota_etiqueta(nota_etiqueta_id: int):
    ne = next((ne for ne in nota_etiquetas_db if ne["id"] == nota_etiqueta_id), None)
    if not ne:
        raise HTTPException(status_code=404, detail="Relación NotaEtiqueta no encontrada")
    nota = next((n for n in notas_db if n["id"] == ne["nota_id"]), None)
    etiqueta = next((e for e in etiquetas_db if e["id"] == ne["etiqueta_id"]), None)
    return {**ne, "nota": nota, "etiqueta": etiqueta}

@app.post("/nota-etiquetas", status_code=201)
def create_nota_etiqueta(data: NotaEtiquetaCreate):
    if not next((n for n in notas_db if n["id"] == data.nota_id), None):
        raise HTTPException(status_code=404, detail="La nota especificada no existe")
    if not next((e for e in etiquetas_db if e["id"] == data.etiqueta_id), None):
        raise HTTPException(status_code=404, detail="La etiqueta especificada no existe")
    if next((ne for ne in nota_etiquetas_db if ne["nota_id"] == data.nota_id and ne["etiqueta_id"] == data.etiqueta_id), None):
        raise HTTPException(status_code=409, detail="Esta nota ya tiene asignada esa etiqueta")
    nueva = {"id": next_id("nota_etiqueta"), "nota_id": data.nota_id, "etiqueta_id": data.etiqueta_id}
    nota_etiquetas_db.append(nueva)
    return nueva

@app.put("/nota-etiquetas/{nota_etiqueta_id}")
def update_nota_etiqueta(nota_etiqueta_id: int, data: NotaEtiquetaUpdate):
    ne = next((ne for ne in nota_etiquetas_db if ne["id"] == nota_etiqueta_id), None)
    if not ne:
        raise HTTPException(status_code=404, detail="Relación NotaEtiqueta no encontrada")
    new_nota_id = data.nota_id if data.nota_id is not None else ne["nota_id"]
    new_etiqueta_id = data.etiqueta_id if data.etiqueta_id is not None else ne["etiqueta_id"]
    if data.nota_id is not None and not next((n for n in notas_db if n["id"] == data.nota_id), None):
        raise HTTPException(status_code=404, detail="La nota especificada no existe")
    if data.etiqueta_id is not None and not next((e for e in etiquetas_db if e["id"] == data.etiqueta_id), None):
        raise HTTPException(status_code=404, detail="La etiqueta especificada no existe")
    if next((x for x in nota_etiquetas_db if x["nota_id"] == new_nota_id and x["etiqueta_id"] == new_etiqueta_id and x["id"] != nota_etiqueta_id), None):
        raise HTTPException(status_code=409, detail="Ya existe esa combinación nota-etiqueta")
    ne["nota_id"] = new_nota_id
    ne["etiqueta_id"] = new_etiqueta_id
    return ne

@app.delete("/nota-etiquetas/{nota_etiqueta_id}")
def delete_nota_etiqueta(nota_etiqueta_id: int):
    global nota_etiquetas_db
    if not next((ne for ne in nota_etiquetas_db if ne["id"] == nota_etiqueta_id), None):
        raise HTTPException(status_code=404, detail="Relación NotaEtiqueta no encontrada")
    nota_etiquetas_db = [x for x in nota_etiquetas_db if x["id"] != nota_etiqueta_id]
    return {"message": "Relación eliminada correctamente", "id": nota_etiqueta_id}

# ─── Entry Point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)