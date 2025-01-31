from setuptools import find_packages, setup

# find_packages will find all the packages with __init__.py
print(find_packages())

setup(
    name="travel_planner",
    version="0.0.1",
    description="This package is used for travel planning in public transport.",
    author="Kokchun",
    author_email="YOUR_EMAIL@mail.com",
    install_requires=[
        "streamlit",
        "pandas",
        "folium",
        "requests",
        "seaborn",
        "matplotlib",
        "numpy",
    ],
    packages=find_packages(
        include=["backend*", "frontend*", "utils*"], exclude=("test*", "explorations")
    ),
    entry_points={"console_scripts": ["dashboard = utils.run_dashboard:run_dashboard"]},
)
