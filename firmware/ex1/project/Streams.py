#-----------------------------------------------------------------------------
# Title      : hlsBs project descriptor -- ex0 (the basics)
#-----------------------------------------------------------------------------
# Description:
# ex1: one build across two FPGAs (clocks), producing two components.
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

def get_project_root (project) :
    # -------------------------------------------------------------
    # This is the default.  It can be used  when the project file
    # is in a directory immediately below the project root. It is
    # shown here just to illustrate it.
    #
    # If the default is acceptable, this method can be omitted
    # or return None.  Returning None is preferred since it serves
    # a visual reminder that it can be set to anything.
    #
    # While the project file directory name is suggested to be
    # 'project/', it is not necessary. To accept the default, the
    # only requirement is that it is in a subdirectory of the
    # project root.
    # -------------------------------------------------------------
    return os.path.split (os.path.split (__file__)[0])[0]
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
def  get_products_root (project) :
    # ------------------------------------------------------------
    # This is the default, but illustrates the recommended way is
    # locate it relative to the project root.
    # ------------------------------------------------------------
    return os.path.join (project.root, 'products')
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
def get_build_root (project) :
    # ------------------------------------------------------------
    # This is the default, but illustrates the recommended way is
    # locate it relative to the products_root
    # ------------------------------------------------------------
    return os.path.join (project.products_root, 'build')
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
def get_workspace (project) :
    # ------------------------------------------------------------
    # This is the default, but illustrates the recommended way is
    # locate it relative to the build root.
    # ------------------------------------------------------------
    return os.path.join (project.build_root, 'ws', '{vitis.version}')
# ------------------------------------------------------------------------------



# ------------------------------------------------------------------------------
def get_products (project) :

    Product       = project.Product

    code_root     = os.path.join (project.root, '../')
    includes      = Product.IncludePaths (code_root, 'include')

    tb_srcs       = Product.Sources (root     = code_root,
                                     files    = 'src/streams/StreamsTb.cc',
                                     includes = includes,
                                     defines  = None)

    syn_srcs      = Product.Sources (root     = code_root,
                                     files    = 'src/streams/StreamsHls.cc',
                                     includes = includes,
                                     defines  = None)

    # --------------------------------------------------------------------------
    # Defines how to build the HLS test bench, synthesis and cosim.
    # --------------------------------------------------------------------------
    build         = Product.Build  (id          = 'streams',
                                    top         = 'doit',
                                    tb          = tb_srcs,
                                    syn         = syn_srcs,
                                    csim_argv   = "",
                                    cosim_argv  = "")

    # ------------------------------------
    # The following symbolics are exported to be used in
    # configuration and component name generation
    #     fpga_part fpga_clock and fpga_id
    # ------------------------------------
    fpgas        = [ Product.Fpga ('6ns', 'xcku115-flvb2104-2-i', '6',  None),
                     Product.Fpga ('5ns', 'xcku115-flvb2104-2-i', '5',  None)]

    contributors = Product.Contributors (Product.CtbBuilds ('build',  build),
                                         Product.CtbFpgas  ('fpga',   fpgas))


    # ------------------------------=--------------------
    # Configuration file name template
    # Makes  project.cfg_root/{build.id}-{fpga.id}.cfg
    #  e.g.  <root>/products/build/cfg/2024.2/streams.cfg
    # ---------------------------------------------------
    cfg_template = Product.CfgTemplate (prefix   = 'cfg',
                                        template = '{build.id}-{fpga.id}.cfg')

    # -----------------------------------------------
    # Name the component after the configuration file
    # -----------------------------------------------
    cmp_template  = Product.CmpTemplate ('cmp', '{cfg.name}')

    components    = Product.Components (contributors = contributors,
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
                                  'ip', '{vitis.version}'),

        # ---------------------------------------------------
        # While None or an explicit name can be used
        # {cmp.name} is the only symbolic that is recognized
        # --------------------------------------------------
        zip_file = '{cmp.name}',

        family   = ('artix7,kintex7,virtex7,zynq,kintexu,virtexu,kintexuplus,'
                    'virtexuplus,virtexuplusHBM,zynqplus,zynquplusRFSOC,versal'),

        # The dcp rename pieces are
        #    dcp_rename : What to rename it to
        #                 By default this follows the cmp.name
        #
        #    dcp_file   : The new file name
        #                 Befault =  '{dcp_rename}'
        #                 '{cmp.name} is also permitted
        #
        #    dgn_dir    : The directory for the journal and log files
        #                 Default = '{dcp.rename}'
        #                 '{cmp.name} is also permitted
        #
        #    jou_file   : The journal file name
        #                 Default = '{dcp.name}' - i.e. the dcp file name
        #                 '{dcp.rename}' or '{cmp.name}' are also permitted
        #
        #    log_file   : The log file name
        #                 Default = '{dcp.name}' - i.e. the dcp_file name
        #                 '{dcp.rename}' or '{cmp.name}' are also permitted
        #
        # Using the defaults names everything after the component
        # -----------------------------------------------------------------

        # ----------------------------------------------------------------
        # The below are all the defaults and can be omitted or set to None
        # The are just provided here for illustration
        # ----------------------------------------------------------------
        dcp_rename = '{cmp.name}',
        dcp_file   = '{cmp.name}',

        dgn_dir    =  os.path.join (project.build_root, 'ip', 'dgn', '{vitis.version}'),
        jou_file   = '{dcp.name}',
        log_file   = '{dcp.name}'
    )

    return ip
# ------------------------------------------------------------------------------
