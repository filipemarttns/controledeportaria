from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.graphics import Color, Rectangle, RoundedRectangle, Line
from kivy.core.window import Window
from kivy.uix.checkbox import CheckBox
from datetime import datetime
import csv
import os
import firebase_admin
from firebase_admin import credentials, firestore
from kivy.clock import Clock
from kivy.lang import Builder
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import sheetshttps, googleapis, idsheet, keyid
from dotenv import load_dotenv

print(os.getcwd())  # Verifique o diretório atual

scope = [sheetshttps, googleapis]
creds = ServiceAccountCredentials.from_json_keyfile_name("google_sheets_cred.json", scope)
client = gspread.authorize(creds)

# Usando o ID da planilha para abrir a planilha
sheet_id = idsheet
worksheet = client.open_by_key(sheet_id).worksheet("GERAL")

# Inicializando o Firebase
cred = credentials.Certificate('banco.json')
firebase_admin.initialize_app(cred)

# Conectando ao Firestore
db = firestore.client()

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        layout = FloatLayout()

        with layout.canvas.before:
            Color(1, 1, 1, 1) 
            self.rect = Rectangle(size=self.size, pos=self.pos)
        layout.bind(size=self._update_rect, pos=self._update_rect)

        self.logo = Image(source="rouxinol.png", size_hint=(None, None), size=(200, 100), pos_hint={"center_x": 0.5, "center_y": 0.85})
        layout.add_widget(self.logo)

        self.username_label = Label(text="Usuário", size_hint=(None, None), size=(200, 50), pos_hint={"center_x": 0.5, "center_y": 0.7})
        layout.add_widget(self.username_label)

        self.username_input = TextInput(
            hint_text="Digite seu nome de usuário", 
            hint_text_color=(1, 1, 1, 1), 
            multiline=False, 
            size_hint=(None, None), 
            size=(250, 35), 
            pos_hint={"center_x": 0.5, "center_y": 0.65}, 
            background_color=(0, 0, 0, 0), 
            foreground_color=(1, 0, 0, 1), 
            font_size=16
        )
        with self.username_input.canvas.before:
            Color(1, 0, 0, 1) 
            self.line_username = Line(points=[self.username_input.x, self.username_input.y, self.username_input.x + self.username_input.width, self.username_input.y], width=1)  # Linha mais fina
        self.username_input.bind(size=self.update_line, pos=self.update_line)
        layout.add_widget(self.username_input)

        self.password_label = Label(text="Senha", size_hint=(None, None), size=(200, 50), pos_hint={"center_x": 0.5, "center_y": 0.55})
        layout.add_widget(self.password_label)

        self.password_input = TextInput(
            hint_text="Digite sua senha", 
            hint_text_color=(1, 1, 1, 1), 
            password=True, 
            multiline=False, 
            size_hint=(None, None), 
            size=(250, 35), 
            pos_hint={"center_x": 0.5, "center_y": 0.5}, 
            background_color=(0, 0, 0, 0), 
            foreground_color=(1, 0, 0, 1), 
            font_size=16
        )
        with self.password_input.canvas.before:
            Color(1, 0, 0, 1) 
            self.line_password = Line(points=[self.password_input.x, self.password_input.y, self.password_input.x + self.password_input.width, self.password_input.y], width=1)  # Linha mais fina
        self.password_input.bind(size=self.update_line, pos=self.update_line)
        layout.add_widget(self.password_input)

        self.login_button = Button(
            text="Entrar",
            size_hint=(None, None),
            size=(230, 45),
            background_normal='',
            background_color=(1, 0, 0, 1), 
            color=(1, 1, 1, 1), 
            pos_hint={"center_x": 0.5, "center_y": 0.35},
            on_press=self.on_login
        )

        with self.login_button.canvas.before:
            Color(1, 0, 0, 1) 
            self.round_rect = RoundedRectangle(
                pos=self.login_button.pos,
                size=self.login_button.size,
                radius=[20] 
            )
        self.login_button.bind(size=self.update_round_rect, pos=self.update_round_rect)
        
        layout.add_widget(self.login_button)
        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def update_line(self, instance, value):
        if instance == self.username_input:
            self.line_username.points = [instance.x, instance.y, instance.x + instance.width, instance.y]
        elif instance == self.password_input:
            self.line_password.points = [instance.x, instance.y, instance.x + instance.width, instance.y]

    def update_round_rect(self, instance, value):
        self.round_rect.pos = instance.pos
        self.round_rect.size = instance.size

    def on_login(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        
        users = {
            "Trafego - Rouxinol": "trafego2025",
            "CCO - Rouxinol": "controlerotas2025",
            "Mecanica - Rouxinol": "mecanicarouxinol2025",
            "Analista - Rouxinol": "analistarouxinol2026",
            "Limpeza - Rouxinol": "limopezarouxinol",
            "Manutenção - Rouxinol": "manutençãorouxinol2025",
            "Supervisor - Rouxinol": "supervisor@2025",
            "Clever - Rouxinol": "clevercastro@2026",
            "Analista - Maxsim": "analistadados2",
            "":"",
        }
        
        if username in users and users[username] == password:
            App.get_running_app().usuario_atual = username
            self.manager.current = 'inicio'
        else:
            self.show_popup("Erro", "Usuário ou senha incorretos.")
    
    def show_popup(self, title, message): 
        content = BoxLayout(orientation='vertical', padding=[20, 30, 20, 10], spacing=15)  

        message_label = Label(
            text=message,
            color=(0, 0, 0, 1),
            font_size=16,
            bold=False,
            halign="center",
            valign="middle",
            size_hint_y=None,
            height=50, 
        )
        message_label.bind(size=lambda instance, value: setattr(instance, 'text_size', value))
        content.add_widget(message_label)

        ok_button = Button(
            text="OK",
            size_hint=(None, None),
            size=(120, 50),
            background_normal='', 
            background_color=(1, 0, 0, 1), 
            color=(1, 1, 1, 1), 
            pos_hint={"center_x": 0.5} 
        )

        popup = Popup(
            title=title,
            content=content,
            size_hint=(None, None),
            size=(300, 180),
            separator_height=0,
            background='',
            auto_dismiss=False
        )

        ok_button.bind(on_press=popup.dismiss)
        content.add_widget(ok_button)
        popup.open()


class TelaInicialScreen(Screen):
    def __init__(self, **kwargs):
        super(TelaInicialScreen, self).__init__(**kwargs)

        with self.canvas.before:
            Color(1, 1, 1, 1) 
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

        layout = FloatLayout()

        self.logo = Image(source="rouxinol.png", size_hint=(None, None), size=(150, 50), pos_hint={"center_x": 0.25, "center_y": 0.95})
        layout.add_widget(self.logo)

        self.logo = Image(source="portaria.png", size_hint=(None, None), size=(350, 250), pos_hint={"center_x": 0.5, "center_y": 0.55})
        layout.add_widget(self.logo)

        self.cadastrar_button = Button(
            text="Cadastrar Veículo",
            size_hint=(None, None),
            size=(250, 50),
            background_normal='',
            background_color=(1, 0, 0, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.40}, 
            on_press=self.on_cadastrar
        )
        layout.add_widget(self.cadastrar_button)

        self.veiculos_button = Button(
            text="Veículos Cadastrados",
            size_hint=(None, None),
            size=(250, 50),
            background_normal='',
            background_color=(1, 0, 0, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.30},
            on_press=self.on_veiculos
        )
        layout.add_widget(self.veiculos_button)

        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def on_cadastrar(self, instance):
        self.manager.current = 'cadastro'

    def on_veiculos(self, instance):
        self.manager.current = 'veiculos'

class CheckBoxLabel(BoxLayout):
    def __init__(self, label_text, checkbox_value, checkbox_style=None, **kwargs):
        super().__init__(orientation='horizontal', spacing=5, size_hint_y=None, height=30, **kwargs) 

        self.checkbox = CheckBox(size_hint_x=None, width=30)
        self.add_widget(self.checkbox)
        
        self.label = Label(
            text=label_text,
            size_hint_x=1, 
            halign='left',
            valign='middle',
            color=(0, 0, 0, 1)
        )
        self.add_widget(self.label)

        if checkbox_style:
            self.checkbox.color = checkbox_style.get("color", (0, 0, 0, 1)) 
            self.checkbox.active_color = checkbox_style.get("active", (1, 0, 0, 1)) 
        
        self.value = checkbox_value
        self.status = checkbox_value 
    
    def get_status(self):
        """Retorna o status do checkbox (marcado/desmarcado)."""
        return self.checkbox.active

from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from datetime import datetime
from kivy.clock import Clock

class CadastroVeiculoScreen(Screen):
    def __init__(self, **kwargs):
        super(CadastroVeiculoScreen, self).__init__(**kwargs)

        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

        scroll_view = ScrollView(size_hint=(1, 1))

        layout = GridLayout(cols=1, spacing=15, padding=20, size_hint_y=None, width=400)
        layout.bind(minimum_height=layout.setter('height'))

        def criar_box(texto, input_widget):
            box = BoxLayout(orientation='vertical', size_hint_y=None, height=100)
            label = Label(text=texto, size_hint_y=None, height=30, color=(0, 0, 0, 1))
            input_widget.size_hint_y = None
            input_widget.height = 40
            input_widget.foreground_color = (0, 0, 0, 1)
            box.add_widget(label)
            box.add_widget(input_widget)
            return box

        vermelho_vibrante = (1, 0, 0, 1)

        # Campos de entrada (caixas de texto)
        self.nome_usuario_spinner = Spinner(text="Selecione", values=("2590", "2569", "2482", "2130"))
        self.nome_usuario_spinner.color = (1, 1, 1, 1)
        self.nome_usuario_spinner.background_normal = ''
        self.nome_usuario_spinner.background_color = vermelho_vibrante
        layout.add_widget(criar_box("Nome do Usuário", self.nome_usuario_spinner))

        self.placa_input = TextInput(hint_text="Número do veículo")
        self.placa_input.foreground_color = (0, 0, 0, 1)
        layout.add_widget(criar_box("Número de Frota", self.placa_input))

        self.hodometro_input = TextInput(hint_text="Digite a quilometragem")
        self.hodometro_input.foreground_color = (0, 0, 0, 1)
        layout.add_widget(criar_box("Hodômetro", self.hodometro_input))

        self.movimentacao_spinner = Spinner(text="Selecione", values=("Entrada", "Saída"))
        self.movimentacao_spinner.color = (1, 1, 1, 1)
        self.movimentacao_spinner.background_normal = ''
        self.movimentacao_spinner.background_color = vermelho_vibrante
        layout.add_widget(criar_box("Tipo de Movimentação", self.movimentacao_spinner))

        self.motorista_input = TextInput(hint_text="Nome do motorista")
        self.motorista_input.foreground_color = (0, 0, 0, 1)
        layout.add_widget(criar_box("Motorista", self.motorista_input))

        self.status_checkboxes = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=200,
            spacing=5,
            padding=[0, 0, 0, 0]
        )

        checkbox_style = {
            "color": (0, 0, 0, 1),
            "active": vermelho_vibrante,
            "background_normal": '',
            "background_active": '',
        }

        self.status_checkboxes.add_widget(CheckBoxLabel("Está OK", "Está OK", checkbox_style))
        self.status_checkboxes.add_widget(CheckBoxLabel("Abastecer", "Abastecer", checkbox_style))
        self.status_checkboxes.add_widget(CheckBoxLabel("Limpar", "Limpar", checkbox_style))
        self.status_checkboxes.add_widget(CheckBoxLabel("Manutenção preventiva", "Manutenção preventiva", checkbox_style))
        self.status_checkboxes.add_widget(CheckBoxLabel("Manutenção corretiva", "Manutenção corretiva", checkbox_style))

        layout.add_widget(self.status_checkboxes)

        self.observacoes_input = TextInput(hint_text="Digite observações sobre o veículo", multiline=True, height=80)
        self.observacoes_input.foreground_color = (0, 0, 0, 1)
        layout.add_widget(criar_box("Observações", self.observacoes_input))

        self.urgencia_spinner = Spinner(text="Selecione a urgência", values=("Baixa", "Média", "Alta", "OK"))
        self.urgencia_spinner.color = (1, 1, 1, 1)
        self.urgencia_spinner.background_normal = ''
        self.urgencia_spinner.background_color = vermelho_vibrante
        layout.add_widget(criar_box("Urgência", self.urgencia_spinner))

        botoes_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=120, spacing=10)

        self.cadastrar_button = Button(text="Cadastrar", size_hint=(None, None), size=(320, 50), background_color=vermelho_vibrante, color=(1, 1, 1, 1))
        self.cadastrar_button.bind(on_press=self.on_cadastrar)
        botoes_layout.add_widget(self.cadastrar_button)

        self.voltar_button = Button(text="Voltar", size_hint=(None, None), size=(320, 50), background_color=vermelho_vibrante, color=(1, 1, 1, 1))
        self.voltar_button.bind(on_press=self.on_voltar)
        botoes_layout.add_widget(self.voltar_button)

        layout.add_widget(botoes_layout)

        scroll_view.add_widget(layout)
        self.add_widget(scroll_view)

    def _update_rect(self, instance, value):
        """Atualiza a posição e o tamanho do retângulo quando a tela mudar."""
        self.rect.pos = self.pos
        self.rect.size = self.size

    def on_cadastrar(self, instance):
        placa = self.placa_input.text
        observacoes = self.observacoes_input.text
        urgencia = self.urgencia_spinner.text
        nome_usuario = self.nome_usuario_spinner.text
        hodometro = self.hodometro_input.text
        movimentacao = self.movimentacao_spinner.text
        motorista = self.motorista_input.text
        data_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if nome_usuario == "Selecione" or movimentacao == "Selecione":
            self.show_popup("Erro no cadastro", "Selecione o nome de usuário e o tipo de movimentação.")
            return

        status_selecionados = [checkbox.status for checkbox in self.status_checkboxes.children if checkbox.checkbox.active]

        if all([placa, status_selecionados, observacoes, urgencia, nome_usuario, hodometro, movimentacao, motorista]):
            # Para cada status selecionado, criar uma entrada separada
            for status in status_selecionados:
                veiculo = {
                    "placa": placa,
                    "hodometro": hodometro,
                    "movimentacao": movimentacao,
                    "motorista": motorista,
                    "status": status,  # Aqui é um único status por vez
                    "observacoes": observacoes,
                    "urgencia": urgencia,
                    "data_hora": data_hora,
                    "resolvido_por": None,
                    "usuario_cadastro": nome_usuario
                }

                if movimentacao == "Saída":
                    # Deletar o veículo do banco quando sair
                    veiculos_ref = db.collection("veiculos").where("placa", "==", placa).get()
                    for doc in veiculos_ref:
                        doc.reference.delete()

                if movimentacao == "Entrada":
                    db.collection("veiculos").add(veiculo)

                dados_planilha = [
                    data_hora,  # DATA/HORA
                    nome_usuario,  # CADASTRADO POR
                    placa,  # VEÍCULO
                    hodometro,  # HODÔMETRO
                    movimentacao,  # SENTIDO
                    motorista,  # MOTORISTA
                    status,  # STATUS (um status por vez)
                    observacoes,  # OBSERVAÇÃO
                    urgencia,  # URGÊNCIA
                    ""  # TEMPO DE CONCLUSÃO DA PENDÊNCIA
                ]
                worksheet.append_row(dados_planilha)

            # Agora, vamos procurar pela combinação de VEÍCULO (placa) e STATUS
            if "concluir" in status_selecionados:  # Verifica se o status é de conclusão
                time_to_finish = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                # Percorrendo as linhas da planilha para encontrar a linha correta
                rows = worksheet.get_all_records()  # Pega todas as linhas da planilha
                for i, row in enumerate(rows, start=2):  # Começa de 2 para pular o cabeçalho
                    # Filtro combinado: VEÍCULO + STATUS + TEMPO DE CONCLUSÃO vazio
                    if row["VEÍCULO"] == placa and row["STATUS"] == status and row["TEMPO DE CONCLUSÃO DA PENDÊNCIA"] == "":
                        # Atualiza a célula correta de TEMPO DE CONCLUSÃO DA PENDÊNCIA
                        worksheet.update_cell(i, 10, time_to_finish)  # Coluna 10 (TEMPO DE CONCLUSÃO DA PENDÊNCIA)
                        break  # Encontrou a linha correta, não precisa continuar a busca

            Clock.schedule_once(lambda dt: Clock.schedule_interval(lambda dt: self.atualizar_lista_veiculos(), 1))  # Atualiza a lista a cada 1 segundo

            self.show_popup("Cadastro bem-sucedido", f"Veículo {placa} cadastrado com sucesso!")
            self.manager.current = 'veiculos'
            self.limpar_campos()

        else:
            self.show_popup("Erro no cadastro", "Preencha todos os campos!")



    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

    def show_confirmation_popup(self, placa, veiculo_data):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=f"O veículo {placa} está pendente em: {veiculo_data['status']}"))
        content.add_widget(Label(text="Tem certeza que deseja registrar a saída?"))

        button_layout = BoxLayout(size_hint_y=None, height=50)
        yes_button = Button(text="Sim", on_press=lambda x: self.registrar_saida(placa))
        no_button = Button(text="Não", on_press=lambda x: self.close_popup())
        button_layout.add_widget(yes_button)
        button_layout.add_widget(no_button)
        content.add_widget(button_layout)

        self.popup = Popup(title="Confirmação", content=content, size_hint=(None, None), size=(400, 200))
        self.popup.open()

    def close_popup(self):
        self.popup.dismiss()

    def registrar_saida(self, placa):
        # Registrar a saída
        self.popup.dismiss()
        self.show_popup("Saída registrada", f"A saída do veículo {placa} foi registrada com sucesso.")

    def limpar_campos(self):
        """Reseta os campos do formulário."""
        self.nome_usuario_spinner.text = "Selecione"
        self.placa_input.text = ""
        self.hodometro_input.text = ""
        self.movimentacao_spinner.text = "Selecione"
        self.motorista_input.text = ""
        self.observacoes_input.text = ""
        self.urgencia_spinner.text = "Selecione a urgência"

        for checkbox in self.status_checkboxes.children:
            checkbox.checkbox.active = False

    def on_voltar(self, instance):
        self.manager.current = 'inicio'

    def atualizar_lista_veiculos(self):
        print("Atualizando lista de veículos...")
        self.manager.get_screen('veiculos').atualizar_lista_veiculos()


class VeiculosCadastradosScreen(Screen):
    def __init__(self, **kwargs):
        super(VeiculosCadastradosScreen, self).__init__(**kwargs)

        layout = FloatLayout()
        self.layout = layout
        self.veiculo_buttons = []

        self.imagem_veiculos = Image(
            source='VEICULOS.png',
            size_hint=(None, None),
            size=(400, 200), 
            pos_hint={"center_x": 0.5, "top": 1} 
        )
        self.layout.add_widget(self.imagem_veiculos)

        self.scroll_view = ScrollView(size_hint=(1, None), size=(600, 400), pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.scroll_content = BoxLayout(orientation='vertical', size_hint_y=None)
        self.scroll_content.bind(minimum_height=self.scroll_content.setter('height'))
        self.scroll_view.add_widget(self.scroll_content)
        self.layout.add_widget(self.scroll_view)

        self.voltar_button = Button(
            text="Voltar",
            size_hint=(None, None),
            size=(250, 50),
            background_color=(1, 0, 0, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.05},
            on_press=self.on_voltar
        )
        self.voltar_button.color = (1, 1, 1, 1)
        self.layout.add_widget(self.voltar_button)

        self.add_widget(layout)

        # Listener do Firestore para atualizar a lista automaticamente
        self.listener = None

    def on_enter(self, *args):
        with self.canvas.before:
            Color(1, 1, 1, 1) 
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        
        # Chama a atualização inicial da lista de veículos
        Clock.schedule_once(lambda dt: self.atualizar_lista_veiculos())

        # Configura o listener para atualizações em tempo real no Firestore
        self.listener = db.collection("veiculos").on_snapshot(self.atualizar_lista_veiculos_em_tempo_real)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def atualizar_lista_veiculos(self):
        self.scroll_content.clear_widgets()

        veiculos_ref = db.collection("veiculos").get()

        for doc in veiculos_ref:
            veiculo = doc.to_dict()
            veiculo['id'] = doc.id  # Adiciona o ID do documento no dicionário 'veiculo'

            cor_fundo = (1, 0, 0, 1)
            if veiculo['status'] == "Está OK":
                cor_fundo = (0, 1, 0, 1)
            elif veiculo['urgencia'] == "Alta":
                cor_fundo = (1, 0, 0, 1)
            elif veiculo['urgencia'] == "Média":
                cor_fundo = (1, 0.647, 0, 1)
            elif veiculo['urgencia'] == "Baixa":
                cor_fundo = (1, 1, 0, 1)

            if veiculo.get('resolvido_por'):
                cor_fundo = (0, 1, 0, 1)

            veiculo_button = Button(
                text=f"{veiculo['placa']} - {veiculo['status']}",
                size_hint=(None, None),
                size=(300, 35),
                pos_hint={"center_x": 0.5}
            )
            veiculo_button.background_normal = ''
            veiculo_button.background_color = cor_fundo
            veiculo_button.color = (0, 0, 0, 1)
            veiculo_button.bind(
                on_press=lambda instance, veiculo=veiculo, veiculo_button=veiculo_button: self.exibir_informacoes(veiculo, veiculo_button)
            )
            self.scroll_content.add_widget(veiculo_button)

    def atualizar_lista_veiculos_em_tempo_real(self, snapshot, changes, read_time):
        # Atualiza a lista de veículos sempre que houver uma mudança no Firestore
        Clock.schedule_once(lambda dt: self.atualizar_lista_veiculos())

    def exibir_informacoes(self, veiculo, veiculo_button):
        info_text = f"Veículo: {veiculo['placa']}\nStatus: {veiculo['status']}\nObservações: {veiculo['observacoes']}\nUrgência: {veiculo['urgencia']}\nData e Hora do Cadastro: {veiculo['data_hora']}\n"
        
        if 'usuario_cadastro' in veiculo:
            info_text += f"Cadastro feito por: {veiculo['usuario_cadastro']}\n"
        
        if 'tempo_execucao' in veiculo:
            info_text += f"Tempo de Execução: {veiculo['tempo_execucao']}"

        popup_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        popup_layout.add_widget(Label(text=info_text, color=(1, 1, 1, 1))) 

        if veiculo.get('resolvido_por'):
            comecar_button_disabled = True
            resolver_button_disabled = True
        else:
            comecar_button_disabled = False
            resolver_button_disabled = False

        comecar_button = Button(
            text="COMEÇAR TAREFA",
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={"center_x": 0.5},
            disabled=comecar_button_disabled,
            background_color=(1, 0, 0, 1), 
            color=(1, 1, 1, 1) 
        )
        comecar_button.bind(on_press=lambda instance: self.iniciar_tarefa(veiculo))
        popup_layout.add_widget(comecar_button)

        resolver_button = Button(
            text="RESOLVIDO",
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={"center_x": 0.5},
            disabled=resolver_button_disabled,
            background_color=(1, 0, 0, 1), 
            color=(1, 1, 1, 1) 
        )
        resolver_button.bind(on_press=lambda instance: self.marcar_resolvido(veiculo, veiculo_button, popup))
        popup_layout.add_widget(resolver_button)

        popup = Popup(
            title="Informações do Veículo",
            content=popup_layout,
            size_hint=(None, None),
            size=(350, 350),
            background_color=(1, 1, 1, 1),
            title_color=(0, 0, 0, 1),  
            auto_dismiss=True 
        )
        popup.open()

    def iniciar_tarefa(self, veiculo):
        veiculo['inicio_tarefa'] = datetime.now()
        self.show_popup("Tarefa Iniciada", f"Tarefa do veículo {veiculo['placa']} iniciada.")

    def marcar_resolvido(self, veiculo, veiculo_button, popup):
        if 'inicio_tarefa' in veiculo:
            tempo_decorrido = datetime.now() - veiculo['inicio_tarefa']
            tempo_execucao = str(tempo_decorrido).split('.')[0] 
            veiculo['tempo_execucao'] = tempo_execucao

        veiculo['resolvido_por'] = "Funcionário"
        veiculo_button.background_color = (0, 1, 0, 1)

        # Atualiza o documento no Firebase usando o ID que foi adicionado ao dicionário
        veiculo_ref = db.collection('veiculos').document(veiculo['id'])
        veiculo_ref.update({
            'resolvido_por': veiculo['resolvido_por'],
            'tempo_execucao': veiculo['tempo_execucao']
        })

        # Atualiza o Google Sheets
        self.atualizar_planilha(veiculo)

        popup.dismiss()
        self.show_popup("Sucesso", f"Veículo {veiculo['placa']} foi marcado como resolvido.")

    def atualizar_planilha(self, veiculo):
        # Acesse a planilha
        sheet = client.open_by_key(keyid).sheet1

        # Encontre a linha onde o veículo está (por exemplo, pela placa)
        cell = sheet.find(veiculo['placa'])

        # Atualize a coluna "TEMPO DE CONCLUSÃO DA PENDÊNCIA" na coluna J (coluna 10)
        column_index = 10  # A coluna J é a décima coluna (índice 10)
        sheet.update_cell(cell.row, column_index, veiculo['tempo_execucao'])

    def show_popup(self, title, message):
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(None, None),
            size=(300, 200),
            auto_dismiss=True
        )
        popup.open()

    def on_voltar(self, instance):
        self.manager.current = "inicio"

    def on_leave(self, *args):
        # Remove o listener quando a tela for deixada
        if self.listener:
            # Correção: use o método de cancelamento adequado, que no caso do Firestore é 'unsubscribe'
            if hasattr(self.listener, 'remove'):
                self.listener.remove()  # Cancela o listener

        
class VeiculoApp(App):
    veiculos = [] 

    def build(self):

        Window.size = (360, 640)
        
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(TelaInicialScreen(name='inicio')) 
        sm.add_widget(CadastroVeiculoScreen(name='cadastro'))
        sm.add_widget(VeiculosCadastradosScreen(name='veiculos'))

        Clock.schedule_once(self.carregar_veiculos, 0)

        return sm

    def on_voltar(self):
        if 'inicio' in self.root.screen_names:
            self.manager.current = "inicio"
        else:
            print("Tela 'inicio' não encontrada!")

            self.manager.current = "login"

    def carregar_veiculos(self, dt):
        db = firestore.client()
        veiculos_ref = db.collection('veiculos') 
        veiculos = veiculos_ref.stream() 

        self.veiculos.clear()

        for veiculo in veiculos:
            veiculo_data = veiculo.to_dict()
            self.veiculos.append(veiculo_data) 

        Clock.schedule_once(self.exibir_veiculos, 0)

    def exibir_veiculos(self, dt):
        veiculos_screen = self.root.get_screen('veiculos')
        
        Clock.schedule_once(lambda dt: self._exibir_veiculos(veiculos_screen), 0)

    def _exibir_veiculos(self, veiculos_screen):
        try:
            layout_veiculos = veiculos_screen.ids.layout_veiculos 
            layout_veiculos.clear_widgets()

            for veiculo in self.veiculos:
                label = Label(text=f"Placa: {veiculo['placa']}, "
                                  f"Motorista: {veiculo['motorista']}, "
                                  f"Status: {veiculo['status']}")
                layout_veiculos.add_widget(label)
        except Exception as e:
            print(f"Erro ao acessar layout_veiculos: {e}")

if __name__ == "__main__":
    VeiculoApp().run()