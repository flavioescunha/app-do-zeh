import flet as ft
import requests
import time

# --- CONFIGURAÇÃO ---
# Cole aqui a URL "Raw" do seu Gist (aquela que mostra só o texto puro na tela)
GIST_ID = 'b71b224dc943d4ca35a342d58cbf6ae8'      # Cole o ID do Gist que você criou

def main(page: ft.Page):
    # Configurações da página
    page.title = "Zeh - Inteligência Artificial"
    page.theme_mode = ft.ThemeMode.DARK 
    
    # Elementos visuais
    chat_list = ft.ListView(expand=True, spacing=10, auto_scroll=True)
    page.add(chat_list)
    
    user_input = ft.TextField(hint_text="Pergunte algo ao Zeh...", expand=True)
    
    def enviar_mensagem(e):
        if not user_input.value:
            return
        
        mensagem = user_input.value
        
        # 1. Adiciona a mensagem do usuário na tela (Padrão novo do Flet: ft.Colors)
        chat_list.controls.append(ft.Text(f"👤 Você: {mensagem}", color=ft.Colors.BLUE_200, size=16))
        user_input.value = ""
       
        page.update() 
        
        try:
            # 1. Pega a URL fresca da API do GitHub
            url_api = f"https://api.github.com/gists/{GIST_ID}"
            resposta_gist = requests.get(url_api)
            resposta_gist.raise_for_status()
            dados_github = resposta_gist.json()
            url_ngrok = dados_github["files"]["ollama_url.txt"]["content"].strip()
            
            print(f"URL capturada da API: {url_ngrok}")
            
            # 2. Manda a mensagem pro Servidor Python (Zeh.py)
            url_backend = f"{url_ngrok}/chat"
            resposta_servidor = requests.post(url_backend, json={"mensagem": mensagem})
            resposta_servidor.raise_for_status() 
            
            # 3. SE DEU TUDO CERTO, o texto_zeh recebe a resposta da IA!
            texto_zeh = resposta_servidor.json().get("resposta", "Opa, não recebi o texto.")
            
        except Exception as erro:
            # 4. SE DER QUALQUER ERRO, o texto_zeh vira a mensagem de erro!
            # Assim a variável SEMPRE existe.
            texto_zeh = f"⚠️ Ops, erro de conexão: {erro}"

        # 5. ADICIONA NA TELA (Isso fica FORA e DEPOIS do try/except)
        chat_list.controls.append(ft.Text(f"🤖 Zeh: {texto_zeh}", color=ft.Colors.GREEN_200, size=16))
        
        # Atualiza a tela e limpa a caixa de texto (se você já tiver isso, mantenha)
        # input_mensagem.value = ""
        page.update()

    # Botão enviar (Padrão novo do Flet: ft.Icons)
    botao_enviar = ft.FloatingActionButton(icon=ft.Icons.SEND, on_click=enviar_mensagem)
    user_input.on_submit = enviar_mensagem

    # Monta a barra inferior
    page.add(
        ft.Row([user_input, botao_enviar])
    )

# Inicia o aplicativo
ft.run(main)