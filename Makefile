build:
	python -m src.code2doc.build

clean:
	rm -rf src/code2doc.egg-info
	rm -rf build
	rm -rf dist
	rm -rf .tox

package:
	python setup.py sdist bdist_wheel

upload:
	twine upload dist/*

major:
	bump2version --allow-dirty major

minor:
	bump2version --allow-dirty minor

patch:
	bump2version --allow-dirty patch
