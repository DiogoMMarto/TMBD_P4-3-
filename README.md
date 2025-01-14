# TMBD - Assignment 3

## API

Build image:
```
cd API
docker build -t traffic_sign_api .
```

Run image:
```
docker run -d -p 8000:8000 -e API_PORT="8000" traffic_sign_api
```

## Web Client

Build image:
```
cd website
docker build -t traffic_sign_client .
```

Run image:
```
docker run -d -p 8001:8001 \
    -e WEB_PORT="8001" \
    -e API_URL="http://localhost:8000/api" \
    traffic_sign_client
```