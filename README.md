# **ngp_docs**

An **unofficial** documentation portal that tracks **per-commit next_gen_prototype releases**, providing visual aides to newly onboarded developers of the Open-RMF Next Generation.

## **Access**

**Access** the public documentation portal below:

> https://cardboardcode.github.io/ngp_docs/latest/

## Build

If you wish to view it **locally**, run the commands below:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

```bash
# build the site
. .venv/bin/activate
sphinx-build -b html . _build/html
```

```bash
# preview
. .venv/bin/activate
python -m http.server -d _build/html
```

**Access** the local documentation portal below:

> http://localhost:8000
