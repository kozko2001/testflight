from setuptools import setup, find_packages
print find_packages();
setup(
        name = "TestFlight",
        version = "0.1",
        packages = find_packages(),
        scripts = ['testflight.py'],
        author = "Jordi Coscolla",
        author_email = "jordi@coscolla.net",
        description = "Basic testflight script in python to compile, sign and upload iPhone projects to testflight",
        )

