import sys
import subprocess
import platform
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QTextEdit, QGroupBox, QRadioButton, QFrame)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QPalette, QLinearGradient, QBrush, QGradient


class PingThread(QThread):
    """Clase para ejecutar el ping en un hilo separado y no bloquear la interfaz"""
    ping_result = pyqtSignal(bool, str)  # Señal para enviar el resultado (éxito/fallo, mensaje)
    
    def __init__(self, host):
        super().__init__()
        self.host = host
        
    def run(self):
        resultado, mensaje = self.hacer_ping(self.host)
        self.ping_result.emit(resultado, mensaje)
    
    def hacer_ping(self, host_destino):
        """Envía un solo paquete ICMP Echo Request (ping) al host_destino
        y devuelve True si hay respuesta, False en caso contrario, junto con un mensaje."""
        mensaje = f"--- Haciendo ping a {host_destino} ---\n"
        
        # Parámetro para el número de pings a enviar.
        # En Windows es '-n', en Linux/macOS es '-c'.
        parametro_count = '-n' if platform.system().lower() == 'windows' else '-c'
        
        # Comando para ejecutar ping. Enviamos solo 1 paquete.
        comando = ['ping', parametro_count, '1', '-w', '1000', host_destino]  # -w 1000 (1 segundo de timeout en ms para Windows)
        if platform.system().lower() != 'windows':
            comando = ['ping', parametro_count, '1', '-W', '1', host_destino]  # -W 1 (1 segundo de timeout para Linux/macOS)
        
        try:
            # Ejecutamos el comando
            proceso = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=5)
            
            # Verificamos el código de retorno. 0 usualmente significa éxito.
            if proceso.returncode == 0:
                mensaje += f"Respuesta recibida de {host_destino}\n"
                mensaje += proceso.stdout
                return True, mensaje
            else:
                mensaje += f"No se recibió respuesta de {host_destino} o hubo un error.\n"
                if proceso.stderr:
                    mensaje += f"Error: {proceso.stderr}\n"
                return False, mensaje
                
        except subprocess.TimeoutExpired:
            mensaje += f"El comando ping a {host_destino} excedió el tiempo de espera.\n"
            return False, mensaje
        except FileNotFoundError:
            mensaje += "Error: El comando 'ping' no se encontró. Asegúrate de que esté instalado y en el PATH.\n"
            return False, mensaje
        except Exception as e:
            mensaje += f"Ocurrió un error inesperado: {e}\n"
            return False, mensaje


class ICMPPingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ICMP Ping Tool")
        self.setMinimumSize(700, 600)  # Ventana más grande
        
        # Configurar el estilo de la aplicación
        self.setup_styles()
        
        # Widget central y layout principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)  # Más espacio entre widgets
        main_layout.setContentsMargins(20, 20, 20, 20)  # Márgenes más amplios
        
        # Título de la aplicación
        title_label = QLabel("ICMP Ping Tool")
        title_font = QFont("Arial", 24, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #ffffff; margin-bottom: 15px;")
        main_layout.addWidget(title_label)
        
        # Sección de entrada de host
        input_group = QGroupBox("Host de destino")
        input_group.setStyleSheet(
            "QGroupBox {font-size: 16px; font-weight: bold; color: #ffffff; border: 2px solid #3498db; border-radius: 8px; margin-top: 15px; padding-top: 10px;}"
            "QGroupBox::title {subcontrol-origin: margin; subcontrol-position: top center; padding: 0 10px;}"
        )
        input_layout = QVBoxLayout()
        input_layout.setSpacing(15)
        
        # Hosts predefinidos
        predefined_layout = QHBoxLayout()
        radio_font = QFont("Arial", 12)
        
        self.radio_custom = QRadioButton("Personalizado:")
        self.radio_custom.setFont(radio_font)
        self.radio_custom.setChecked(True)
        
        self.radio_google_dns = QRadioButton("Google DNS (8.8.8.8)")
        self.radio_google_dns.setFont(radio_font)
        
        self.radio_local = QRadioButton("Red local (192.168.10.250)")
        self.radio_local.setFont(radio_font)
        
        self.radio_google = QRadioButton("www.google.com")
        self.radio_google.setFont(radio_font)
        
        predefined_layout.addWidget(self.radio_custom)
        predefined_layout.addWidget(self.radio_google_dns)
        predefined_layout.addWidget(self.radio_local)
        predefined_layout.addWidget(self.radio_google)
        
        # Conectar señales de los radio buttons
        self.radio_custom.toggled.connect(self.update_host_input)
        self.radio_google_dns.toggled.connect(self.update_host_input)
        self.radio_local.toggled.connect(self.update_host_input)
        self.radio_google.toggled.connect(self.update_host_input)
        
        # Campo de entrada para el host
        host_layout = QHBoxLayout()
        host_label = QLabel("Host:")
        host_label.setFont(QFont("Arial", 14))
        host_label.setStyleSheet("color: #ffffff;")
        
        self.host_input = QLineEdit()
        self.host_input.setFont(QFont("Arial", 14))
        self.host_input.setPlaceholderText("Ingrese dirección IP o nombre de dominio")
        self.host_input.setStyleSheet(
            "QLineEdit {padding: 8px; border: 2px solid #3498db; border-radius: 6px; background-color: #f8f9fa;}"
            "QLineEdit:focus {border-color: #2980b9; background-color: white;}"
        )
        
        host_layout.addWidget(host_label)
        host_layout.addWidget(self.host_input)
        
        # Botón de ping
        self.ping_button = QPushButton("Hacer Ping")
        self.ping_button.setFont(QFont("Arial", 14, QFont.Bold))
        self.ping_button.setMinimumHeight(50)
        self.ping_button.setCursor(Qt.PointingHandCursor)  # Cambiar cursor al pasar por encima
        self.ping_button.setStyleSheet(
            "QPushButton {background-color: #3498db; color: white; border-radius: 8px; padding: 10px;}"
            "QPushButton:hover {background-color: #2980b9;}"
            "QPushButton:pressed {background-color: #1c6ea4;}"
            "QPushButton:disabled {background-color: #95a5a6; color: #ecf0f1;}"
        )
        self.ping_button.clicked.connect(self.start_ping)
        
        # Agregar widgets al layout de entrada
        input_layout.addLayout(predefined_layout)
        input_layout.addLayout(host_layout)
        input_layout.addWidget(self.ping_button)
        input_group.setLayout(input_layout)
        
        # Área de resultados
        result_group = QGroupBox("Resultados")
        result_group.setStyleSheet(
            "QGroupBox {font-size: 16px; font-weight: bold; color: #ffffff; border: 2px solid #2ecc71; border-radius: 8px; margin-top: 15px; padding-top: 10px;}"
            "QGroupBox::title {subcontrol-origin: margin; subcontrol-position: top center; padding: 0 10px;}"
        )
        result_layout = QVBoxLayout()
        
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setFont(QFont("Consolas", 12))  # Fuente monoespaciada más grande
        self.result_text.setStyleSheet(
            "QTextEdit {background-color: #1e2a38; color: #ffffff; border: 2px solid #2ecc71; border-radius: 6px; padding: 10px;}"
        )
        self.result_text.setMinimumHeight(250)  # Altura mínima para ver más resultados
        
        result_layout.addWidget(self.result_text)
        result_group.setLayout(result_layout)
        
        # Agregar grupos al layout principal
        main_layout.addWidget(input_group)
        main_layout.addWidget(result_group)
        
        # Inicializar la interfaz
        self.show()
    
    def setup_styles(self):
        """Configura los estilos globales de la aplicación"""
        # Crear un degradado para el fondo con azul oscuro
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor(25, 42, 86))  # Azul oscuro arriba
        gradient.setColorAt(1.0, QColor(13, 27, 62))  # Azul muy oscuro abajo
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)
        
        # Estilo global para la aplicación
        self.setStyleSheet("""
            QMainWindow {background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                                                        stop:0 #192a56, stop:1 #0d1b3e);}
            QLabel {color: #ffffff;}
            QRadioButton {color: #ffffff; spacing: 8px;}
            QRadioButton::indicator {width: 18px; height: 18px;}
        """)
    
    def update_host_input(self):
        """Actualiza el campo de entrada según el radio button seleccionado"""
        if self.radio_custom.isChecked():
            self.host_input.setEnabled(True)
            self.host_input.clear()
            self.host_input.setStyleSheet(
                "QLineEdit {padding: 8px; border: 2px solid #3498db; border-radius: 6px; background-color: #f8f9fa;}"
                "QLineEdit:focus {border-color: #2980b9; background-color: white;}"
            )
        else:
            self.host_input.setEnabled(False)
            self.host_input.setStyleSheet(
                "QLineEdit {padding: 8px; border: 2px solid #bdc3c7; border-radius: 6px; background-color: #ecf0f1;}"
            )
            if self.radio_google_dns.isChecked():
                self.host_input.setText("8.8.8.8")
            elif self.radio_local.isChecked():
                self.host_input.setText("192.168.10.250")
            elif self.radio_google.isChecked():
                self.host_input.setText("www.google.com")
    
    def start_ping(self):
        """Inicia el proceso de ping en un hilo separado"""
        host = self.host_input.text().strip()
        if not host:
            self.result_text.setTextColor(QColor(255, 0, 0))  # Rojo para error
            self.result_text.append("Error: Por favor ingrese un host válido.")
            self.result_text.setTextColor(QColor(255, 255, 255))  # Volver a blanco
            return
        
        # Deshabilitar el botón mientras se ejecuta el ping
        self.ping_button.setEnabled(False)
        self.ping_button.setText("Ejecutando...")
        
        # Limpiar resultados anteriores
        self.result_text.clear()
        
        # Crear y ejecutar el hilo de ping
        self.ping_thread = PingThread(host)
        self.ping_thread.ping_result.connect(self.handle_ping_result)
        self.ping_thread.start()
    
    def handle_ping_result(self, success, message):
        """Maneja el resultado del ping"""
        # Configurar fuente para el resultado
        self.result_text.setCurrentFont(QFont("Consolas", 12))
        
        if success:
            self.result_text.setTextColor(QColor(46, 204, 113))  # Verde para éxito
        else:
            self.result_text.setTextColor(QColor(231, 76, 60))  # Rojo para error
        
        self.result_text.append(message)
        self.result_text.setTextColor(QColor(255, 255, 255))  # Color blanco para texto normal
        
        # Habilitar el botón nuevamente
        self.ping_button.setEnabled(True)
        self.ping_button.setText("Hacer Ping")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  
    window = ICMPPingApp()
    sys.exit(app.exec_())