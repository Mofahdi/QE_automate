# QE_automate
## Motivation
Generate Qunatum Espresso (QE) input files more efficiently with less human intervention.
## How to use the script:
* The name of the script that can read structures and generate Quantum Espresso input files is "jarvis_qe_general.py"
1. You have to provide the path to your structure in the static method 'get_struc_input'. The script can only read 'CIF' or 'POSCAR' formats 
   * you could also provide read or provide the structure as an attribute through a different method, but it must be converted to jarvis Atoms 
2. After providing the structure, the kpoints must be obtained and must be inputted in "QEinfile". Two types of kpoints are available in the script so far:
   * 'scf': homogeneous monkhorst-pack kpoints
   * 'nscf': explicit listing of special equidistant kpoints around the gamma point
   * I plan on adding a third option for crystal_b kpoints in which I have to provide the high-symmetry path to obtain the band structure
3. you have to download the pseudopotentials and provide the path to "QEinfile". If you don't have the pseudopotentials downloaded already, you can install them from the script 'get_psp.py'.
4. you have to provide the dictionary of your "system" and "control" cards. The script will output "ATOMIC_POSITIONS" and "CELL_PARAMETERS" automatically.

* An example of the above instructions can be seen at the end of the script

Note: I usually use this script to perform "vc-relax", "scf", and "nscf" calculations. If you need to run calculations with ph.x, matdyn.x, or some other executables, I am afraid to say that this script is not developed enough. However, I plan on writing such a script in the future!

## Required Packages
* The script assumes that you had previously installed the following python packages <br />
<code> jarvis-tools==2022.9.16</code><br />

* I believe installing the exact version is not necessary, so you can install other versions that are different from the above and still be able to run the script!

<dl>
<dt><code>jarvis-tools</code></dt>
<dd>The method I implemented to install jarvis-tools is through running the following in the command line:<br />
<code> pip install -U jarvis-tools </code>

for more information on how to install jarvis-tools with the source code, please use this [link](https://github.com/usnistgov/jarvis)</dd>
</dl>

## Usage and Development
* to copy this repository to your own computer please run the following in the command line: <br />
<code>git clone https://github.com/Mofahdi/QE_automate </code>

* if you have any questions or would like to see more functionalities in this script, please do not hesistate to email me at malfahdi@email.sc.edu
* also please consider reading my published work in Google Scholar using this [link](https://scholar.google.com/citations?user=5tkWy4AAAAAJ&hl=en&oi=ao) thank you :)
