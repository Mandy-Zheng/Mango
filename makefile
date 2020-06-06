test: final0.mdl final1.mdl final2.mdl final3.mdl final4.mdl final5.mdl final6.mdl main.py matrix.py mdl.py display.py draw.py gmath.py
	python3 main.py final0.mdl
	python3 main.py final1.mdl
	python3 main.py final2.mdl
	python3 main.py final3.mdl
	python3 main.py final4.mdl
	python3 main.py final5.mdl
	python3 main.py final6.mdl


clean:
	rm -rf __pycache__
	rm -rf ply/__pycache__
	rm *pyc *out parsetab.py

clear:
	rm -rf __pycache__
	rm -rf ply/__pycache__
	rm *pyc *out parsetab.py *ppm *png
