.PHONY= frontend wheels

frontend:
	npm run build --prefix streamlit_observable/frontend

wheels: frontend
	python3 setup.py sdist bdist_wheel

upload: wheels
	echo "python3 -m twine upload dist/*"