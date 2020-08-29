.PHONY= frontend wheels

frontend:
	npm run build --prefix streamlit_observable/frontend

wheels:
	python3 setup.py sdist bdist_wheel

upload:
	echo "python3 -m twine upload dist/*"