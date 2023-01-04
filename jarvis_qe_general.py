from jarvis.core.kpoints import Kpoints3D
from jarvis.core.atoms import Atoms
from jarvis.io.qe.inputs import QEinfile
from jarvis.io.qe.inputs import GenericInputs
from jarvis.analysis.magnetism import magmom_setup
import warnings


class qe_input:
	def __init__(self, jarvis_struc):
		self.struc=jarvis_struc 
		# I called it jarvis structure because the attributes used in later functions come from jarvis structure 
		# you might be able to get away with ASE or pymatgen since I believe they use the same attributes used in this script but havent tested
		# feel free to change the code and i am sure you wont find much difficulty :)

	 
	@staticmethod
	def get_struc_input(struc_path, struc_type='cif'):
		struc_type=struc_type.lower()
		if struc_type=='cif':
			struc=Atoms.from_cif(struc_path, use_cif2cell=False, get_primitive_atoms=False)
		elif struc_type=='poscar':
			struc=Atoms.from_poscar(struc_path)
		else:
			raise Exception("sorry, the code currently supports 'cif' and 'poscar' formats. Case is ignored!")
		return qe_input(struc)
		
	def prepare_SCF_calc(self, dict_change, init_mag=0.6, hub_val=3):
		sample_SCF_initial={'control': {'calculation': "'scf'", 'restart_mode': "'from_scratch'", 'prefix': None, 'outdir': "'./'", 'tstress': '.true.', 'tprnfor': '.true.', 'pseudo_dir': None, 'verbosity': "'high'"}, 
		'system': {'ibrav': 0, 'nat': None, 'ntyp': None, 'ecutwfc': 45, 'ecutrho': 250, 'occupations': "'smearing'", 'degauss': 0.011, 'nspin': 1, 'lda_plus_u': '.false.', 'lda_plus_u_kind': None}, 
		'electrons': {'diagonalization': "'david'", 'mixing_beta': 0.3, 'conv_thr': '1d-6'}}

		for key0, val0 in dict_change.items():
			for key1, val1 in val0.items():
				sample_SCF_initial[key0][key1]=val1
		if sample_SCF_initial['system']['nspin']==1 and sample_SCF_initial['system']['lda_plus_u']=='.true.':
			warnings.warn("you cannot have spin=1 with magnetization and therefore Hubbards model is not useful")
		if sample_SCF_initial['system']['nspin']==2:
			for i in range(self.struc.num_atoms):
				sample_SCF_initial['system']['starting_magnetization('+str(i+1)+')']=init_mag
	
		if 'lspinorb' in sample_SCF_initial['system'] and sample_SCF_initial['system']['lspinorb']=='.true.':
			sample_SCF_initial['system']['lspinorb']='.true.'
			sample_SCF_initial['system']['noncolin']='.true.'
			sample_SCF_initial['system']['nspin']=4
			warnings.warn("since you intend to perform s*l calculations, this script changes nspin=4 automatically")
			for i in range(self.struc.num_atoms):
				sample_SCF_initial['system']['starting_magnetization('+str(i+1)+')']=init_mag

		elif 'noncolin' in sample_SCF_initial['system'] and sample_SCF_initial['system']['noncolin']=='.true.':
			sample_SCF_initial['system']['lspinorb']='.true.'
			sample_SCF_initial['system']['noncolin']='.true.'
			sample_SCF_initial['system']['nspin']=4
			warnings.warn("since you intend to perform s*l calculations, this script changes nspin=4 automatically")
			for i in range(self.struc.num_atoms):
				sample_SCF_initial['system']['starting_magnetization('+str(i+1)+')']=init_mag
			
		magnetic_atoms=magmom_setup.MagneticOrdering(self.struc).get_mag_ions()
		if sample_SCF_initial['system']['lda_plus_u']=='.true.':
			mag_i=[]
			for i, el in enumerate(self.struc.elements):
				for j in magnetic_atoms:
					if el==j:
						mag_i.append(i+1)
						sample_SCF_initial['system']['Hubbard_U('+str(i+1)+')']=hub_val
					
		if sample_SCF_initial['control']['prefix']==None:
			sample_SCF_initial['control']['prefix']="'{formula}'".format(formula=self.struc.composition.reduced_formula)		
		
		return sample_SCF_initial
		
	def obtain_kpoints(self, calc_type: str, kpoint_grid=20, line_density=20):
		calc_type=calc_type.lower()
		if calc_type=='scf':
			kpts=Kpoints3D().automatic_length_mesh(
		lattice_mat=self.struc.lattice_mat, length=length
		)
		elif calc_type=='nscf':
			kpts=Kpoints3D().kpath(atoms=self.struc, line_density=line_density)
		#elif calc_type=='hi_sym_path':
		#	kpts=Kpoints3D().high_kpath(atoms=struc)
		### this is something I would like to work on in the future for band.x 
		### you need to use high symmetry points under crystal_b type of kpoints
		else:
			raise Exception("sorry, you can only enter 'scf' or 'nscf' as your calculation type. Case is ignored!")
		return kpts



if __name__=='__main__':
	MnCo2Si=qe_input.get_struc_input('MnCo2Si.cif')

	#MnCo2Si_kpts=qe_input.get_struc_input('MnCo2Si.cif').obtain_kpoints('nscf')
	kpts=MnCo2Si.obtain_kpoints('nscf')
	dict_change={'system':{'nspin': 2, 'lda_plus_u': '.true.', 'lspinorb': '.true.', 'noncolin': '.true.'},
	'control':{'calculation': "'nscf'"}}
	sample_SCF_updated=MnCo2Si.prepare_SCF_calc(dict_change)
	
	#pseudo_dir='C:\\your\\PSP\\path'
	pseudo_dir='C:\\your\\PSP\\path'
	qe = QEinfile(MnCo2Si.struc, kpts, psp_dir=pseudo_dir, input_params=sample_SCF_updated)
	qe.write_file("scf.in")

