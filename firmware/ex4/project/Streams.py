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

    Product      = project.Product
    code_root    = os.path.join (project.root, '../')

    # -----------------------------------------------------------------
    # These values are included via a #define specified at compile-time
    # -----------------------------------------------------------------
    defines  = Product.DefineValue   ('DEF_SEED', '{def_seed}')

    includes = Product.IncludePaths  (root       = code_root,
                                      paths      = 'include')

    tb_srcs  = Product.Sources       (root       = code_root,
                                      files      = 'src/streams/StreamsTb.cc',
                                      includes   = includes,
                                      defines    = defines)

    syn_srcs = Product.Sources      (root       = code_root,
                                     files      = 'src/streams/StreamsHls.cc',
                                     includes   = includes,
                                     defines    = None)

    build    = Product.Build        (top        = 'doit',
                                     tb         = tb_srcs,
                                     syn        = syn_srcs,
                                     csim_argv  = "",
                                     cosim_argv = "")

    # ------------------------------------
    # The following symbolics are exported to be used in
    # configuration and component name generation
    #     fpga_part fpga_clock and fpga_id
    # ------------------------------------
    fpgas    = [ Product.Fpga ('xcku115-flvb2104-2-i', '6',  None, '6ns'),
                 Product.Fpga ('xcku115-flvb2104-2-i', '5',  None, '5ns') ]

    # --------------------------------------------------------------------------
    # These are the contributes defining the set of components
    #   The Builds and Fpgas are mandatory
    #   The Values contributor makes #define macros available.
    #       This has the advantage of providing these without editting the code.
    #
    # The 'build', 'def_seed',  and 'fpga' act as prefixes for the attributes.
    #
    # Have already encountered the FPGAs attributes
    #     fpga                - The fully Fpga class
    #     fpga_part           - The Fpga part
    #     fpga_clock          - The fpga clock
    #     fpga_unceratinity.  - The fpga clock uncertainity
    #     fpga_id             - User assigned identifier
    #
    # For the Values these attributes are
    #     def_seed
    # -------------------------------------------------------------------------
    contributors = (Product.CtbBuilds ('build', [['stream', build]]),
                    Product.CtbFpgas  ('fpga',                fpgas),
                    Product.CtbValues ('def_seed',          (10,20)))

    # -----------------------------------------------------------------------
    # Construct the configuration file name template to create a unique name.
    #
    # To ensure uniqueness, in general, it must contain a symbolic name
    # from each of the components classes, here Builds, Values, Fpgas.
    # The exception is if the class has only 1 member.
    #
    #  e.g.  products/cfg/2024.2/stream-seed10-6ns.cfg
    #
    # Here is example where adding some text helps add meaning
    # -----------------------------------------------------------------------
    cfg_template = (os.path.join (project.products_root,
                                  'cfg',
                                  '{vitis_version}',
                                  '{build_id}-seed{def_seed}-{fpga_id}.cfg'))

    # -----------------------------------------------
    # Name the component after the configuration file
    # -----------------------------------------------
    cmp_template   = '{cfg_name}'

    components     = Product.Components (contributors = contributors,
                                         cfg_template = cfg_template,
                                         cmp_template = cmp_template)

    package_ip     = Product.Package.Ip (name    = '{cfg_name}',
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
        # Using the defaults names everything after the component
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
