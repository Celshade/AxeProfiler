import os
import json


class TempConfig():
   """
   A Context Manager for the testing suite.

   Will setup and teardown a temp config file for AxeProfiler to use during
   testing.
   """
   def __init__(self, profile_dir: str):
       """
       Expects a `profile_dir` passed in from the pytext `tmp_path` fixture.

       Args:
           profile_dir: The temp profile_dir to store in the config file.
       """
       self.profile_dir = profile_dir

   def __enter__(self):
        if os.path.exists(".config"):
            os.rename(".config", ".config.backup")
            print("\noriginal config backed up! ☑")
        with open(".config", 'w') as f:
            f.write(json.dumps({"profile_dir": self.profile_dir}, indent=4))

   def __exit__(self, exc_type, exc_val, exc_tb):
       os.remove(".config")
       print("\ntemp config deleted")
       os.rename(".config.backup", ".config")
       print("\noriginal config restored! ✅")
