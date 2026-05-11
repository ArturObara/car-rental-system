# 1. Wybieramy bazę (nasz fundament)
FROM python:3.12-slim

# 2. Ustawiamy zmienne środowiskowe, żeby Python nie śmiecił i logi sypały się na bieżąco
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Tworzymy folder /app wewnątrz kontenera i tam będziemy pracować
WORKDIR /app

# 4. Kopiujemy listę zakupów i instalujemy biblioteki
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Kopiujemy całą resztę kodu do kontenera
COPY . .

# 6. Mówimy Dockerowi, że nasza aplikacja słucha na porcie 8000
EXPOSE 8000

# 7. Komenda, która odpali serwer po starcie kontenera
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]