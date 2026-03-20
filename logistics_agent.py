import re
import unicodedata

from logistics_tool import costs_by_model, estimate_eta, nearest_courier


DEFAULT_PICKUP_LAT = 6.2442030
DEFAULT_PICKUP_LON = -75.5812120


def _normalize(text: str) -> str:
    text = text.lower().strip()
    return "".join(
        c for c in unicodedata.normalize("NFD", text)
        if unicodedata.category(c) != "Mn"
    )


def _extract_two_floats(text: str):
    nums = re.findall(r"-?\d+\.\d+|-?\d+", text)
    if len(nums) < 2:
        return None
    return float(nums[0]), float(nums[1])


def _extract_distance_km(text: str, default: float = 8.4) -> float:
    match = re.search(r"(\d+(?:\.\d+)?)\s*km", text)
    if match:
        return float(match.group(1))

    any_number = re.search(r"(\d+(?:\.\d+)?)", text)
    if any_number:
        return float(any_number.group(1))

    return default


def _extract_carga(text: str, default: int = 2) -> int:
    match = re.search(r"carga\s*(\d+)", text)
    if match:
        return int(match.group(1))
    return default


def agent(question: str) -> str:
    q = _normalize(question)

    if any(k in q for k in ["cercano", "cerca", "pickup", "recogida", "prioritario", "repartidor"]):
        coords = _extract_two_floats(q)
        if coords:
            lat, lon = coords
        else:
            lat, lon = DEFAULT_PICKUP_LAT, DEFAULT_PICKUP_LON

        return nearest_courier(lat, lon)

    if (
        "costo" in q
        or "combustible" in q
        or "mantenimiento" in q
    ) and (
        "km" in q
        or "kilometro" in q
        or "kilometraje" in q
        or "motocicleta" in q
        or "flota" in q
    ):
        return costs_by_model()

    if any(k in q for k in ["eta", "tarda", "tiempo", "demora", "llegar", "predecir"]):
        distancia = _extract_distance_km(q)
        carga = _extract_carga(q)
        return estimate_eta(distancia, carga)

    return (
        "Puedo ayudarte con 3 consultas: repartidor mas cercano, "
        "costo por km por modelo y estimacion ETA."
    )
