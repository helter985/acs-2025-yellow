test-service:
	PYTHONPATH=. python -W ignore -m app.tests.test_item_service

test-handler:
	PYTHONPATH=. python -W ignore -m app.tests.test_item_handlers

test-all:
	PYTHONPATH=. python -W ignore -m app.tests.test_item_service
	PYTHONPATH=. python -W ignore -m app.tests.test_item_handlers

test:
	PYTHONPATH=. python3 -W ignore -m unittest discover app/tests -v