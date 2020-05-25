test: simple_anim.mdl main.py matrix.py mdl.py display.py draw.py gmath.py
	python3 main.py simple_anim.mdl

clean:
	rm -rf __pycache__
	rm -rf ply/__pycache__
	rm *pyc *out parsetab.py

clear:
	rm -rf __pycache__
	rm -rf ply/__pycache__
	rm *pyc *out parsetab.py *ppm *png
