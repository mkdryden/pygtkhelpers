# -*- coding: utf-8 -*-
import logging
import os

import gtk
from ...delegates import SlaveView

logger = logging.getLogger(__name__)


class GtkCairoView(SlaveView):
    """
    SlaveView for Cairo drawing surface.
    """
    def __init__(self, width=None, height=None):
        if width is None:
            self.width = 640
        else:
            self.width = width
        if height is None:
            self.height = 480
        else:
            self.height = height
        super(GtkCairoView, self).__init__()

    def create_ui(self):
        self.widget = gtk.DrawingArea()
        self.widget.set_size_request(self.width, self.height)
        self.window_xid = None
        self._set_window_title = False

    def show_and_run(self):
        self._set_window_title = True
        super(GtkCairoView, self).show_and_run()

    def on_widget__realize(self, widget):
        if not self.widget.window.has_native():
            # Note that this is required (at least for Windows) to ensure that
            # the DrawingArea has a native window assigned.  In Windows, if
            # this is not done, the video is written to the parent OS window
            # (not a "window" in the traditional sense of an app, but rather in
            # the window manager clipped rectangle sense).  The symptom is that
            # the video will be drawn over top of any widgets, etc. in the
            # parent window.
            if not self.widget.window.ensure_native():
                raise RuntimeError('Failed to get native window handle')
        if os.name == 'nt':
            self.window_xid = self.widget.window.handle
        else:
            self.window_xid = self.widget.window.xid
        logger.info('window_xid=%s', self.window_xid)
