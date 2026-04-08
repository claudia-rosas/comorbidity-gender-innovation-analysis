#!/usr/bin/env python3
"""
Inspecciona, extrae y transforma JSON comprimido (.gz)
Maneja múltiples encodings y formatos
"""

import json
import gzip
import bz2
from pathlib import Path
from collections import Counter
from typing import Any, List, Dict

def load_json_smart(file_path: str) -> tuple[Any, str]:
    """
    Intenta cargar JSON de múltiples formatos comprimidos
    Retorna (data, formato_detectado)
    """
    path = Path(file_path)
    
    # Intenta gzip
    try:
        print(f" Intentando gzip (.gz)...")
        with gzip.open(path, 'rt', encoding='utf-8') as f:
            data = json.load(f)
        print("✓ Detectado: gzip")
        return data, "gzip"
    except Exception as e:
        print(f"  ✗ gzip falló: {type(e).__name__}")
    
    # Intenta bz2
    try:
        print(f" Intentando bz2 (.bz2)...")
        with bz2.open(path, 'rt', encoding='utf-8') as f:
            data = json.load(f)
        print("✓ Detectado: bz2")
        return data, "bz2"
    except Exception as e:
        print(f"  ✗ bz2 falló: {type(e).__name__}")
    
    # Intenta JSON plano con diferentes encodings
    for encoding in ['utf-8', 'utf-16', 'latin-1', 'cp1252']:
        try:
            print(f" Intentando JSON plano ({encoding})...")
            with open(path, 'r', encoding=encoding) as f:
                data = json.load(f)
            print(f"✓ Detectado: JSON plano ({encoding})")
            return data, f"json-{encoding}"
        except Exception as e:
            print(f"  ✗ {encoding} falló: {type(e).__name__}")
    
    raise ValueError(f"No se pudo cargar el archivo: {file_path}")


def analyze_data(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analiza la estructura y contenido del dataset
    """
    stats = {}
    
    # Tamaño
    stats['total_articles'] = len(data)
    
    if not data:
        return stats
    
    first_article = data[0]
    stats['fields'] = list(first_article.keys())
    
    # Años
    years = [art.get('year') for art in data if art.get('year')]
    if years:
        stats['year_range'] = f"{min(years)}-{max(years)}"
        stats['articles_with_year'] = len(years)
    
    # Journals
    journals = Counter(art.get('journal') for art in data if art.get('journal'))
    stats['unique_journals'] = len(journals)
    stats['top_5_journals'] = journals.most_common(5)
    
    # Keywords MeSH
    all_mesh = []
    for art in data:
        mesh = art.get('mesh_terms', art.get('keywords_mesh', []))
        if isinstance(mesh, list):
            all_mesh.extend(mesh)
        elif isinstance(mesh, str):
            all_mesh.append(mesh)
    stats['unique_mesh_keywords'] = len(set(all_mesh))
    stats['top_10_mesh'] = Counter(all_mesh).most_common(10)
    
    # Autores
    all_authors = []
    for art in data:
        authors = art.get('authors', []) or art.get('authors_full', [])
        if isinstance(authors, list):
            all_authors.extend(authors)
        elif isinstance(authors, str):
            all_authors.append(authors)
    stats['unique_authors'] = len(set(all_authors))
    
    # Abstracts
    abstracts = [art for art in data if art.get('abstract')]
    stats['articles_with_abstract'] = len(abstracts)
    
    return stats


def print_analysis(stats: Dict[str, Any], first_article: Dict[str, Any] = None):
    """
    Imprime análisis de forma legible
    """
    print("\n" + "="*70)
    print(" ANÁLISIS DEL DATASET COMORBIDITY")
    print("="*70)
    
    print(f"\n TAMAÑO:")
    print(f"  Total de artículos: {stats.get('total_articles', 0)}")
    
    print(f"\n CAMPOS DISPONIBLES:")
    for field in stats.get('fields', []):
        print(f"  - {field}")
    
    year_range = stats.get('year_range')
    if year_range:
        print(f"\n AÑOS:")
        print(f"  Rango: {year_range}")
        print(f"  Artículos con año: {stats.get('articles_with_year', 0)}")
    
    print(f"\n JOURNALS:")
    print(f"  Únicos: {stats.get('unique_journals', 0)}")
    print(f"  Top 5:")
    for journal, count in stats.get('top_5_journals', []):
        print(f"    - {journal}: {count}")
    
    print(f"\n KEYWORDS MeSH:")
    print(f"  Únicos: {stats.get('unique_mesh_keywords', 0)}")
    print(f"  Top 10:")
    for keyword, count in stats.get('top_10_mesh', [])[:10]:
        print(f"    - {keyword}: {count}")
    
    print(f"\n AUTORES:")
    print(f"  Únicos: {stats.get('unique_authors', 0)}")
    
    print(f"\n ABSTRACTS:")
    print(f"  Artículos con abstract: {stats.get('articles_with_abstract', 0)}")
    
    if first_article:
        print(f"\n PRIMER ARTÍCULO (estructura):")
        print(json.dumps(first_article, indent=2, ensure_ascii=False)[:1000])
        if len(json.dumps(first_article, indent=2, ensure_ascii=False)) > 1000:
            print("  ... [truncado]")
    
    print("\n" + "="*70)


def main():
    # CONFIGURACIÓN
    json_path = r"C:\Users\crosas\Documents\LifeSciencesGroup\B4W Research\ComorbidityAnalysis\data\comorbidity_all.json.gz"
    
    print(f"\n Inspeccionando: {json_path}\n")
    
    # Cargar
    try:
        data, format_type = load_json_smart(json_path)
        print(f"\n✓ Cargado exitosamente ({format_type})")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return
    
    # Validar estructura
    if not isinstance(data, list):
        print(f"\n Estructura inesperada: esperaba lista, obtuve {type(data).__name__}")
        print(f"Contenido: {str(data)[:200]}")
        return
    
    # Analizar
    stats = analyze_data(data)
    first_article = data[0] if data else None
    
    # Imprimir
    print_analysis(stats, first_article)
    
    # Guardar versión descomprimida
    print(f"\n Guardando versión descomprimida...")
    output_path = Path(json_path).parent / "comorbidity_all_extracted.json"
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✓ Guardado en: {output_path}")
        print(f"  Tamaño: {Path(output_path).stat().st_size / 1024 / 1024:.2f} MB")
    except Exception as e:
        print(f"✗ Error al guardar: {e}")
    
    # Resumen para análisis
    print(f"\n PRÓXIMOS PASOS:")
    print(f"  1. Dataset listo para análisis de sesgo de género")
    print(f"  2. Keywords MeSH disponibles para filtrado")
    print(f"  3. {stats.get('total_articles', 0)} artículos disponibles")
    print(f"  4. Puedes ahora hacer análisis de: composición de equipo, innovación, comorbilidades")


if __name__ == '__main__':
    main()