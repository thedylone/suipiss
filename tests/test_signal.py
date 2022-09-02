import os
import unittest
import subprocess
import time
import signal


class TestSignal(unittest.TestCase):
    def test_signal(self):
        if os.name == "nt":
            # windows
            proc = subprocess.Popen(
                ["python", "bot.py"],
                shell=True,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
            )
            time.sleep(2)
            print("sending signal")
            proc.send_signal(signal.CTRL_BREAK_EVENT)
            time.sleep(2)
            self.assertIsNotNone(proc.poll)
        elif os.name == "posix":
            # linux
            proc = subprocess.Popen(
                ["nohup", "python", "bot.py"],
                shell=True,
            )
            time.sleep(2)
            print("sending signal")
            proc.send_signal(signal.SIGTERM)
            time.sleep(2)
            self.assertIsNotNone(proc.poll)


if __name__ == "__main__":
    unittest.main()
