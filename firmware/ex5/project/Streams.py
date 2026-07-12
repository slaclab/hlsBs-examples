#-----------------------------------------------------------------------------
# Title      : hlsBs project descriptor -- ex5 (#include wildcarding + #define values)
#-----------------------------------------------------------------------------
# Description:
# ex5: combine ex3 (#include wildcarding) and ex4 (#define values), producing
# eight components.
#-----------------------------------------------------------------------------
# This file is part of the 'hlsBs-examples'. It is subject to
# the license terms in the LICENSE.txt file found in the top-level directory
# of this distribution and at:
#    https://confluence.slac.stanford.edu/display/ppareg/LICENSE.html.
# No part of the 'hlsBs-examples', including this file, may be
# copied, modified, propagated, or distributed except according to the terms
# contained in the LICENSE.txt file.
#-----------------------------------------------------------------------------

import os


# ------------------------------------------------------------------------------
def get_project_root(project):
    # Accept the default, which is effectively the commented out value
    return None  # os.path.split(os.path.split(__file__)[0])[0]
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
def get_products_root(project):
    # Accept the default, which is effectively the commented out value
    return None  # os.path.join(project.root, 'products')
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
def get_workspace(project):
    # Override the hlsBs default -> put the Vitis workspace in <target>/build/
    return os.path.join(project.root, 'build')
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
def get_products(project):

    # -------------------------------------------------------------------------
    # ex5 combines the ex3 (#include wildcarding) and ex4 (#define value)
    # techniques in a single project. The components are the cartesian product
    # of the seed include files (Files) x the DEF_SEED values (Values) x the
    # FPGAs, demonstrating the "Final Word" claim that the component classes
    # combine in any mix:
    #     1 build x 2 seeds x 2 def_seed values x 2 FPGAs = 8 components
    # -------------------------------------------------------------------------

    Product      = project.Product

    include_path = os.path.join(project.root, '../', 'include')

    testbench    = os.path.join(project.root, '../src/streams/StreamsTb.cc')
    syn          = os.path.join(project.root, '../src/streams/StreamsHls.cc')
    includes     = [ {'paths' : include_path,
                      'type'  : 'rel_path'} ]

    # --------------------------------------------
    # ex3-style: wildcard selecting the Seed files
    # --------------------------------------------
    stream_seeds = os.path.join(include_path, "seeds", "Seed*.hh")

    # -------------------------------------------------------------------
    # Two defines are used together:
    #   STREAM_SEED - ex3-style, #include of a seed file (a relative path)
    #   DEF_SEED    - ex4-style, a #define value that steers the code
    # -------------------------------------------------------------------
    defines      = [ {'name'     : 'STREAM_SEED',   # #include STREAM_SEED
                      'value'    : '{seed_path}',   # value = the seed file
                      'type'     :  'rel_path',     # a relative path
                      'rel_path' : include_path},   # relative to this path
                     {'name'     :    'DEF_SEED',   # #define DEF_SEED
                      'type'     :    'string',     # just a text value
                      'value'    : '{def_seed}'} ]  # value from Values below

    build        = { 'top'       : 'doit',
                     'tb'        : [ { 'files'    : testbench,
                                       'includes' :  includes,
                                       'defines'  :   defines} ],
                     'syn'       : [ { 'files'    :       syn,
                                       'includes' :  includes} ],
                     'csim_argv'  : '',
                     'cosim_argv' : ''}

    fpgas        = [ Product.Fpga('xcku115-flvb2104-2-i', '6',  None, '6ns'),
                     Product.Fpga('xcku115-flvb2104-2-i', '5',  None, '5ns')]

    # -------------------------------------------------------------------------
    # Builds x Files(seed) x Values(def_seed) x Fpgas. Every class prefix
    # ('build', 'seed', 'def_seed', 'fpga') must be unique.
    # -------------------------------------------------------------------------
    components   = (Product.Builds('build', [['stream', build]]),
                    Product.Files ('seed',     stream_seeds),
                    Product.Values('def_seed',      (10, 20)),
                    Product.Fpgas ('fpga',           fpgas))

    # -----------------------------------------------------------------------
    # The configuration path must be unique across every class that has more
    # than one member: here seed_name, def_seed and fpga_id ('build' has a
    # single member, so build_id is constant and only adds meaning).
    #   e.g.  build/stream-Seed1-def10-6ns.cfg
    # -----------------------------------------------------------------------
    cfg_template = (os.path.join(project.root,
                                 'build',
                                 '{build_id}-{seed_name}-def{def_seed}-{fpga_id}.cfg'))

    # -----------------------------------------------
    # Name the component after the configuration file
    # -----------------------------------------------
    cmp_template = '{cfg_name}'


    targets      = [ { 'Components'        :   components,
                       'SourceFiles'       :       'seed',
                       'ConfigurationName' : cfg_template,
                       'ComponentName'     : cmp_template } ]

    package_ip   = Product.Package.Ip(name    = '{cfg_name}',
                                      vendor  = 'SLAC',
                                      version = '1.0.0',
                                      library = 'hls')

    package_output = Product.Package.Output(format    = 'ip_catalog',
                                            syn       = 'false')

    vivado         = Product.Vivado(flow ='syn',     syn_dcp = '1')


    return Product(project = project,
                   targets = targets,
                   package = Product.Package(ip     = package_ip,
                                             output = package_output),
                   vivado  = vivado)
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
def get_ip(project):
    ip = project.Ip(
        dir      =  os.path.join(project.root, 'ip'),
        zip_file = '{cmp_name}',
        # Keep ip/ to just the .zip/.dcp; send the DCP rename journal/log to
        # build/dgn/ (gitignored/cleaned) instead of the default ip/dgn/.
        dgn_dir  = os.path.join(project.root, 'build', 'dgn'),
        family   = ('artix7,kintex7,virtex7,zynq,kintexu,virtexu,kintexuplus,'
                    'virtexuplus,virtexuplusHBM,zynquplus,zynquplusRFSOC,versal'),
    )

    return ip
# ------------------------------------------------------------------------------
