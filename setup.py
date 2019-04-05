import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="d-save-last",
    version="0.1.0",
    author="Bryan Thornbury",
    author_email="author@example.com",
    description="A command line utility effectively replicating `docker save` except that it " +
            "will only save the LAST layer of the image in the output archive.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/brthor/docker-save-last",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Utilities"
    ],
    scripts=[
        "bin/d-save-last"
    ]
)