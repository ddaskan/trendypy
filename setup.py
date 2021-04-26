import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt', 'r') as f:
    install_requires = f.read().splitlines()

setuptools.setup(
    name="trendypy",
    version="0.2.2",
    author="Dogan Askan",
    author_email="doganaskan@gmail.com",
    description="A package for trend line clustering.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ddaskan/trendypy",
    download_url="https://pypi.python.org/pypi/trendypy",
    project_urls={
        "Bug Tracker": "https://github.com/ddaskan/trendypy/issues",
        "Documentation": "https://trendypy.readthedocs.io/",
        "Source Code": "https://github.com/ddaskan/trendypy",
    },
    license='MIT',
    keywords='ml ai data-analysis machine-learning clustering',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Topic :: Scientific/Engineering',
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development",
    ],
    python_requires='>=3.7',
    install_requires=install_requires,
)