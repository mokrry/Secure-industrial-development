## DV
### Репозитории и контекст

- **P07 — контейнеризация:** репозиторий со своим FastAPI-сервисом `study_planner`.
- **P08 — CI/CD:** репозиторий `Secure-industrial-development` с полноценным CI/CD-конвейером.

Ниже — разбор по чек-листу DV 0.2.

---

### 1. Стабильный CI (зелёные прогоны)

**Что сделано**

- Для `study_planner`:
  - Общий `ci.yml` запускает линтеры (`ruff`, `black`, `isort`), тесты (`pytest`) и сборку Docker-образа.
  - Отдельный `ci-security.yml` — Hadolint + Trivy.
  - Все нужные джобы проходят зелёным на ветке `p07`.

    <img width="774" height="313" alt="image" src="https://github.com/user-attachments/assets/0055bcca-dc07-4cf7-9187-90369a13c7e9" />

- Для `Secure-industrial-development`:
  - Workflow `.github/workflows/ci.yml` с матрицей Python `3.10/3.11/3.12`.
  - На каждый `push`/`pull_request` в `main` прогоняются линтеры, тесты и CD-часть.
  - Есть успешные зелёные прогоны:

    <img width="1817" height="830" alt="image" src="https://github.com/user-attachments/assets/52dc7e1a-5f1b-4077-b5b0-cae3680adea9" />  

    Run: https://github.com/mokrry/Secure-industrial-development/actions/runs/19515213442

**Итого:** стабильный CI с автоматическими проверками на коммит и PR ✅

---

### 2. Сборка / тесты / артефакты

**Сборка и тесты**

- `study_planner`:
  - Dockerfile в продакшн-формате (multi-stage, `python:3.11-slim`, non-root).
  - Проверен размер и история слоёв образа:

    <img width="1252" height="781" alt="image" src="https://github.com/user-attachments/assets/a1f3140a-987a-4723-a02c-49f9f02437b8" />

  - Сборка образа в CI (job в `ci.yml`).
  - `pytest -q` зелёный локально и в CI.

- `Secure-industrial-development`:
  - Job `Test & lint (matrix)`:
    - установка зависимостей из `requirements.txt` и `requirements-dev.txt`;
    - `ruff`, `black --check`, `isort --check-only`;
    - `pytest -q` с генерацией JUnit и coverage-репортов (XML + HTML).

**Артефакты**

- Для каждой версии Python (`3.10/3.11/3.12`) загружаются артефакты:
  - каталоги `reports-3.10/3.11/3.12` с JUnit-логами и отчётами покрытия:

    <img width="1817" height="830" alt="image" src="https://github.com/user-attachments/assets/52dc7e1a-5f1b-4077-b5b0-cae3680adea9" />

- В `deploy-staging` собираемый Docker-образ сохраняется как артефакт `docker-image-staging` и переиспользуется в `promote-prod`.

**Итого:** сборка, тесты и артефакты отчётности/образов настроены ✅

---

### 3. Секреты вынесены из кода

- В `Secure-industrial-development` заведены Secrets GitHub Actions:
  - `DB_URL`.

    <img width="996" height="187" alt="image" src="https://github.com/user-attachments/assets/c9404400-c20f-4b87-884b-d6519f6ddd4a" />

- В кодовой базе нет хардкода чувствительных данных; подключение к БД определяется переменными окружения.

**Итого:** секреты вынесены из кода в Secrets, используются безопасно в CI/CD ✅

---

### 4. PR-политика и ревью по чек-листу

- Ветви под задачи:
  - `p07` — контейнеризация `study_planner` (Dockerfile, compose, security CI).
  - `p08-cicd-minimal` — CI/CD для `Secure-industrial-development`.
- Для каждой ветки оформлен отдельный **PR** с описанием того, что реализовано по критериям (C1–C5).

  <img width="1386" height="141" alt="image" src="https://github.com/user-attachments/assets/2a205c2b-0b97-465c-89f9-8949163f862a" />

  <img width="1385" height="84" alt="image" src="https://github.com/user-attachments/assets/b11f0392-db42-4fde-a6ac-bbd2cef46b38" />


- В описаниях PR:
  - перечислены выполненные пункты чек-листа;
  - приложены ссылки на зелёные прогонки и скриншоты.
- Локально перед пушем запускаются `ruff/black/isort`, `pytest` и `pre-commit run --all-files` — это фактический чек-лист для самопроверки.

**Итого:** работа ведётся через ветки и PR, изменения сопровождаются чек-листом и проверками ✅

---

### 5. Воспроизводимый локальный запуск (Docker / compose)

**Для `study_planner` (P07)**

- Продакшн-готовый `Dockerfile`:
  - multi-stage (builder/runtime), base image `python:3.11-slim`;
  - установка зависимостей с `--no-cache-dir`;
  - non-root пользователь `appuser`, `HEALTHCHECK` на `/health`.
- Стек в `compose.yaml`:
  - `app` — FastAPI-сервис `study_planner`;
  - `db` — `postgres:16-alpine` с volume `pgdata` и healthcheck’ом.
- Hardening контейнера `app`:
  - `read_only: true`, `tmpfs: ["/tmp"]`;
  - `security_opt: ["no-new-privileges:true"]`;
  - `cap_drop: ["ALL"]`.
- `depends_on` с `condition: service_healthy`, чтобы `app` ждал готовность БД.
- Локальный запуск одной командой:
  ```bash
  docker compose up -d
<img width="1812" height="689" alt="image" src="https://github.com/user-attachments/assets/7966d63e-c133-41f8-8905-2d9bce4d7774" />

После этого `GET /health` возвращает `200 OK`.

**Итого:** локальный запуск всего стека воспроизводим через Docker/Compose ✅

---

### 6. Превосходство (на 9–10 баллов)

Дополнительно к базовому чек-листу выполнен ряд «старших» практик:

* **Матрица окружений:** CI-матрица по Python `3.10/3.11/3.12` в `Secure-industrial-development`.
* **Кэширование и конкуррентность:**

  * `actions/cache@v4` для pip по ключу ОС + версия Python + `requirements*.txt`;
  * `concurrency` по `${{ github.workflow }}-${{ github.ref }}` для отмены старых прогонов.
* **Отчёты покрытия:** сохраняются coverage XML/HTML как артефакты по каждой версии Python.
* **Безопасность Docker-образов:**

  * Hadolint с `.hadolint.yaml` (игнор-правила и threshold);
  * Trivy с `trivy.yaml`, `.trivyignore` и выгрузкой отчёта в формате `sarif`.
* **Эмуляция CD с промоушном:**

  * `deploy-staging`:

    * собирает Docker-образ;
    * запускает контейнер и делает неблокирующий `/health`-чек;
    * сохраняет образ как артефакт.
  * `promote-prod` (по тегам `v*`):

    * скачивает `docker-image-staging`, делает `docker load`;
    * выполняет условный prod smoke-test (mock промоушн).

**Итого:** помимо базового DevOps-конвейера реализованы дополнительные практики (матрица, кэш, отчёты покрытия, security-сканирование, staged-деплой), что соответствует уровню «превосходство» ✅

---

