#!/usr/bin/env python3
"""
Script de Prueba - Sacred Rebirth Marketing System
Prueba todas las funcionalidades sin necesidad de Telegram
"""
import os
import sys
sys.path.append('/workspaces/sacred-rebirth-ai-agent')

def test_appointment_setter():
    """Prueba el appointment setter"""
    print("\n🤖 PROBANDO APPOINTMENT SETTER (Maya)...")
    
    try:
        from src.appointment_setter import AppointmentSetterAgent
        agent = AppointmentSetterAgent()
        
        test_questions = [
            "¿Dónde está ubicado el retiro?",
            "¿En qué consiste Sacred Rebirth?", 
            "¿Qué medicinas usan?",
            "¿Cuánto cuesta el retiro?",
            "¿Es seguro la ayahuasca?"
        ]
        
        for question in test_questions:
            question_type = agent.analyze_message(question)
            print(f"\n❓ Pregunta: {question}")
            print(f"🎯 Tipo detectado: {question_type}")
            
            if not os.getenv('OPENAI_API_KEY'):
                print("⚠️ OpenAI API key no configurado - saltando respuesta")
            else:
                response = agent.generate_response(question, question_type)
                print(f"💬 Respuesta: {response[:100]}...")
        
        print("\n✅ Appointment setter configurado correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error en appointment setter: {str(e)}")
        return False

def test_image_generator():
    """Prueba el generador de imágenes"""
    print("\n🎨 PROBANDO GENERADOR DE IMÁGENES...")
    
    try:
        from src.image_generator import SacredRebirthImageGenerator
        generator = SacredRebirthImageGenerator()
        
        print("✅ Generador de imágenes configurado")
        print("🎨 Temas disponibles: retreat_announcement, medicine, transformation, location")
        print("💡 Ejemplo: generator.generate_retreat_image('retreat_announcement')")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en generador de imágenes: {str(e)}")
        return False

def test_campaign_manager():
    """Prueba el campaign manager"""
    print("\n📊 PROBANDO CAMPAIGN MANAGER...")
    
    try:
        from src.campaign_manager import MarketingCampaignManager
        manager = MarketingCampaignManager()
        
        print("✅ Campaign manager configurado")
        print("🎯 Audiencias disponibles:")
        for audience, info in manager.target_audiences.items():
            print(f"   • {audience}: {info['description']}")
        
        print(f"\n📅 Retiro objetivo: {manager.retreat_info['date']}")
        print(f"🎨 Tema: {manager.retreat_info['theme']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en campaign manager: {str(e)}")
        return False

def test_daily_content():
    """Prueba el contenido diario"""
    print("\n📅 PROBANDO CONTENIDO DIARIO...")
    
    try:
        from src.daily_content import DailyContentAutomation
        daily = DailyContentAutomation()
        
        print("✅ Daily content configurado")
        print("📅 Temas semanales:")
        for day, theme in daily.weekly_themes.items():
            time = daily.posting_times.get(day, "12:00")
            print(f"   • {day} ({time}): {theme['theme']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en daily content: {str(e)}")
        return False

def test_facebook_integration():
    """Verifica configuración de Facebook"""
    print("\n📱 VERIFICANDO CONFIGURACIÓN FACEBOOK...")
    
    facebook_token = os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')
    if facebook_token:
        print("✅ Facebook Page Access Token configurado")
        print(f"🔑 Token: {facebook_token[:20]}...{facebook_token[-10:]}")
    else:
        print("❌ Facebook Page Access Token NO configurado")
        print("💡 Agregar a Railway: FACEBOOK_PAGE_ACCESS_TOKEN")
    
    return bool(facebook_token)

def show_usage_examples():
    """Muestra ejemplos de uso"""
    print("\n📱 EJEMPLOS DE USO EN TELEGRAM:")
    print("""
🎯 APPOINTMENT SETTER (automático):
   • "¿Dónde está el retiro?" → Respuesta de Maya + discovery call
   • "¿Cuánto cuesta?" → NO menciona precio + discovery call
   
🎨 GENERAR CONTENIDO + IMAGEN:
   • "Crea un foto y promueva el retiro de enero 11"
   • "/daily Monday" → Contenido lunes + imagen
   • "/image retiro" → Solo imagen
   
📊 MARKETING COMPLETO:
   • "/campaign" → Estudio mercado + calendario + estrategia
   • "/audience" → Estrategias captación audiencia
   • "/content 30" → 30 días contenido
   • "/video" → Guión video profesional
   
📅 CONTENIDO AUTOMÁTICO:
   • "/weekly" → Calendario semana completa
   • "/daily Tuesday" → Contenido específico día
   
📱 PUBLICAR FACEBOOK:
   • "/facebook [contenido]" → Publicar directo
   • "Sube contenido a Facebook sobre ayahuasca"
""")

def main():
    """Ejecuta todas las pruebas"""
    print("🚀 SACRED REBIRTH MARKETING SYSTEM - PRUEBAS")
    print("=" * 50)
    
    results = {
        "appointment_setter": test_appointment_setter(),
        "image_generator": test_image_generator(), 
        "campaign_manager": test_campaign_manager(),
        "daily_content": test_daily_content(),
        "facebook_config": test_facebook_integration()
    }
    
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE PRUEBAS:")
    
    for component, status in results.items():
        status_emoji = "✅" if status else "❌"
        print(f"{status_emoji} {component.replace('_', ' ').title()}")
    
    total_working = sum(results.values())
    print(f"\n🎯 {total_working}/5 componentes funcionando")
    
    if total_working >= 4:
        print("🎉 Sistema prácticamente listo!")
        if not results["facebook_config"]:
            print("💡 Solo falta agregar FACEBOOK_PAGE_ACCESS_TOKEN a Railway")
    else:
        print("⚠️ Revisar componentes con errores")
    
    show_usage_examples()

if __name__ == "__main__":
    main()