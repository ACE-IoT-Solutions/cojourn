## Cojourn
A small dev server to accelerate development on the Open HEMS mobile app.

### Installation
```
brew install pipenv
pipenv install
```

### Start the dev server at [localhost:5000](localhost:5000)
```
pipenv run python api_mock/main.py
```

Alternatively (if you're not into the whole brevity thing)
```
pipenv shell
cd api_mock
FLASK_APP=main FLASK_ENV=development flask run
```

### Interacting with [Swagger UI](http://localhost:5000/api/v1)
The Swagger UI is a convenient GUI for interacting with the existing endpoints.

- Visit [jwt.io](https://jwt.io) and replace `your-256-bit-secret` with `super secret` (or whatever `JWT_SECRET_KEY` value from app config)
- Copy the encoded JWT
- Visit [Swagger UI](http://localhost:5000/api/v1) and tap `🔓 Authorize`
- Paste `Bearer <YOUR_ENCODED_JWT>` in the value and hit submit.
- ...
- Profit!

Once authorized, try hitting the `GET /devices` endpoint. You should receive a `200` response with some interesting device data. If you receive a `422` or otherwise you probably have a poorly-formed JWT.
