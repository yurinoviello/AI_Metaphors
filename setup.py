from setuptools import setup, find_packages

setup(
    name="ai-metaphors",
    version="0.1.0",
    description="AI Metaphors - Generate metaphors and animations",
    author="JB",
    author_email="yuri.noviello@jetbrains.com",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "ai-metaphors=ai_metaphors.main:main",
        ],
    },
)