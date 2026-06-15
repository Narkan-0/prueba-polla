import streamlit as st
import pandas as pd
import json
import os
import random
import base64
from datetime import datetime
import pytz

# CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Polla Mundial 2026 - LABORATORIO DE PRUEBAS", page_icon="🧪", layout="wide")

# CONFIGURACIÓN GENERAL DE USUARIOS Y VARIABLES
PARTICIPANTES = ["Constanza", "David", "Franco", "José Alonso", "José Mario", "Leonardo", "Marlene", "Mario", "Néstor", "Renato", "Sergio"]
CUOTA_INSCRIPCION = 5000
PASSWORD_ADMIN = "admin123"
ARCHIVO_DATOS = "datos_prueba.json"

# CONSOLIDADO OFICIAL DE LOS 104 PARTIDOS SEGÚN FORMATO FIFA
@st.cache_data
def obtener_fixture_completo():
    return [
        # --- FECHA 1 ---
        {"id": 1, "fase_bloque": "Fecha 1", "grupo": "Grupo A", "fecha_ref": "2026-06-11 15:00", "fecha": "11 de Junio", "hora": "15:00", "local": "MÉXICO", "flag_l": "🇲🇽", "visita": "SUDÁFRICA", "flag_v": "🇿🇦", "estadio": "Ciudad de México"},
        {"id": 2, "fase_bloque": "Fecha 1", "grupo": "Grupo A", "fecha_ref": "2026-06-11 22:00", "fecha": "11 de Junio", "hora": "22:00", "local": "COREA DEL SUR", "flag_l": "🇰🇷", "visita": "REP. CHECA", "flag_v": "🇨🇿", "estadio": "Guadalajara"},
        {"id": 3, "fase_bloque": "Fecha 1", "grupo": "Grupo B", "fecha_ref": "2026-06-12 15:00", "fecha": "12 de Junio", "hora": "15:00", "local": "CANADÁ", "flag_l": "🇨🇦", "visita": "BOSNIA Y HERZEG.", "flag_v": "🇧🇦", "estadio": "Toronto"},
        {"id": 4, "fase_bloque": "Fecha 1", "grupo": "Grupo D", "fecha_ref": "2026-06-12 21:00", "fecha": "12 de Junio", "hora": "21:00", "local": "ESTADOS UNIDOS", "flag_l": "🇺🇸", "visita": "PARAGUAY", "flag_v": "🇵🇾", "estadio": "Los Angeles"},
        {"id": 5, "fase_bloque": "Fecha 1", "grupo": "Grupo B", "fecha_ref": "2026-06-13 15:00", "fecha": "13 de Junio", "hora": "15:00", "local": "CATAR", "flag_l": "🇶🇦", "visita": "SUIZA", "flag_v": "🇨🇭", "estadio": "San Francisco"},
        {"id": 6, "fase_bloque": "Fecha 1", "grupo": "Grupo C", "fecha_ref": "2026-06-13 18:00", "fecha": "13 de Junio", "hora": "18:00", "local": "BRASIL", "flag_l": "🇧🇷", "visita": "MARRUECOS", "flag_v": "🇲🇦", "estadio": "N. York/N. Jersey"},
        {"id": 7, "fase_bloque": "Fecha 1", "grupo": "Grupo C", "fecha_ref": "2026-06-13 21:00", "fecha": "13 de Junio", "hora": "21:00", "local": "HAITÍ", "flag_l": "🇭🇹", "visita": "ESCOCIA", "flag_v": "\U0001F3F4\U000E0067\U000E0062\U000E0073\U000E0063\U000E0074\U000E007F", "estadio": "Boston"},
        {"id": 8, "fase_bloque": "Fecha 1", "grupo": "Grupo D", "fecha_ref": "2026-06-14 00:00", "fecha": "14 de Junio", "hora": "00:00", "local": "AUSTRALIA", "flag_l": "🇦🇺", "visita": "TURQUÍA", "flag_v": "🇹🇷", "estadio": "Vancouver"},
        {"id": 9, "fase_bloque": "Fecha 1", "grupo": "Grupo E", "fecha_ref": "2026-06-14 13:00", "fecha": "14 de Junio", "hora": "13:00", "local": "ALEMANIA", "flag_l": "🇩🇪", "visita": "CURAZAO", "flag_v": "🇨🇼", "estadio": "Houston"},
        {"id": 10, "fase_bloque": "Fecha 1", "grupo": "Grupo F", "fecha_ref": "2026-06-14 16:00", "fecha": "14 de Junio", "hora": "16:00", "local": "PAÍSES BAJOS", "flag_l": "🇳🇱", "visita": "JAPÓN", "flag_v": "🇯🇵", "estadio": "Dallas"},
        {"id": 11, "fase_bloque": "Fecha 1", "grupo": "Grupo E", "fecha_ref": "2026-06-14 19:00", "fecha": "14 de Junio", "hora": "19:00", "local": "COSTA DE MARFIL", "flag_l": "🇨🇮", "visita": "ECUADOR", "flag_v": "🇪🇨", "estadio": "Filadelfia"},
        {"id": 12, "fase_bloque": "Fecha 1", "grupo": "Grupo F", "fecha_ref": "2026-06-14 22:00", "fecha": "14 de Junio", "hora": "22:00", "local": "SUECIA", "flag_l": "🇸🇪", "visita": "TÚNEZ", "flag_v": "🇹🇳", "estadio": "Monterrey"},
        {"id": 13, "fase_bloque": "Fecha 1", "grupo": "Grupo H", "fecha_ref": "2026-06-15 12:00", "fecha": "15 de Junio", "hora": "12:00", "local": "ESPAÑA", "flag_l": "🇪🇸", "visita": "CABO VERDE", "flag_v": "🇨🇻", "estadio": "Atlanta"},
        {"id": 14, "fase_bloque": "Fecha 1", "grupo": "Grupo G", "fecha_ref": "2026-06-15 15:00", "fecha": "15 de Junio", "hora": "15:00", "local": "BÉLGICA", "flag_l": "🇧🇪", "visita": "EGIPTO", "flag_v": "🇪🇬", "estadio": "Seattle"},
        {"id": 15, "fase_bloque": "Fecha 1", "grupo": "Grupo H", "fecha_ref": "2026-06-15 18:00", "fecha": "15 de Junio", "hora": "18:00", "local": "ARABIA SAUDITA", "flag_l": "🇸🇦", "visita": "URUGUAY", "flag_v": "🇺🇾", "estadio": "Miami"},
        {"id": 16, "fase_bloque": "Fecha 1", "grupo": "Grupo G", "fecha_ref": "2026-06-15 21:00", "fecha": "15 de Junio", "hora": "21:00", "local": "IRÁN", "flag_l": "🇮🇷", "visita": "NUEVA ZELANDA", "flag_v": "🇳🇿", "estadio": "Los Angeles"},
        {"id": 17, "fase_bloque": "Fecha 1", "grupo": "Grupo I", "fecha_ref": "2026-06-16 15:00", "fecha": "16 de Junio", "hora": "15:00", "local": "FRANCIA", "flag_l": "🇫🇷", "visita": "SENEGAL", "flag_v": "🇸🇳", "estadio": "N. York/N. Jersey"},
        {"id": 18, "fase_bloque": "Fecha 1", "grupo": "Grupo L", "fecha_ref": "2026-06-17 16:00", "fecha": "17 de Junio", "hora": "16:00", "local": "INGLATERRA", "flag_l": "\U0001F3F4\U000E0067\U000E0062\U000E0065\U000E006E\U000E0067\U000E007F", "visita": "CROACIA", "flag_v": "🇭🇷", "estadio": "Dallas"},
        {"id": 19, "fase_bloque": "Fecha 1", "grupo": "Grupo I", "fecha_ref": "2026-06-16 18:00", "fecha": "16 de Junio", "hora": "18:00", "local": "IRAK", "flag_l": "🇮🇶", "visita": "NORUEGA", "flag_v": "🇳🇴", "estadio": "Boston"},
        {"id": 20, "fase_bloque": "Fecha 1", "grupo": "Grupo J", "fecha_ref": "2026-06-16 21:00", "fecha": "16 de Junio", "hora": "21:00", "local": "ARGENTINA", "flag_l": "🇦🇷", "visita": "ARGELIA", "flag_v": "🇩🇿", "estadio": "Kansas City"},
        {"id": 21, "fase_bloque": "Fecha 1", "grupo": "Grupo J", "fecha_ref": "2026-06-17 00:00", "fecha": "17 de Junio", "hora": "00:00", "local": "AUSTRIA", "flag_l": "🇦🇹", "visita": "JORDANIA", "flag_v": "🇯🇴", "estadio": "San Francisco"},
        {"id": 22, "fase_bloque": "Fecha 1", "grupo": "Grupo K", "fecha_ref": "2026-06-17 13:00", "fecha": "17 de Junio", "hora": "13:00", "local": "PORTUGAL", "flag_l": "🇵🇹", "visita": "REP. DEL CONGO", "flag_v": "🇨🇬", "estadio": "Houston"},
        {"id": 23, "fase_bloque": "Fecha 1", "grupo": "Grupo L", "fecha_ref": "2026-06-17 19:00", "fecha": "17 de Junio", "hora": "19:00", "local": "GHANA", "flag_l": "🇬🇭", "visita": "PANAMÁ", "flag_v": "🇵🇦", "estadio": "Toronto"},
        {"id": 24, "fase_bloque": "Fecha 1", "grupo": "Grupo K", "fecha_ref": "2026-06-17 22:00", "fecha": "17 de Junio", "hora": "22:00", "local": "UZBEKISTÁN", "flag_l": "🇺🇿", "visita": "COLOMBIA", "flag_v": "🇨🇴", "estadio": "Ciudad de México"},

        # --- FECHA 2 ---
        {"id": 25, "fase_bloque": "Fecha 2", "grupo": "Grupo A", "fecha_ref": "2026-06-18 12:00", "fecha": "18 de Junio", "hora": "12:00", "local": "REP. CHECA", "flag_l": "🇨🇿", "visita": "SUDÁFRICA", "flag_v": "🇿🇦", "estadio": "Atlanta"},
        {"id": 26, "fase_bloque": "Fecha 2", "grupo": "Grupo B", "fecha_ref": "2026-06-18 15:00", "fecha": "18 de Junio", "hora": "15:00", "local": "SUIZA", "flag_l": "🇨🇭", "visita": "BOSNIA Y HERZEG.", "flag_v": "🇧🇦", "estadio": "Los Angeles"},
        {"id": 27, "fase_bloque": "Fecha 2", "grupo": "Grupo B", "fecha_ref": "2026-06-18 18:00", "fecha": "18 de Junio", "hora": "18:00", "local": "CANADÁ", "flag_l": "🇨🇦", "visita": "CATAR", "flag_v": "🇶🇦", "estadio": "Vancouver"},
        {"id": 28, "fase_bloque": "Fecha 2", "grupo": "Grupo A", "fecha_ref": "2026-06-18 21:00", "fecha": "18 de Junio", "hora": "21:00", "local": "MÉXICO", "flag_l": "🇲🇽", "visita": "COREA DEL SUR", "flag_v": "🇰🇷", "estadio": "Guadalajara"},
        {"id": 29, "fase_bloque": "Fecha 2", "grupo": "Grupo D", "fecha_ref": "2026-06-19 15:00", "fecha": "19 de Junio", "hora": "15:00", "local": "ESTADOS UNIDOS", "flag_l": "🇺🇸", "visita": "AUSTRALIA", "flag_v": "🇦🇺", "estadio": "Seattle"},
        {"id": 30, "fase_bloque": "Fecha 2", "grupo": "Grupo C", "fecha_ref": "2026-06-19 18:00", "fecha": "19 de Junio", "hora": "18:00", "local": "ESCOCIA", "flag_l": "\U0001F3F4\U000E0067\U000E0062\U000E0073\U000E0063\U000E0074\U000E007F", "visita": "MARRUECOS", "flag_v": "🇲🇦", "estadio": "Boston"},
        {"id": 31, "fase_bloque": "Fecha 2", "grupo": "Grupo C", "fecha_ref": "2026-06-19 20:30", "fecha": "19 de Junio", "hora": "20:30", "local": "BRASIL", "flag_l": "🇧🇷", "visita": "HAITÍ", "flag_v": "🇭🇹", "estadio": "Filadelfia"},
        {"id": 32, "fase_bloque": "Fecha 2", "grupo": "Grupo D", "fecha_ref": "2026-06-19 23:00", "fecha": "19 de Junio", "hora": "23:00", "local": "TURQUÍA", "flag_l": "🇹🇷", "visita": "PARAGUAY", "flag_v": "🇵🇾", "estadio": "San Francisco"},
        {"id": 33, "fase_bloque": "Fecha 2", "grupo": "Grupo F", "fecha_ref": "2026-06-20 13:00", "fecha": "20 de Junio", "hora": "13:00", "local": "PAÍSES BAJOS", "flag_l": "🇳🇱", "visita": "SUECIA", "flag_v": "🇸🇪", "estadio": "Houston"},
        {"id": 34, "fase_bloque": "Fecha 2", "grupo": "Grupo E", "fecha_ref": "2026-06-20 16:00", "fecha": "20 de Junio", "hora": "16:00", "local": "ALEMANIA", "flag_l": "🇩🇪", "visita": "COSTA DE MARFIL", "flag_v": "🇨🇮", "estadio": "Toronto"},
        {"id": 35, "fase_bloque": "Fecha 2", "grupo": "Grupo E", "fecha_ref": "2026-06-20 20:00", "fecha": "20 de Junio", "hora": "20:00", "local": "ECUADOR", "flag_l": "🇪🇨", "visita": "CURAZAO", "flag_v": "🇨🇼", "estadio": "Kansas City"},
        {"id": 36, "fase_bloque": "Fecha 2", "grupo": "Grupo F", "fecha_ref": "2026-06-21 00:00", "fecha": "21 de Junio", "hora": "00:00", "local": "TÚNEZ", "flag_l": "🇹🇳", "visita": "JAPÓN", "flag_v": "🇯🇵", "estadio": "Monterrey"},
        {"id": 37, "fase_bloque": "Fecha 2", "grupo": "Grupo H", "fecha_ref": "2026-06-21 12:00", "fecha": "21 de Junio", "hora": "12:00", "local": "ESPAÑA", "flag_l": "🇪🇸", "visita": "ARABIA SAUDITA", "flag_v": "🇸🇦", "estadio": "Atlanta"},
        {"id": 38, "fase_bloque": "Fecha 2", "grupo": "Grupo G", "fecha_ref": "2026-06-21 15:00", "fecha": "21 de Junio", "hora": "15:00", "local": "BÉLGICA", "flag_l": "🇧🇪", "visita": "IRÁN", "flag_v": "🇮🇷", "estadio": "Los Angeles"},
        {"id": 39, "fase_bloque": "Fecha 2", "grupo": "Grupo H", "fecha_ref": "2026-06-21 18:00", "fecha": "21 de Junio", "hora": "18:00", "local": "URUGUAY", "flag_l": "🇺🇾", "visita": "CABO VERDE", "flag_v": "🇨🇻", "estadio": "Miami"},
        {"id": 40, "fase_bloque": "Fecha 2", "grupo": "Grupo G", "fecha_ref": "2026-06-21 21:00", "fecha": "21 de Junio", "hora": "21:00", "local": "NUEVA ZELANDA", "flag_l": "🇳🇿", "visita": "EGIPTO", "flag_v": "🇪🇬", "estadio": "Vancouver"},
        {"id": 41, "fase_bloque": "Fecha 2", "grupo": "Grupo K", "fecha_ref": "2026-06-23 13:00", "fecha": "23 de Junio", "hora": "13:00", "local": "PORTUGAL", "flag_l": "🇵🇹", "visita": "UZBEKISTÁN", "flag_v": "🇺🇿", "estadio": "Houston"},
        {"id": 42, "fase_bloque": "Fecha 2", "grupo": "Grupo J", "fecha_ref": "2026-06-22 13:00", "fecha": "22 de Junio", "hora": "13:00", "local": "ARGENTINA", "flag_l": "🇦🇷", "visita": "AUSTRIA", "flag_v": "🇦🇹", "estadio": "Dallas"},
        {"id": 43, "fase_bloque": "Fecha 2", "grupo": "Grupo L", "fecha_ref": "2026-06-23 16:00", "fecha": "23 de Junio", "hora": "16:00", "local": "INGLATERRA", "flag_l": "\U0001F3F4\U000E0067\U000E0062\U000E0065\U000E006E\U000E0067\U000E007F", "visita": "GHANA", "flag_v": "🇬🇭", "estadio": "Boston"},
        {"id": 44, "fase_bloque": "Fecha 2", "grupo": "Grupo I", "fecha_ref": "2026-06-22 17:00", "fecha": "22 de Junio", "hora": "17:00", "local": "FRANCIA", "flag_l": "🇫🇷", "visita": "IRAK", "flag_v": "🇮🇶", "estadio": "Filadelfia"},
        {"id": 45, "fase_bloque": "Fecha 2", "grupo": "Grupo L", "fecha_ref": "2026-06-23 19:00", "fecha": "23 de Junio", "hora": "19:00", "local": "PANAMÁ", "flag_l": "🇵🇦", "visita": "CROACIA", "flag_v": "🇭🇷", "estadio": "Toronto"},
        {"id": 46, "fase_bloque": "Fecha 2", "grupo": "Grupo I", "fecha_ref": "2026-06-22 20:00", "fecha": "22 de Junio", "hora": "20:00", "local": "NORUEGA", "flag_l": "🇳🇴", "visita": "SENEGAL", "flag_v": "🇸🇳", "estadio": "N. York/N. Jersey"},
        {"id": 47, "fase_bloque": "Fecha 2", "grupo": "Grupo K", "fecha_ref": "2026-06-23 22:00", "fecha": "23 de Junio", "hora": "22:00", "local": "COLOMBIA", "flag_l": "🇨🇴", "visita": "REP. DEL CONGO", "flag_v": "🇨🇬", "estadio": "Guadalajara"},
        {"id": 48, "fase_bloque": "Fecha 2", "grupo": "Grupo J", "fecha_ref": "2026-06-22 23:00", "fecha": "22 de Junio", "hora": "23:00", "local": "JORDANIA", "flag_l": "🇯🇴", "visita": "ARGELIA", "flag_v": "🇩🇿", "estadio": "San Francisco"},

        # --- FECHA 3 ---
        {"id": 49, "fase_bloque": "Fecha 3", "grupo": "Grupo B", "fecha_ref": "2026-06-24 15:00", "fecha": "24 de Junio", "hora": "15:00", "local": "SUIZA", "flag_l": "🇨🇭", "visita": "CANADÁ", "flag_v": "🇨🇦", "estadio": "Vancouver"},
        {"id": 50, "fase_bloque": "Fecha 3", "grupo": "Grupo B", "fecha_ref": "2026-06-24 15:00", "fecha": "24 de Junio", "hora": "15:00", "local": "BOSNIA Y HERZEG.", "flag_l": "🇧🇦", "visita": "CATAR", "flag_v": "🇶🇦", "estadio": "Seattle"},
        {"id": 51, "fase_bloque": "Fecha 3", "grupo": "Grupo C", "fecha_ref": "2026-06-24 18:00", "fecha": "24 de Junio", "hora": "18:00", "local": "ESCOCIA", "flag_l": "\U0001F3F4\U000E0067\U000E0062\U000E0073\U000E0063\U000E0074\U000E007F", "visita": "BRASIL", "flag_v": "🇧🇷", "estadio": "Miami"},
        {"id": 52, "fase_bloque": "Fecha 3", "grupo": "Grupo C", "fecha_ref": "2026-06-24 18:00", "fecha": "24 de Junio", "hora": "18:00", "local": "MARRUECOS", "flag_l": "🇲🇦", "visita": "HAITÍ", "flag_v": "🇭🇹", "estadio": "Atlanta"},
        {"id": 53, "fase_bloque": "Fecha 3", "grupo": "Grupo A", "fecha_ref": "2026-06-24 21:00", "fecha": "24 de Junio", "hora": "21:00", "local": "REP. CHECA", "flag_l": "🇨🇿", "visita": "MÉXICO", "flag_v": "🇲🇽", "estadio": "Ciudad de México"},
        {"id": 54, "fase_bloque": "Fecha 3", "grupo": "Grupo A", "fecha_ref": "2026-06-24 21:00", "fecha": "24 de Junio", "hora": "21:00", "local": "SUDÁFRICA", "flag_l": "🇿🇦", "visita": "COREA DEL SUR", "flag_v": "🇰🇷", "estadio": "Monterrey"},
        {"id": 55, "fase_bloque": "Fecha 3", "grupo": "Grupo I", "fecha_ref": "2026-06-26 15:00", "fecha": "26 de Junio", "hora": "15:00", "local": "NORUEGA", "flag_l": "🇳🇴", "visita": "FRANCIA", "flag_v": "🇫🇷", "estadio": "Boston"},
        {"id": 56, "fase_bloque": "Fecha 3", "grupo": "Grupo I", "fecha_ref": "2026-06-26 15:00", "fecha": "26 de Junio", "hora": "15:00", "local": "SENEGAL", "flag_l": "🇸🇳", "visita": "IRAK", "flag_v": "🇮🇶", "estadio": "Toronto"},
        {"id": 57, "fase_bloque": "Fecha 3", "grupo": "Grupo E", "fecha_ref": "2026-06-25 16:00", "fecha": "25 de Junio", "hora": "16:00", "local": "CURAZAO", "flag_l": "🇨🇼", "visita": "COSTA DE MARFIL", "flag_v": "🇨🇮", "estadio": "Filadelfia"},
        {"id": 58, "fase_bloque": "Fecha 3", "grupo": "Grupo E", "fecha_ref": "2026-06-25 16:00", "fecha": "25 de Junio", "hora": "16:00", "local": "ECUADOR", "flag_l": "🇪🇨", "visita": "ALEMANIA", "flag_v": "🇩🇪", "estadio": "N. York/N. Jersey"},
        {"id": 59, "fase_bloque": "Fecha 3", "grupo": "Grupo L", "fecha_ref": "2026-06-27 17:00", "fecha": "27 de Junio", "hora": "17:00", "local": "PANAMÁ", "flag_l": "🇵🇦", "visita": "INGLATERRA", "flag_v": "\U0001F3F4\U000E0067\U000E0062\U000E0065\U000E006E\U000E0067\U000E007F", "estadio": "N. York/N. Jersey"},
        {"id": 60, "fase_bloque": "Fecha 3", "grupo": "Grupo L", "fecha_ref": "2026-06-27 17:00", "fecha": "27 de Junio", "hora": "17:00", "local": "CROACIA", "flag_l": "🇭🇷", "visita": "GHANA", "flag_v": "🇬🇭", "estadio": "Filadelfia"},
        {"id": 61, "fase_bloque": "Fecha 3", "grupo": "Grupo F", "fecha_ref": "2026-06-25 19:00", "fecha": "25 de Junio", "hora": "19:00", "local": "JAPÓN", "flag_l": "🇯🇵", "visita": "SUECIA", "flag_v": "🇸🇪", "estadio": "Dallas"},
        {"id": 62, "fase_bloque": "Fecha 3", "grupo": "Grupo F", "fecha_ref": "2026-06-25 19:00", "fecha": "25 de Junio", "hora": "19:00", "local": "TÚNEZ", "flag_l": "🇹🇳", "visita": "PAÍSES BAJOS", "flag_v": "🇳🇱", "estadio": "Kansas City"},
        {"id": 63, "fase_bloque": "Fecha 3", "grupo": "Grupo K", "fecha_ref": "2026-06-27 19:30", "fecha": "27 de Junio", "hora": "19:30", "local": "COLOMBIA", "flag_l": "🇨🇴", "visita": "PORTUGAL", "flag_v": "🇵🇹", "estadio": "Miami"},
        {"id": 64, "fase_bloque": "Fecha 3", "grupo": "Grupo K", "fecha_ref": "2026-06-27 19:30", "fecha": "27 de Junio", "hora": "19:30", "local": "REP. DEL CONGO", "flag_l": "🇨🇬", "visita": "UZBEKISTÁN", "flag_v": "🇺🇿", "estadio": "Atlanta"},
        {"id": 65, "fase_bloque": "Fecha 3", "grupo": "Grupo H", "fecha_ref": "2026-06-26 20:00", "fecha": "26 de Junio", "hora": "20:00", "local": "CABO VERDE", "flag_l": "🇨🇻", "visita": "ARABIA SAUDITA", "flag_v": "🇸🇦", "estadio": "Houston"},
        {"id": 66, "fase_bloque": "Fecha 3", "grupo": "Grupo H", "fecha_ref": "2026-06-26 20:00", "fecha": "26 de Junio", "hora": "20:00", "local": "URUGUAY", "flag_l": "🇺🇾", "visita": "ESPAÑA", "flag_v": "🇪🇸", "estadio": "Guadalajara"},
        {"id": 67, "fase_bloque": "Fecha 3", "grupo": "Grupo D", "fecha_ref": "2026-06-25 22:00", "fecha": "25 de Junio", "hora": "22:00", "local": "TURQUÍA", "flag_l": "🇹🇷", "visita": "ESTADOS UNIDOS", "flag_v": "🇺🇸", "estadio": "Los Angeles"},
        {"id": 68, "fase_bloque": "Fecha 3", "grupo": "Grupo D", "fecha_ref": "2026-06-25 22:00", "fecha": "25 de Junio", "hora": "22:00", "local": "PARAGUAY", "flag_l": "🇵🇾", "visita": "AUSTRALIA", "flag_v": "🇦🇺", "estadio": "San Francisco"},
        {"id": 69, "fase_bloque": "Fecha 3", "grupo": "Grupo J", "fecha_ref": "2026-06-27 22:00", "fecha": "27 de Junio", "hora": "22:00", "local": "ARGELIA", "flag_l": "🇩🇿", "visita": "AUSTRIA", "flag_v": "🇦🇹", "estadio": "Kansas City"},
        {"id": 70, "fase_bloque": "Fecha 3", "grupo": "Grupo J", "fecha_ref": "2026-06-27 22:00", "fecha": "27 de Junio", "hora": "22:00", "local": "JORDANIA", "flag_l": "🇯🇴", "visita": "ARGENTINA", "flag_v": "🇦🇷", "estadio": "Dallas"},
        {"id": 71, "fase_bloque": "Fecha 3", "grupo": "Grupo G", "fecha_ref": "2026-06-26 23:00", "fecha": "26 de Junio", "hora": "23:00", "local": "EGIPTO", "flag_l": "🇪🇬", "visita": "IRÁN", "flag_v": "🇮🇷", "estadio": "Seattle"},
        {"id": 72, "fase_bloque": "Fecha 3", "grupo": "Grupo G", "fecha_ref": "2026-06-26 23:00", "fecha": "26 de Junio", "hora": "23:00", "local": "NUEVA ZELANDA", "flag_l": "🇳🇿", "visita": "BÉLGICA", "flag_v": "🇧🇪", "estadio": "Vancouver"},

        # --- DIEZISEISAVOS DE FINAL ---
        {"id": 73, "fase_bloque": "Fases Finales", "grupo": "Dieciseisavos", "fecha_ref": "2026-06-28 16:00", "fecha": "28 de Junio", "hora": "16:00", "local": "2A", "flag_l": "⚽", "visita": "2B", "flag_v": "⚽", "estadio": "Los Angeles"},
        {"id": 74, "fase_bloque": "Fases Finales", "grupo": "Dieciseisavos", "fecha_ref": "2026-06-29 15:00", "fecha": "29 de Junio", "hora": "15:00", "local": "1A", "flag_l": "⚽", "visita": "3C/E/F/I", "flag_v": "⚽", "estadio": "Boston"},
        {"id": 75, "fase_bloque": "Fases Finales", "grupo": "Dieciseisavos", "fecha_ref": "2026-06-29 18:00", "fecha": "29 de Junio", "hora": "18:00", "local": "1B", "flag_l": "⚽", "visita": "3A/C/F/H", "flag_v": "⚽", "estadio": "Atlanta"},
        {"id": 76, "fase_bloque": "Fases Finales", "grupo": "Dieciseisavos", "fecha_ref": "2026-06-29 21:00", "fecha": "29 de Junio", "hora": "21:00", "local": "2C", "flag_l": "⚽", "visita": "2D", "flag_v": "⚽", "estadio": "Houston"},
        {"id": 77, "fase_bloque": "Fases Finales", "grupo": "Dieciseisavos", "fecha_ref": "2026-06-30 14:00", "fecha": "30 de Junio", "hora": "14:00", "local": "1F", "flag_l": "⚽", "visita": "2E", "flag_v": "⚽", "estadio": "Dallas"},
        {"id": 78, "fase_bloque": "Fases Finales", "grupo": "Dieciseisavos", "fecha_ref": "2026-06-30 17:00", "fecha": "30 de Junio", "hora": "17:00", "local": "1E", "flag_l": "⚽", "visita": "3A/B/C/D", "flag_v": "⚽", "estadio": "Seattle"},
        {"id": 79, "fase_bloque": "Fases Finales", "grupo": "Dieciseisavos", "fecha_ref": "2026-06-30 20:00", "fecha": "30 de Junio", "hora": "20:00", "local": "1D", "flag_l": "⚽", "visita": "3F/G/H/I", "flag_v": "⚽", "estadio": "San Francisco"},
        {"id": 80, "fase_bloque": "Fases Finales", "grupo": "Dieciseisavos", "fecha_ref": "2026-07-01 13:00", "fecha": "01 de Julio", "hora": "13:00", "local": "1C", "flag_l": "⚽", "visita": "3D/E/I/J", "flag_v": "⚽", "estadio": "Toronto"},
        {"id": 81, "fase_bloque": "Fases Finales", "grupo": "Dieciseisavos", "fecha_ref": "2026-07-01 16:00", "fecha": "01 de Julio", "hora": "16:00", "local": "1I", "flag_l": "⚽", "visita": "3G/H/K/L", "flag_v": "⚽", "estadio": "Filadelfia"},
        {"id": 82, "fase_bloque": "Fases Finales", "grupo": "Dieciseisavos", "fecha_ref": "2026-07-01 19:00", "fecha": "01 de Julio", "hora": "19:00", "local": "2G", "flag_l": "⚽", "visita": "2H", "flag_v": "⚽", "estadio": "Kansas City"},
        {"id": 83, "fase_bloque": "Fases Finales", "grupo": "Dieciseisavos", "fecha_ref": "2026-07-02 14:00", "fecha": "02 de Julio", "hora": "14:00", "local": "1K", "flag_l": "⚽", "visita": "3I/J/L", "flag_v": "⚽", "estadio": "Miami"},
        {"id": 84, "fase_bloque": "Fases Finales", "grupo": "Dieciseisavos", "fecha_ref": "2026-07-02 17:00", "fecha": "02 de Julio", "hora": "17:00", "local": "1G", "flag_l": "⚽", "visita": "3A/B/E/F", "flag_v": "⚽", "estadio": "Vancouver"},
        {"id": 85, "fase_bloque": "Fases Finales", "grupo": "Dieciseisavos", "fecha_ref": "2026-07-02 20:00", "fecha": "02 de Julio", "hora": "20:00", "local": "1H", "flag_l": "⚽", "visita": "2J", "flag_v": "⚽", "estadio": "Ciudad de México"},
        {"id": 86, "fase_bloque": "Fases Finales", "grupo": "Dieciseisavos", "fecha_ref": "2026-07-03 14:00", "fecha": "03 de Julio", "hora": "14:00", "local": "1J", "flag_l": "⚽", "visita": "2K", "flag_v": "⚽", "estadio": "Monterrey"},
        {"id": 87, "fase_bloque": "Fases Finales", "grupo": "Dieciseisavos", "fecha_ref": "2026-07-03 17:00", "fecha": "03 de Julio", "hora": "17:00", "local": "1L", "flag_l": "⚽", "visita": "3G/H/J/K", "flag_v": "⚽", "estadio": "Houston"},
        {"id": 88, "fase_bloque": "Fases Finales", "grupo": "Dieciseisavos", "fecha_ref": "2026-07-03 20:00", "fecha": "03 de Julio", "hora": "20:00", "local": "2I", "flag_l": "⚽", "visita": "2L", "flag_v": "⚽", "estadio": "Dallas"},

        # --- OCTAVOS DE FINAL ---
        {"id": 89, "fase_bloque": "Fases Finales", "grupo": "Octavos", "fecha_ref": "2026-07-04 15:00", "fecha": "04 de Julio", "hora": "15:00", "local": "GANADOR P74", "flag_l": "🥇", "visita": "GANADOR P73", "flag_v": "🥇", "estadio": "Philadelphia"},
        {"id": 90, "fase_bloque": "Fases Finales", "grupo": "Octavos", "fecha_ref": "2026-07-04 18:00", "fecha": "04 de Julio", "hora": "18:00", "local": "GANADOR P75", "flag_l": "🥇", "visita": "GANADOR P76", "flag_v": "🥇", "estadio": "Houston"},
        {"id": 91, "fase_bloque": "Fases Finales", "grupo": "Octavos", "fecha_ref": "2026-07-05 14:00", "fecha": "05 de Julio", "hora": "14:00", "local": "GANADOR P77", "flag_l": "🥇", "visita": "GANADOR P78", "flag_v": "🥇", "estadio": "N. York/N. Jersey"},
        {"id": 92, "fase_bloque": "Fases Finales", "grupo": "Octavos", "fecha_ref": "2026-07-05 18:00", "fecha": "05 de Julio", "hora": "18:00", "local": "GANADOR P79", "flag_l": "🥇", "visita": "GANADOR P80", "flag_v": "🥇", "estadio": "Mexico City"},
        {"id": 93, "fase_bloque": "Fases Finales", "grupo": "Octavos", "fecha_ref": "2026-07-06 15:00", "fecha": "06 de Julio", "hora": "15:00", "local": "GANADOR P81", "flag_l": "🥇", "visita": "GANADOR P82", "flag_v": "🥇", "estadio": "Dallas"},
        {"id": 94, "fase_bloque": "Fases Finales", "grupo": "Octavos", "fecha_ref": "2026-07-06 19:00", "fecha": "06 de Julio", "hora": "19:00", "local": "GANADOR P83", "flag_l": "🥇", "visita": "GANADOR P84", "flag_v": "🥇", "estadio": "Seattle"},
        {"id": 95, "fase_bloque": "Fases Finales", "grupo": "Octavos", "fecha_ref": "2026-07-07 16:00", "fecha": "07 de Julio", "hora": "16:00", "local": "GANADOR P85", "flag_l": "🥇", "visita": "GANADOR P86", "flag_v": "🥇", "estadio": "Atlanta"},
        {"id": 96, "fase_bloque": "Fases Finales", "grupo": "Octavos", "fecha_ref": "2026-07-07 20:00", "fecha": "07 de Julio", "hora": "20:00", "local": "GANADOR P87", "flag_l": "🥇", "visita": "GANADOR P88", "flag_v": "🥇", "estadio": "Vancouver"},

        # --- CUARTOS DE FINAL ---
        {"id": 97, "fase_bloque": "Fases Finales", "grupo": "Cuartos", "fecha_ref": "2026-07-09 16:00", "fecha": "09 de Julio", "hora": "16:00", "local": "GANADOR P89", "flag_l": "🥇", "visita": "GANADOR P90", "flag_v": "🥇", "estadio": "Boston"},
        {"id": 98, "fase_bloque": "Fases Finales", "grupo": "Cuartos", "fecha_ref": "2026-07-10 18:00", "fecha": "10 de Julio", "hora": "18:00", "local": "GANADOR P91", "flag_l": "🥇", "visita": "GANADOR P92", "flag_v": "🥇", "estadio": "Los Angeles"},
        {"id": 99, "fase_bloque": "Fases Finales", "grupo": "Cuartos", "fecha_ref": "2026-07-11 15:00", "fecha": "11 de Julio", "hora": "15:00", "local": "GANADOR P93", "flag_l": "🥇", "visita": "GANADOR P94", "flag_v": "🥇", "estadio": "Miami"},
        {"id": 100, "fase_bloque": "Fases Finales", "grupo": "Cuartos", "fecha_ref": "2026-07-11 20:00", "fecha": "11 de Julio", "hora": "20:00", "local": "GANADOR P95", "flag_l": "🥇", "visita": "GANADOR P96", "flag_v": "🥇", "estadio": "Kansas City"},

        # --- SEMIFINALES ---
        {"id": 101, "fase_bloque": "Fases Finales", "grupo": "Semifinales", "fecha_ref": "2026-07-14 15:00", "fecha": "14 de Julio", "hora": "15:00", "local": "GANADOR P97", "flag_l": "🥇", "visita": "GANADOR P98", "flag_v": "🥇", "estadio": "Dallas"},
        {"id": 102, "fase_bloque": "Fases Finales", "grupo": "Semifinales", "fecha_ref": "2026-07-15 18:00", "fecha": "15 de Julio", "hora": "18:00", "local": "GANADOR P99", "flag_l": "🥇", "visita": "GANADOR P100", "flag_v": "🥇", "estadio": "Atlanta"},

        # --- TERCER PUESTO ---
        {"id": 103, "fase_bloque": "Fases Finales", "grupo": "Tercer Puesto", "fecha_ref": "2026-07-18 15:00", "fecha": "18 de Julio", "hora": "15:00", "local": "PERDEDOR P101", "flag_l": "🥉", "visita": "PERDEDOR P102", "flag_v": "🥉", "estadio": "Miami"},

        # --- GRAN FINAL ---
        {"id": 104, "fase_bloque": "Fases Finales", "grupo": "Gran Final", "fecha_ref": "2026-07-19 15:00", "fecha": "19 de Julio", "hora": "15:00", "local": "GANADOR P101", "flag_l": "🏆", "visita": "GANADOR P102", "flag_v": "🏆", "estadio": "N. York/N. Jersey"}
    ]

FIXTURE = sorted(obtener_fixture_completo(), key=lambda x: x['id'])

@st.cache_data(ttl=10)
def obtener_frase_futbolera():
    frases = [
        "«Todo lo que sé con mayor certeza sobre la moral y las obligaciones de los hombres, se lo debo al fútbol.» — Albert Camus",
        "«El fútbol es el juego más lindo y más sano del mundo. Yo me equivoqué y pagué, pero la pelota no se mancha.» — Diego Maradona",
        "«El fútbol es música, danza y armonía. Y no hay nada más hermoso que la alegría que le da a la gente.» — Pelé",
        "«Por más que los poderosos lo manipulen, el fútbol sigue queriendo ser el arte de lo imprevisto.» — Eduardo Galeano"
    ]
    return random.choice(frases)

# --- INYECTAR TEMA OSCURO FORZADO ---
st.markdown(
    """
    <script>
        var elements = window.parent.document.getElementsByTagName('html');
        if (elements.length > 0) {
            elements[0].setAttribute('data-theme', 'dark');
        }
    </script>
    """,
    unsafe_allow_html=True
)

# --- CARGA SEGURA DE IMÁGENES ---
def cargar_imagen_local(nombre_archivo):
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    return ""

portada_base64 = cargar_imagen_local("portada.jpeg")
fondo_base64 = cargar_imagen_local("fondo.png")
balon_base64 = cargar_imagen_local("balon.jpeg")

# --- DISEÑO Y CSS ---
estilos_css = f"""
<style>
    .stApp {{
        background-color: #0e1117;
        color: #ffffff;
    }}
    
    {" .stApp { background-image: linear-gradient(rgba(14, 17, 23, 0.85), rgba(14, 17, 23, 0.85)), url('data:image/png;base64," + fondo_base64 + "'); background-size: cover; background-attachment: fixed; }" if fondo_base64 else ""}

    .banner-portada {{
        width: 100%;
        height: 220px;
        background-image: url('data:image/jpeg;base64,{portada_base64}');
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
        border-radius: 12px;
        margin-bottom: 20px;
    }}

    .card-partido {{
        background: rgba(38, 43, 54, 0.7);
        border: 1px solid rgba(255, 215, 0, 0.2);
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }}

    .balon-giratorio {{
        width: 50px;
        height: 50px;
        background-image: url('data:image/jpeg;base64,{balon_base64}');
        background-size: cover;
        border-radius: 50%;
        display: inline-block;
        animation: spin 2s linear infinite;
    }}
    @keyframes spin {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}
</style>
"""
st.markdown(estilos_css, unsafe_allow_html=True)

if portada_base64:
    st.markdown('<div class="banner-portada"></div>', unsafe_allow_html=True)
else:
    st.title("⚽ Polla Mundial 2026")

st.markdown(f"<p style='text-align:center; font-style:italic; color:#f1f5f9; font-size:1.05rem; padding:15px 20px 0 20px;'>{obtener_frase_futbolera()}</p>", unsafe_allow_html=True)

if "mensaje_exito" in st.session_state:
    st.success(st.session_state["mensaje_exito"])
    del st.session_state["mensaje_exito"]

st.write("---")

# --- LÓGICA DE PERSISTENCIA ---
def inicializar_base_de_datos():
    base_inicial = {
        "resultados_reales": {},
        "pronosticos": {p: {} for p in PARTICIPANTES}
    }
    if os.path.exists(ARCHIVO_DATOS):
        with open(ARCHIVO_DATOS, "r") as f:
            try:
                content = json.load(f)
                if isinstance(content, dict):
                    if "resultados_reales" in content:
                        base_inicial["resultados_reales"] = content["resultados_reales"]
                    if "pronosticos" in content:
                        for p in PARTICIPANTES:
                            base_inicial["pronosticos"][p] = content["pronosticos"].get(p, {})
                    return base_inicial
            except:
                pass
    return base_inicial

if "datos_globales" not in st.session_state:
    st.session_state["datos_globales"] = inicializar_base_de_datos()

datos = st.session_state["datos_globales"]

def guardar_datos(datos_completos):
    st.session_state["datos_globales"] = datos_completos
    try:
        with open(ARCHIVO_DATOS, "w") as f:
            json.dump(datos_completos, f, indent=4)
    except:
        pass

def resolver_fixture_dinamico(fixture_base, resultados_reales):
    fixture_copia = [dict(m) for m in fixture_base]
    for m in fixture_copia:
        if "GANADOR P" in m["local"]:
            prev_id = m["local"].replace("GANADOR P", "")
            if prev_id in resultados_reales and "avanza" in resultados_reales[prev_id]:
                m["local"] = resultados_reales[prev_id]["avanza"].upper()
                m["flag_l"] = "⚽"
        if "GANADOR P" in m["visita"]:
            prev_id = m["visita"].replace("GANADOR P", "")
            if prev_id in resultados_reales and "avanza" in resultados_reales[prev_id]:
                m["visita"] = resultados_reales[prev_id]["avanza"].upper()
                m["flag_v"] = "⚽"
    return fixture_copia

FIXTURE_DINAMICO = resolver_fixture_dinamico(FIXTURE, datos["resultados_reales"])

def calcular_puntos(real_l, real_v, pred_l, pred_v):
    if real_l is None or real_v is None or pred_l is None or pred_v is None:
        return 0, "#64748b", "⚪ Sin Jugar"
    try:
        rl, rv = int(real_l), int(real_v)
        pl, pv = int(pred_l), int(pred_v)
    except (ValueError, TypeError):
        return 0, "#64748b", "⚪ Sin Jugar"
        
    if rl == pl and rv == pv:
        return 3, "#22c55e", "🟢 Exacto (+3)"
    signo_real = (rl > rv) - (rl < rv)
    signo_pred = (pl > pv) - (pl < pv)
    if signo_real == signo_pred:
        return 1, "#eab308", "🟡 Tendencia (+1)"
    return 0, "#ef4444", "🔴 Fallado (0)"

def verificar_partido_empezado(fecha_ref_str):
    tz_chile = pytz.timezone('America/Santiago')
    ahora_chile = datetime.now(tz_chile)
    try:
        hora_partido = datetime.strptime(fecha_ref_str, "%Y-%m-%d %H:%M")
        hora_partido_tz = tz_chile.localize(hora_partido)
        return ahora_chile >= hora_partido_tz
    except:
        return False

def animar_balon_oficial():
    src_balon = f"data:image/jpeg;base64,{balon_base64}" if balon_base64 else "⚽"
    html_anim = f"""
    <div id="ball-box" style="position:fixed;top:0;left:0;width:100vw;height:100vh;pointer-events:none;z-index:99999;display:flex;justify-content:center;align-items:center;">
        {"<img src='" + src_balon + "' style='width:160px;height:160px;border-radius:50%;animation: spin 1.5s ease-out forwards;'>" if balon_base64 else "<div style='font-size:120px; animation: spin 1.4s ease-out forwards;'>⚽</div>"}
    </div>
    <script>setTimeout(() => {{ document.getElementById('ball-box').remove(); }}, 1500);</script>
    """
    st.components.v1.html(html_anim, height=0, width=0)

tabs = st.tabs(["📜 BASES DEL JUEGO", "📊 CLASIFICACIÓN EN VIVO", "✍️ REGISTRAR PRONÓSTICOS", "📅 CRONOGRAMA", "⚙️ PANEL CONTROL"])

# --- TAB 1: BASES ---
with tabs[0]:
    st.markdown("""
    ## 🏆 BASES POLLA MUNDIALERA 🏆
    
    ⚽ **Inscripción:** $5.000 por cartilla. El 100% va al pozo familiar.
    📅 **Plazo de envío:** Se puede apostar o modificar el pronóstico **hasta el pitazo inicial** de cada partido.
    ⏱️ **Tiempo Reglamentario:** Válido **exclusivamente para los 90 minutos reglamentarios**.
    
    💰 **Premios:**
    * 🥇 **1er Lugar:** 50% del pozo.
    * 🥈 **2do Lugar:** 33,3% del pozo.
    * 🥉 **3er Lugar:** 16,6% del pozo.
    
    📊 **Puntuación:**
    * **3 puntos:** Resultado exacto.
    * **1 punto:** Acierto a Ganador o Empate.
    * **0 puntos:** No acierta nada.
    """)

# --- TAB 2: CLASIFICACIÓN ---
with tabs[1]:
    st.markdown("## 📊 RENDIMIENTO DE LA FAMILIA")
    tabla_posiciones = []
    fondo_total = len(PARTICIPANTES) * CUOTA_INSCRIPCION
    
    for p in PARTICIPANTES:
        pts_totales, exactos, tendencias = 0, 0, 0
        for part in FIXTURE_DINAMICO:
            pid = str(part["id"])
            real = datos["resultados_reales"].get(pid)
            pred = datos["pronosticos"].get(p, {}).get(pid)
            
            if real and pred and "l" in real and "v" in real and "l" in pred and "v" in pred:
                pts, _, _ = calcular_puntos(real["l"], real["v"], pred["l"], pred["v"])
                pts_totales += pts
                if pts == 3: exactos += 1
                elif pts == 1: tendencias += 1
        tabla_posiciones.append({"Participante": p, "Puntos Totales 🌟": pts_totales, "Marcadores Exactos 🎯": exactos, "Aciertos Simples (1pt) 🏟️": tendencias})
    
    df_tabla = pd.DataFrame(tabla_posiciones).sort_values(by=["Puntos Totales 🌟", "Marcadores Exactos 🎯"], ascending=False).reset_index(drop=True)
    df_tabla.index += 1
    
    c_p1, c_p2, c_p3 = st.columns(3)
    with c_p1:
        st.markdown(f"<div style='background:rgba(34,197,94,0.15);padding:15px;border-radius:10px;border:1px solid #22c55e;text-align:center;'><span>🥇 1er Lugar</span><br><strong style='font-size:1.6rem;color:#fbbf24;'>{df_tabla.iloc[0]['Participante'].upper()}</strong><br><span>${fondo_total * 0.50:,.0f}</span></div>", unsafe_allow_html=True)
    with c_p2:
        st.markdown(f"<div style='background:rgba(234,179,8,0.1);padding:15px;border-radius:10px;border:1px solid #eab308;text-align:center;'><span>🥈 2do Lugar</span><br><strong style='font-size:1.4rem;color:#e2e8f0;'>{df_tabla.iloc[1]['Participante'].upper()}</strong><br><span>${fondo_total * 0.333:,.0f}</span></div>", unsafe_allow_html=True)
    with c_p3:
        st.markdown(f"<div style='background:rgba(239,68,68,0.1);padding:15px;border-radius:10px;border:1px solid #ef4444;text-align:center;'><span>🥉 3er Lugar</span><br><strong style='font-size:1.4rem;color:#e2e8f0;'>{df_tabla.iloc[2]['Participante'].upper()}</strong><br><span>${fondo_total * 0.166:,.0f}</span></div>", unsafe_allow_html=True)
        
    st.write("---")
    st.dataframe(df_tabla, use_container_width=True)

# --- TAB 3: REGISTRAR PRONÓSTICOS ---
with tabs[2]:
    st.markdown("## ✍️ ARMA TU JUGADA")
    usuario = st.selectbox("Selecciona tu nombre para apostar:", PARTICIPANTES)
    
    bloque_seleccionado = st.radio("Filtrar por fecha:", ["Fecha 1 (Partidos 1-24)", "Fecha 2 (Partidos 25-48)", "Fecha 3 (Partidos 49-72)", "Fases Finales"], horizontal=True)
    if "Fecha 1" in bloque_seleccionado: filtro_fia = "Fecha 1"
    elif "Fecha 2" in bloque_seleccionado: filtro_fia = "Fecha 2"
    elif "Fecha 3" in bloque_seleccionado: filtro_fia = "Fecha 3"
    else: filtro_fia = "Fases Finales"
    
    partidos_visibles = [m for m in FIXTURE_DINAMICO if m["fase_bloque"] == filtro_fia]
    st.write("---")
    
    with st.form(key=f"form_seguro_{usuario}_{filtro_fia}"):
        respuestas_temporales = {}
        for part in partidos_visibles:
            pid = str(part["id"])
            pred_actual = datos["pronosticos"].get(usuario, {}).get(pid, {})
            real_actual = datos["resultados_reales"].get(pid)
            
            ya_empezo = verificar_partido_empezado(part.get("fecha_ref", "2026-06-11 00:00"))
            congelado_por_admin = pid in datos["resultados_reales"]
            bloquear_casilla = ya_empezo or congelado_por_admin
            
            real_l = real_actual.get("l") if real_actual else None
            real_v = real_actual.get("v") if real_actual else None
            pred_l_val = pred_actual.get("l") if "l" in pred_actual else None
            pred_v_val = pred_actual.get("v") if "v" in pred_actual else None
            
            _, color_hex, texto_status = calcular_puntos(real_l, real_v, pred_l_val, pred_v_val)
            if congelado_por_admin: texto_status += " | 🔒 CERRADO"
            elif ya_empezo: color_hex, texto_status = "#be123c", "🔒 EN CURSO"
            
            # ¡SOLUCIÓN 1!: Fecha y hora explícitas en cada tarjeta de partido
            st.markdown(f"<div style='background:rgba(30,41,59,0.7);padding:6px 12px;border-left:5px solid {color_hex};font-size:0.85rem;margin-top:12px;'><b>{part['grupo'].upper()} — PARTIDO #{pid}</b> ({part['fecha']} - {part['hora']} hrs) | {part['estadio']} | <span style='color:{color_hex};font-weight:bold;'>{texto_status}</span></div>", unsafe_allow_html=True)
            
            c_l, c_in1, c_in2, c_v = st.columns([4, 1, 1, 4])
            with c_l: st.markdown(f"<div style='text-align:right;font-weight:bold;font-size:1rem;padding-top:6px;'>{part['local']} {part['flag_l']}</div>", unsafe_allow_html=True)
            # ¡SOLUCIÓN 2!: Clave única por usuario para que no se hereden los marcadores al cambiar de perfil
            with c_in1: g_l = st.number_input("L", min_value=0, max_value=15, value=pred_l_val, placeholder="-", key=f"l_{usuario}_{pid}", disabled=bloquear_casilla, label_visibility="collapsed")
            with c_in2: g_v = st.number_input("V", min_value=0, max_value=15, value=pred_v_val, placeholder="-", key=f"v_{usuario}_{pid}", disabled=bloquear_casilla, label_visibility="collapsed")
            with c_v: st.markdown(f"<div style='text-align:left;font-weight:bold;font-size:1rem;padding-top:6px;'>{part['flag_v']} {part['visita']}</div>", unsafe_allow_html=True)
            
            respuestas_temporales[pid] = {"l": g_l, "v": g_v}
            
        st.write("---")
        if st.form_submit_button("💾 GUARDAR APUESTAS", use_container_width=True):
            if usuario not in datos["pronosticos"]: datos["pronosticos"][usuario] = {}
            for pid, scores in respuestas_temporales.items():
                p_info = next((m for m in partidos_visibles if str(m["id"]) == pid), None)
                if p_info and not verificar_partido_empezado(p_info.get("fecha_ref", "")) and pid not in datos["resultados_reales"]:
                    if scores["l"] is not None and scores["v"] is not None:
                        datos["pronosticos"][usuario][pid] = {"l": int(scores["l"]), "v": int(scores["v"])}
                    else:
                        datos["pronosticos"][usuario].pop(pid, None)
            guardar_datos(datos)
            animar_balon_oficial()
            st.session_state["mensaje_exito"] = f"¡Excelente, tus pronósticos activos de la {filtro_fia} fueron guardados correctamente!"
            st.html("<script>window.parent.document.querySelector('section.main').scrollTo(0, 0);</script>")
            st.rerun()

# --- TAB 4: CRONOGRAMA ---
with tabs[3]:
    st.markdown("## 📅 CRONOGRAMA OFICIAL Y MARCADORES EN VIVO")
    lista_cronograma = []
    for part in FIXTURE_DINAMICO:
        pid = str(part["id"])
        real = datos["resultados_reales"].get(pid)
        if real: estado, ml, mv = "🔒 FINALIZADO", str(real["l"]), str(real["v"])
        elif verificar_partido_empezado(part.get("fecha_ref", "")): estado, ml, mv = "⏱️ EN CURSO", "-", "-"
        else: estado, ml, mv = "🟢 ABIERTO", "-", "-"
        
        # ¡SOLUCIÓN 1!: Reincorporación de la columna Fecha/Hora legible y ordenada por tiempo real
        lista_cronograma.append({
            "fecha_orden": part["fecha_ref"],
            "N°": pid,
            "Fase": part["grupo"],
            "Fecha/Hora ⏱️": f"{part['fecha']} ({part['hora']} hrs)",
            "Local": f"{part['flag_l']} {part['local']}",
            "L": ml,
            "V": mv,
            "Visita": f"{part['flag_v']} {part['visita']}",
            "Estadio": part["estadio"],
            "Estado": estado
        })
        
    df_crono = pd.DataFrame(lista_cronograma)
    df_crono["fecha_orden"] = pd.to_datetime(df_crono["fecha_orden"])
    df_crono = df_crono.sort_values(by="fecha_orden", ascending=True).reset_index(drop=True)
    df_crono = df_crono.drop(columns=["fecha_orden"])
    
    st.dataframe(df_crono.style.apply(lambda r: ['background:rgba(71,85,105,0.3);color:#cbd5e1;font-style:italic;']*len(r) if r["Estado"]=="🔒 FINALIZADO" else ['background:rgba(186,18,60,0.2);color:#fda4af;font-weight:bold;']*len(r) if r["Estado"]=="⏱️ EN CURSO" else ['']*len(r), axis=1), use_container_width=True, hide_index=True)

# --- TAB 5: PANEL CONTROL ---
with tabs[4]:
    st.markdown("## ⚙️ PANEL DE CONTROL DE ADMINISTRADOR")
    if st.text_input("Token de Seguridad Mandamás:", type="password") == PASSWORD_ADMIN:
        st.success("🔓 Acceso Concedido")
        accion_admin = st.radio("Acción:", ["Marcadores Oficiales", "Forzar Apuestas"], horizontal=True)
        fase_admin = st.selectbox("Fase:", ["Fecha 1", "Fecha 2", "Fecha 3", "Fases Finales"])
        partidos_admin = [m for m in FIXTURE_DINAMICO if m["fase_bloque"] == fase_admin]
        st.write("---")
        
        if accion_admin == "Marcadores Oficiales":
            nuevos_cierres = dict(datos["resultados_reales"])
            for part in partidos_admin:
                pid = str(part["id"])
                real_actual = datos["resultados_reales"].get(pid, {"l": 0, "v": 0})
                
                st.markdown(f"**Partido #{pid} ({part['grupo']}): {part['local']} vs {part['visita']}**")
                c_l, c_v, c_check = st.columns([2, 2, 3])
                with c_l: g_r_l = st.number_input(f"Goles L", 0, 15, int(real_actual.get("l", 0)), key=f"ar_{pid}l", label_visibility="collapsed")
                with c_v: g_r_v = st.number_input(f"Goles V", 0, 15, int(real_actual.get("v", 0)), key=f"ar_{pid}v", label_visibility="collapsed")
                with c_check: fin = st.checkbox("Cerrar Oficial", value=(pid in datos["resultados_reales"]), key=f"chk_{pid}")
                
                if fin: 
                    nuevos_cierres[pid] = {"l": g_r_l, "v": g_r_v}
                    if "Fases Finales" in part["fase_bloque"]:
                        if g_r_l == g_r_v:
                            nuevos_cierres[pid]["avanza"] = st.selectbox("🏆 Clasifica:", [part['local'], part['visita']], key=f"avanza_{pid}")
                        else:
                            nuevos_cierres[pid]["avanza"] = part['local'] if g_r_l > g_r_v else part['visita']
                else: nuevos_cierres.pop(pid, None)
            
            if st.button("🔄 ACTUALIZAR MARCADORES MUNDIALES", use_container_width=True):
                datos["resultados_reales"] = nuevos_cierres
                guardar_datos(datos)
                st.session_state["mensaje_exito"] = "¡Los marcadores oficiales se actualizaron con éxito!"
                st.html("<script>window.parent.document.querySelector('section.main').scrollTo(0, 0);</script>")
                st.rerun()

        elif accion_admin == "Forzar Apuestas":
            jugador = st.selectbox("Selecciona al jugador:", PARTICIPANTES)
            resp_admin = {}
            for part in partidos_admin:
                pid = str(part["id"])
                pred = datos["pronosticos"].get(jugador, {}).get(pid, {})
                
                st.markdown(f"**Partido #{pid}: {part['local']} vs {part['visita']}**")
                c_l, c_v = st.columns(2)
                # ¡SOLUCIÓN 2 (Admin)!: Claves únicas por jugador también en el panel del administrador
                with c_l: gl = st.number_input(f"L", 0, 15, pred.get("l"), placeholder="-", key=f"fa_{jugador}_{pid}l")
                with c_v: gv = st.number_input(f"V", 0, 15, pred.get("v"), placeholder="-", key=f"fa_{jugador}_{pid}v")
                resp_admin[pid] = {"l": gl, "v": gv}
                
            if st.button(f"💾 SALVAR CARTILLA DE {jugador.upper()}", use_container_width=True):
                if jugador not in datos["pronosticos"]: datos["pronosticos"][jugador] = {}
                for pid, sc in resp_admin.items():
                    if sc["l"] is not None and sc["v"] is not None: datos["pronosticos"][jugador][pid] = {"l": int(sc["l"]), "v": int(sc["v"])}
                    else: datos["pronosticos"][jugador].pop(pid, None)
                guardar_datos(datos)
                st.session_state["mensaje_exito"] = f"¡Cartilla forzada de {jugador} guardada con éxito!"
                st.html("<script>window.parent.document.querySelector('section.main').scrollTo(0, 0);</script>")
                st.rerun()
