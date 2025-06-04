import sys
import types
import importlib
import pytest

@pytest.fixture(autouse=True)
def stub_dependencies(monkeypatch):
    modules = {
        'numpy': types.ModuleType('numpy'),
        'pandas': types.ModuleType('pandas'),
        'sklearn': types.ModuleType('sklearn'),
        'sklearn.linear_model': types.ModuleType('sklearn.linear_model'),
        'sklearn.preprocessing': types.ModuleType('sklearn.preprocessing'),
        'scipy': types.ModuleType('scipy'),
        'scipy.signal': types.ModuleType('scipy.signal'),
        'matplotlib': types.ModuleType('matplotlib'),
        'matplotlib.pyplot': types.ModuleType('matplotlib.pyplot'),
        'matplotlib.gridspec': types.ModuleType('matplotlib.gridspec'),
        'mpl_finance': types.ModuleType('mpl_finance'),
    }
    modules['numpy'].nan = float('nan')
    modules['pandas'].DataFrame = type('DataFrame', (), {})
    modules['pandas'].Series = type('Series', (), {})
    modules['pandas'].concat = lambda *args, **kwargs: modules['pandas'].DataFrame()
    modules['pandas'].to_datetime = lambda *args, **kwargs: None
    modules['sklearn.linear_model'].LinearRegression = object
    modules['sklearn.preprocessing'].MinMaxScaler = object
    modules['scipy.signal'].argrelextrema = lambda *a, **k: [0]
    modules['mpl_finance'].candlestick_ohlc = lambda *a, **k: None

    modules['sklearn'].linear_model = modules['sklearn.linear_model']
    modules['sklearn'].preprocessing = modules['sklearn.preprocessing']
    modules['scipy'].signal = modules['scipy.signal']
    modules['matplotlib'].pyplot = modules['matplotlib.pyplot']
    modules['matplotlib'].gridspec = modules['matplotlib.gridspec']

    for name, mod in modules.items():
        monkeypatch.setitem(sys.modules, name, mod)
    yield


def test_import_package():
    pkg = importlib.import_module('pattern_scanner')
    assert hasattr(pkg, '__version__')


def test_get_crosspt_basic():
    from pattern_scanner.core.util import get_crosspt
    cx, cy = get_crosspt(0, 0, 1, 1, 0, 1, 1, 0)
    assert round(cx, 2) == 0.5
    assert round(cy, 2) == 0.5
