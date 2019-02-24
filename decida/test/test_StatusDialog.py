#! /usr/bin/env python
from builtins import object
import threading
import decida
from decida.StatusDialog import StatusDialog

class ProgressReport(object) :
    def __init__(self):
        self._iter = 0
        self._report = None
        self._report_ready = False
        self._thread = threading.Thread(target=self._generate_report, args=())
        self._thread.setDaemon(True)
        self._thread.start()
    def _generate_report(self):
        while True:
            if self._report_ready :
                continue
            self._iter += 1
          # output = decida.syscall("/usr/bin/top -l 1")
            output = decida.syscall("/bin/ps -ax")
            lines = output.split("\n")
            lines.append(" iteration: %s" % (self._iter))
            self._report = "\n".join(lines)
            self._report_ready = True
    def get_report(self):
        if self._report_ready :
            self._report_ready = False
            return self._report
        return None

pr = ProgressReport()
sts = StatusDialog(title="top monitor", command=pr.get_report)
