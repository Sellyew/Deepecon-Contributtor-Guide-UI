"""The upload handler for the form without JavaScript (plan §2.5).

Django normally writes a large posted file to the system's temporary folder, whatever its
size, before the view can refuse it. This handler writes into private storage instead
(UPLOAD_INCOMING_DIR, mode 0700) and stops storing once the paper's size limit is passed; the
view then tells the contributor the file was too large. The stored temporary file is moved
into place, not copied.
"""
import os
import tempfile
from pathlib import Path

from django.conf import settings
from django.core.files.uploadedfile import TemporaryUploadedFile, UploadedFile
from django.core.files.uploadhandler import FileUploadHandler, TemporaryFileUploadHandler


class PrivateTemporaryUploadedFile(TemporaryUploadedFile):
    def __init__(self, name, content_type, size, charset, content_type_extra=None):
        incoming = Path(settings.UPLOAD_INCOMING_DIR)
        incoming.mkdir(parents=True, exist_ok=True)
        os.chmod(incoming, 0o700)
        file = tempfile.NamedTemporaryFile(suffix=".upload", dir=incoming)
        UploadedFile.__init__(self, file, name, content_type, size, charset, content_type_extra)


class LimitedPrivateUploadHandler(TemporaryFileUploadHandler):
    def __init__(self, request=None, limit=0):
        super().__init__(request)
        self.limit, self.seen, self.too_large = limit, 0, False

    def new_file(self, *args, **kwargs):
        FileUploadHandler.new_file(self, *args, **kwargs)
        self.file = PrivateTemporaryUploadedFile(self.file_name, self.content_type, 0, self.charset, self.content_type_extra)

    def receive_data_chunk(self, raw_data, start):
        self.seen += len(raw_data)
        if self.seen > self.limit:
            self.too_large = True        # keep reading the request so that the answer reaches the browser,
            return None                  # but store nothing more
        self.file.write(raw_data)

    def file_complete(self, file_size):
        if self.too_large:
            self.file.close()
            return None                  # no file: the view reports that it was too large
        return super().file_complete(file_size)
