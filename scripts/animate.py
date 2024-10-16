import sys
import os
from pathlib import Path

from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QUrl
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
        self.showFullScreen()

        # QLabel to display the images
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("background-color: rgba(0, 0, 0, 0);")  # Transparent background

        # Add QLabel to the layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.label)

        # Load PNG images
        self.image_files = sorted(Path(self.image_folder).glob("*.png"))
        if not self.image_files:
            # No PNG images found, close the window
            self.close()
            return

        # Preload images into a list for quick access
        self.pixmaps = []
        for img_path in self.image_files:
            pixmap = QPixmap(str(img_path))
            if not pixmap.isNull():
                self.pixmaps.append(pixmap)

        # Calculate the total duration of the animation based on the number of images and fps
        self.total_duration = len(self.pixmaps) * (1000 / self.fps)  # in milliseconds

        # Start the sound if available
        if self.sound_file and os.path.exists(self.sound_file):
            url = QUrl.fromLocalFile(self.sound_file)
            self.audio_output = QAudioOutput()
            self.player = QMediaPlayer()
            self.player.setAudioOutput(self.audio_output)
            self.player.setSource(url)
            self.player.positionChanged.connect(self.update_image)
            self.player.play()
        else:
            # Audio file not found, exit the application
            sys.exit(1)

    def update_image(self, position):
        # position is the elapsed time in milliseconds
        if position >= self.total_duration:
            self.player.stop()
            self.close()
            return

        # Calculate the image index based on the elapsed time
        frame_number = int(position / (1000 / self.fps))
        if frame_number >= len(self.pixmaps):
            frame_number = len(self.pixmaps) - 1

        pixmap = self.pixmaps[frame_number]
        # Resize the pixmap to the screen size
        screen_size = self.screen().size()
        scaled_pixmap = pixmap.scaled(
            screen_size, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.label.setPixmap(scaled_pixmap)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Path to the folder containing the "over" animation images in PNG
    base_path = os.path.dirname(os.path.abspath(__file__))
    image_folder = os.path.join(base_path, "img", "over_png")
    sound_file = os.path.join(base_path, "se", "over.wav")  # Ensure the audio file exists

    # Verify that the image folder exists
    if not os.path.exists(image_folder):
        sys.exit(1)

    # Verify that there are images in the folder
    image_files = sorted(Path(image_folder).glob("*.png"))
    if not image_files:
        sys.exit(1)

    animation = FullScreenAnimation(image_folder, sound_file, fps=30)
    sys.exit(app.exec())
