env:
	/Library/Frameworks/Python.framework/Versions/3.8/bin/virtualenv venv
	venv/bin/pip install -U pip
	venv/bin/pip install -r requirements.txt
	# for dev work:
	venv/bin/pip install ipython

output/casestudy_moby_dick.pdf: src/moby_dick.py
	venv/bin/python $<

output/casestudy_moby_dick_with_stopwords.pdf: src/moby_dick.py
	venv/bin/python $<

output/case_study_moby_dick_combined.pdf: output/casestudy_moby_dick.pdf output/casestudy_moby_dick_with_stopwords.pdf
	/Users/andyreagan/tools/perl/kitchentable/pdftile.pl 1 2 .48 3 0 l 8 "" "" output/casestudy_moby_dick.pdf "" output/casestudy_moby_dick_with_stopwords.pdf output/case_study_moby_dick_combined
	open $@

all: output/casestudy_moby_dick.pdf output/case_study_moby_dick_combined.pdf
