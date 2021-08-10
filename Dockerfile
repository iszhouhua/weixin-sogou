FROM python:3.9-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
EXPOSE 80
CMD ["uvicorn","main:app","--host","0.0.0.0","--port","80","--log-config","logger_config.json"]

