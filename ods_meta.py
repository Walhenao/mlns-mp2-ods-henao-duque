# -*- coding: utf-8 -*-
"""Pictogramas ODS (paleta oficial) + metadatos."""
from __future__ import annotations

ODS_COLOR = {
    1: "#E5243B",
    2: "#DDA63A",
    3: "#4C9F38",
    4: "#C5192D",
    5: "#FF3A21",
    6: "#26BDE2",
    7: "#FCC30B",
    8: "#A21942",
    9: "#FD6925",
    10: "#DD1367",
    11: "#FD9D24",
    12: "#BF8B2E",
    13: "#3F7E44",
    14: "#0A97D9",
    15: "#56C02B",
    16: "#00689D",
}

ODS_NOMBRE = {
    1: "Fin de la pobreza",
    2: "Hambre cero",
    3: "Salud y bienestar",
    4: "Educación de calidad",
    5: "Igualdad de género",
    6: "Agua limpia y saneamiento",
    7: "Energía asequible",
    8: "Trabajo decente",
    9: "Industria e innovación",
    10: "Reducir desigualdades",
    11: "Ciudades sostenibles",
    12: "Producción y consumo",
    13: "Acción por el clima",
    14: "Vida submarina",
    15: "Vida de ecosistemas",
    16: "Paz, justicia e instituciones",
}

ODS_BLURB = {
    1: "Poner fin a la pobreza en todas sus formas.",
    2: "Poner fin al hambre y lograr la seguridad alimentaria.",
    3: "Garantizar una vida sana y promover el bienestar.",
    4: "Garantizar una educación inclusiva, equitativa y de calidad.",
    5: "Lograr la igualdad entre los géneros y empoderar a las mujeres.",
    6: "Garantizar la disponibilidad de agua y saneamiento.",
    7: "Garantizar el acceso a energía asequible y sostenible.",
    8: "Promover el crecimiento económico y el trabajo decente.",
    9: "Construir infraestructuras e impulsar la innovación.",
    10: "Reducir la desigualdad en y entre los países.",
    11: "Lograr que las ciudades sean inclusivas y sostenibles.",
    12: "Garantizar modalidades de consumo y producción sostenibles.",
    13: "Adoptar medidas urgentes contra el cambio climático.",
    14: "Conservar y utilizar de forma sostenible los océanos.",
    15: "Proteger, restablecer y promover el uso sostenible de los ecosistemas.",
    16: "Promover sociedades pacíficas e instituciones eficaces.",
}

_GLYPHS = {
    1: '<circle cx="32" cy="38" r="10"/><path d="M18 58c0-8 6-14 14-14h12c8 0 14 6 14 14"/>',
    2: '<path d="M20 44c0-10 8-18 18-18h0c10 0 18 8 18 18v10H20z"/><rect x="28" y="22" width="16" height="8" rx="2"/>',
    3: '<path d="M32 18c-8 10-16 18-16 28a16 16 0 0032 0c0-10-8-18-16-28z"/>',
    4: '<path d="M16 46V26l16-8 16 8v20"/><path d="M24 42v-10l8-4 8 4v10"/><rect x="46" y="28" width="4" height="18"/>',
    5: '<circle cx="32" cy="24" r="8"/><path d="M20 54V40c0-4 5-8 12-8h0c7 0 12 4 12 8v14"/><path d="M32 40v16"/>',
    6: '<path d="M18 28c6 0 8 8 14 8s8-8 14-8 8 8 14 8"/><path d="M18 40c6 0 8 8 14 8s8-8 14-8 8 8 14 8"/><path d="M18 52c6 0 8 8 14 8s8-8 14-8"/>',
    7: '<circle cx="32" cy="32" r="10"/><path d="M32 14v6M32 44v6M14 32h6M44 32h6M19 19l4 4M41 41l4 4M45 19l-4 4M23 41l-4 4"/>',
    8: '<rect x="18" y="28" width="28" height="22" rx="2"/><path d="M24 28v-6a8 8 0 0116 0v6"/>',
    9: '<path d="M16 50V30l10-8 10 8v20"/><path d="M28 50V34l8-6 8 6v16"/><rect x="44" y="26" width="6" height="24"/>',
    10: '<circle cx="24" cy="36" r="8"/><circle cx="40" cy="28" r="10"/><path d="M14 52h36"/>',
    11: '<path d="M14 50V34l10-8 8 6V22l10-6 10 8v26z"/><rect x="28" y="40" width="6" height="10"/>',
    12: '<path d="M20 24h24l4 12H16z"/><rect x="22" y="36" width="20" height="16" rx="1"/><circle cx="26" cy="52" r="3"/><circle cx="38" cy="52" r="3"/>',
    13: '<path d="M32 16c10 8 16 16 16 26a16 16 0 01-32 0c0-6 3-12 8-18"/><path d="M28 34h8v16h-8z"/>',
    14: '<path d="M12 34c8-8 16-10 20-10s12 2 20 10"/><path d="M16 42c6-4 12-6 16-6s10 2 16 6"/><circle cx="40" cy="28" r="4"/>',
    15: '<path d="M32 50V28"/><path d="M32 34c-8-2-14 4-14 10"/><path d="M32 30c8-2 14 4 14 10"/><circle cx="32" cy="22" r="5"/>',
    16: '<path d="M20 20h24v8H20z"/><path d="M24 28v24"/><path d="M40 28v24"/><path d="M24 40h16"/><path d="M28 52h8"/>',
}


def icon_svg(ods: int, size: int = 64) -> str:
    color = ODS_COLOR.get(ods, "#333333")
    glyph = _GLYPHS.get(ods, "")
    name = ODS_NOMBRE.get(ods, f"ODS {ods}")
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 64 64" role="img" aria-label="ODS {ods}: {name}">'
        f'<rect width="64" height="64" fill="{color}"/>'
        f'<g fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" '
        f'stroke-linejoin="round">{glyph}</g>'
        f'<text x="6" y="14" fill="#fff" font-size="10" '
        f'font-family="Georgia, serif" font-weight="700">{ods}</text>'
        f"</svg>"
    )
