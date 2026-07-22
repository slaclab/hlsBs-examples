import os

# ------------------------------------------------------------------------------
# Accepting the default directory layout so no get_project_root,_workspace,etc
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
def get_products (project) :

    Product   = project.Product
    code_root = os.path.join (project.root, '../')

    includes  = Product.IncludePaths (root      =  code_root,
                                      paths     ='include')

    tb_srcs   = Product.Sources      (root      =  code_root,
                                      files     = 'src/streams/StreamsTb.cc',
                                      includes  = includes,
                                      defines   = None)

    syn_srcs  = Product.Sources      (root      =  code_root,
                                      files     = 'src/streams/StreamsHls.cc',
                                      includes  = includes,
                                      defines   = None)

    build     = Product.Build       (top        =   'doit',
                                    tb         =  tb_srcs,
                                    syn        = syn_srcs,
                                    csim_argv  = "",
                                    cosim_argv = "")

    fpgas    = [ Product.Fpga ('xcku115-flvb2104-2-i', '6',  None, '6ns'),
                 Product.Fpga ('xcku115-flvb2104-2-i', '5',  None, '5ns')]

    # ----------------------------------------------------------------
    # Create 4 components, 2 different builds, paired with the 2 Fpgas
    #    streamA-6ns streamA-5ns
    #    streamB-6ns streamB-5ns
    #
    # Note: the 'build' and 'fpga' strings are the prefix of the
    #       constructed logical names.
    #
    #       See cfg_template which includes {build_id} and {fpga_id}
    #       The 'build' and 'fpga' prefixes are those strings.
    # ----------------------------------------------------------------
    contributors = (Product.CtbBuilds ('build', [['streamA', build],
                                                 ['streamB', build]]),
                    Product.CtbFpgas  ( 'fpga',               fpgas))

    cfg_template = (os.path.join (project.products_root,
                                  'cfg',
                                  '{vitis_version}',
                                  '{build_id}-{fpga_id}.cfg'))

    cmp_template = '{cfg_name}'

    components   = Product.Components (contributors = contributors,
                                       cfg_template = cfg_template,
                                       cmp_template = cmp_template)

    package_ip   = Product.Package.Ip (name    = '{cfg_name}',
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
        zip_file = '{cmp_name}',
        family   = ('artix7,kintex7,virtex7,zynq,kintexu,virtexu,kintexuplus,'
                    'virtexuplus,virtexuplusHBM,zynqplus,zynquplusRFSOC,veral'),

        # The dcp rename pieces are
        #    dcp_rename : What to rename it to
        #                 By default this follows the cmp_name
        #
        #    dcp_file   : The new file name
        #                 Befault =  '{dcp_rename}'
        #                 '{cmp_name} is also permitted
        #
        #    dgn_dir    : The directory for the journal and log files
        #                 Default = '{dcp_rename}'
        #                 '{cmp_name} is also permitted
        #
        #    jou_file   : The journal file name
        #                 Default = '{dcp_name}' - i.e. the dcp file name
        #                 '{dcp_rename}' or '{cmp_name}' are also permitted
        #
        #    log_file   : The log file name
        #                 Default = '{dcp_name}' - i.e. the dcp_file name
        #                 '{dcp_rename}' or '{cmp_name}' are also permitted
        #
        # Using the default names everything after the component
        # -----------------------------------------------------------------

        # ----------------------------------------------------------------
        # The below are all the defaults and can be omitted or set to None
        # The are just provided here for illustration
        # ----------------------------------------------------------------
        #dcp_rename = '{cmp_name}',
        #dcp_file   = '{dcp_rename}',

        #dgn_dir    = 'dgn/',
        #jou_file   = '{dcp_name}',
        #log_file   = '{dcp_name}'
    )

    return ip
# ------------------------------------------------------------------------------
