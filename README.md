## Cojourn
A small dev server to accelerate development on the Open HEMS mobile app.

### Installation
```
brew install pipenv
pipenv install
```

### Start the dev server at [http://localhost:5000/api/v1](http://localhost:5000/api/v1)
```
% pipenv shell
((cojourn)) % cd api_mock
((cojourn)) % FLASK_APP=main FLASK_ENV=development flask run
```
