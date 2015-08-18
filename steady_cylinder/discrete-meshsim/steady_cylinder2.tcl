#
#   Copyright (c) 2015 Stanford University
#   All rights reserved.  
#
#   Portions of the code Copyright (c) 2009-2012 Open Source Medical Software Corporation
#
#  This script requires the following files:
#     solver.inp
#  and should be sourced interactively from SimVascular
#

solid_setKernel -name Discrete
mesh_setKernel -name MeshSim
set gOptions(meshing_kernel) MeshSim
set gOptions(meshing_solid_kernel) Discrete

set num_procs ""
set selected_LS ""

# shared functions
source ../../common/executable_names.tcl

# custom functions
source cylinder_create_model_discrete.tcl
source steady_cylinder_create_mesh_meshsim.tcl

# run example
source ../generic/steady_cylinder_generic2.tcl
