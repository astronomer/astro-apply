FROM python:3.9-slim-buster

RUN pip install --upgrade pip

RUN useradd -u 50000 -m astro
USER astro
WORKDIR /home/astro

COPY --chown=astro:astro requirements.txt requirements.txt
RUN pip install --user -r requirements.txt

ENV PATH="/home/astro/.local/bin:${PATH}"

COPY --chown=astro:astro . .

CMD ["python", "client.py"]