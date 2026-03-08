FROM codalab/codalab-legacy:py39

ENV DEBIAN_FRONTEND=noninteractive

RUN pip install -U pip

# Force uninstall all NumPy 1.x compiled packages before upgrading
RUN pip uninstall -y numpy numexpr bottleneck || true

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Verify — if these pass, there's no conflict
RUN python3 -c "import numpy; print('NumPy:', numpy.__version__)"
RUN python3 -c "import sklearn; print('sklearn OK')"
RUN python3 -c "import xgboost; print('XGBoost OK')"