#!/usr/bin/env python3
"""
Modo Chat Interactivo - Sacred Rebirth AI Agent
Conversa naturalmente con el agente y él ejecutará todo por ti

Uso: python chat.py
"""

import sys
from src.crew import MarketingCrew
from crewai import Agent, Task, Crew, Process
from config.settings import OPENAI_MODEL
import re


class ChatAgent:
    """Agente de chat que interpreta comandos naturales"""
    
    def __init__(self):
        print("🤖 Inicializando agente de chat...")
        self.crew = MarketingCrew()
        
        # Crear agente conversacional
        self.chat_agent = Agent(
            role='Asistente Personal de Marketing IA',
            goal='Entender las necesidades del usuario y ejecutar las acciones apropiadas',
            backstory="""Eres un asistente inteligente que ayuda a gestionar el marketing 
            de Sacred Rebirth. Puedes generar contenido, publicar en redes, enviar emails, 
            gestionar leads y más. Entiendes lenguaje natural en español e inglés y ejecutas 
            las acciones que el usuario necesita.""",
            verbose=False,
            allow_delegation=True,
            llm=OPENAI_MODEL
        )
        
        print("✅ Agente de chat listo!\n")
    
    def interpret_command(self, user_input: str) -> dict:
        """Interpreta el comando del usuario usando IA"""
        
        interpretation_task = Task(
            description=f"""Analiza esta solicitud del usuario: "{user_input}"
            
            Determina QUÉ quiere hacer el usuario. Opciones:
            
            1. GENERAR_CONTENIDO_IG - Si quiere crear/generar post de Instagram
            2. GENERAR_CONTENIDO_FB - Si quiere crear post de Facebook  
            3. PUBLICAR_IG - Si quiere publicar en Instagram
            4. PUBLICAR_FB - Si quiere publicar en Facebook
            5. EMAIL - Si quiere enviar email o campaña
            6. ESTRATEGIA - Si quiere planificar o crear estrategia
            7. LEADS - Si quiere gestionar/ver leads
            8. ANALYTICS - Si quiere ver métricas o análisis
            9. CAMPANA_COMPLETA - Si quiere campaña completa multicanal
            10. AYUDA - Si pide ayuda o no está claro
            
            Extrae también:
            - TEMA: El tema del contenido si lo menciona
            - PLATAFORMA: instagram, facebook, o ambas
            - TIPO: tipo de email (promotional, educational, etc)
            
            Responde en formato:
            ACCION: [nombre de la acción]
            TEMA: [tema o "ninguno"]
            PLATAFORMA: [plataforma o "ninguna"]
            TIPO: [tipo o "ninguno"]
            RAZON: [breve explicación de por qué elegiste esta acción]
            """,
            expected_output="Interpretación de la solicitud del usuario",
            agent=self.chat_agent
        )
        
        crew = Crew(
            agents=[self.chat_agent],
            tasks=[interpretation_task],
            process=Process.sequential,
            verbose=False
        )
        
        result = crew.kickoff()
        
        # Parsear resultado
        action = "AYUDA"
        tema = None
        platform = None
        tipo = None
        
        result_str = str(result)
        
        if "ACCION:" in result_str:
            action_match = re.search(r'ACCION:\s*(\w+)', result_str)
            if action_match:
                action = action_match.group(1)
        
        if "TEMA:" in result_str:
            tema_match = re.search(r'TEMA:\s*(.+?)(?:\n|$)', result_str)
            if tema_match and tema_match.group(1).lower() != 'ninguno':
                tema = tema_match.group(1).strip()
        
        if "PLATAFORMA:" in result_str:
            platform_match = re.search(r'PLATAFORMA:\s*(\w+)', result_str)
            if platform_match and platform_match.group(1).lower() != 'ninguna':
                platform = platform_match.group(1)
        
        if "TIPO:" in result_str:
            tipo_match = re.search(r'TIPO:\s*(\w+)', result_str)
            if tipo_match and tipo_match.group(1).lower() != 'ninguno':
                tipo = tipo_match.group(1)
        
        return {
            'action': action,
            'tema': tema,
            'platform': platform,
            'tipo': tipo,
            'raw_result': result_str
        }
    
    def execute_action(self, interpretation: dict):
        """Ejecuta la acción interpretada"""
        action = interpretation['action']
        tema = interpretation['tema']
        platform = interpretation['platform']
        tipo = interpretation['tipo']
        
        print(f"\n🎯 Acción detectada: {action}")
        if tema:
            print(f"📝 Tema: {tema}")
        if platform:
            print(f"📱 Plataforma: {platform}")
        
        print("\n⚙️ Ejecutando...\n")
        
        try:
            if action == 'GENERAR_CONTENIDO_IG':
                tema = tema or "Transformación con Ayahuasca"
                from src.crew import quick_instagram_post
                result = quick_instagram_post(tema)
                print(f"\n✅ CONTENIDO GENERADO:\n{result}")
            
            elif action == 'GENERAR_CONTENIDO_FB':
                tema = tema or "Retiros espirituales en Valle de Bravo"
                from src.crew import quick_facebook_post
                result = quick_facebook_post(tema)
                print(f"\n✅ CONTENIDO GENERADO:\n{result}")
            
            elif action == 'PUBLICAR_IG':
                print("📸 Generando y publicando en Instagram...")
                tema = tema or "Sacred Rebirth"
                result = self.crew.run_social_media_campaign({'instagram': tema})
                print(f"\n✅ PUBLICADO:\n{result}")
            
            elif action == 'PUBLICAR_FB':
                print("📘 Generando y publicando en Facebook...")
                tema = tema or "Sacred Rebirth"
                result = self.crew.run_social_media_campaign({'facebook': tema})
                print(f"\n✅ PUBLICADO:\n{result}")
            
            elif action == 'EMAIL':
                tipo = tipo or 'promotional'
                print(f"📧 Creando campaña de email {tipo}...")
                result = self.crew.run_email_campaign(tipo)
                print(f"\n✅ EMAIL CREADO:\n{result}")
            
            elif action == 'ESTRATEGIA':
                print("🎯 Creando estrategia de contenido...")
                result = self.crew.run_content_strategy()
                print(f"\n✅ ESTRATEGIA:\n{result}")
            
            elif action == 'LEADS':
                print("👥 Gestionando leads...")
                result = self.crew.run_leads_management('nurture', 'interested')
                print(f"\n✅ LEADS:\n{result}")
            
            elif action == 'ANALYTICS':
                print("📊 Analizando métricas...")
                result = self.crew.run_analytics('all')
                print(f"\n✅ ANÁLISIS:\n{result}")
            
            elif action == 'CAMPANA_COMPLETA':
                tema = tema or "próximo retiro"
                print(f"🚀 Ejecutando campaña completa: {tema}...")
                result = self.crew.run_full_campaign(tema)
                print(f"\n✅ CAMPAÑA COMPLETA:\n{result}")
            
            else:
                print("\n❓ No estoy seguro de qué quieres hacer.")
                self.show_help()
        
        except Exception as e:
            print(f"\n❌ Error ejecutando acción: {e}")
            import traceback
            traceback.print_exc()
    
    def show_help(self):
        """Muestra ayuda"""
        print("""
╔═══════════════════════════════════════════════════════════╗
║                  💬 AYUDA - MODO CHAT                     ║
╚═══════════════════════════════════════════════════════════╝

Puedes hablar naturalmente. Ejemplos:

📝 GENERAR CONTENIDO:
   - "crea un post de instagram sobre ayahuasca"
   - "genera contenido para facebook sobre kambo"
   - "hazme un post sobre el retiro de enero"

📱 PUBLICAR:
   - "publica en instagram sobre transformación"
   - "sube a facebook información del retiro"

📧 EMAILS:
   - "envía un email promocional"
   - "crea un email educativo sobre preparación"

🎯 ESTRATEGIA:
   - "crea una estrategia de contenido"
   - "planifica la semana"

👥 LEADS:
   - "gestiona los leads"
   - "nutre a los interesados"

📊 ANÁLISIS:
   - "muéstrame las métricas"
   - "analiza el engagement"

🚀 CAMPAÑA:
   - "ejecuta una campaña completa"
   - "haz campaña para el retiro de enero"

Comandos especiales:
   - 'ayuda' - muestra esto
   - 'salir' / 'exit' - termina el chat
        """)
    
    def start_chat(self):
        """Inicia el modo chat"""
        print("""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║         💬 MODO CHAT - Sacred Rebirth AI Agent           ║
║                                                           ║
║         Háblame naturalmente, yo entenderé y haré        ║
║         todo lo que necesites para tu marketing          ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝

Escribe 'ayuda' para ver ejemplos o 'salir' para terminar.
        """)
        
        while True:
            try:
                user_input = input("\n💬 Tú: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['salir', 'exit', 'quit', 'adiós', 'adios']:
                    print("\n👋 ¡Hasta luego! Que tengas un excelente día.")
                    break
                
                if user_input.lower() in ['ayuda', 'help', '?']:
                    self.show_help()
                    continue
                
                # Interpretar y ejecutar
                print("\n🤔 Analizando tu solicitud...")
                interpretation = self.interpret_command(user_input)
                self.execute_action(interpretation)
                
            except KeyboardInterrupt:
                print("\n\n👋 ¡Hasta luego!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                import traceback
                traceback.print_exc()


def main():
    """Función principal"""
    try:
        chat = ChatAgent()
        chat.start_chat()
    except KeyboardInterrupt:
        print("\n\n👋 ¡Hasta luego!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
