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
    return None
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
def get_products_root(project):
    # Accept the default, which is effectively the commented out value
    return None
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
def get_workspace(project):
    # Override the hlsBs default -> put the Vitis workspace in <target>/build/
    return None
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

    Product   = project.Product
    code_root     = os.path.join (project.root, '../')
    include_path  = os.path.join (code_root,   'include')
    includes      = Product.IncludePaths (root  = None,
                                          paths = include_path)

    # --------------------------------------------------------------------
    # Two defines are used together:
    #   STREAM_SEED - ex3-style, #include of a seed file (a relative path)
    #   DEF_SEED    - ex4-style, #define value, for an immediate seed
    # --------------------------------------------------------------------
    defines      = ( Product.IncludeFile ('STREAM_SEED',
                                          '{seed.path}',
                                          include_path),

                     Product.DefineValue ('DEF_SEED',
                                          '{def.value}') )

    tb_srcs  = Product.Sources (root     = code_root,
                                files    = 'src/streams/StreamsTb.cc',
                                includes = includes,
                                defines  = defines)

    syn_srcs = Product.Sources (root     = code_root,
                                files    = 'src/streams/StreamsHls.cc',
                                includes = includes,
                                defines  = None)

    build    = Product.Build   (id         = 'stream',
                                top        = 'doit',
                                tb         =  tb_srcs,
                                syn        =  syn_srcs,
                                csim_argv  = '--ntests=5',
                                cosim_argv = '--ntests=10')

    fpgas    = Product.Fpga('5ns', 'xcku115-flvb2104-2-i', '6',  None)


    # -------------------------------------------------------------------------
    # Builds x Files(seed) x Values(def_seed) x Fpgas. Every class prefix
    # ('build', 'seed', 'def_seed', 'fpga') must be unique.
    # -------------------------------------------------------------------------
    stream_seeds = os.path.join (include_path, "seeds", "Seed*.hh")

    values       = ( Product.Value ('D10', 10),
                     Product.Value ('D20', 20) )

    contributors = Product.Contributors (
                           Product.CtbBuilds('build',           build),
                           Product.CtbFpgas ('fpga',            fpgas),
                           Product.CtbFiles ('seed',     stream_seeds),
                           Product.CtbValues('def',            values))

    # -----------------------------------------------------------------------
    # The configuration path must be unique across every class that has more
    # than one member: here seed_name, def_seed and fpga_id ('build' has a
    # single member, so build_id is constant and only adds meaning).
    #   e.g.  build/stream-Seed1-def10-6ns
    # -----------------------------------------------------------------------
    cfg_template = Product.CfgTemplate ('cfg',
                                        '{build.id}-{seed.name}-{def.id}-{fpga.id}')


    # -----------------------------------------------
    # Name the component after the configuration file
    # -----------------------------------------------
    cmp_template = Product.CmpTemplate ('cmp', '{cfg.name}')


    components   = Product.Components (contributors = contributors,
                                       cfg_template = cfg_template,
                                       cmp_template = cmp_template)

    package_ip   = Product.Package.Ip(name    = '{cfg.name}',
                                      vendor  = 'SLAC',
                                      version = '1.0.0',
                                      library = 'hls')

    package_output = Product.Package.Output(format    = 'ip_catalog',
                                            syn       = 'false')

    vivado         = Product.Vivado(flow ='syn',     syn_dcp = '1')


    return Product(project    = project,
                   components = components,
                   package    = Product.Package(ip     = package_ip,
                                                output = package_output),
                   vivado     = vivado)
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
def get_ip(project):
    ip = project.Ip \
    (
        #dir      =  os.path.join (project.products_root,
        #                          'ip', '{vitis_version}'),
        #zip_file = '{cmp.name}',

        family   = ('artix7,kintex7,virtex7,zynq,kintexu,virtexu,kintexuplus,'
                    'virtexuplus,virtexuplusHBM,zynquplus,zynquplusRFSOC,versal'),

        # The dcp rename pieces are
        #    dcp_rename : What to rename it to
        #                 By default this follows the cmp.name
        #
        #    dcp_file   : The new file name
        #                 Befault =  '{dcp_rename}'
        #                 '{cmp.name} is also permitted
        #
        #    dgn_dir    : The directory for the journal and log files
        #                 Default = '{dcp_rename}'
        #                 '{cmp.name} is also permitted
        #
        #    jou_file   : The journal file name
        #                 Default = '{dcp_name}' - i.e. the dcp file name
        #                 '{dcp_rename}' or '{cmp.name}' are also permitted
        #
        #    log_file   : The log file name
        #                 Default = '{dcp_name}' - i.e. the dcp_file name
        #                 '{dcp_rename}' or '{cmp.name}' are also permitted
        #
        # Using the defaults names everything after the component
        # -----------------------------------------------------------------

        # ----------------------------------------------------------------
        # The below are all the defaults and can be omitted or set to None
        # The are just provided here for illustration
        # ----------------------------------------------------------------
        #dcp_rename = '{cmp.name}',
        #dcp_file   = '{dcp_rename}',

        #dgn_dir    = 'dgn/',
        #jou_file   = '{dcp_name}',
        #log_file   = '{dcp_name}'
    )

    return ip
# ------------------------------------------------------------------------------
