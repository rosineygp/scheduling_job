include $(shell [ ! -f .mkdkr ] && curl -fsSL https://git.io/JOBYz > .mkdkr; bash .mkdkr init)

format.autopep8:
	for i in $$(git diff --cached --name-only | grep \.py$$); do \
		autopep8 -i $$i; \
		git add $$i; \
	done

lint.pylint:
	@$(dkr)
	instance: python:3.8
	run: pip install pylint
	run: 'find . -type f -name "*.py" | xargs pylint -E'

test.unit-%:
	@$(dkr)
	instance: python:$*
	run: pip install -r requirements.txt
	run: python test_scheduler.py

test.unit: test.unit-3.6 test.unit-3.7 test.unit-3.8 test.unit-3.9

pre-commit: 
	make --silent format.autopep8 
	make --silent lint.pylint
	make --silent test.unit -j 4 --output-sync

pos-commit: lint.commit

git.hooks:
	$(MAKE) .git/hooks/pre-commit
	$(MAKE) .git/hooks/commit-msg

.git/hooks/pre-commit:
	echo "make pre-commit" > .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit

.git/hooks/commit-msg:
	echo "make pos-commit" > .git/hooks/commit-msg
	chmod +x .git/hooks/commit-msg