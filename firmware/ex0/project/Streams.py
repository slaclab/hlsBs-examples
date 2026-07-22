import os

# ----------------------------------------------------------------------------
# For this simple example, the default output directories have been accepted.
# See ex1 for how to customize the placement of the following directories:
#    what                Python method                   Environment Variable
#    -------------    ---------------------------------  --------------------
#    project_root     def get_project_root  (project)    <none>
#    products_root    def get_products_root (project)    HLSBS_PRODUCTS
#    build_root       def get_build_root    (project)    HLSBS_BUILD
#    workspace        def get_workspace     (project)    HLSBS_WORKSPACE
#    cfg_root         def get_cfg_root      (project)    HLSBS_CFG
#
# The default is
#    <project_root>/products/build/ws/<vitis_version>
#                                 cfg/<vitis_version>
#                                  ip/<vitis_version>
#
# The defaults are also accepted for the ip directory (.dcp & .zip files)
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
def get_products (project) :

    Product       = project.Product
    code_root     = os.path.join (project.root, '../')

    includes      = Product.IncludePaths (root  = code_root,
                                          paths = 'include')

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
    build         = Product.Build  (top         = 'doit',
                                    tb          = tb_srcs,
                                    syn         = syn_srcs,
                                    csim_argv   = "",
                                    cosim_argv  = "")

    # ------------------------------------------------------------------------
    # Define the Fpga or Fpgas. This may a single, list or tuple
    # ------------------------------------------------------------------------
    fpga         =  Product.Fpga ('xcku115-flvb2104-2-i', '6',  None, 'f0')

    # -----------------------------------------------------
    # The contributors are determine the set of commponents
    # The Builds and Fpgas contributors are mandatory.
    # As the plural form is meant to suggest, there can be
    # more than one as in the Fpgas, but Builds can consist
    # of multiple.
    # -----------------------------------------------------
    contributors = ( Product.CtbBuilds ('build', ['streams', build]),
                     Product.CtbFpgas  ('fpga',               fpga) )

    # --------------------------------------------------
    # Configuration file name template
    # Generates the name of the configuration file.
    # Here:  <cfg_root>/{build_id}.cfg
    # Using the default value of cfg_root this is
    #        <root>/products/build/cfg/2024.2/streams.cfg
    # --------------------------------------------------
    cfg_template = os.path.join (project.cfg_root, '{build_id}.cfg')

    # -----------------------------------------------
    # Name the component after the configuration file
    # -----------------------------------------------
    cmp_template = '{cfg_name}'

    # -------------------------------------------------------------
    # The fully specified components are the component contributors
    # bound to their configuration and component names
    #
    # As the plural 'targets' suggestions this may be a
    # single, list or tuple.
    # --------------------------------------------------
    components    = Product.Components (contributors = contributors,
                                        cfg_template = cfg_template,
                                        cmp_template = cmp_template)

    # --------------------------------------------------
    # Fill out the package IP description
    # The version can also be the symbolic {git_tag}
    # NOTE: Other suggestions are welcomed. For example
    #       a command line parameter (ip_version?) could
    #       be useful.
    # --------------------------------------------------
    package_ip   = Product.Package.Ip (name    = '{cfg_name}',
                                       vendor  = 'SLAC',
                                       version = '1.0.0',
                                       library = 'hls')

    # -------------------------------------------------
    # Is there any reason these could not be defaulted?
    # -------------------------------------------------
    package_output = Product.Package.Output (format = 'ip_catalog',
                                             syn    = 'false')

    vivado         = Product.Vivado  (flow ='syn',     syn_dcp = '1')


    # -----------------------------------------------------
    # As the plural 'get_products' suggests this may return
    # either a single, list or tuple of products.
    # -----------------------------------------------------
    return Product (project    = project,
                    components = components,
                    package    = Product.Package (ip     = package_ip,
                                                  output = package_output),
                    vivado     = vivado)
# ------------------------------------------------------------------------------
