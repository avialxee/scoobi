from setuptools import setup

with open("README.md", "r") as rdme:
    desc = rdme.read()

setup(
    name = 'scoobi',
    version = '0.0.1.5',
    url='https://github.com/avialxee/scoobi',
    author='Avinash Kumar',
    author_email='avialxee@gmail.com',
    description='Solar Conventionality-based Organizing Observation data ( SCOOBI )',
    py_modules = ["scoobi"],
    package_dir={'':'src'},
    classifiers=["Programming Language :: Python :: 3",
                 "Programming Language :: Python :: 3.7",
                 "Programming Language :: Python :: 3.8",
                 "Programming Language :: Python :: 3.9",
                 "Programming Language :: Python :: 3.10",
                 "License :: OSI Approved :: BSD License",
                 "Intended Audience :: Science/Research",
                 ],
    long_description=desc,
    long_description_content_type = "text/markdown",
    install_requires=["astropy", "numpy", "exifread"
                      ],
    extras_require = {
        "dev" : ["pytest>=3.7",
        ]
    },
     entry_points={ 
        "console_scripts": [
            "scoobi=scoobi.cli:cli"
        ],
    },

)