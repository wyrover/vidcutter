#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtCore import Qt, QObject, QEvent
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QFrame, QMessageBox


parent_frame = QFrame
if sys.platform == 'darwin':
    from PyQt5.QtWidgets import QMacCocoaViewContainer
    parent_frame = QMacCocoaViewContainer


class VideoFrame(parent_frame):
    def __init__(self, parent=None, *arg, **kwargs):
        super(VideoFrame, self).__init__(parent, *arg, **kwargs)
        if sys.platform == 'darwin':
            self.setCocoaView(0)
        self.parent = parent
        self.setAttribute(Qt.WA_DontCreateNativeAncestors)
        self.setAttribute(Qt.WA_NativeWindow)
        self.installEventFilter(self)

    def toggleFullscreen(self) -> None:
        if self.isFullScreen():
            self.parent.mediaPlayer.fullscreen = False
            self.parent.setWindowState(self.parent.windowState() & ~Qt.WindowFullScreen)
            # self.setWindowFlags(Qt.Widget)
            # self.showNormal()
        else:
            self.parent.mediaPlayer.fullscreen = True
            self.parent.setWindowState(self.parent.windowState() | Qt.WindowFullScreen)
            # self.setWindowFlags(Qt.Window)
            # self.showFullScreen()

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        self.toggleFullscreen()
        event.accept()

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        if self.parent.mediaAvailable and event.type() == QEvent.WinIdChange:
            QMessageBox.warning(self, 'winId CHANGE', 'winId change has been detected.\n\n' +
                                'winId: %s\neffective winId: %s' % (self.winId().asstring(),
                                                                    self.effectiveWinId().asstring()))
        return super(VideoFrame, self).eventFilter(obj, event)

