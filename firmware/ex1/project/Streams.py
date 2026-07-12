#-----------------------------------------------------------------------------
# Title      : hlsBs project descriptor -- ex1 (adding multiple FPGAs)
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


def get_project_root(project):
    # -------------------------------------------------------------
    # This is the default. It can be used when the project file
    # is in a directory immediately below the project root. It is
    # shown here just to illustrate it.
    #
    # If the default is acceptable, this method can be omitted
    # or return None. Returning None is preferred since it serves
    # as a visual reminder that it can be set to anything.
    #
    # While the project file directory name is suggested to be
    # 'project/', it is not necessary. To accept the default, the
    # only requirement is that it is in a subdirectory of the
    # project root.
    # -------------------------------------------------------------
    return None  # os.path.split(os.path.split(__file__)[0])[0]
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
def get_products_root(project):
    # ------------------------------------------------------------
    # This is the default, but illustrates that the recommended
    # way is to locate it relative to the project root.
    # ------------------------------------------------------------
    return os.path.join(project.root, 'products')
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
def get_workspace(project):
    # ------------------------------------------------------------
    # Override the hlsBs default: put the Vitis workspace in
    # <target>/build/ to match the build/ + ip/ layout.
    # ------------------------------------------------------------
    return os.path.join(project.root, 'build')
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
def get_products(project):

    Product      = project.Product

    testbench    = os.path.join(project.root, '../src/streams/StreamsTb.cc')
    syn          = os.path.join(project.root, '../src/streams/StreamsHls.cc')
    includes     = ( {'paths' : os.path.join(project.root, '../', 'include'),
                      'type'  : 'rel_path'} )

    # ----------------------------------------------------
    # Note: here the name of the build is packaged with it
    # ----------------------------------------------------
    build       = ( 'stream',
                    { 'top'       : 'doit',
                      'tb'        : [ { 'files'    : testbench,
                                        'includes' :  includes} ],
                      'syn'       : [ { 'files'    :       syn,
                                        'includes' :  includes} ],
                      'csim_argv' : None,
                      'cosim_argv': None} )

    # --------------------------------------------------
    # The following symbolics are exported to be used in
    # configuration and component name generation:
    #     fpga_part, fpga_clock and fpga_id
    # --------------------------------------------------
    fpgas        = [ Product.Fpga('xcku115-flvb2104-2-i', '6',  None, '6ns'),
                     Product.Fpga('xcku115-flvb2104-2-i', '5',  None, '5ns')]

    components   = (Product.Builds('build',  build),
                    Product.Fpgas ('fpga',   fpgas))


    # --------------------------------------------------
    # Configuration file name template.
    # Makes  build/{build_id}-{fpga_id}.cfg
    #  e.g.  build/stream-6ns.cfg
    # --------------------------------------------------
    cfg_template = (os.path.join(project.root,
                                 'build',
                                 '{build_id}-{fpga_id}.cfg'))

    # -----------------------------------------------
    # Name the component after the configuration file
    # -----------------------------------------------
    cmp_template = '{cfg_name}'


    targets      = [ { 'Components'        : components,
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

        # The dcp rename pieces are:
        #    dcp_rename : What to rename it to.
        #                 By default this follows the cmp_name.
        #
        #    dcp_file   : The new file name.
        #                 Default =  '{dcp_rename}'.
        #                 '{cmp_name}' is also permitted.
        #
        #    dgn_dir    : The directory for the journal and log files.
        #                 Default = '{dcp_rename}'.
        #                 '{cmp_name}' is also permitted.
        #
        #    jou_file   : The journal file name.
        #                 Default = '{dcp_name}' - i.e. the dcp file name.
        #                 '{dcp_rename}' or '{cmp_name}' are also permitted.
        #
        #    log_file   : The log file name.
        #                 Default = '{dcp_name}' - i.e. the dcp_file name.
        #                 '{dcp_rename}' or '{cmp_name}' are also permitted.
        #
        # Using the default names everything after the component.
        # -----------------------------------------------------------------

        # ----------------------------------------------------------------
        # The below are all the defaults and can be omitted or set to None.
        # They are just provided here for illustration.
        # ----------------------------------------------------------------
        #dcp_rename = '{cmp_name}',
        #dcp_file   = '{dcp_rename}',

        #dgn_dir    = 'dgn/',
        #jou_file   = '{dcp_name}',
        #log_file   = '{dcp_name}'
    )

    return ip
# ------------------------------------------------------------------------------
