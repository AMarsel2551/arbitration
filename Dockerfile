FROM python:3.11-slim

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN groupadd -g 501 appuser
RUN useradd -r -g 501 -u 501 appuser
COPY start.sh .
RUN chmod a+x start.sh && chown appuser:appuser start.sh
USER appuser
COPY app app

EXPOSE 8080

ENTRYPOINT ["/start.sh"]
