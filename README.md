# Database Things (Python)
A small toolbox to:
1) connect to databases (Postgres / SQL Server / SQLite)
2) run SQL queries saved in `.sql` files
3) export results to **CSV / Excel / Parquet** using a simple command

This repository is made for people who always need to do “database stuff” but don’t memorize the code.

---

## ✅ What you can do
- Run a query from a file like `queries/sample.sql`
- Export results to:
  - `.csv`
  - `.xlsx`
  - `.parquet`
- Works with:
  - **Postgres**
  - **SQL Server**
  - **SQLite**

---

## 🧭 Step-by-step guide (from zero to export)

### 1) Install Python & clone
- Install Python 3.10+.
- Clone the repo:
  ```bash
  git clone <YOUR_REPO_URL_HERE>
  cd <YOUR_REPO_FOLDER_HERE>
  ```

### 2) Create a virtual environment (recommended)
```bash
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate
```

### 3) Install dependencies
```bash
pip install -r requirements.txt
```

### 4) Set your database credentials
- Copy the sample env and edit values:
  ```bash
  cp database_things/.env database_things/.env.local
  # edit database_things/.env.local with your DB credentials
  ```
- The CLI loads `.env` automatically (it can also read `.env.local` if you `export $(cat ... | xargs)` beforehand).

### 5) Prepare a SQL file
- Put your query in a `.sql` file, e.g. `database_things/queries/sample.sql`.
- You can add parameters in the query (positional placeholders):
  - Postgres/SQLite use `?` or `%s`? → use the DB default (`%s` for Postgres, `?` for SQLite/SQL Server via pyodbc).

### 6) Run the exporter CLI
From repo root:
```bash
python -m database_things.tools.db_exporter.cli \
  --db postgres \
  --query-file database_things/queries/sample.sql \
  --out outputs/sample.csv
```
- For SQL Server: `--db sqlserver`
- For SQLite: `--db sqlite --sqlite-path path/to/file.db`
- Add params (strings) if your query needs them:
  ```bash
  --params foo bar
  ```

### 7) Check the output
- Find your file in `outputs/` (or the path you set).
- Supported formats: `.csv`, `.parquet`, `.xlsx`.

---

## 🧪 Minimal end-to-end example
1. Ensure Postgres is reachable and env vars are set in `database_things/.env.local`.
2. Use the provided `database_things/queries/sample.sql`.
3. Run:
   ```bash
   python -m database_things.tools.db_exporter.cli \
     --db postgres \
     --query-file database_things/queries/sample.sql \
     --out outputs/sample.csv
   ```
4. Open `outputs/sample.csv` to see the rows.

---

## 🛟 Tips
- Logs go to `logs/db_exporter.log`.
- If you see connection errors, re-check `.env` values and network access.
- For SQLite, no server is needed—just point `--sqlite-path` to your `.db` file.

---

## 🧩 Complete filled example (copy-paste friendly)

1) Create and populate the env file:
```bash
cat > database_things/.env.local <<'EOF'
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=super_secret
DB_NAME=demo_db

DB_DRIVER={ODBC Driver 17 for SQL Server}
DB_SERVER=localhost
DB_DATABASE=demo_db
DB_USERNAME=sa
DB_PASSWORD=super_secret
EOF
```

2) Create the sample SQL (you can reuse/overwrite `database_things/queries/sample.sql`):
```bash
cat > database_things/queries/sample.sql <<'EOF'
SELECT
  id,
  name,
  created_at
FROM users
WHERE created_at >= %s;
EOF
```

3) Run the exporter (Postgres example) from repo root:
```bash
python -m database_things.tools.db_exporter.cli \
  --db postgres \
  --query-file database_things/queries/sample.sql \
  --out outputs/users_since.csv \
  --params "2024-01-01"
```

4) Check the output (preview):
```
$ head -n 5 outputs/users_since.csv
id,name,created_at
1,Alice,2024-02-10 12:34:56
2,Bob,2024-03-01 09:10:11
3,Charlie,2024-04-05 15:00:00
4,Dana,2024-05-12 08:22:33
```

5) Logs (if needed):
```
$ tail -n 5 logs/db_exporter.log
2024-06-01 10:00:00 | INFO | Starting export: db=postgres query_file=database_things/queries/sample.sql out=outputs/users_since.csv
...
2024-06-01 10:00:02 | INFO | Export finished: rows=123 cols=3 file=outputs/users_since.csv
```

