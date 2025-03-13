import importlib.util
import sys

DEPENDENCIES = [
    "flask", "PyQt5", "plotly", "pylatex", "pytest", "pytest_qt",
    "numpy", "pandas", "matplotlib", "requests"
]


def check_dependency(module_name):
    spec = importlib.util.find_spec(module_name)
    return spec is not None


def main():
    missing_packages = [pkg for pkg in DEPENDENCIES if not check_dependency(pkg)]

    if missing_packages:
        print("❌ Missing dependencies:", ", ".join(missing_packages))
        print("Try installing them using:")
        print("  pip install -r requirements.txt  (for pip users)")
        print("  conda env update --file environment.yml  (for Conda users)")
        sys.exit(1)
    else:
        print("✅ All dependencies installed correctly!")


if __name__ == "__main__":
    main()
