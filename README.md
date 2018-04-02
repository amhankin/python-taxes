# python-taxes
by David Moore

Python code for computing Federal and CA state taxes.

Licensed under the GNU GPL v2.0. Please contact me if you are planning to
use or redistribute this code for any serious purpose.

Disclaimer: This code comes with no warranty. It will probably not work
for your tax return or specific circumstances without modification. If you
rely on this, you will probably be audited by the IRS. I am not a tax
accountant.

See `example_*.py` files in each year's subdirectory.

# Notes on forked code
by Aaron Hankin

* Added input for deductions for student Loan interest
* Added CO 104 state income tax return form
	* Added C0 104us use tax form (for large untaxed online purcahses that
	  require sales tax)

## Instillation Instructions with conda
I have included a quick instillation instructions below. You will first create
a python 2.7 environment using conda if you do not already have one. Following
that, you can clone the code from the repository. 
```
conda create -n py27 python=2.7 anaconda
source activate py27
cd <target-folder>
git clone git@github.com:amhankin/python-taxes.git
```

To use the code, you will have to add this year's code to your python path.
```
import sys
sys.path.append('<target-folder>/python-taxes/2017/')
```
