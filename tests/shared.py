import os
import json


class TempConfig:
    """
    A Context Manager for the testing suite.

    Will setup and teardown a temp config file for AxeProfiler to use during
    testing.
    """

    def __init__(self, profile_dir: str, num_profiles: int = 0,
                 extra_profile: dict | None = None):
        """
        Expects a `profile_dir` passed in from the pytext `tmp_path` fixture.

        Args:
            profile_dir: The temp profile_dir to store in the config file.
            num_profiles: The number of profiles to mock (default=0).
            extra_profile: Optional dict containing a single profile to
                create in the profile dir. If provided, the file will be
                named from the profile's `profile_name` field.
        """
        self.profile_dir = profile_dir
        self.num_profiles = num_profiles
        self.extra_profile = extra_profile

    def __enter__(self):
        # Backup existing config file (if one exists)
        if os.path.exists(".config"):
            os.rename(".config", ".config.backup")
            print("\noriginal config backed up! ☑")

        # Create a temp config file that points to the temp testing profile dir
        with open(".config", 'w') as f:
            f.write(json.dumps({"profile_dir": self.profile_dir}, indent=4))

        # Create mock profiles
        if self.num_profiles:
            for i in range(0, self.num_profiles):
                path = f"{self.profile_dir}test_{i}.json"
                print(f"profile created at: {path}")
                with open(path, 'w') as f:
                    f.write(
                        json.dumps(
                            {
                                "profile_name": f"test_{i}",
                                "hostname": "Unknown",
                                "frequency": 600,
                                "coreVoltage": 1200,
                                "fanspeed": 100
                            },
                            indent=4)
                    )

        # Create an additional profile provided as a single dict. Use the
        # `profile_name` field (if present) to name the file, otherwise fall
        # back to 'extra.json'.
        if self.extra_profile:
            name = self.extra_profile.get('profile_name', 'extra')
            filename = f"{name}.json" if not name.endswith('.json') else name
            path = f"{self.profile_dir}{filename}"
            print(f"extra profile created at: {path}")
            with open(path, 'w') as f:
                f.write(json.dumps(self.extra_profile, indent=4))

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.remove(".config")
        print("\ntemp config deleted")
        os.rename(".config.backup", ".config")
        print("\noriginal config restored! ✅")
