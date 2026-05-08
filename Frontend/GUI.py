from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QStackedWidget, QWidget, 
                            QLineEdit, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QFrame, QLabel, QSizePolicy, QGraphicsDropShadowEffect, QGraphicsOpacityEffect)
from PyQt5.QtGui import (QIcon, QPainter, QMovie, QColor, QTextCharFormat, QFont, QPixmap, 
                        QTextBlockFormat, QPen, QBrush, QLinearGradient, QRadialGradient, QPainterPath, QPolygonF)
from PyQt5.QtCore import Qt, QSize, QTimer, QPropertyAnimation, QEasingCurve, QRect, pyqtProperty, QParallelAnimationGroup, QPointF
from dotenv import dotenv_values
import sys
import os
import math
import random

# Load environment variables
env_vars = dotenv_values(".env")
Assistantname = env_vars.get("Assistantname", "JARVIS")
Username = env_vars.get("Username", "User")
old_chat_message = ""

# Directory paths
current_dir = os.getcwd()
TempDirPath = rf"{current_dir}\Frontend\Files"
GraphicsDirPath = rf"{current_dir}\Frontend\Graphics"

# Global microphone state to persist across screens - DEFAULT OFF
GLOBAL_MIC_STATE = {"is_active": False, "toggled": False}  # Changed toggled from True to False

def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line.strip() for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ['how','what','who','where','when','why','which','whom','can you',"what's", "where's","how's"]
    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] in ['.','?','!']:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"
    else:
        if query_words[-1][-1] in ['.','?','!']:
            new_query = new_query[:-1] + '.'
        else:
            new_query += '.'
    return new_query.capitalize()

def SetMicrophoneStatus(Command):
    with open(TempDirectoryPath('Mic.data'), 'w', encoding='utf-8') as file:
        file.write(Command)

def GetMicrophoneStatus():
    try:
        with open(TempDirectoryPath('Mic.data'), 'r', encoding='utf-8') as file:
            Status = file.read().strip()
        return Status
    except:
        return "False"

def SetAsssistantStatus(Status):
    with open(rf'{TempDirPath}\Status.data','w',encoding='utf-8') as file:
        file.write(Status)

def GetAssistantStatus():
    try:
        with open(rf'{TempDirPath}\Status.data', 'r', encoding='utf-8') as file:
            Status = file.read()
        return Status
    except:
        return "Available..."

def MicButtonInitiated():
    SetMicrophoneStatus("True")  # Changed from "False" to "True" 
    GLOBAL_MIC_STATE["is_active"] = True

def MicButtonClosed():
    SetMicrophoneStatus("False")  # Changed from "True" to "False"
    GLOBAL_MIC_STATE["is_active"] = False

def GraphicsDirectoryPath(Filename):
    path = rf'{GraphicsDirPath}\{Filename}'
    return path

def TempDirectoryPath(Filename):
    path = rf'{TempDirPath}\{Filename}'
    return path

def ShowTextToScreen(Text):
    with open(rf'{TempDirPath}\Responses.data','w', encoding='utf-8') as file:
        file.write(Text)

class ElegantJarvisCore(QWidget):
    def __init__(self, parent=None, size=400):
        super().__init__(parent)
        self.core_size = size
        self.setFixedSize(size, size)
        self.pulse_phase = 0
        self.rotation_phase = 0
        self.energy_level = 0.3
        self.breathing_phase = 0
        self.wave_phase = 0
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(30)
        
    def update_animation(self):
        self.pulse_phase += 0.08
        self.rotation_phase += 0.02
        self.breathing_phase += 0.05
        self.wave_phase += 0.12
        
        if self.pulse_phase >= 2 * math.pi:
            self.pulse_phase = 0
        if self.rotation_phase >= 2 * math.pi:
            self.rotation_phase = 0
        if self.breathing_phase >= 2 * math.pi:
            self.breathing_phase = 0
        if self.wave_phase >= 2 * math.pi:
            self.wave_phase = 0
            
        self.update()
        
    def set_energy_level(self, level):
        self.energy_level = max(0.1, min(1, level))
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        center = self.rect().center()
        scale_factor = self.core_size / 400.0  # Scale based on size
        
        # Calculate dynamic values
        pulse_scale = 1.0 + 0.15 * math.sin(self.pulse_phase) * self.energy_level
        breathing_scale = 1.0 + 0.08 * math.sin(self.breathing_phase)
        
        # Outer glow layers (scaled)
        for i in range(4):
            glow_radius = int((140 + i * 25) * pulse_scale * scale_factor)
            glow_alpha = int((60 - i * 10) * self.energy_level)
            
            glow_gradient = QRadialGradient(center, glow_radius)
            glow_gradient.setColorAt(0, QColor(0, 0, 0, 0))
            glow_gradient.setColorAt(0.6, QColor(0, 200, 255, glow_alpha))
            glow_gradient.setColorAt(0.8, QColor(0, 150, 255, glow_alpha // 2))
            glow_gradient.setColorAt(1, QColor(0, 0, 0, 0))
            
            painter.setBrush(QBrush(glow_gradient))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(center.x() - glow_radius, center.y() - glow_radius,
                              glow_radius * 2, glow_radius * 2)
        
        # Animated energy waves (scaled)
        if self.energy_level > 0.5:
            for i in range(3):
                wave_radius = int((100 + i * 35 + 40 * math.sin(self.wave_phase + i * 0.8)) * scale_factor)
                wave_alpha = int(100 * self.energy_level * (1 - i * 0.2))
                
                painter.setPen(QPen(QColor(0, 255, 255, wave_alpha), 2))
                painter.setBrush(Qt.NoBrush)
                painter.drawEllipse(center.x() - wave_radius, center.y() - wave_radius,
                                  wave_radius * 2, wave_radius * 2)
        
        # Main circle (scaled)
        main_radius = int(80 * breathing_scale * scale_factor)
        
        main_gradient = QRadialGradient(center, main_radius)
        main_gradient.setColorAt(0, QColor(0, 0, 0, 255))
        main_gradient.setColorAt(0.7, QColor(0, 100, 200, int(200 * self.energy_level)))
        main_gradient.setColorAt(0.85, QColor(0, 150, 255, int(255 * self.energy_level)))
        main_gradient.setColorAt(0.95, QColor(100, 200, 255, int(255 * self.energy_level)))
        main_gradient.setColorAt(1, QColor(150, 255, 255, int(200 * self.energy_level)))
        
        painter.setBrush(QBrush(main_gradient))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(center.x() - main_radius, center.y() - main_radius, 
                          main_radius * 2, main_radius * 2)
        
        # Bright outer ring (scaled)
        ring_radius = int(75 * breathing_scale * scale_factor)
        ring_width = max(1, int(3 * scale_factor))
        
        ring_gradient = QRadialGradient(center, ring_radius)
        ring_gradient.setColorAt(0, QColor(0, 0, 0, 0))
        ring_gradient.setColorAt(0.9, QColor(0, 255, 255, int(150 * self.energy_level)))
        ring_gradient.setColorAt(1, QColor(100, 255, 255, int(255 * self.energy_level)))
        
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(QBrush(ring_gradient), ring_width))
        painter.drawEllipse(center.x() - ring_radius, center.y() - ring_radius,
                          ring_radius * 2, ring_radius * 2)
        
        # Rotating particles (scaled)
        if self.energy_level > 0.3:
            painter.save()
            painter.translate(center)
            painter.rotate(self.rotation_phase * 57.3)
            
            for i in range(8):
                angle = i * 45
                distance = (90 + 10 * math.sin(self.pulse_phase + i * 0.5)) * scale_factor
                
                x = distance * math.cos(math.radians(angle))
                y = distance * math.sin(math.radians(angle))
                
                particle_alpha = int(150 * self.energy_level * (0.5 + 0.5 * math.sin(self.pulse_phase + i)))
                painter.setBrush(QBrush(QColor(0, 200, 255, particle_alpha)))
                painter.setPen(Qt.NoPen)
                particle_size = max(1, int(2 * scale_factor))
                painter.drawEllipse(int(x) - particle_size, int(y) - particle_size, 
                                  particle_size * 2, particle_size * 2)
                
            painter.restore()

class ResponsiveMicButton(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(60, 60)
        self.hover_scale = 1.0
        self.is_active = GLOBAL_MIC_STATE["is_active"]
        self.toggled = GLOBAL_MIC_STATE["toggled"]
        self.pulse_phase = 0
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(50)
        
    def update_animation(self):
        self.is_active = GLOBAL_MIC_STATE["is_active"]
        self.toggled = GLOBAL_MIC_STATE["toggled"]
        
        if self.is_active:
            self.pulse_phase += 0.2
            if self.pulse_phase >= 2 * math.pi:
                self.pulse_phase = 0
        
        self.update()
        
    def enterEvent(self, event):
        self.hover_scale = 1.15
        self.update()
        
    def leaveEvent(self, event):
        self.hover_scale = 1.0
        self.update()
        
    def mousePressEvent(self, event):
        if not self.toggled:  # Changed from if self.toggled to if not self.toggled
            MicButtonInitiated()
            GLOBAL_MIC_STATE["is_active"] = True
            GLOBAL_MIC_STATE["toggled"] = True  # Changed from False to True
        else:
            MicButtonClosed()
            GLOBAL_MIC_STATE["is_active"] = False
            GLOBAL_MIC_STATE["toggled"] = False  # Changed from True to False
        
        self.toggled = GLOBAL_MIC_STATE["toggled"]
        self.is_active = GLOBAL_MIC_STATE["is_active"]
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        center = self.rect().center()
        radius = int(25 * self.hover_scale)
        
        # Pulsing glow when active
        if self.is_active:
            glow_radius = int(radius + 15 * (1 + 0.3 * math.sin(self.pulse_phase)))
            glow_gradient = QRadialGradient(center, glow_radius)
            glow_gradient.setColorAt(0, QColor(255, 100, 100, 100))
            glow_gradient.setColorAt(1, QColor(255, 100, 100, 0))
            
            painter.setBrush(QBrush(glow_gradient))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(center.x() - glow_radius, center.y() - glow_radius,
                              glow_radius * 2, glow_radius * 2)
        
        # Button background
        if self.is_active:
            color = QColor(255, 100, 100, 200)
            border_color = QColor(255, 150, 150)
        else:
            color = QColor(0, 150, 255, 200)
            border_color = QColor(0, 200, 255)
            
        painter.setBrush(QBrush(color))
        painter.setPen(QPen(border_color, 2))
        painter.drawEllipse(center.x() - radius, center.y() - radius, radius * 2, radius * 2)
        
        # Microphone icon
        painter.setPen(QPen(QColor(255, 255, 255), 2))
        mic_rect = QRect(center.x() - 5, center.y() - 8, 10, 12)
        painter.drawRoundedRect(mic_rect, 5, 5)
        painter.drawLine(center.x(), center.y() + 6, center.x(), center.y() + 12)
        painter.drawLine(center.x() - 6, center.y() + 12, center.x() + 6, center.y() + 12)

class ResponsiveChatSection(QWidget):
    def __init__(self):
        super(ResponsiveChatSection, self).__init__()
        self.initUI()
        
    def initUI(self):
        # Main horizontal layout - chat left, controls right
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(15)
        
        # LEFT SIDE - Chat display (takes most space)
        chat_container = QWidget()
        chat_layout = QVBoxLayout(chat_container)
        chat_layout.setContentsMargins(10, 10, 10, 10)
        chat_layout.setSpacing(10)
        
        # Chat display
        self.chat_text_edit = QTextEdit()
        self.chat_text_edit.setReadOnly(True)
        self.chat_text_edit.setTextInteractionFlags(Qt.NoTextInteraction)
        self.chat_text_edit.setFrameStyle(QFrame.NoFrame)
        
        # Responsive chat styling
        self.chat_text_edit.setStyleSheet("""
            QTextEdit {
                background: rgba(5, 5, 5, 220);
                border: 1px solid rgba(0, 150, 255, 80);
                border-radius: 8px;
                padding: 15px;
                color: rgba(200, 200, 200, 255);
                font-family: 'Consolas', 'Monaco', monospace;
                min-height: 400px;
            }
            QScrollBar:vertical {
                border: none;
                background: rgba(15, 15, 15, 100);
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: rgba(0, 150, 255, 150);
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(0, 200, 255, 200);
            }
        """)
        
        chat_layout.addWidget(self.chat_text_edit)
        
        # RIGHT SIDE - JARVIS core and controls (compact)
        controls_container = QWidget()
        controls_container.setFixedWidth(320)  # Fixed width for right panel
        controls_layout = QVBoxLayout(controls_container)
        controls_layout.setContentsMargins(10, 20, 10, 20)
        controls_layout.setSpacing(20)
        
        # Add some top spacing
        controls_layout.addStretch(1)
        
        # JARVIS core (smaller for right panel)
        core_container = QHBoxLayout()
        core_container.addStretch()
        
        # Create smaller core for side panel
        self.jarvis_core = ElegantJarvisCore()
        self.jarvis_core.setFixedSize(250, 250)  # Smaller than main screen
        core_container.addWidget(self.jarvis_core)
        core_container.addStretch()
        
        controls_layout.addLayout(core_container)
        
        # Mic button
        mic_container = QHBoxLayout()
        mic_container.addStretch()
        
        self.mic_button = ResponsiveMicButton()
        mic_container.addWidget(self.mic_button)
        mic_container.addStretch()
        
        controls_layout.addLayout(mic_container)
        
        # Status label
        self.status_label = QLabel("Available...")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                color: rgba(0, 200, 255, 255);
                font-family: 'Consolas', monospace;
                font-size: 12px;
                font-weight: bold;
                padding: 8px 15px;
                background: rgba(0, 0, 0, 150);
                border: 1px solid rgba(0, 150, 255, 100);
                border-radius: 15px;
                min-width: 120px;
                max-width: 250px;
                margin: 5px;
            }
        """)
        
        status_container = QHBoxLayout()
        status_container.addStretch()
        status_container.addWidget(self.status_label)
        status_container.addStretch()
        
        controls_layout.addLayout(status_container)
        
        # Add bottom spacing
        controls_layout.addStretch(1)
        
        # Add both sides to main layout
        main_layout.addWidget(chat_container, 3)  # Chat takes 3/4 of space
        main_layout.addWidget(controls_container, 1)  # Controls take 1/4 of space
        
        # Set minimum sizes
        self.setMinimumHeight(400)
        self.setMinimumSize(600, 400)
        
        # Dark background
        self.setStyleSheet("""
            QWidget {
                background: rgb(0, 0, 0);
            }
        """)
        
        font = QFont("Consolas", 10)
        self.chat_text_edit.setFont(font)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loadMessages)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(100)

        
    def loadMessages(self):
        global old_chat_message
        try:
            with open(rf'{TempDirPath}\Responses.data', 'r', encoding='utf-8') as file:
                messages = file.read()
            if messages and messages != old_chat_message:
                self.addMessage(message=messages, color='White')
                old_chat_message = messages
        except FileNotFoundError:
            pass
            
    def SpeechRecogText(self):
        try:
            with open(rf'{TempDirPath}\Status.data', 'r', encoding='utf-8') as file:
                status = file.read()
            self.status_label.setText(status)
            
            # Update JARVIS core energy based on status
            if "Listening" in status:
                self.jarvis_core.set_energy_level(1.0)
            elif "Thinking" in status or "Searching" in status:
                self.jarvis_core.set_energy_level(0.8)
            else:
                self.jarvis_core.set_energy_level(0.3)
                
        except FileNotFoundError:
            pass
            
    def addMessage(self, message, color):
        cursor = self.chat_text_edit.textCursor()
        cursor.movePosition(cursor.End)
        
        lines = message.split('\n')
        for line in lines:
            if line.strip():
                format = QTextCharFormat()
                block_format = QTextBlockFormat()
                block_format.setTopMargin(6)
                block_format.setBottomMargin(6)
                block_format.setLeftMargin(10)
                
                if line.startswith(f"{Username}:"):
                    format.setForeground(QColor(100, 200, 255))
                    format.setBackground(QColor(0, 40, 80, 60))
                    block_format.setRightMargin(30)
                elif ":" in line:
                    format.setForeground(QColor(150, 255, 150))
                    format.setBackground(QColor(0, 40, 0, 60))
                    block_format.setRightMargin(30)
                else:
                    format.setForeground(QColor(200, 200, 200))
                
                font = QFont("Consolas", 10)
                format.setFont(font)
                
                cursor.setCharFormat(format)
                cursor.setBlockFormat(block_format)
                cursor.insertText(line + "\n")
                
        self.chat_text_edit.setTextCursor(cursor)
        self.chat_text_edit.ensureCursorVisible()

class ResponsiveInitialScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        
    def initUI(self):
        # Main layout with proper margins
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 40, 20, 60)  # Increased bottom margin
        main_layout.setSpacing(20)
        
        # Title section
        title_container = QVBoxLayout()
        title_container.setSpacing(10)
        
        title_label = QLabel(Assistantname.upper())
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: rgba(0, 200, 255, 255);
                font-family: 'Arial Black', sans-serif;
                font-size: 36px;
                font-weight: bold;
                margin: 15px;
                letter-spacing: 6px;
            }
        """)
        
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(15)
        shadow_effect.setColor(QColor(0, 150, 255, 150))
        shadow_effect.setOffset(0, 0)
        title_label.setGraphicsEffect(shadow_effect)
        
        subtitle_label = QLabel("Artificial Intelligence System")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("""
            QLabel {
                color: rgba(150, 150, 150, 200);
                font-family: 'Arial', sans-serif;
                font-size: 16px;
                font-style: italic;
                margin-bottom: 20px;
                letter-spacing: 2px;
            }
        """)
        
        title_container.addWidget(title_label)
        title_container.addWidget(subtitle_label)
        main_layout.addLayout(title_container)
        
        # Central area with JARVIS core
        central_widget = QWidget()
        central_layout = QVBoxLayout(central_widget)
        central_layout.setSpacing(20)
        
        # JARVIS core
        core_container = QHBoxLayout()
        core_container.addStretch()
        
        self.main_core = ElegantJarvisCore(size=500)
        core_container.addWidget(self.main_core)
        core_container.addStretch()
        
        central_layout.addLayout(core_container)
        
        # Microphone button
        mic_container = QHBoxLayout()
        mic_container.addStretch()
        
        self.mic_button = ResponsiveMicButton()
        mic_container.addWidget(self.mic_button)
        mic_container.addStretch()
        
        central_layout.addLayout(mic_container)
        
        main_layout.addWidget(central_widget, 1)  # Give it stretch
        
        # Status display with FIXED positioning
        status_container = QHBoxLayout()
        status_container.setContentsMargins(20, 0, 20, 0)
        status_container.addStretch()
        
        self.status_label = QLabel("Available...")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                color: rgba(0, 200, 255, 255);
                font-family: 'Consolas', monospace;
                font-size: 16px;
                font-weight: bold;
                padding: 12px 25px;
                background: rgba(0, 0, 0, 150);
                border: 1px solid rgba(0, 150, 255, 100);
                border-radius: 25px;
                min-width: 200px;
                max-width: 400px;
            }
        """)
        
        status_container.addWidget(self.status_label)
        status_container.addStretch()
        
        main_layout.addLayout(status_container)
        
        self.setLayout(main_layout)
        
        # Set minimum size for responsiveness
        self.setMinimumSize(400, 300)
        
        # Pure black background
        self.setStyleSheet("""
            QWidget {
                background: rgb(0, 0, 0);
            }
        """)
        
        # Status update timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_status)
        self.timer.start(100)
        
    def update_status(self):
        try:
            with open(TempDirectoryPath('Status.data'), 'r', encoding='utf-8') as file:
                status = file.read()
            self.status_label.setText(status)
            
            # Update core energy based on status
            if "Listening" in status:
                self.main_core.set_energy_level(1.0)
            elif "Thinking" in status or "Searching" in status:
                self.main_core.set_energy_level(0.8)
            else:
                self.main_core.set_energy_level(0.3)
                
        except FileNotFoundError:
            pass
    
    def resizeEvent(self, event):
        # Adjust font sizes based on window size
        width = event.size().width()
        height = event.size().height()
        
        # Scale title font
        if width < 1000:
            font_size = 28
        elif width < 1200:
            font_size = 32
        else:
            font_size = 36
            
        # Update title styling
        title_label = self.findChild(QLabel)
        if title_label and title_label.text() == Assistantname.upper():
            title_label.setStyleSheet(f"""
                QLabel {{
                    color: rgba(0, 200, 255, 255);
                    font-family: 'Arial Black', sans-serif;
                    font-size: {font_size}px;
                    font-weight: bold;
                    margin: 15px;
                    letter-spacing: 6px;
                }}
            """)
        
        super().resizeEvent(event)

class MessageScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Simple header
        header = QLabel(f"{Assistantname.upper()} Interface")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("""
            QLabel {
                color: rgba(0, 200, 255, 255);
                font-family: 'Arial Black', sans-serif;
                font-size: 20px;
                font-weight: bold;
                padding: 15px;
                background: rgba(5, 5, 5, 200);
                border-bottom: 1px solid rgba(0, 150, 255, 100);
                letter-spacing: 2px;
            }
        """)
        layout.addWidget(header)
        
        # Responsive chat section
        chat_section = ResponsiveChatSection()
        layout.addWidget(chat_section)
        
        self.setLayout(layout)
        
        # Set minimum size
        self.setMinimumSize(400, 300)
        
        # Pure black background
        self.setStyleSheet("""
            QWidget {
                background: rgb(0, 0, 0);
            }
        """)

class CustomTopBar(QWidget):
    def __init__(self, parent, stacked_widget):
        super().__init__(parent)
        self.stacked_widget = stacked_widget
        self.setFixedHeight(40)
        self.initUI()
        
    def initUI(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(8)
        
        # Logo
        logo_label = QLabel(Assistantname.upper())
        logo_label.setStyleSheet("""
            QLabel {
                color: rgba(0, 200, 255, 255);
                font-family: 'Arial Black', sans-serif;
                font-size: 14px;
                font-weight: bold;
                padding: 3px 10px;
            }
        """)
        layout.addWidget(logo_label)
        layout.addStretch()
        
        # Compact buttons
        button_style = """
            QPushButton {
                background: rgba(0, 150, 255, 80);
                color: white;
                border: 1px solid rgba(0, 200, 255, 120);
                border-radius: 12px;
                padding: 6px 12px;
                font-weight: bold;
                font-size: 10px;
            }
            QPushButton:hover {
                background: rgba(0, 200, 255, 120);
                border: 1px solid rgba(0, 255, 255, 150);
            }
            QPushButton:pressed {
                background: rgba(0, 100, 200, 120);
            }
        """
        
        home_button = QPushButton("Home")
        home_button.setStyleSheet(button_style)
        home_button.clicked.connect(self.showInitialScreen)
        
        message_button = QPushButton("Messages")
        message_button.setStyleSheet(button_style)
        message_button.clicked.connect(self.showMessageScreen)
        
        minimize_button = QPushButton("−")
        minimize_button.setStyleSheet(button_style + "QPushButton { padding: 6px 10px; }")
        minimize_button.clicked.connect(self.minimizeWindow)
        
        self.maximize_button = QPushButton("□")
        self.maximize_button.setStyleSheet(button_style + "QPushButton { padding: 6px 10px; }")
        self.maximize_button.clicked.connect(self.maximizeWindow)
        
        close_button = QPushButton("✕")
        close_button.setStyleSheet("""
            QPushButton {
                background: rgba(255, 100, 100, 80);
                color: white;
                border: 1px solid rgba(255, 150, 150, 120);
                border-radius: 12px;
                padding: 6px 10px;
                font-weight: bold;
                font-size: 10px;
            }
            QPushButton:hover {
                background: rgba(255, 150, 150, 120);
            }
        """)
        close_button.clicked.connect(self.closeWindow)
        
        layout.addWidget(home_button)
        layout.addWidget(message_button)
        layout.addWidget(minimize_button)
        layout.addWidget(self.maximize_button)
        layout.addWidget(close_button)
        
        self.setStyleSheet("""
            QWidget {
                background: rgba(5, 5, 5, 200);
                border-bottom: 1px solid rgba(0, 150, 255, 80);
            }
        """)
        
    def minimizeWindow(self):
        self.parent().showMinimized()
        
    def maximizeWindow(self):
        if self.parent().isMaximized():
            self.parent().showNormal()
            self.maximize_button.setText("□")
        else:
            self.parent().showMaximized()
            self.maximize_button.setText("❐")
            
    def closeWindow(self):
        self.parent().close()
        
    def showMessageScreen(self):
        self.stacked_widget.setCurrentIndex(1)
        
    def showInitialScreen(self):
        self.stacked_widget.setCurrentIndex(0)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.initUI()
        
    def initUI(self):
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()
        
        # Create stacked widget for screens
        stacked_widget = QStackedWidget(self)
        
        # Create responsive screens
        initial_screen = ResponsiveInitialScreen()
        message_screen = MessageScreen()
        
        stacked_widget.addWidget(initial_screen)
        stacked_widget.addWidget(message_screen)
        
        # Set window properties with minimum size
        self.setGeometry(0, 0, screen_width, screen_height)
        self.setMinimumSize(400, 300)  # Allow much smaller window size
        
        # Create compact top bar
        top_bar = CustomTopBar(self, stacked_widget)
        self.setMenuWidget(top_bar)
        self.setCentralWidget(stacked_widget)
        
        # Pure black window
        self.setStyleSheet("""
            QMainWindow {
                background: rgb(0, 0, 0);
            }
        """)

def GraphicalUserInterface():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
