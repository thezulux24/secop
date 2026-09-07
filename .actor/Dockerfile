# Plain JSON API client - no browser, no TLS impersonation needed. SECOP II's Socrata
# endpoint is a public, unauthenticated, non-hostile REST API.
FROM apify/actor-python:3.13

COPY requirements.txt ./

RUN echo "Python version:" \
 && python --version \
 && pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt \
 && echo "Installed:" \
 && pip freeze

COPY . ./

CMD ["python", "-m", "src"]
