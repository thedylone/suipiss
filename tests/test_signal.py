"""test signal handling"""

import os
import signal
import subprocess
import time
import unittest


class TestSignal(unittest.TestCase):
    """test signal handling"""

    def test_signal(self):
        """test signal handling"""
        if os.name == "nt":
            # windows
            proc = subprocess.Popen(
                ["python", "bot.py", "--debug"],
                shell=False,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
            )
            time.sleep(2)
            print("sending signal")
            proc.send_signal(signal.CTRL_BREAK_EVENT)
            time.sleep(2)
            proc.wait()
            self.assertIsNotNone(proc.poll)
        elif os.name == "posix":
            # linux
            proc = subprocess.Popen(
                ["python", "bot.py", "--debug"],
                shell=False,
                preexec_fn=os.setpgrp,
            )
            time.sleep(2)
            print("sending signal")
            proc.send_signal(signal.SIGTERM)
            time.sleep(2)
            proc.wait()
            self.assertIsNotNone(proc.poll)


if __name__ == "__main__":
    unittest.main()
