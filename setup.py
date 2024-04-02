from setuptools import setup

setup(
    name='pygame-headers',
    version='1.0',
    author='RetroButterbacke',
    author_email='butterbacke51@gmail.com',
    description='A simple compilation of headers for the pygame libary made for my computer sience course in school',
    install_requires=[
        "pygame>=2.5.2",
        "numpy>=1.22.2",
        "pyperclip>=1.8.2"
    ],
    packages=['graphics_pg', 'graphics_pg_old'],#, 'graphics_pg_plus', 'graphics_pg_3d'],
    python_requires='>=3.7'
)