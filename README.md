# Cojourn
A small dev server to accelerate development on the Open HEMS mobile app.

# Installation
1. Install [`pipenv`](http://pipenv.pypa.io)
```
brew install pipenv
```

2. Install project dependencies
```
pipenv install
```

# Run the dev server
```
% pipenv shell
((cojourn)) % cd api_mock
((cojourn)) % FLASK_APP=main FLASK_ENV=development flask run
```
