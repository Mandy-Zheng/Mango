test: mdl/final0.mdl mdl/final1.mdl mdl/final2.mdl mdl/final3.mdl mdl/final4.mdl mdl/final5.mdl mdl/final6.mdl main.py matrix.py mdl.py display.py draw.py gmath.py
	python3 main.py mdl/final0.mdl
	python3 main.py mdl/final1.mdl
	python3 main.py mdl/final2.mdl
	python3 main.py mdl/final3.mdl
	python3 main.py mdl/final4.mdl
	python3 main.py mdl/final5.mdl
	python3 main.py mdl/final6.mdl


clean:
	rm -rf __pycache__
	rm -rf ply/__pycache__
	rm *pyc *out parsetab.py

clear:
	rm -rf __pycache__
	rm -rf ply/__pycache__
	rm *pyc *out parsetab.py anim/*ppm anim/*png
