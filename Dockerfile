FROM python:3.9-slim
COPY ./app requirements.txt /app/
RUN mkdir /logs \
    && pip install -r /app/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
EXPOSE 80
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","80"]

