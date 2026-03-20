from glob import glob
import os

from setuptools import setup

package_name = "tidebreaker"

setup(
    name=package_name,
    version="0.0.0",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        (os.path.join("share", package_name, "launch"), glob("launch/*.launch.py")),
        (os.path.join('share', package_name, 'config'), glob('config/*')),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Matthew Barrs",
    maintainer_email="matthewbarrs@ucf.edu",
    description="Vehicle operations and supervisor",
    license="MIT",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
		"send_gps_to_ardupilot = tidebraker.send_gps_to_ardupilot:main"
        ],
    },
)
