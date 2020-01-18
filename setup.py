from setuptools import setup


setup(
    name="WordAssistant",
    version="0.1.1",
    scripts=["word_assistant.pyw"],
    package_data={
        "background": ["*jpg"],
    },

    author="Daniiya Ipatova",
    author_email=" ",
    keywords="transcriber transcribation speech_recognize",
    url="https://github.com/daniiyang/WordAssistant",
)