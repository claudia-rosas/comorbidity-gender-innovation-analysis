#!/usr/bin/env python3
"""
Debuggea el contenido real del archivo JSON
"""

import json
import gzip
import bz2
from pathlib import Path

json_path = r"C:\Users\crosas\Documents\LifeSciencesGroup\B4W Research\ComorbidityAnalysis\comorbidity_all_converted.json.gz"

path = Path(json_path)
print(f"📁 Archivo: {json_path}")
print(f"📊 Tamaño: {path.stat().st_size / 1024 / 1024:.2f} MB")
print(f"✓ Existe: {path.exists()}\n")

# Lee los primeros bytes para ver qué es
with open(json_path, 'rb') as f:
    first_bytes = f.read(20)
    print(f"Primeros 20 bytes (hex): {first_bytes.hex()}")
    print(f"Primeros 20 bytes (repr): {first_bytes}\n")

# Intenta cargar
try:
    print("⏳ Intentando gzip...")
    with gzip.open(json_path, 'rt', encoding='utf-8') as f:
        content = f.read(500)  # Lee solo primeros 500 caracteres
    print(f"✓ Es gzip")
    print(f"Contenido (primeros 500 chars):\n{content}\n")
    
    # Intenta parsear como JSON
    with gzip.open(json_path, 'rt', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Tipo de datos: {type(data)}")
    print(f"Largo: {len(data) if hasattr(data, '__len__') else 'N/A'}")
    
    if isinstance(data, dict):
        print(f"Keys: {list(data.keys())}")
        for key, value in list(data.items())[:3]:
            print(f"  {key}: {type(value)} - {str(value)[:100]}")
    
    elif isinstance(data, list):
        print(f"Es lista con {len(data)} elementos")
        if data:
            print(f"Primer elemento: {data[0]}")
    
    else:
        print(f"Estructura: {str(data)[:500]}")

except Exception as e:
    print(f"✗ gzip falló: {e}\n")
    
    # Intenta JSON plano
    try:
        print("⏳ Intentando JSON plano...")
        with open(json_path, 'r', encoding='utf-8') as f:
            content = f.read(500)
        print(f"✓ Es JSON plano")
        print(f"Contenido (primeros 500 chars):\n{content}\n")
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"Tipo de datos: {type(data)}")
        print(f"Largo: {len(data) if hasattr(data, '__len__') else 'N/A'}")
        
        if isinstance(data, dict):
            print(f"Keys: {list(data.keys())}")
            for key, value in list(data.items())[:3]:
                print(f"  {key}: {type(value)} - {str(value)[:100]}")
        
        elif isinstance(data, list):
            print(f"Es lista con {len(data)} elementos")
            if data:
                print(f"Primer elemento: {data[0]}")
        
        else:
            print(f"Estructura: {str(data)[:500]}")
    
    except Exception as e2:
        print(f"✗ JSON plano falló: {e2}")
        print("\n💡 Intenta abrirlo manualmente o revisa su formato")