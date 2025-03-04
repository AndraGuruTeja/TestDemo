# weather-monitoring-app/
# ├─ .env
# ├─ .gitignore
# ├─ README.md
# ├─ backend/
# │  ├─ .env
# │  ├─ Dockerfile
# │  ├─ app/
# │  │  ├─ __init__.py
# │  │  ├─ __pycache__/
# │  │  │  ├─ __init__.cpython-312.pyc
# │  │  │  └─ main.cpython-312.pyc
# │  │  ├─ cache.py
# │  │  ├─ config.py
# │  │  ├─ database.py
# │  │  ├─ main.py
# │  │  ├─ models.py
# │  │  ├─ schemas.py
# │  │  └─ services.py
# │  ├─ docker-compose.yml
# │  ├─ requirements.txt
# │  ├─ tests/
# │  │  ├─ __init__.py
# │  │  ├─ test_api.py
# │  │  └─ test_services.py
# │  └─ weather.db
# ├─ ci-cd/
# │  ├─ github-actions/
# │  │  ├─ ci.yml
# │  │  └─ deploy.yml
# │  └─ jenkins/
# │     └─ Jenkinsfile
# ├─ docs/
# │  ├─ API_DOCS.md
# │  ├─ ARCHITECTURE.md
# │  └─ diagrams/
# ├─ frontend/
# │  ├─ .env
# │  ├─ Dockerfile
# │  ├─ package-lock.json
# │  ├─ package.json
# │  ├─ postcss.config.js
# │  ├─ public/
# │  │  └─ index.html
# │  ├─ src/
# │  │  ├─ App.js
# │  │  ├─ api.js
# │  │  ├─ components/
# │  │  │  ├─ SearchBar.js
# │  │  │  └─ WeatherCard.js
# │  │  ├─ index.js
# │  │  ├─ styles.css
# │  │  └─ tailwind.css
# │  └─ tailwind.config.js
# ├─ infrastructure/
# │  ├─ scripts/
# │  │  ├─ backup_restore.sh
# │  │  └─ deploy.sh
# │  └─ terraform/
# │     ├─ environments/
# │     │  ├─ dev/
# │     │  │  ├─ main.tf
# │     │  │  └─ variables.tf
# │     │  └─ prod/
# │     │     ├─ main.tf
# │     │     └─ variables.tf
# │     └─ modules/
# │        ├─ cache/
# │        │  └─ main.tf
# │        ├─ compute/
# │        │  └─ main.tf
# │        ├─ database/
# │        │  └─ main.tf
# │        └─ network/
# │           └─ main.tf
# └─ monitoring/
#    ├─ grafana/
#    │  └─ dashboards/
#    │     └─ weather-dashboard.json
#    ├─ loki/
#    └─ prometheus/
#       ├─ alerts.yml
#       └─ prometheus.yml
