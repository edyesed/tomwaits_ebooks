# get pipenv
FROM python:3.8-slim
#
#COPY --chown=app bin/download-lyrics/*txt /app/lyrics/
#COPY --chown=app chatbot.py /app/
RUN pip install pipenv 
RUN useradd -d /app -m app
USER app 
WORKDIR /app
COPY Pipfile* /app/
RUN pipenv install
RUN pipenv run python3 -m nltk.downloader punkt
RUN pipenv run python3 -m nltk.downloader wordnet
RUN pipenv run python3 -m nltk.downloader tagsets
RUN pipenv run python3 -m nltk.downloader averaged_perceptron_tagger
RUN pipenv run python3 -m nltk.downloader book_grammars
# Not using stanza yet
# RUN pipenv exec python3 -c "import stanza; stanza.download('en');"

COPY *.py /app/
COPY bin/download-lyrics/*txt /app/bin/download-lyrics/
CMD pipenv run python3 /app/chatbot.py
