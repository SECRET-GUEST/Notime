import sys
import os
from pathlib import Path

from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QWidget, QLabel, QVBoxLayout, QStyle
from PySide6.QtGui import QIcon, QAction, QPixmap
from PySide6.QtCore import Qt, QUrl, Slot, QObject, Signal, QTimer
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput

class FullScreenAnimation(QWidget):
    def __init__(self, image_folder, sound_file=None, fps=30):
        super().__init__()

        self.image_folder = image_folder
        self.sound_file = sound_file
        self.fps = fps

        # Window configuration
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)  # Enable transparency
        self.setAttribute(Qt.WA_DeleteOnClose)  # Ensure object deletion upon close
        self.showFullScreen()

        # QLabel to display the images
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("background-color: rgba(0, 0, 0, 0);")  # Transparent background

        # Add QLabel to the layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.label)

        # Load webp images
        self.image_files = sorted(Path(self.image_folder).glob("*.webp"))
        if not self.image_files:
            # No images found, close the window
            self.close()
            return

        # Preload the images
        self.pixmaps = []
        for img_path in self.image_files:
            pixmap = QPixmap(str(img_path))
            if not pixmap.isNull():
                self.pixmaps.append(pixmap)

        self.current_index = 0

        # Start sound if available
        if self.sound_file and os.path.exists(self.sound_file):
            url = QUrl.fromLocalFile(self.sound_file)
            self.audio_output = QAudioOutput()
            self.player = QMediaPlayer()
            self.player.setAudioOutput(self.audio_output)
            self.player.setSource(url)
            # Sync images with the sound position
            self.player.positionChanged.connect(self.update_image)
            self.player.play()
        else:
            # Start timer for animation if no sound
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_image)
            self.timer.start(int(1000 / self.fps))

    def update_image(self, position=None):
        if position is not None:
            # Sync images with the sound position
            frame_number = int(position / (1000 / self.fps))
        else:
            # If no position is provided, use the current index
            frame_number = self.current_index
            self.current_index += 1

        if frame_number < len(self.pixmaps):
            # Resize pixmap to fit screen
            screen_size = self.screen().size()
            scaled_pixmap = self.pixmaps[frame_number].scaled(
                screen_size, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.label.setPixmap(scaled_pixmap)
        else:
            # Animation finished
            if hasattr(self, "timer"):
                self.timer.stop()
            if hasattr(self, "player"):
                self.player.stop()
            self.close()
            self.deleteLater()  # Ensure object deletion

class MainApp(QObject):
    # Signals to trigger animations and sounds
    show_animation_signal = Signal(str, str)
    play_sound_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)

        self.sound_enabled = True
        self.animation_enabled = True

        # Resource management
        if getattr(sys, 'frozen', False):
            self.resource_path = sys._MEIPASS
        else:
            self.resource_path = os.path.dirname(os.path.abspath(__file__))

        # Resource paths
        self.sound_folder = os.path.join(self.resource_path, "se")
        self.image_folder = os.path.join(self.resource_path, "img")
        self.icon_path = os.path.join(self.image_folder, "notime.ico")

        # Set application icon
        if os.path.exists(self.icon_path):
            app_icon = QIcon(self.icon_path)
            self.app.setWindowIcon(app_icon)

        # Initialize the system tray icon
        self.create_tray_icon()

        # Connect signals to slots
        self.show_animation_signal.connect(self.show_animation)
        self.play_sound_signal.connect(self.play_sound)

        # Paths for animations and sounds
        self.counter_folder = os.path.join(self.image_folder, "counter")
        self.over_folder = os.path.join(self.image_folder, "over")
        self.counter_sound = os.path.join(self.sound_folder, "counter.wav")
        self.over_sound = os.path.join(self.sound_folder, "over.wav")

        # Start timers
        self.init_timers()

        # Show 'counter' animation at startup
        self.show_counter_animation()

    def create_tray_icon(self):
        if os.path.exists(self.icon_path):
            tray_icon = QIcon(self.icon_path)
        else:
            tray_icon = self.app.style().standardIcon(QStyle.SP_ComputerIcon)

        self.tray_icon = QSystemTrayIcon(tray_icon)
        self.menu = QMenu()

        self.sound_action = QAction("Disable Sound", checkable=True)
        self.sound_action.setChecked(False)
        self.sound_action.triggered.connect(self.toggle_sound)
        self.menu.addAction(self.sound_action)

        #self.animation_action = QAction("Disable Animation", checkable=True)
        #self.animation_action.setChecked(False)
        #self.animation_action.triggered.connect(self.toggle_animation)
        #self.menu.addAction(self.animation_action)

        self.exit_action = QAction("Exit")
        self.exit_action.triggered.connect(self.exit_app)
        self.menu.addAction(self.exit_action)

        self.tray_icon.setContextMenu(self.menu)
        self.tray_icon.show()

    def toggle_sound(self):
        self.sound_enabled = not self.sound_action.isChecked()

    def toggle_animation(self):
        self.animation_enabled = not self.animation_action.isChecked()

    def exit_app(self):
        QApplication.quit()

    def init_timers(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.run_cycle)
        self.cycle_step = 0  # To track the cycle state
        self.interval_work = 45 * 60 * 1000  # 45 minutes in milliseconds
        self.intervals_pause = [10 * 60 * 1000, 20 * 60 * 1000]  # 10 minutes and 20 minutes

        # Start the first cycle after the 'counter' animation
        self.timer.start(self.interval_work)

    def run_cycle(self):
        if self.cycle_step % 2 == 0:
            # End of work period, show 'over' animation
            if self.animation_enabled:
                self.show_animation_signal.emit(
                    self.over_folder, self.over_sound if self.sound_enabled else None
                )
            elif self.sound_enabled:
                self.play_sound_signal.emit(self.over_sound)

            # Set up the break
            if (self.cycle_step // 2) % 2 == 0:
                current_interval = self.intervals_pause[0]  # 10 minutes
            else:
                current_interval = self.intervals_pause[1]  # 20 minutes

            # Restart the timer for the break
            self.timer.start(current_interval)
        else:
            # End of break, show 'counter' animation
            if self.animation_enabled:
                self.show_animation_signal.emit(
                    self.counter_folder, self.counter_sound if self.sound_enabled else None
                )
            elif self.sound_enabled:
                self.play_sound_signal.emit(self.counter_sound)

            # Restart the timer for work
            self.timer.start(self.interval_work)

        self.cycle_step += 1

    def show_counter_animation(self):
        if self.animation_enabled:
            self.show_animation(self.counter_folder, self.counter_sound if self.sound_enabled else None)
        elif self.sound_enabled:
            self.play_sound(self.counter_sound)

    @Slot(str, str)
    def show_animation(self, folder, sound_file):
        self.animation_window = FullScreenAnimation(folder, sound_file)

    @Slot(str)
    def play_sound(self, sound_file):
        # Play sound without showing the animation
        self.audio_output = QAudioOutput()
        self.player = QMediaPlayer()
        self.player.setAudioOutput(self.audio_output)
        url = QUrl.fromLocalFile(sound_file)
        self.player.setSource(url)
        self.player.play()

    def run(self):
        self.app.exec()

if __name__ == "__main__":
    app = MainApp()
    app.run()
