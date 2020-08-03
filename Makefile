env:
	/Library/Frameworks/Python.framework/Versions/3.8/bin/virtualenv venv
	venv/bin/pip install -U pip
	venv/bin/pip install -r requirements.txt
	# for dev work:
	venv/bin/pip install ipython

output/casestudy_moby_dick.pdf: src/moby_dick.py
	venv/bin/python $<
