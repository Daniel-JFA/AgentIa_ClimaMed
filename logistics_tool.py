import os
import subprocess


DB_HOST = os.getenv("LOGISTIC_DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("LOGISTIC_DB_PORT", "3306")
DB_USER = os.getenv("LOGISTIC_DB_USER", "root")
DB_PASS = os.getenv("LOGISTIC_DB_PASS", "root")
DB_NAME = os.getenv("LOGISTIC_DB_NAME", "Logistic")
RESPONSE_MODE = "tecnico"


def set_response_mode(mode: str) -> bool:
    global RESPONSE_MODE
    mode = mode.lower().strip()
    if mode not in {"presentacion", "tecnico"}:
        return False
    RESPONSE_MODE = mode
    return True


def get_response_mode() -> str:
    return RESPONSE_MODE


def _with_source(answer: str, source: str, method: str) -> str:
    if RESPONSE_MODE == "presentacion":
        return answer
    return (
        f"{answer}\n"
        f"Fuente: {source}\n"
        f"Metodo: {method}"
    )


def _run_sql(sql: str) -> str:
    """Run a SQL statement via mysql CLI and return raw tab-separated output."""
    cmd = [
        "mysql",
        f"-h{DB_HOST}",
        f"-P{DB_PORT}",
        f"-u{DB_USER}",
        f"-D{DB_NAME}",
        "-N",
        "-B",
        "-e",
        sql,
    ]

    env = os.environ.copy()
    env["MYSQL_PWD"] = DB_PASS

    result = subprocess.run(cmd, capture_output=True, text=True, env=env)

    if result.returncode != 0:
        msg = result.stderr.strip() or "Error desconocido al consultar la BD."
        return f"ERROR: {msg}"

    return result.stdout.strip()


def nearest_courier(pickup_lat: float, pickup_lon: float) -> str:
    sql = f"""
    SELECT
        r.id_repartidor,
        r.nombre,
        u.latitud,
        u.longitud,
        ROUND((6371 * ACOS(
            COS(RADIANS({pickup_lat})) * COS(RADIANS(u.latitud))
            * COS(RADIANS(u.longitud) - RADIANS({pickup_lon}))
            + SIN(RADIANS({pickup_lat})) * SIN(RADIANS(u.latitud))
        )), 3) AS distancia_km
    FROM repartidores r
    JOIN (
        SELECT ur1.*
        FROM ubicaciones_repartidor ur1
        JOIN (
            SELECT id_repartidor, MAX(fecha_registro) AS fecha_max
            FROM ubicaciones_repartidor
            GROUP BY id_repartidor
        ) ult
          ON ult.id_repartidor = ur1.id_repartidor
         AND ult.fecha_max = ur1.fecha_registro
    ) u ON u.id_repartidor = r.id_repartidor
    WHERE r.estado = 'disponible'
    ORDER BY distancia_km ASC
    LIMIT 1;
    """

    out = _run_sql(sql)
    if out.startswith("ERROR:"):
        return out
    if not out:
        return _with_source(
            "No hay repartidores disponibles con ubicacion registrada.",
            "tablas repartidores y ubicaciones_repartidor",
            "ultima ubicacion por repartidor + distancia Haversine"
        )

    row = out.split("\t")
    answer = (
        "Repartidor mas cercano: "
        f"ID {row[0]} - {row[1]}, "
        f"ubicacion ({row[2]}, {row[3]}), "
        f"distancia aprox {row[4]} km."
    )
    return _with_source(
        answer,
        "tablas repartidores y ubicaciones_repartidor",
        "ultima ubicacion por repartidor + distancia Haversine + filtro estado=disponible"
    )


def costs_by_model() -> str:
    sql = """
    SELECT modelo, costo_combustible_km, costo_mantenimiento_km, costo_total_km
    FROM costo_km_modelo
    ORDER BY costo_total_km ASC;
    """

    out = _run_sql(sql)
    if out.startswith("ERROR:"):
        return out
    if not out:
        return _with_source(
            "No hay datos de costos para calcular costo por km.",
            "vista costo_km_modelo",
            "agregacion de combustible y mantenimiento por kilometro"
        )

    lines = ["Costo por km por modelo:"]
    for line in out.splitlines():
        modelo, comb, mant, total = line.split("\t")
        lines.append(
            f"- {modelo}: combustible={comb}, mantenimiento={mant}, total={total}"
        )

    return _with_source(
        "\n".join(lines),
        "vista costo_km_modelo (motos + costos_operacion)",
        "SUM(costos) / SUM(km) agrupado por modelo"
    )


def estimate_eta(distance_km: float, carga_repartidor: int = 2) -> str:
    sql = f"""
    SELECT estimar_eta_minutos(
        {distance_km},
        COALESCE((
            SELECT factor_trafico
            FROM trafico_historico
            WHERE dia_semana = WEEKDAY(CURDATE()) + 1
              AND hora = HOUR(NOW())
            ORDER BY id_trafico DESC
            LIMIT 1
        ), 1.00),
        COALESCE((
            SELECT factor_clima
            FROM clima_historico
            WHERE fecha = CURDATE()
              AND hora = HOUR(NOW())
            ORDER BY id_clima DESC
            LIMIT 1
        ), 1.00),
        {carga_repartidor}
    );
    """

    out = _run_sql(sql)
    if out.startswith("ERROR:"):
        return out
    if not out:
        return _with_source(
            "No se pudo estimar ETA en este momento.",
            "funcion estimar_eta_minutos + tablas trafico_historico y clima_historico",
            "velocidad base ajustada por trafico, clima y carga"
        )

    answer = (
        f"ETA estimado para {distance_km} km "
        f"con carga {carga_repartidor}: {out} minutos."
    )
    return _with_source(
        answer,
        "funcion estimar_eta_minutos + tablas trafico_historico y clima_historico",
        "COALESCE factor_trafico/factor_clima del momento + penalizacion por carga"
    )
