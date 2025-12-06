#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analizador de uso y costos del bot
Muestra qué modelos se usaron y cuánto gastaste
"""

import re
from datetime import datetime, timedelta
from collections import Counter

# Costos por modelo (por cada request)
COSTS = {
    'gpt-4o-mini': 0.0003,
    'gpt-4o': 0.003,
    'gpt-4-turbo': 0.01
}

def analyze_bot_usage(log_file='telegram_bot.log', days=7):
    """Analiza uso del bot en los últimos N días"""
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            logs = f.readlines()
    except FileNotFoundError:
        print("❌ No se encontró telegram_bot.log")
        return
    
    # Buscar líneas con "🤖 Modelo:"
    pattern = r'🤖 Modelo: ([\w-]+) \| (.+?) \| Costo: \(\$([0-9.]+)\)'
    
    model_usage = Counter()
    total_cost = 0.0
    dates = []
    
    for line in logs:
        match = re.search(pattern, line)
        if match:
            model = match.group(1)
            cost = float(match.group(3))
            
            model_usage[model] += 1
            total_cost += cost
            
            # Extraer fecha si está en el log
            # Formato: 2025-12-06 19:40:22
            date_match = re.search(r'(\d{4}-\d{2}-\d{2})', line)
            if date_match:
                dates.append(date_match.group(1))
    
    # Resultados
    print("\n" + "="*60)
    print("📊 ESTADÍSTICAS DE USO DEL BOT")
    print("="*60)
    
    if not model_usage:
        print("\n❌ No se encontraron registros de uso de modelos")
        print("   El bot aún no ha procesado mensajes con el nuevo sistema")
        return
    
    total_requests = sum(model_usage.values())
    
    print(f"\n📈 Total de requests: {total_requests}")
    print(f"💰 Costo total: ${total_cost:.4f} USD")
    print(f"📅 Periodo: últimos {days} días")
    
    print("\n" + "-"*60)
    print("🔍 DESGLOSE POR MODELO:")
    print("-"*60)
    
    for model, count in model_usage.most_common():
        percentage = (count / total_requests) * 100
        model_cost = COSTS.get(model, 0) * count
        
        # Etiquetas visuales
        if model == 'gpt-4o-mini':
            label = "⚡ BÁSICO"
        elif model == 'gpt-4o':
            label = "✨ PRO"
        elif model == 'gpt-4-turbo':
            label = "🔥 ULTRA"
        else:
            label = model
        
        bar_length = int(percentage / 2)  # Barra visual
        bar = "█" * bar_length
        
        print(f"\n{label} ({model})")
        print(f"  Uso: {count} requests ({percentage:.1f}%)")
        print(f"  Costo: ${model_cost:.4f} USD")
        print(f"  {bar}")
    
    print("\n" + "="*60)
    print("💡 ANÁLISIS DE AHORRO:")
    print("="*60)
    
    # Calcular ahorro vs usar solo gpt-4o
    cost_if_all_premium = total_requests * COSTS['gpt-4o']
    savings = cost_if_all_premium - total_cost
    savings_percentage = (savings / cost_if_all_premium) * 100 if cost_if_all_premium > 0 else 0
    
    print(f"\n✅ Si hubieras usado solo gpt-4o: ${cost_if_all_premium:.4f} USD")
    print(f"✅ Usando sistema híbrido: ${total_cost:.4f} USD")
    print(f"💰 AHORRO: ${savings:.4f} USD ({savings_percentage:.1f}%)")
    
    # Proyección anual
    if total_requests > 0:
        avg_cost_per_request = total_cost / total_requests
        
        print("\n" + "-"*60)
        print("📊 PROYECCIONES:")
        print("-"*60)
        
        scenarios = [
            ("10 posts/día", 10 * 365),
            ("30 posts/día", 30 * 365),
            ("50 posts/día", 50 * 365),
            ("100 posts/día", 100 * 365),
        ]
        
        for scenario_name, yearly_requests in scenarios:
            yearly_cost = yearly_requests * avg_cost_per_request
            print(f"\n{scenario_name}:")
            print(f"  • Costo anual: ${yearly_cost:.2f} USD")
            print(f"  • Costo mensual: ${yearly_cost/12:.2f} USD")
    
    print("\n" + "="*60)
    print("✅ Sistema híbrido trabajando para AHORRAR costos!")
    print("="*60 + "\n")


if __name__ == "__main__":
    analyze_bot_usage()
