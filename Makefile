.PHONY: publish
testpypi:
	# poetry config http-basic.testpypi {{USER_NAME}} {{PASSWORD}}
	poetry build
	poetry publish -r testpypi
