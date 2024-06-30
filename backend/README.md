# SuperSEO Analyzer Backend

This is the backend API for the SuperSEO Analyzer, a tool designed to help users analyze SEO performance by extracting keywords, managing URLs, and providing user management features.

## Features

- **Keyword Extraction**: Analyze text and extract keywords.
- **URL Management**: Add and manage URLs for SEO analysis.
- **User Authentication**: Register and authenticate users.

## Project Structure

```plaintext
.
├── base
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── keywords_extractor
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── utils.py
│   └── ...
├── urls
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── utils.py
│   └── ...
├── users
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── ...
├── manage.py
├── README.md
└── requirements.txt


## Getting Started
### Prerequisites
    Python 3.10+
    Django
    Django REST Framework

# Installation

1- clone the repo
```
git clone https://github.com/yourusername/SuperSEO-analyzer.git
cd SuperSEO-analyzer/backend
```


2- Install the dependencies:
```
pip install -r requirements.txt

```

3- Apply migrations:

```
python manage.py migrate

```

4- Run the server:

```
python manage.py runserver
```


## Testing
```
python manage.py test
```


## API Endpoints


### Keywords Extractor

- **GET /api/keywords/**: Retrieve extracted keywords.
- **POST /api/keywords/**: Submit text for keyword extraction.


### URLs

- **GET /api/urls/**: List all URLs.
- **POST /api/urls/**: Add a new URL for analysis.
- **GET /api/urls/{id}/**: Retrieve details of a specific URL.


### Users

- **POST /api/users/register/**: Register a new user.
- **POST /api/users/login/**: Authenticate a user.
- **GET /api/users/profile/**: Retrieve the authenticated user's profile.


## Contributing

Contributions are welcome! Please submit a pull request or open an issue for suggestions.
