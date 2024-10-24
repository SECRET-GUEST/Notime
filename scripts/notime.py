import sys
import os
import datetime
import json
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication,
    QSystemTrayIcon,
    QMenu,
    QWidget,
    QLabel,
    QVBoxLayout,
    QStyle,
    QLineEdit,
    QPushButton,
    QFormLayout,
    QMessageBox,
)
from PySide6.QtGui import QIcon, QAction, QPixmap
from PySide6.QtCore import (
    Qt,
    QUrl,
    Slot,
    QObject,
    QTimer,
    QElapsedTimer,
    QStandardPaths,
    QCoreApplication,
)
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput


class FullScreenAnimation(QWidget):
    def __init__(self, image_folder, sound_file=None, fps=30):
        super().__init__()

        self.image_folder = image_folder
        self.sound_file = sound_file
        self.fps = fps
        self.frame_duration = 1000 / self.fps  # Duration of each frame in milliseconds

        # Window configuration
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.showFullScreen()

        # QLabel to display images
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("background-color: transparent;")

        # Layout setup
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.label)

        # Preload and scale images
        self.pixmaps = self.load_and_scale_images()

        if not self.pixmaps:
            self.close()
            return

        self.total_frames = len(self.pixmaps)

        # Start sound if available
        self.start_sound()

        # Start timer to update images
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_image)
        self.timer.start(0)  # Start immediately

        # Timer to track elapsed time
        self.elapsed_timer = QElapsedTimer()
        self.elapsed_timer.start()

        # Connect destroyed signal for cleanup
        self.destroyed.connect(self.cleanup)

    def load_and_scale_images(self):
        pixmaps = []
        image_files = sorted(Path(self.image_folder).glob("*.webp"))
        screen_size = self.screen().size()
        for img_path in image_files:
            pixmap = QPixmap(str(img_path))
            if not pixmap.isNull():
                # Pre-scale the image
                scaled_pixmap = pixmap.scaled(
                    screen_size,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation,
                )
                pixmaps.append(scaled_pixmap)
        return pixmaps

    def start_sound(self):
        if self.sound_file and os.path.exists(self.sound_file):
            self.audio_output = QAudioOutput()
            self.player = QMediaPlayer()
            self.player.setAudioOutput(self.audio_output)
            self.player.setSource(QUrl.fromLocalFile(self.sound_file))
            self.player.play()
        else:
            self.player = None

    def update_image(self):
        # Calculate frame index based on elapsed time
        elapsed_ms = self.elapsed_timer.elapsed()
        frame_index = int(elapsed_ms / self.frame_duration)

        if frame_index < self.total_frames:
            self.label.setPixmap(self.pixmaps[frame_index])
        else:
            self.timer.stop()
            self.end_animation()

    def end_animation(self):
        # Clear the label
        self.label.clear()
        # Close the window
        self.close()

    def cleanup(self):
        # Clean up resources
        if hasattr(self, "player") and self.player:
            self.player.stop()
            self.player.deleteLater()
            del self.player
        if hasattr(self, "audio_output"):
            self.audio_output.deleteLater()
            del self.audio_output
        self.pixmaps.clear()


class SettingsWindow(QWidget):
    def __init__(self, settings, parent=None):
        super().__init__()
        self.settings = settings
        self.parent = parent

        self.setWindowTitle("Settings")  # Window title

        # Create input fields for settings
        self.work_interval_input = QLineEdit(str(self.settings["work_interval"] // 60))
        self.break_interval_1_input = QLineEdit(str(self.settings["break_intervals"][0] // 60))
        self.break_interval_2_input = QLineEdit(str(self.settings["break_intervals"][1] // 60))
        self.total_duration_input = QLineEdit(str(self.settings["total_duration"] // 3600))

        # Buttons
        self.save_button = QPushButton("Save Settings")
        self.restore_button = QPushButton("Restore Default Settings")

        # Layout setup
        layout = QFormLayout()
        layout.addRow("Work Interval (minutes):", self.work_interval_input)
        layout.addRow("Break 1 (minutes):", self.break_interval_1_input)
        layout.addRow("Break 2 (minutes):", self.break_interval_2_input)
        layout.addRow("Total Duration (hours):", self.total_duration_input)
        layout.addRow(self.save_button, self.restore_button)
        self.setLayout(layout)

        # Connect buttons to functions
        self.save_button.clicked.connect(self.save_settings)
        self.restore_button.clicked.connect(self.restore_defaults)

    def save_settings(self):
        try:
            work_interval = int(self.work_interval_input.text()) * 60
            break_interval_1 = int(self.break_interval_1_input.text()) * 60
            break_interval_2 = int(self.break_interval_2_input.text()) * 60
            total_duration = int(self.total_duration_input.text()) * 3600

            self.settings["work_interval"] = work_interval
            self.settings["break_intervals"] = [break_interval_1, break_interval_2]
            self.settings["total_duration"] = total_duration

            # Save settings to configuration file
            self.parent.save_settings()

            # Restart the program with new settings
            self.parent.restart_program()

            QMessageBox.information(self, "Settings", "Settings saved successfully.")
            self.close()
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter valid numbers.")

    def restore_defaults(self):
        # Restore default settings
        self.work_interval_input.setText("45")
        self.break_interval_1_input.setText("10")
        self.break_interval_2_input.setText("20")
        self.total_duration_input.setText("8")


class MainApp(QObject):
    def __init__(self):
        super().__init__()
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)

        self.sound_enabled = True
        self.animation_enabled = True
        self.is_paused = False

        # Initialize animation_window
        self.animation_window = None

        # Set application and organization name for correct paths
        QCoreApplication.setOrganizationName("SECRET_GUEST")
        QCoreApplication.setApplicationName("NOTIME")

        # Resource management
        if getattr(sys, "frozen", False):
            self.resource_path = sys._MEIPASS
        else:
            self.resource_path = os.path.dirname(os.path.abspath(__file__))

        # Paths to resources
        self.sound_folder = os.path.join(self.resource_path, "se")
        self.image_folder = os.path.join(self.resource_path, "img")
        self.icon_path = os.path.join(self.image_folder, "notime.ico")

        # Set application icon
        if os.path.exists(self.icon_path):
            app_icon = QIcon(self.icon_path)
            self.app.setWindowIcon(app_icon)

        # Default settings
        self.default_settings = {
            "work_interval": 45 * 60,
            "break_intervals": [10 * 60, 20 * 60],
            "total_duration": 8 * 60 * 60,
        }
        self.settings = self.default_settings.copy()
        self.load_settings()

        # Initialize system tray icon
        self.create_tray_icon()

        # Paths for animations and sounds
        self.counter_folder = os.path.join(self.image_folder, "counter")
        self.over_folder = os.path.join(self.image_folder, "over")
        self.counter_sound = os.path.join(self.sound_folder, "counter.wav")
        self.over_sound = os.path.join(self.sound_folder, "over.wav")

        # Start timers
        self.start_time = datetime.datetime.now()
        self.elapsed_time = datetime.timedelta(0)
        self.init_timers()

        # Start the initial 'counter' animation
        self.show_counter_animation()

    def create_tray_icon(self):
        if os.path.exists(self.icon_path):
            tray_icon = QIcon(self.icon_path)
        else:
            tray_icon = self.app.style().standardIcon(QStyle.SP_ComputerIcon)

        self.tray_icon = QSystemTrayIcon(tray_icon)
        self.menu = QMenu()

        # Elapsed time display (disabled, for display only)
        self.elapsed_time_action = QAction("Elapsed Time: 00:00:00")
        self.elapsed_time_action.setDisabled(True)
        self.menu.addAction(self.elapsed_time_action)

        # Pause/Resume action
        self.pause_action = QAction("Pause")
        self.pause_action.triggered.connect(self.toggle_pause)
        self.menu.addAction(self.pause_action)

        # Sound toggle action
        self.sound_action = QAction("Disable Sound", checkable=True)
        self.sound_action.setChecked(False)
        self.sound_action.triggered.connect(self.toggle_sound)
        self.menu.addAction(self.sound_action)

        # Settings action
        self.settings_action = QAction("Settings")
        self.settings_action.triggered.connect(self.show_settings)
        self.menu.addAction(self.settings_action)

        # Exit action
        self.exit_action = QAction("Exit")
        self.exit_action.triggered.connect(self.exit_app)
        self.menu.addAction(self.exit_action)

        # Set the context menu and show the tray icon
        self.tray_icon.setContextMenu(self.menu)
        self.tray_icon.show()

        # Timer to update the elapsed time display
        self.elapsed_time_timer = QTimer()
        self.elapsed_time_timer.timeout.connect(self.update_elapsed_time)
        self.elapsed_time_timer.start(1000)

    def toggle_sound(self):
        # Toggle sound enabled/disabled
        self.sound_enabled = not self.sound_action.isChecked()

    def exit_app(self):
        # Exit the application
        QApplication.quit()

    def toggle_pause(self):
        if not self.is_paused:
            # Pause the timers
            self.timer.stop()
            self.elapsed_time_timer.stop()
            if self.animation_window:
                self.animation_window.close()
                self.animation_window = None
            self.pause_action.setText("Start")
            self.is_paused = True
            # Save elapsed time up to now
            self.elapsed_time += datetime.datetime.now() - self.start_time
        else:
            # Reload settings in case they were changed
            self.load_settings()

            # Restart the program
            self.start_time = datetime.datetime.now()
            self.init_timers()
            self.elapsed_time_timer.start(1000)
            self.pause_action.setText("Pause")
            self.is_paused = False
            self.show_counter_animation()

    def show_settings(self):
        # Display the settings window
        self.settings_window = SettingsWindow(self.settings, self)
        self.settings_window.show()

    def restart_program(self):
        # Restart the program with current settings
        self.timer.stop()
        self.start_time = datetime.datetime.now()
        self.elapsed_time = datetime.timedelta(0)
        self.init_timers()
        if self.is_paused:
            self.elapsed_time_timer.start(1000)
            self.pause_action.setText("Pause")
            self.is_paused = False
        self.show_counter_animation()

    def init_timers(self):
        # Initialize the main timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.run_cycle)
        self.cycle_step = 0
        self.interval_work = self.settings["work_interval"]
        self.intervals_pause = self.settings["break_intervals"]

        self.timer.start(self.interval_work * 1000)

    def run_cycle(self):
        if self.is_paused:
            return

        if self.cycle_step % 2 == 0:
            # End of work period, show 'over' animation
            if self.animation_enabled:
                self.show_animation(self.over_folder, self.over_sound)
            elif self.sound_enabled:
                self.play_sound(self.over_sound)

            # Set up the break interval
            current_interval = self.intervals_pause[(self.cycle_step // 2) % 2]
            self.timer.start(current_interval * 1000)
        else:
            # End of break, show 'counter' animation
            if self.animation_enabled:
                self.show_animation(self.counter_folder, self.counter_sound)
            elif self.sound_enabled:
                self.play_sound(self.counter_sound)

            self.timer.start(self.interval_work * 1000)

        self.cycle_step += 1

    def show_counter_animation(self):
        # Display the initial 'counter' animation
        if self.animation_enabled:
            self.show_animation(self.counter_folder, self.counter_sound)
        elif self.sound_enabled:
            self.play_sound(self.counter_sound)

    def show_animation(self, folder, sound_file):
        # Before creating a new animation, check if the previous one exists
        if self.animation_window is not None:
            try:
                self.animation_window.close()
            except RuntimeError:
                pass
            self.animation_window = None

        # Create a new animation window
        self.animation_window = FullScreenAnimation(
            folder,
            sound_file if self.sound_enabled else None,
            fps=30  # Ensure the FPS matches your animation
        )

        # Connect the destroyed signal to update the animation_window reference
        self.animation_window.destroyed.connect(self.on_animation_closed)

    def on_animation_closed(self):
        # Update the reference when the animation window is closed
        self.animation_window = None

    def play_sound(self, sound_file):
        # Play a sound without animation
        audio_output = QAudioOutput()
        player = QMediaPlayer()
        player.setAudioOutput(audio_output)
        url = QUrl.fromLocalFile(sound_file)
        player.setSource(url)
        player.play()

    def update_elapsed_time(self):
        if self.is_paused:
            return

        # Update the elapsed time display
        total_elapsed = self.elapsed_time + (datetime.datetime.now() - self.start_time)
        total_seconds = int(total_elapsed.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        elapsed_str = f"Elapsed Time: {hours:02}:{minutes:02}:{seconds:02}"
        self.elapsed_time_action.setText(elapsed_str)

        # Check if the total duration is reached
        if total_seconds >= self.settings["total_duration"]:
            self.exit_app()

    def load_settings(self):
        # Load settings from the configuration file
        config_dir = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        config_path = os.path.join(config_dir, "notime_config.json")
        self.config_path = config_path
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                try:
                    self.settings.update(json.load(f))
                except json.JSONDecodeError:
                    pass

    def save_settings(self):
        # Save settings to the configuration file
        config_dir = os.path.dirname(self.config_path)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        with open(self.config_path, "w") as f:
            json.dump(self.settings, f)

    def run(self):
        # Start the application event loop
        self.app.exec()


if __name__ == "__main__":
    app = MainApp()
    app.run()
