test: final0.mdl final1.mdl final2.mdl final3.mdl final4.mdl final5.mdl final6.mdl main.py matrix.py mdl.py display.py draw.py gmath.py
	python3 main.py final6.mdl

clean:
	rm -rf __pycache__
	rm -rf ply/__pycache__
	rm *pyc *out parsetab.py

clear:
	rm -rf __pycache__
	rm -rf ply/__pycache__
	rm *pyc *out parsetab.py *ppm *png
