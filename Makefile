.PHONY= frontend wheels

frontend:
	npm run build --prefix streamlit_observable/frontend

wheels:
	python setup.py sdist bdist_wheel

upload:
	echo "python -m twine upload dist/*"