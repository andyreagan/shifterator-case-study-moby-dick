env: requirements.txt
	/Library/Frameworks/Python.framework/Versions/3.8/bin/virtualenv venv
	venv/bin/pip install -U pip
	venv/bin/pip install -r requirements.txt
	venv/bin/python -m spacy download en_core_web_lg
	# for dev work:
	venv/bin/pip install ipython

output/casestudy_moby_dick.pdf: src/moby_dick.py
	venv/bin/python $<

output/casestudy_moby_dick_with_stopwords.pdf: src/moby_dick.py
	venv/bin/python $<

output/casestudy_moby_dick_raw.pdf: src/moby_dick_raw.py
	mv output/casestudy_moby_dick{,_}.pdf
	venv/bin/python $<
	mv output/casestudy_moby_dick.pdf $@
	mv output/casestudy_moby_dick{_,}.pdf

output/casestudy_moby_dick_with_stopwords_raw.pdf: src/moby_dick_raw.py
	mv output/casestudy_moby_dick_with_stopwords{,_}.pdf
	venv/bin/python $<
	mv output/casestudy_moby_dick_with_stopwords.pdf $@
	mv output/casestudy_moby_dick_with_stopwords{_,}.pdf

output/case_study_moby_dick_combined.pdf: output/casestudy_moby_dick.pdf output/casestudy_moby_dick_with_stopwords.pdf
	/Users/andyreagan/tools/perl/kitchentable/pdftile.pl 1 2 .48 3 0 l 8 "" "" output/casestudy_moby_dick.pdf "" output/casestudy_moby_dick_with_stopwords.pdf output/case_study_moby_dick_combined
	open $@

output/case_study_moby_dick_raw_combined.pdf: output/casestudy_moby_dick_raw.pdf output/casestudy_moby_dick_with_stopwords_raw.pdf
	/Users/andyreagan/tools/perl/kitchentable/pdftile.pl 1 2 .48 3 0 l 8 "" "" output/casestudy_moby_dick_raw.pdf "" output/casestudy_moby_dick_with_stopwords_raw.pdf output/case_study_moby_dick_raw_combined
	open $@

all: output/case_study_moby_dick_combined.pdf output/case_study_moby_dick_raw_combined.pdf
