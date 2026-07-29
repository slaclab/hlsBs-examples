#-----------------------------------------------------------------------------
# Title      : hlsBs project descriptor -- ex0 (the basics)
#-----------------------------------------------------------------------------
# Description:
# ex3: wildcard #include of 2 seed files (Product.Files) and 2 Fpgas,
#      producing four components.
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
def get_project_root (project) :
    # Accept the default which is effectively the commented out value
    return None # os.path.split (os.path.split (__file__)[0])[0]
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
def  get_products_root (project) :
    # Accept the default which is effectively the commented out value
    return None # os.path.join (project.root, 'products')
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
def get_workspace (project) :
    # Accept the default which is effectively the commented out value
    return None # os.path.join (project.products_root, 'ws', '{vitis_version}')
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
def get_products (project) :

    Product       = project.Product

    code_root     = os.path.join (project.root, '../')
    include_path  = os.path.join (code_root,   'include')
    includes      = Product.IncludePaths (root  = None,
                                          paths = include_path)

    # --------------------------------------------
    # Define the wildcard to select the Seed files
    # -------------------------------------------
    stream_seeds = os.path.join (include_path, "seeds", "Seed*.hh")

    # --------------------------------------------
    # These are included via a special #define
    # --------------------------------------------
    defines       = Product.IncludeFile ('STREAM_SEED',
                                         '{seed.path}',
                                          include_path)

    tb_srcs       = Product.Sources (root     = code_root,
                                     files    = 'src/streams/StreamsTb.cc',
                                     includes = includes,
                                     defines  = defines)

    syn_srcs      = Product.Sources (root     = code_root,
                                     files    = 'src/streams/StreamsHls.cc',
                                     includes = includes,
                                     defines  = defines)

    build        = Product.Build   (top        =    'doit',
                                    tb         =   tb_srcs,
                                    syn        =  syn_srcs,
                                    csim_argv  =        "",
                                    cosim_argv =        "")

    # ------------------------------------
    # The following symbolics are exported to be used in
    # configuration and component name generation
    #     fpga.part fpga.clock and fpga.id
    # ------------------------------------
    fpgas        = [ Product.Fpga ('xcku115-flvb2104-2-i', '6',  None, '6ns'),
                     Product.Fpga ('xcku115-flvb2104-2-i', '5',  None, '5ns')]

    # --------------------------------------------------------------------------
    # The component is constructed for the build, the seed files, and FPGAs
    # The 'build', 'seed',  and 'fpga' act as prefixes for the attributes.
    #
    # Have already encountered the FPGAs attributes
    #     fpga                - The fully Fpga class
    #     fpga.part           - The Fpga part
    #     fpga.clock          - The fpga clock
    #     fpga.unceratint     - The fpga clock uncertainity
    #     fpga.id             - User assigned identifier
    #
    # For the files these attributes are
    #     seed.path          - Full path to the include file
    #     seed.dir           - The directory of the include file
    #     seed.name          - The file name of include file
    #     seed.ext           - The file extension of the inclde file
    # The 'defines' uses {seed.path} as the logical symbol for the include file
    #
    # Note that the Product.Builds,Files,Fpgas can be specified multiple times
    # as long as a unique prefix is given for each instance.
    # -------------------------------------------------------------------------
    contributors = Product.Contributors (
                           Product.CtbBuilds ('build', [['stream', build]]),
                           Product.CtbFpgas  ('fpga',                fpgas),
                           Product.CtbFiles  ('seed',         stream_seeds))


    # -----------------------------------------------------------------------
    # Construct the configuration file name template to create a unique name.
    #
    # To ensure uniqueness, in general, it must contain a symbolic name
    # from each of the components classes, here Builds, Files, Fpgas.
    # The exception is if the class has only 1 member.
    #
    # In addition to being unique, it is good to select a name giving an
    # idea of what the component is all about. Here 'build.id' and 'fpga.id'
    # are specified in this file.  The 'seed.name' is taken from the file
    # name of the compile-time included files - chose wisely.
    #
    # NOTE: Text can also be included to help with clarity.
    #       B{build.id}-I{seed.name}-F{fpga.id}
    #
    #  e.g.  products/cfg/2024.2/streamA--Seed1-6ns.cfg
    # -----------------------------------------------------------------------
    cfg_template = Product.CfgTemplate ('cfg',
                                        '{build.id}-{seed.name}-{fpga.id}')

    # -----------------------------------------------
    # Name the component after the configuration file
    # -----------------------------------------------
    cmp_template = Product.CmpTemplate ('cmp', '{cfg.name}')


    components   = Product.Components (contributors = contributors,
                                       cfg_template = cfg_template,
                                       cmp_template = cmp_template)

    package_ip   = Product.Package.Ip (name    = '{cfg.name}',
                                       vendor  = 'SLAC',
                                       version = '1.0.0',
                                       library = 'hls')

    package_output = Product.Package.Output (format    = 'ip_catalog',
                                             syn       = 'false')

    vivado         = Product.Vivado  (flow ='syn',     syn_dcp = '1')


    return Product (project    = project,
                    components = components,
                    package    = Product.Package (ip     = package_ip,
                                                  output = package_output),
                    vivado     = vivado)
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
def get_ip (project) :
    ip = project.Ip \
    (
        dir      =  os.path.join (project.products_root,
                                  'ip', '{vitis_version}'),
        zip_file = '{cmp.name}',
        family   = ('artix7,kintex7,virtex7,zynq,kintexu,virtexu,kintexuplus,'
                    'virtexuplus,virtexuplusHBM,zynqplus,zynquplusRFSOC,veral'),

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
