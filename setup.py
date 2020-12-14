import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xps",
    version="0.2.1",
    description="X-Ray photonelectron spectroscopy (XPS) analysis tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="David Kalliecharan",
    author_email="david@david.science",
    url="https://gitlab.com/ddkn/xps",
    packages=setuptools.find_packages(),
    include_package_data=True,
    license='ISC',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Scientific/Engineering :: Physics",
        "Natural Language :: English",
    ],
)
