# get pipenv
FROM kennethreitz/pipenv@sha256:47b251b3b53fcc71a0a57549210f1cd6c34a730d49560fc71ac269c542bcca24
#
#COPY --chown=app bin/download-lyrics/*txt /app/lyrics/
#COPY --chown=app chatbot.py /app/
RUN python3 -m nltk.downloader punkt
RUN python3 -m nltk.downloader wordnet
RUN python3 -m nltk.downloader tagsets
RUN python3 -m nltk.downloader averaged_perceptron_tagger
# Not using stanza yet
# RUN python3 -c "import stanza; stanza.download('en');"

COPY *.py /app/
COPY bin/download-lyrics/*txt /app/bin/download-lyrics/
CMD python3 /app/chatbot.py