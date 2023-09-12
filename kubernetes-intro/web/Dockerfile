
FROM python:3.10-alpine
WORKDIR /app
RUN chown -R 1001 /app
USER 1001
EXPOSE 8000
CMD ["python", "-m", "http.server", "8000"]