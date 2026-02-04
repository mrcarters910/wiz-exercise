FROM python:3.12-slim

WORKDIR /app

# wizexercise requirement: file with my name
RUN echo "Corey Carter" > /wizexercise.txt

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=5001
EXPOSE 5001

CMD ["python", "app.py"]
