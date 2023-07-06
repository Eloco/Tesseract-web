FROM richardarpanet/python-tesseract-alpine:latest

COPY . .

RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.mirrors.ustc.edu.cn/simple

COPY traineddata /usr/local/share/tessdata

CMD ["python", "app.py"]
