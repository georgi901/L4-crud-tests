# Laborator 4 - Teste Automate + GitHub Actions

Aplicatia CRUD din L3 cu teste pytest si GitHub Actions pentru rulare automata.

## Structura
```
L4/
├── .github/
│   └── workflows/
│       └── tests.yml       # GitHub Actions workflow
├── server.py               # Server Flask (API REST)
├── test_server.py           # Teste pytest (15 teste)
├── requirements.txt         # Dependente Python
└── README.md
```

## Teste incluse
- **TestGetCourses** - GET cursuri (lista + individual + 404)
- **TestCreateCourse** - POST curs nou (valid + invalid + defaults)
- **TestUpdateCourse** - PUT modificare (partial + total + 404)
- **TestDeleteCourse** - DELETE stergere (valid + 404 + integritate)

## Rulare locala
```bash
pip install -r requirements.txt
pytest test_server.py -v
```

## GitHub Actions
Testele ruleaza automat la fiecare push pe `main`.
