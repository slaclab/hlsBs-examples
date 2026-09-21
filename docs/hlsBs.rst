hlsBs Examples and Tutorial
===========================

This tutorial shows how to use the HLS build and development system tools
using 5 example HLS projects of increasing complexity, cleverly labeled
*ex0, ex1, ex2, e3, ex4, ex5, ex6*.

.. list-table:: hlsBs Examples
   :header-rows: 1

   * - Ex
     - Demonstrates
   * - ex0
     - The basics
   * - ex1
     - ex0, targeting 2 FPGAs
   * - ex2
     - Uses 2 build descriptions and 2 FPGAs
   * - ex3
     - Generating components by wildcarding include files
   * - ex4
     - Generating components with #defines values
   * - ex5
     - Combines ex3's includes + ex4's defines
   * - ex6
     - How to quickly modify command line parameters

..

Getting Started
---------------

The next few sections attempt to provide some context and a few details.
For the *let's just try it crowd*, skip to
:ref:`Tutorial - Preliminaries <tutorial_preliminaries-label>` or even
further to
:ref:`Tutorial - The Annotated Version <tutorial_annotated_version-label>`,
then come back to here.  Documents like this are rarely linearly read.

Where is the code?
~~~~~~~~~~~~~~~~~~

The code is in the
`hlsBs-examples <https://github.com/slaclab/hlsBs-examples>`_ repository. It
uses `ruckus <https://github.com/slaclab/ruckus>`_ as a submodule, so specify
*\-\-recursive* when cloning it.

Vitis IDE/GUI Compatibility
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**hlsBs** is designed to be compatible with the Vitis GUI/IDE. The
various steps may be mixed and matched, using whichever is the most
convenient or appropriate.

About the GUI
^^^^^^^^^^^^^
While the Vitis IDE/GUI has usability issues, it does have some nice features.
It is very cautious, which means sometimes unnecessary and time-consuming
steps are repeated, *just to be safe*.

Since **hlsBs** is a command line implementation of the steps found in the
IDE/GUI, for those new to HLS and depending on your personal style, the GUI
could be a reasonable starting point, a place to *learn the ropes*. Once
comfortable, the workflow of **hlsBs** will be recognizable,

Besides being able to script operations and streamlining common operations,
**hlsBs** deals with multi-component projects better than the GUI. Here
multi-components arise from

- Making tweaks to the code/pragmas to study resource/performance trade-offs.
- A chain of FPGAs, where each receives data from the previous with different
  HLS processing on each FPGA in the chain.


The GUI has a very nice facility to compare multiple components of the
resource/performance trade-off type. Even if **hlsBs** is used to produce
the output products, the GUI can be very helpful in comparing them.


For More Information
~~~~~~~~~~~~~~~~~~~~

This tutorial is just a starting point. See the
`hlsBs Reference Manual <https://github.com/slaclab/ruckus>`_ for
a more complete description of all of **hlsBs**'s capabilities. **hlsBs**
is more than a fancy 'make', it is meant to aid in the development of
HLS code, catering to specific nuances and common usage patterns.


The 30,000ft / 9144m look at **hlsBs**
--------------------------------------

This illustrates a typical **hlsBs** workflow, covering the initial setup
and commonly used commands. Don't worry if some seems mysterious; that's
for the rest of this document.


Setup - Overview
~~~~~~~~~~~~~~~~

The following need only be done one-time at each login. It

.. code-block:: bash

   $ bash              # Spawn a clean shell
   $ hlsToolChain      # Define the site specific search path for Vitis version settings script
   $ hlsBs-examples    # Setup the hlsBs examples tutorial, project specific
                       # User written projects would have something similar
   $ hlsVersion 2024.2 # Select Vitis Version 2024.2, uses the path established by hlsToolChain
   $ exSelect ex0      # Select the ex0 project, relevant because there are multiple examples

.. note::

   To make the **hlsBs**  commands available to the shell. the **hlsBs**
   setup script, *setup_hls.sh* located in *hlsBs/scripts* subdirectory within
   `ruckus <https://github.com/slaclab/ruckus>`_, must be sourced.

   The *hlsBs* setup script can be sourced either

   - at shell login

     - there is nothing project specific in **hlsBs**'s setup

   ..

   - as part of the project's setup, here **hlsBs-examples**.

     - Since `ruckus <https://github.com/slaclab/ruckus>`_ ,
       which **hlsBs** is a part of, is often a submodule
       of the project, its setup script can be conveniently located relative
       to the project's directory tree, thus removing the need for an absolute
       path to locate it.

   - The **hlsBs** setup script can be executed multiple times

     - it cleans up its context and quick so neither is an issue.

   If there are multiple projects under a common package (*e.g.* as does
   **hlsBs-examples**) then consider something similar to *exSelect*
   to select the current target project.  This is not common, so something
   like *exSelect* is generally unnecessary.

.. warning::

   **hlsBs** does not setup the Vivado license servers. This is so
   site dependent that it was deemed out of **hlsBs**'s scope. Vitis
   does not need it, but if running Vivado, it will be needed.

Command Flow - Overview
~~~~~~~~~~~~~~~~~~~~~~~

This is the general usage pattern of the commonly used **hlsBs** commands.
The commands use the :ref:`project file <project_file-label>` specific to
each example and common set of C++ source code, which together produce the
various *HLS* output products.

hlsWs, hlsCfg
^^^^^^^^^^^^^

This is a one-time each new project setup (**hlsWs** & **hlsCfg**) or at
a structural change to the project (just **hlsCfg**), *e.g.* when adding a new or
modifying an existing configuration.

.. code-block:: bash

   $ hlsWs  --create # Create the workspace
   $ hlsCfg --create # Create the configuration files and components

hlsRun
^^^^^^

This is the workhorse and is the **hlsBs** command used almost exclusively
after creating the workspace and configuration files/components.

.. code-block:: bash

   $ hlsRun --csim=make      # Make csim.exe
   $ hlsRun --csim=run       # Run csim.exe
   $ hlsRun --synthesis      # Create the synthesis
   $ hlsRun --cosim          # Run the CoSim
   $ hlsRun --package        # Create a .dcp
   $ hlsRun --implementation # Create the implementation (the .zip file)
   $ hlsRun --ip             # Rename the .dcp and augment the permissiable FPGA families

Any combination of these stages can be run with a single **hlsRun** command

.. code-block:: bash

   $ hlsRun --csim=m,r                      # Do the csim make and run, abbreviations are allowed
   $ hlsRun --package --implementation --ip # Run these stages
   $ hlsRun --all --exclude=ip              # Run all but the ip stage

hlsExe, hlsGdb
^^^^^^^^^^^^^^

These are used to run/debug a specific component's *csim.exe*,  most commonly
in the initial stages of developing and verifying the code.

.. code-block:: bash

   $ hlsExe <component-name>  [options]
   $ hlsGdb <component-name>  [options]

These target a single component, thus differing from ``hlsRun --csim=run``
which can target one or many components and has no ability to run *gdb*.

   They also offer the ability to modify the set of command line
   options, for example, changing the number of tests or the test vectors
   as opposed to ``hlsRun`` which always uses the *csim_argv* in the
   configuration file as the source of the command line parameters.

   See :ref:`ex6 <ex6-label>` for all the ways this can be done.


hlsVersion
^^^^^^^^^^

**hlsVersion** selects a different Vitis version to use.  Since the products
(workspace, configuration file, components, csim.exe, *etc.*) are Vitis
version dependent, the previous steps, starting with **hlsWs** must be
rerun for this new version.

   For this tutorial, changing versions is optional.  It is meant to
   illustrate how easy it is to work with different Vitis versions.

.. code-block:: bash

   $ hlsVersion 2025.1


.. _tutorial_preliminaries-label:

Tutorial - Preliminaries
========================

What does the code do?
----------------------

While what the code actually does is unimportant, the terse description for
the interested is

- Copies an input stream -> temporary stream -> output stream, adding some
  constants during each copy.

Directory Layout
----------------

This section provides context which is somewhat tangential to **hlsBs**. For
the impatient, skip ahead to
:ref:`Tutorial - The Annotated Version <tutorial_annotated_version-label>` and
revisit this later.

   Every new *HLS* project starts with this step, so while **hlsBs**
   is agnostic about this, it may provide a starting point.

This tutorial uses the following directory structure for the user written files:

.. code-block:: bash

   hlsBs-examples/
                  firmware/
                           scripts/setup_env.sh
                           shared/
                                  include/streams/    -- Shared common includes
                                          Streams.hh
                                  src/streams/        -- Shared common source code
                                          StreamsTb.cc
                                          StreamsHls.cc
                           ex0/
                               project/Streams.py     -- The ex0 project file
                           ex1/
                               project/Streams.py     -- The ex1 project file
                           ex2/
                               project/Streams.py     -- The ex2 project file
                           ex3/
                               project/Streams.py     -- The ex3 project file
                           ex4/
                               project/Streams.py     -- The ex4 project file
                           ex5/
                               project/Streams.py     -- The ex5 project file

Most setups will only have 1 project, but this tutorial has 6. In a 1 project
setup, the *ex\*/* and *shared/* directories are not necessary, moving their
subdirectories to be under firmware.


   Distinguish this directory structure from that of the eventual HLS products.
   Think of this as the *input* file layout and the *products* as the output
   file layout.



Creating your own project
-------------------------

The above is a suggested **hlsBs** layout for the project's source
code.  **hlsBs** can accomodate any directory structure, but
if you are at a loss where to start,
`ruckus <https://github.com/slaclab/ruckus>`_ the repository
that **hlsBs** lives in, contains a nice script to produce a very
similar directory layout. It is a great place to start and tailor to
your needs.

By default, **hlsBs** assumes the project file, a file necessary to
take full advantage of **hlsBs**'s capabilities, is located in the
**project/** directory directly under the project root. The project
file name can be named anything; select something meaningful, not, for
example *Project.py*.

.. note::

   To be technically correct, by default, **hlsBs** locates the project root
   with respect to the project file, *i.e.* it assumes the project root is one
   directory up from the project file. This means that directory containing
   the Project file need not be in a subdirectory named *project/*, but that
   name seems appropriate. The import of the project root is typically file
   specifications (e.g. the source files, include paths) are made using it as
   an anchor. This is a convention, not a requirement of **hlsBs**.


.. admonition:: Recommendation
   :class: tip

   - If you have more than one project under a common directory/repo, isolate
     the shared code as above.

   - Create a root directory for each project, here these are,
     *ex0, ex1, ex2, ex3, ex4, ex5*.

   - Create a directory called *project/* under the project root directory to
     hold the Project definition file.

   - Create any project code specific directories in the same fashion as the
     shared code but under the project root, *i.e.* *ex0*, *ex1*, *etc.*.

..  admonition:: Recommendation
    :class: tip

    While **hlsBs** does not require this layout of the output products - it
    provides simple ways to specify any layout - there should be a good reason
    for not using it. Having conventions is good when others use your project.


.. _setup_details-label:

Setup
-----
This is one of many different ways to do the setup.  It comes down to personal
preference and project needs.  It is convenient and **hlsBs**
friendly. A design goal was to have as few references to absolute file paths
as possible and having them well contained. **hlsBs** requires only two such
paths. This is the next's section topic.


Define Site and Project Specifics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There is one site specific and one project specific definition, Neither
can be part of the *hlsBs-examples* repository nor **hlsBs** itself,
since both contain absolute file paths specific to the site and the project.

- Site Specific - the Vitis installation directory tree(s)
- Project Specific - the project's setup script, here the
  *hlsBs-examples* setup script.

.. _hlsToolChain-label:

hlsToolChain
~~~~~~~~~~~~

This defines the environment variable **HLSBS_XILINX_SETUP** used by
**hlsVersion** to locate and source the settings script for a specified
Vitis Version.

While this definition could be entered on the command line via an
*export HLSBS_XILINX_SETUP*, this is inconvenient at best

- Need to remember the path to the site's Vitis installation.
- The syntax is awkward, with various characters needing to be escaped
  to avoid misinterpretation by the shell.

For these reasons it is recommended to capture this in a script that either

- directly does the export

  - here *hlsToolChain* could be the name of script defining the environment variable
- defines an alias to do the export
- defines a shell function that does the export

Both of the last two just enter a name in to bash shell. The shell function is
the better option as it avoids the error-prone and fragile escaping.

As an example and for definitiveness, this is what a bash shell function
would be for SLAC.

 .. code-block::

    hlsToolChain ()
    {
        export HLSBS_XILINX_SETUP='/sdf/group/faders/tools/xilinx/${version}'
    }


- The variable **version** will be translated to the Vitis version when
  requested by **hlsVersion**.

  .. tip::

     Locating the correct *settings64.sh* script involves a file search.

     If the versions of Vitis are not under a single directory path, specific
     paths can be entered colon separated list to avoid  broad searchs which
     may be slow.

.. _hlsBs_examples-label:

hlsBs-examples
~~~~~~~~~~~~~~

This will be used to source the project setup script.

.. code-block:: bash

   alias hlsBs-examples="source <path/to>/hlsBs-examples/firmware/scripts/setup_env"

Defining this alias is not strictly necessary, it is more of a convenience
to avoid remembering and typing long file paths. If using an alias, as is done
here, name the alias after something related to your project.

Recommendation
~~~~~~~~~~~~~~

To save typing and avoid needing to remember long file paths

   - Since these both HLSBS_XILINX_SETUP and project paths are relatively
     stable, create a shell script where all your personal aliases and
     bash shell functions are defined and enter **hlsToolChain** and
     the alias to the project's setup files (here **hlsBs-examples**) into it.

     - **hlsToolChain** is just the name chosen here to set the Vitis
       settings search path.
     - The name is a personal choice.

   ..

   - Source this alias defining script in your login script, making the
     aliases available for use.

     - Both are innocous, basically just definitions, so entering them into
       the login script is safe.
       
       - The only concern is possible name pollution in the shell. The
         **hlsBs** commands are all prefixed by *hls* to help.

     - Alternatively, source it when needed.

   ..

   - Since typically `ruckus <https://github.com/slaclab/ruckus>`_  will
     be a submodule of the user's project's directory tree, it may be
     convenient to source **hlsBs** setup script by a relative path within
     the project's setup script rather than a one-time source at the
     shell's login.


.. _tutorial_annotated_version-label:

Tutorial -- The Annotated Version
=================================

Presuming :ref:`hlsToolChain <hlsToolChain-label>` and
:ref:`hlsBs-examples <hlsBs_examples-label>` have been defined, this
begins a type-along tutorial, bash Karaoke. All the commands and their
expected outputs are presented here.


bash - Spawn a clean shell
--------------------------

.. code-block:: bash

   $ bash

..

This is to start with as clean a shell as possible.

.. note::

   The spawning of a new bash shell is strictly personal preference. It makes
   it easy to get back to a clean shell by simply exiting - the shell
   equivalent of *rm -rf* for files. Try it, you may find you like it.

   It is not perfect since environment variables and bash shell
   function names get carried over, so it is best to spawn the shell
   immediately on opening a new session.

..

hlsToolChain - Vitis Search Path
--------------------------------

.. code-block:: bash

   $ hlsToolChain

This defines the environment variable **HLSBS_XILINX_SETUP** which is
used by **hlsVersion** to locate and source the version specific Vitis/HLS
setup script.

.. warning::

   Setting up the Vivado license server is a user responsibility.

hlsBs-examples - Project Setup
------------------------------

.. code-block:: bash

   $ hlsBs-examples


This sources the **hlsBs-examples** setup script.  This setup script itself
sources **hlsBs** setup script which makes the **hlsBs** command set available
to the shell.

Sourcing of the **hlsBs** setup script within the project's setup script
rather than at shell login time is purely personal preference. There are
pros and cons.

.. list-table:: Sourcing **hlsBs** setup script
   :header-rows: 1

   * - Which
     - Pros
     - Cons
   * - At shell login
     - | There is nothing Vitis version or
       | package specific, so **hlsBs** setup
       | is truly a one-time thing.
     - | Issue is where is the **ruckus**
       | submodule which contains **hlsBs**.
       |
       | Since the absolute path to the **hlsBs**
       | setup script is hard-coded into
       | whatever sources it, this somewhat
       | implies there is a single, central
       | checked-out version of **ruckus**.
       |
       | This is not common practice.
   * - | In the package's
       | setup script
     - | Since **ruckus** is commonly
       | a submodule of the project,
       | can find the **hlsBs** script relative
       | to the **ruskus** submodule.
     - | If working on more than 1 project
       | this can result in unnecesarily
       | sourcing the **hlsBs**
       | setup script multiple times.
       |
       | Not serious,
       | **hlsBs** setup is quick, so
       |  - very small time penalty
       |  - it is careful to clean-up
       |  - does not accumulate context
       |

.. admonition:: Recommendation
   :class: tip

   Weighing the above pros and cons:

   While the absolute correct thing to do is source it once, usage patterns
   and convenience comes down on the side to source it as part of the
   project's setup script.

   Because of this, the **hlsBs** setup script is careful to not accumulate
   context if sourced multiple times, behaving as if each sourcing is the
   first.  Contrast this with the Vitis setup scripts which keeps adding to
   various colon separated environment variables.

      For example, the necessary paths in PYTHONPATH get appended with
      every sourcing. Particularly deadly if some paths are version
      dependent and one switches versions. This may be corrected in future
      releases after AMD/XILINX was notified of this. This is a problem
      **hlsVersion** must contend with.

hlsVersion - Set Vitis Version
------------------------------

.. code-block:: bash

   $ hlsVersion 2024.2
   Setting Xilinx to version = 2024.2

exSelect - Select ex0 Project
-----------------------------

.. code-block:: bash

   $exSelect ex0
   ex =<path_to>/hlsBs-examples/firmware/ex0/project/Streams.py

.. note::
   This is strictly not a usual part of the **hlsBs** workflow. It is here
   only because **hlsBs-examples** contains mulitple projects. Such a step
   is only necessary if a user's directory tree also contained multiple
   projects.

One can select any of *ex\** examples. Here, have started with the simplest, *ex0*.

hlsWs - Workspace Creation
--------------------------

Before creating the workspace, check on its status

.. code-block:: bash

   $ hlsWs --status  # Check on the status of the workspace
   ==============================================================================
   Workspace - Status
   ------------------
   Workspace : <path/to>/hlsBs-examples/firmware/ex0/products/ws/2024.2
   State     : Does not exist
   ==============================================================================

As expected it does not exist, so need to create it.

.. note::

   If for some reason the workspace does exist, say this tutorial was started,
   but now wish to start over with a clean slate, it can be removed by
   ``$ hlsWs --remove``

Now create the workspace.

.. code-block:: bash

   $ hlsWs --create
   Vitis Server started on port '41429'.
   ==============================================================================
   Workspace - Create
   ------------------
   Workspace : <path/to>/hlsBs-examples/firmware/ex0/products/ws/2024.2
   State     : Created
   ==============================================================================
   Shutting down Vitis server running on port '41429'

The workspace has now been created.

.. note::
   Sorry this does take a bit of time, but this invokes the Vitis
   utility to do the creation and anything involving Vitis is slow, even asking
   for the version number.

hlsCfg - Configuration/Components Creation
------------------------------------------

Before creating configuration files and components, check on their state.


   .. tip::

      Doing a listing is useful when doing more complex multi-component projects,
      allowing checking of the expected results. For this single component, it is
      not as useful.

      Almost all commands also have *--dry-run* parameter to see what would have
      been done.

.. code-block:: bash

   $ hlsCfg --list
   ==============================================================================
   Listing Configurations & Components
   -----------------------------------
   Workspace           : <path/to>/hlsBs-examples/firmware/ex0/products/ws/2024.2
   Vitis Version       : 2024.2
   Build time          : 20260625125755
   Project.Root        : <path/to>/hlsBs-examples/firmware/ex0
          .File        : <path/to>/hlsBs-examples/firmware/ex0/project/Streams.py
   Components          : *

   Existing
        None

   Missing
     1. Configuration  : <path/to>/hlsBs-examples/firmware/ex0/products/cfg/2024.2/stream.cfg
        Component      : <path/to>/hlsBs-examples/firmware/ex0/products/ws/2024.2/stream

   Cruft
        None
   ==============================================================================

After some global information about the project setup, the listing classifies the
configuration files and components into 3 categories

.. list-table:: Component Categories
   :header-rows: 1

   * - Category
     - Meaning
   * - Existing
     - Configuration files/components that exist.
   * - Missing
     - Configuration files/components that are missing
   * - Cruft
     - Configuration files/components present, but not defined by the project file.

The *Existing* and *Missing* are self-explanatory and, as expected, all are *Missing*.

The *Cruft* category has been found to be useful.  Sooner or later, via typos, not cleaning up properly or changing the set in the project file, *Cruft* creeps in. For simple projects this is generally not an issue, but for multi-component projects it can be.

.. note::

   The listing can be trimmed by category and component name.

   - *--list* option can accept category qualifiers (*existing, missing, cruft*)

     - *e.g.* ``--list=missing,cruft`` or ``list=e``  (abbreviations are excepted)

  ..

   - | Using a postional parameter, ``<selection>`` or
     | the optional parameters ``--components=<selection>``

     - where ``selection`` can be an explicit, wildcarded or list of any
       comma separated combination of component names. In this simple example,
       the only component is *stream*.

   ..

   For details do ``$ hlsCfg --help``

..

   | If for some reason, categories other than **Missing** are not empty, clean the with
   | ``$ hlsCfg '*' --clean``

Now create the configurations/components.

.. code-block:: bash

   $ hlsCfg --create
   Vitis Server started on port '46585'.
   ==============================================================================
   Creating Configuration + Component
   ----------------------------------
   Workspace     : <path/to>/hlsBs-examples/firmware/ex0/products/ws/2024.2
   Vitis Version : 2024.2
   Build time    : 20260625131240
   Project.Root  : <path/to>/hlsBs-examples/firmware/ex0
          .File  : <path/to>/hlsBs-examples/firmware/ex0/project/Streams.py
   Components    : *


   Creating Missing -> Existing
     1. Configuration : <path/to>/hlsBs-examples/firmware/ex0/products/cfg/2024.2/stream.cfg
        Component     : <path/to>/hlsBs-examples/firmware/ex0/products/ws/2024.2/stream
   ==============================================================================

The configuration file and component have now been created.

2 flags of interest can be added

- *\-\-verbose*  Gives more complete information on the global context and
  contents
- *\-\-dry-run*  Tells what would have happened but does not do the action

Additional actions are:

- *--clean*    Removes configuration file(s) and component(s)
- *--replace*  Replaces configuration file(s) and component(s)

All actions target a default category and component selection, but can be
explicitly specified.

- The categoies by ``--<action>=<categories of interest>``
- The components by positional parameters or ``--components=<selection>``

The defaults are:

.. list-table:: Default Categories By Action
   :header-rows: 1

   * - Action
     - Category
     - Component
   * - list
     - all
     - '\*'
   * - create
     - missing
     - '\*'
   * - replace
     - existing
     - '\*'
   * - clean
     - existing
     - no default


Example:

List only components in the *existing* category that match the wildcard
specifications *a\** and *s\**

.. code-block:: bash

   $ hlsCfg --list=existing --components=a*,s*

.. note::
   As a convenience one can create and replace all by

   .. code-block:: bash

      $ hlsCfg --replace=existing,missing
      # or
      $ hlsCfg --replace=e,m


hlsRun - Output Products Creation
---------------------------------

Once the workspace and configuration files and components have been
created, **hlsWs** and **hlsCfg** have done their work and recede into
the backwaters until needed again and **hlsRun** becomes the main command.

**hlsRun** runs the various product creation stages either
individually or in any combination that is permissible. (*e.g.*
*cosim* cannot be run before *synthesis*.)

.. list-table:: Run Stages
   :header-rows: 1

   * - Stage
     - What
   * - csim
     - The C simulation (clean, make, run)
   * - synthesis
     - The synthesis
   * - cosim
     - The CoSimulation
   * - package
     - The packaging (.dcp)
   * - implementation
     - The bit file (generally .zip)
   * - ip
     - Modifications of the .dcp and .zip files that have been found to be useful


hlsRun --csim
~~~~~~~~~~~~~

To create/make the csim.exe

.. code-block:: bash

   $ hlsRun --csim=make

The first time this is run on a new component, Vitis is needed to create the
make file.

.. note::

   The Vitis output is too extensive and uninformative and not included here.

The *--csim* qualifier accepts a list of *clean,make,run* to match your needs.
They can be abbreviated to 1 character (*c,m,r*). If no list is specified, the
default is *clean,make,run*.

Once the make file has been created, **hlsBs** just uses it. This is much
faster.  Try a *clean* and *make* just to observe. The *--verbose* flag was
added to show what happened.

.. code-block:: bash

   $ hlsRun --csim=c,m --verbose  # Clean, Make, Run may be abbreviated to s
   single character
   ==============================================================================
   Workspace         : <path/to/>/hlsBs-examples/firmware/ex0/products/ws/2024.2
   Component
   Vitis Version     : 2024.2
   Build time        : 20260625140702
   Project.Root      : <path/to/hlsBs-examples/firmware/ex0
          .File      : <path/to/hlsBs-examples/firmware/ex0/project/Streams.py

   Git    .repo      : hlsBs-examples
          .branch    : main
          .dirty     : Dirty

   Run CSim          : Clean,Make (fast)
   ----------------------------------------
     1. Component           : <path/to>/hlsBs-examples/firmware/ex0/products/ws/2024.2/stream
        Removing
        obj/StreamsTb.o
        obj/StreamsHls.o
        obj/../../../../../../../../../src/streams/StreamsTb.d
        obj/../../../../../../../../../src/streams/StreamsHls.d
        csim.exe
        --------------------
        Building:
        Compiling ../../../../../../../../../src/streams/StreamsTb.cc in debug mode
        Compiling ../../../../../../../../../src/streams/StreamsHls.cc in debug mode
        Generating csim.exe
   ==============================================================================

The next logical step is to run it.  Of course any combination of *clean*,
*make*, *run* can be used.  Since it was just made, only need *\-\-csim=run*.

.. code-block:: bash

   $ hlsRun --csim=r
   ==============================================================================
   Workspace         : <path/to>/hlsBs-examples/firmware/ex0/products/ws/2024.2
   Component
   Vitis Version     : 2024.2
   Build time        : 20260625141032
   Project.Root      : <path/to>/hlsBs-examples/firmware/ex0
          .File      : <path/to>/hlsBs-examples/firmware/ex0/project/Streams.py

   Run CSim          : Run (fast)
   ----------------------------------------
     1. Component           : <path/to>/hlsBs-examples/firmware/ex0/products/ws/2024.2/stream

   Stream.source = Internal
         .incval =   0
         .defval =   0
          ntests =   5 (Streams.py)

     0. Success
     1. Success
     2. Success
     3. Success
     4. Success

   INFO [HLS SIM]: The maximum depth reached by any hls::stream() instance in the design is 100
   ==============================================================================

.. warning::

   If the configuration composition, (*e.g.* a new source file was added or
   an existing one removed) that was used in building csim.exe, the
   configuration file needs to be rebuilt.  When doing this the component
   will be removed, taking the make file with it, so that when
   **hlsRun \-\-csim** is executed, it will be have to go through the slow
   Vitis method.

.. note::

   **hlsBs** has been designed to use the slow method when no make file exists
   and the fast method when it does.  Just in case there is a corner **hlsBs**
   missed, one can force the slow method by adding *\-\-slow*.  The default is

    - *make* file exists -> Use the fast method
    - *make* file does not exists -> Use the slow method

How Fast is Fast?
^^^^^^^^^^^^^^^^^

.. list-table:: Run Slow vs Fast
   :header-rows: 1

   * - Action
     - Slow
     - Fast
     - Notes
   * - clean
     - 10s
     - .25s
     - |
       | Vitis (slow method) insists on doing a make after a clean.
       | Fast only does what it is told.
   * - make
     - 7.7s
     - 2.6s
     -
   * - make (no need)
     - 9.8s
     -  .26s
     - |
       | Vitis (slow method) always remakes the make file
       | Wonder the purpose of a make file.
       | Fast only does what it is told.
   * - run
     - 9.9s
     -  .24s
     -
   * - clean, make
     -  10s
     -   2.7s
     -
   * - clean,make,run
     - 10s
     -  2.5s
     -

hlsRun [ --synthesis \| --cosim \| --package \| --implemntation \|
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Can now create these products. Unfortunately there is no *fast* method. These
all invoke **Vitis** or **Vivado**, so get your favorite beverage.

.. admonition:: Recommendation

   While all can be combined on a single command, *.i.e.*

   .. code-block:: bash

      $ hlsRun --syn --cosim --package --impl # Can abbreviate to uniqueness
       ...or...
      $ hlsRun --all --exclude=csim,ip

   it is not recommended unless this is a remake of a known working component.
   The amount of output makes it very easy to miss warning/error messages.
   **hlsBs** has tried to abort the sequence on error, but never hurts to check.

hlsRun --ip=zip,dcp
^^^^^^^^^^^^^^^^^^^

This stage selectively produces 2 output products that have been found to be
useful.  They are modifications of the standard Vitis/Vivado *.dcp* and *.zip*
build products. The default is to produce both.

- Renaming the internal name carried in *.dcp* file (from the
  *\-\-implementation* stage)

  - The internal name of the standard *.dcp* file is fixed to a constant string.
  - This makes it difficult/impossible when the final FPGA image is composed
    of multiple *.dcp* files
  - This gives the ability to uniquely name it.
    
    - The default is after the component, but can be user determined.

..

- Modify the families of acceptable FPGAs this can run on contained in the
  *.zip* file (from the *--package* stage).

  - At times the same FPGA image can be run on different families of FPGAs.
  - The knowledgeable user can set this set of families.
  - While *family* has a default, it may not be appropriate. It is the one parameter here that likely should not be defaulted.

Given the time involved in producing the original *.dcp* and *.zip*, by just modifying this file rather creating mulitple versions, this can save a lot of time. One is also assured it is the same image with just a name change.

.. note

   Using the usual output directory structure, these files are placed outside
   the build directory, a directory that generally is **not** committed to
   *git*.  By being placed outside of the build directory, unless an explicit
   entry is placed in *.gitignore*, these files will be committed to *git*.

   This is by design.
   - They are time-wish very expensive
   - Because of this, make sure such files have the *lfs* attribute set.


Additional Commmands
--------------------

These commands are less commonly used, but are very handy when they are needed.


hlsExe, hlsGdb
~~~~~~~~~~~~~~

These 2 commands are used when developing, debugging or verifying a specific component
and, as such, differ from **hlsRun --csim** which targets a user specified set of
components.

   A very useful feature of these 2 commands is the ability to modify the
   command line options,  for example, changing the number of tests or the test
   vectors as opposed to ``hlsRun`` which always uses the *csim_argv* in the
   configuration file as the source of the command line parameters.

   There is a lot more to this feature, see :ref:`ex6 <ex6-label>`.

Example:

Change the default number of tests from 5 to 6.

.. code-block:: bash

   $ hlsExe streams --ntests=6

   Stream.source = Internal
         .incval =   0
         .defval =   0
          ntests =   6 (CommandLine)

     0. Success
     1. Success
     2. Success
     3. Success
     4. Success
     5. Success

**hlsGdb** works similarly, except it invokes the gdb on the *csim.exe*.

Example:

.. code-block:: bash

   $ hlsGdb streams --ntests=6
   .
   .
   .
   (gdb) start
   Temporary breakpoint 1 at 0x21e53d: file ../../../../../../../../../../src/streams/StreamsTb.cc, line 94.
   Starting program: <path_to>/hlsBs-examples/firmware/ex0/products/build/ws/2024.2/streams/streams/hls/csim/build/csim.exe --ntests=5 --ntests=6
   [Thread debugging using libthread_db enabled]
   Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".

   Temporary breakpoint 1, main (argc=3, argv=0x7fffffffb4d8) at ../../../../../../../../../../src/streams/StreamsTb.cc:94
   94	   SrcStream srcStream;
   (gdb) c
   Continuing.

   Stream.source = Internal
         .incval =   0
         .defval =   0
          ntests =   6 (CommandLine)

   [New Thread 0x7ffff77ff640 (LWP 2361379)]
     0. Success
     1. Success
     2. Success
     3. Success
     4. Success
     5. Success

   INFO [HLS SIM]: The maximum depth reached by any hls::stream() instance in the design is 100
   [Thread 0x7ffff77ff640 (LWP 2361379) exited]
   [Inferior 1 (process 2361373) exited normally]
   (gdb) quit


hlsBs
~~~~~

Prints a manpage giving a brief summary and description of all the **hlsBs** commands.

  .. code-block:: bash

     $ hlsBs

It attempts to capture a highly condensed version of this document, but it is still
to extensive to be included here.

hlsCtx
~~~~~~

This displays the hidden context used by **hlsBs**, namely values of  environment
variables it uses

  .. code-block:: bash

     $ hlsCtx
     HLSBS Project environment variables
     HLSBS_ROOT           = <path-to>/hlsBs-examples/firmware/submodules/ruckus/vitis/hlsBs
     HLSBS_XILINX_SETUP   = <path-to-xilinx-tools>/${version}
     HLSBS_XILINX_VERSION = 2024.2
     HLSBS_PROJECT        = <path-to>/hlsBs-examples/firmware/ex0/project/Streams.py

hlsGui
~~~~~~

Once the configuration files and components have been created, if desired,
the Vitis GUI can be activated by

  .. code-block:: bash

     $ hlsGui

It will use the workspace as defined by and in this priority order

- The command line parameter ``--workspace=<workspace>``
- The environment variable HLSBS_WORKSPACE
- The project file

One can use the Vitis IDE/GUI as usual on the **hlsBs** created configuration files
and components.

.. _project_file-label:

The Project File
================

This important file contains all the information necessary to produce the various products, *i.e.* the workspace, configuration files, components, *etc* and where to place them in the directory structure.

The general features are documented in the reference manual, *hlsBs_ref*, found in the
`ruckus <https://github.com/slaclab/ruckus>`_ repository. But, much as one cannot
document all that a programming language can do (it is open-ended), it is impossible to
document all that can be done with the project file. There are many ways to
*skin-the-cat*. The fallback is to present a number of examples showing what is
possible.

.. warning::

   Try not to merely clone these examples. Avoid shoehorning in a
   complicated project into one of these fairly simple examples.

   **hlsBs**'s project file is Python, so it is capable of so much more. Hopefully
   concepts presented in these examples are orthogonal and straight-forward, so
   that once they are understood, mixing and matching are straight-forward.

Rather than annotate the Project files in this document, they have been verbosely
internally documented. Each example illustrates and explains its new feature.


.. note::

   The reference manual `ruckus <https://github.com/slaclab/ruckus>`_ more
   completely and formally documents all the features  with an (admittedly an
   non-working, it is meant only to illustrate) example project file.

The examples are

.. list-table::
   :header-rows: 1

   * - Project
     - What it does
   * - ex0
     - | Basic one component generator for a project with
       |
       | 1 test bench file
       | 1 hls file
       | 1 include path
       | 1 target FPGA
   * - ex1
     - | 2 components
       | Same code targeting 2 FPGAs
   * - ex2
     - | 4 components,
       | 2 sets of build codes
       | 2 FPGA targets
   * - ex3
     - | Uses normal file wildcarding to cox the preprocessor into #including
       | these files into the test bench source code at compile time.
       |
       | Each wildcarded file produces a uniquely named component.
   * - ex4
     - | Uses values from a list to #define preprocessor macro names.
       |
       | Each value in the list produces a uniquely named component.
   * - ex5
     - | Combines
       |   - the wildcarding include file feature of ex3
       |   - the macro definitions of ex4
   * - ex6
     - | Demonstrates techniques of entering command line parameters
       |    - via an environment variable specified in the project file
       |    - via a parameter file
       |    - directly on the command line


It is worth noting the practical difference between the *#include* and *#define*
methods of generating multiple variations of the same base component

    - The *#include* method is open-ended. Adding more include files that satisfy
      the wildcarding generates new components without touching any code or the
      Project file.

    ..

    - The *#define* often requires cooperation between the values defined in the
      Project file and the use of macro values in the code.

      - With some imagination, the project file could read the values from a file,
      - Except for very simple use cases, it is hard to avoid littering the source
        code with *#if #elif #endif*'s, essentially casing on the macro value.

    ..

    - The reference manual makes a case, that while both can accomplish almost
      all the same goals, the *#include* of a file is more flexible and easier
      to extend.  It also encourages an almost compile time API on how the
      include file should be structured, essentially using the include files
      akin to a plug-in.

  - Both have their uses and can be used separately or in combination.

  ..

  - In this very simple usage, each include file or value defines a new seed
    value that is added to a stream

    - A more sophisicated usage would be define

      - Constants to set the values of pragmas
      - Provide different implementation of some algorithm

Having done *ex0*, now explore *ex1*.

ex1
---

Select this project

.. code-block:: bash

   $ exSelect ex1

and create its workspace

.. code-block:: bash

   $ hlsWs --create

*ex1* is just the *ex0* project file changed to have 2 FPGA targets for the same code.
In this example, only FPGA clock speed is different.

.. code-block:: python

                       #                Id                    Part  Clock  Uncertainity
       fpgas        = ( Product.Fpga ('6ns', 'xcku115-flvb2104-2-i',   '6',        None),
                        Product.Fpga ('5ns', 'xcku115-flvb2104-2-i',   '5',        None))

Form the set of contributors by binding the build definition and the FPGAs.

.. code-block:: python

       contributors = (Product.CtbBuilds ('build',  build),
                       Product.CtbFpgas  ('fpga',   fpgas))

..

  There must be a *CtbBuilds* and a *CfgFpgas* and they must be in that order.

Modify the template defining the configuration file path to produce a unique name.
Here the *fpga.id* (*6ns* or *5ns*) is used to accomplish this and also to convey
meaning in the name.

.. code-block:: python

       # --------------------------------------------------
       # Configuration file name template
       # Makes  products/cfg/{vitis_version}/{build_id}.cfg
       #  e.g.  products/cfg/2024.2/streams-5ns.cfg
       #
       # If not specified
       #   - The directory is project.cfg_root
       #   - The extension is 'cfg'
       # --------------------------------------------------
       cfg_template = Product.CfgTemplate (prefix   = 'cfg',
                                           template = '{build.id}-{fpga.id}'))

3 symbolic names have be used

- {*vitis.version*} - The Vitis Version number, *i.e.* 2024.2, 2025.1, *etc* ...
- {*build.id*}      - An identifier for the specific build that is being used.

  - The *build* prefix on '{*build*\.id}' is user defined; it is the string '*build*'
    in the components definition

- {fpga.id}       - A user assigned identifier for the specific FPGA; think of it as
  a nickname. Including the *fpga.id* makes the configuration name unique. Other
  FPGA attributes listed below could also be used, provided they make the
  configuration file path unique.

  - The *fpga* prefix is user defined - it is the string '*fpga*' in the components
    definition. The complete list of FPGA attributes are

    - *fpga* - The full FPGA class (not terribly useful in this usage)
    - *fpga.part*  - The specfic FPGA part
    - *fpga.clock* - The FPGA clock
    - *fpga.uncertainity* - The FPGA clock uncertainity
    - *fpga.id*   - An arbitrary string to identify this FPGA specification
      (the '*6ns*' or '*5ns*').

 .. admonition:: Recommendation
    :class: tip

    While the *fpga.id* string can be anything, but given that it is often used in
    composing file paths, it is recommended to stick with the usual alphanumerics
    and limit symbols to '-' and '_'. Because the *fgpa.uncertainity* can contain
    *'+', '%', etc.*, it is not recommended to be used in the *cfg_template*. Better
    to reexpress it in a more canonical form in the 'fpga.id'.

.. note::

   In this example the component name is taken from the configuration name. It could
   be reversed.  This ordering was chosen since the configuration file name need not
   be unique, only its path.  For example, the *fpga.id* could have been used as
   directory with only the *build.id* specifying the configuration file name.

   While the configuration name and component name are entirely independent, sanity
   suggests making them related.

hlsCfg
~~~~~~

Assuming **hlsWs** has created the *ex1* workspace, to create the 2 configuration files and their respective components

.. code-block:: bash

   $ hlsCfg --create
   Vitis Server started on port '41953'.
   ==============================================================================
   Creating Configuration + Component
   ----------------------------------
   Workspace     :<path_to>/hlsBs-examples/firmware/ex1/products/ws/2024.2
   Vitis Version : 2024.2
   Build time    : 20260629124319
   Project.Root  :<path_to>/hlsBs-examples/firmware/ex1
          .File  :<path_to>/hlsBs-examples/firmware/ex1/project/Streams.py
   Components    : ['*']

   Creating Missing -> Existing
     1. Configuration :<path_to>/hlsBs-examples/firmware/ex1/products/cfg/2024.2/stream-5ns.cfg
        Component     :<path_to>/hlsBs-examples/firmware/ex1/products/ws/2024.2/stream-5ns

     2. Configuration :<path_to>/hlsBs-examples/firmware/ex1/products/cfg/2024.2/stream-6ns.cfg
        Component     :<path_to>/hlsBs-examples/firmware/ex1/products/ws/2024.2/stream-6ns
   ==============================================================================
   Shutting down Vitis server running on port '41953'

As expected, the 2 configuration files and components have been created. Note how the naming matches the template.

hlsRun
~~~~~~

To demonstrate a feature of **hlsBs**, **hlsRun** can target a single component or group of components. The following commands all build stream-6ns

.. code-block:: bash

   $ hlsRun stream-6ns --csim=m    # Explicit component name
   $ hlsRun '*-6ns' --csim=m       # Wildcard the component name. The '' to prevents the shell from doing the wildcarding
   $ hlsRun --comp=*-6ns --csim=m  # Safer way to prevent the shell from doing the wildcarding
   ==============================================================================
   Workspace         :<path_to>/hlsBs-examples/firmware/ex1/products/ws/2024.2
   Component         : ['*-6ns']
   Vitis Version     : 2024.2
   Build time        : 20260629125145
   Project.Root      :<path_to>/hlsBs-examples/firmware/ex1
          .File      :<path_to>/hlsBs-examples/firmware/ex1/project/Streams.py
   Components        : ['*6ns']

   Run CSim          : Make (fast)
   ----------------------------------------
     1. Component           :<path_to>/hlsBs-examples/firmware/ex1/products/ws/2024.2/stream-6ns
     .
     .

Without a component specification, the default is to apply the specified action
(here ``--csim=m``) to all existing components.

Handy options to remember which configuration/components exist are:

.. code-block:: bash

   $ hlsCfg --list           # Full listing of the existing, missing and cruft
   $ hlsCfg --list=existing  # Full listing of only the existing
   $ hlsRun --list           # Short listing of only the existing components


ex2
---

Select the *ex2* project and create its workspace

.. code-block:: bash

   $ exSelect ex2
   $ hlsWs --create

The *ex2* project defines

- 2 different builds (code sets)
- 2 FPGA configurations
- Yielding 4 components.

The FPGA specification is as the last example, but the *Builds* is now a tuple
(lists also work). In this fabricated example the builds are the same. In a
realistic example these would be different.

  A potential use case would be a chained processing involving
  
  - one FPGA processing its data
  - the next FPGA in the chain processing the output of the first, etc

  with each FPGA using different *HLS* processing code.

.. code-block:: python

       ctb_builds   = Product.CtbBuilds ('build', (buildA, buildB))

The remainder of the project file stays the same.

hlsCfg
~~~~~~

Assuming the workspace has been created, create the 4 components

.. code-block:: bash

   $ hlsCfg --create
   ==============================================================================
   Creating Configuration + Component
   ----------------------------------
   Workspace     : <path_to>/hlsBs-examples/firmware/ex2/products/ws/2024.2
   Vitis Version : 2024.2
   Build time    : 20260629130941
   Project.Root  : <path_to>/sandbox/hlsBs-examples/firmware/ex2
          .File  : <path_to>/sandbox/hlsBs-examples/firmware/ex2/project/Streams.py
   Components    : ['*']


   Creating Missing -> Existing
     1. Configuration :<path_to>/hlsBs-examples/firmware/ex2/products/cfg/2024.2/streamA-5ns.cfg
        Component     :<path_to>/hlsBs-examples/firmware/ex2/products/ws/2024.2/streamA-5ns

     2. Configuration :<path_to>/hlsBs-examples/firmware/ex2/products/cfg/2024.2/streamA-6ns.cfg
        Component     :<path_to>/hlsBs-examples/firmware/ex2/products/ws/2024.2/streamA-6ns

     3. Configuration :<path_to>/hlsBs-examples/firmware/ex2/products/cfg/2024.2/streamB-5ns.cfg
        Component     :<path_to>/hlsBs-examples/firmware/ex2/products/ws/2024.2/streamB-5ns

     4. Configuration :<path_to>/hlsBs-examples/firmware/ex2/products/cfg/2024.2/streamB-6ns.cfg
        Component     :<path_to>/hlsBs-examples/firmware/ex2/products/ws/2024.2/streamB-6ns
   ==============================================================================

The same configuration file path template has been used, but the names of the 2 builds are *streamA* and *streamB*, each built with the 2 FPGA configurations.

hlsRun
~~~~~~

Suppose all 4 have been built and had csim successfully run, but the synthesis is failing for the 5ns version of each. Might try something like:

.. code-block:: bash

   $ hlsRun --comp=*5ns --syn --verbose

or you wish to just rebuild csim.exe for streamA variations

.. code-block:: bash

   $ hlsRun --comp=streamA* --csim=m

This selection of components (it can be any list of wildcards and explicit definitions) is a general feature.  The *--dry-run* option is available on most commands to see what would have happened.  It is useful when a project has many targets as a quick check that the targeted components are as intended.

ex3
---

This examples shows how a generic piece of code can be tailored by providing a file to be included at compile-time. In this example, in the include directory is a subdirectory for 2 such include files:

::

    include/seeds/
                  Seed1.hh
                  Seed2.hh

In this toy example they only specify

- An integer used to seed the constants
- A  message indicating the include file's name

.. admonition:: Recommendation
   :class: tip

   Create a dedicated directory, here *seeds*, to hold these and only
   these include files. It allows the wildcarding to be narrowly defined,
   reducing an unintended file to be included.

In the project file, these pieces have been modified

.. code-block:: python

   # --------------------------------------------
   # Define the wildcard to select the Seed files
   # --------------------------------------------
   stream_seeds = os.path.join (include_path, "seeds", "Seed*.hh")

   # -----------------------------------------------
   # These are included via a special #define
   # The 'defines' are only needed in the test bench
   # -----------------------------------------------
   defines     = Product.IncludeFile (name     = 'STREAM_SEED', # macro name
                                      path     ='{seed.path}',  # file path
                                      rel_path = include_path)  # relative path to file

   tb_srcs     = Product.Sources (root     = code_root,
                                  files    = 'src/streams/StreamsTb.cc',
                                  includes = includes,
                                  defines  = defines)

   syn_srcs    = Product.Sources (root     = code_root,
                                  files    = 'src/streams/StreamsHls.cc',
                                  includes = includes,
                                  defines  = defines)

Modify the contributor specification to include these compile-time loaded include files.

.. code-block:: python

    # -------------------------------------------------------------------------
    # For the CtbFiles these attributes are defined
    #     seed.path          - Full path to the include file
    #     seed.dir           - The directory of the include file
    #     seed.name          - The file name of include file
    #     seed.ext           - The file extension of the inclde file
    #
    # The 'defines' uses {seed.path} as the product parameter name for the include file
    # The 'cfg_template' uses {seed.name}
    #
    # Note that the Product.CtbBuilds,CtbFiles,CtbFpgas can be specified
    # multiple times but all prefixes must be unique.
    # -------------------------------------------------------------------------
    contributors = Product.Contributors (Product.CtbBuilds ('build',  build),
                                         Product.CtbFpgas  ('fpga',   fpgas),
                                         Product.CtbFiles  ('seed',   stream_seeds))


    # -----------------------------------------------------------------------
    # Construct the configuration file path template to create a unique name.
    # Including the include file's name, this will yield,
    #       e.g.  project.cfg_root/streamA--Seed1-6ns.cfg
    # -----------------------------------------------------------------------
    cfg_template = Product.CfgTemplate ('cfg',
                                        '{build.id}-{seed.name}-{fpga.id}')


hlsCfg
~~~~~~

Assuming the *ex3* workspace has been created, now create the configurations/components.

.. code-block:: bash

   $ hlsCfg --create
   Vitis Server started on port '40481'.
   ==============================================================================
   Creating Configuration + Component
   ----------------------------------
   Workspace     :<path_to>/hlsBs-examples/firmware/ex3/products/ws/2024.2
   Vitis Version : 2024.2
   Build time    : 20260707141521
   Project.Root  :<path_to>/hlsBs-examples/firmware/ex3
          .File  :<path_to>/hlsBs-examples/firmware/ex3/project/Streams.py
   Components    : ['*']

   Creating Missing -> Existing
     1. Configuration :<path_to>/hlsBs-examples/firmware/ex3/products/cfg/2024.2/stream-Seed1-5ns.cfg
        Component     :<path_to>/hlsBs-examples/firmware/ex3/products/ws/2024.2/stream-Seed1-5ns

     2. Configuration :<path_to>/hlsBs-examples/firmware/ex3/products/cfg/2024.2/stream-Seed1-6ns.cfg
        Component     :<path_to>/hlsBs-examples/firmware/ex3/products/ws/2024.2/stream-Seed1-6ns

     3. Configuration :<path_to>/hlsBs-examples/firmware/ex3/products/cfg/2024.2/stream-Seed2-5ns.cfg
        Component     :<path_to>/hlsBs-examples/firmware/ex3/products/ws/2024.2/stream-Seed2-5ns

     4. Configuration :<path_to>/hlsBs-examples/firmware/ex3/products/cfg/2024.2/stream-Seed2-6ns.cfg
        Component     :<path_to>/hlsBs-examples/firmware/ex3/products/ws/2024.2/stream-Seed2-6ns
   ==============================================================================
   Shutting down Vitis server running on port '40481'

New components can be created just by adding more Seed*.hh files, *e.g.* Seed3.hh. This is a selling point of using compile-time loaded include files - new components can be created without touching the base code. In some sense, the base code acts as a super-template to construct variations.

hlsRun
~~~~~~

Make all the *csim.exe*'s with ``hlsRun --csim=m`` (not shown), then run only the
stream-Seed2-5ns component

.. code-block:: bash

   $ hlsRun '*Seed1-5ns' --csim=r --verbose
   ==============================================================================
   Workspace         :<path_to>/hlsBs-examples/firmware/ex3/products/ws/2024.2
   Component         : ['*Seed1-5ns']
   Vitis Version     : 2024.2
   Build time        : 20260707141709
   Project.Root      :<path_to>/hlsBs-examples/firmware/ex3
          .File      :<path_to>/hlsBs-examples/firmware/ex3/project/Streams.py

   Git    .repo      : hlsBs-examples
          .branch    : main
          .dirty     : Dirty

   Run CSim          : Run (fast)
   ----------------------------------------
     1. Component           :<path_to>/hlsBs-examples/firmware/ex3/products/ws/2024.2/stream-Seed1-5ns
        Running:

   Stream.source =<path_to>/hlsBs-examples/firmware/include/seeds/Seed1.hh
         .incval =   1
         .defval =   0
          ntests =   5 (Default)

     0. Success
     1. Success
     2. Success
     3. Success
     4. Success

   INFO [HLS SIM]: The maximum depth reached by any hls::stream() instance in the design is 100
   ==============================================================================

In the output, just to illustrate the effect of the compile-time include file,
the test bench has printed

- The name of the included file
- Its seed value *incval*

The *.defval* is the subject of the next example.

ex4
---

This example uses compile time *\#defines* to achieve results similar to the *ex3*
example.

Define the Set of Values
~~~~~~~~~~~~~~~~~~~~~~~~
These can be a single, list or tuple of *Product.Value*'s.

.. code-block:: python

    values   = ( Product.Value (id = None,  value = 20),
                 Product.Value (id = 'D30', value = 30) )

Each *Product.Value* defines

- An identifier, generally used in configuration file path and/or component name
  construction.

  - If specified as *None*, the *id* will be the *value*.
  - For simple cases, this may be sufficient, but if the value is complex, say
    *ap_fixed<10,7>* using this string in the configuration file path or component
    would make an unwieldy name and is not recommended.
  - A value, this can be any string that is a valid *\#define* target.

Add to the List of Contributors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These values are now added to the contributors

.. code-block:: python

   contributors = Product.Contributors (Product.CtbBuilds ('build', build),
                                        Product.CtbFpgas  ('fpga',  fpgas),
                                        Product.CtbValues ('def',   values))

The following product parameters names are defined for each generated configuration
and component.

- *def.id* - The identifier
- *def.value* - The value

Construct the Configuration Path
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Incorporate this into the configuration file path template to ensure a unique path
for each generated configuration file path and, eventually, component.

.. code-block:: python

   cfg_template = Product.CfgTemplate ('cfg', '{build.id}-{def.id}-{fpga.id}')

Where:

- The identifier of this *#define* has been referenced as *'{def.id}'*


Add to the Source's #defines
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Provide the information needed to construct the *#define* and include it in test bench
source definition. In this example, this ##define# is not needed in the *syn_srcs* so
is not included.

.. code-block:: python

    defines = Product.DefineValue ('DEF_SEED', '{def.value}')

    tb_srcs = Product.Sources     (root       = code_root,
                                   files      = 'src/streams/StreamsTb.cc',
                                   includes   = includes,
                                   defines    = defines)

Where:

- DEF_SEED is the *#define* macro name, *i.e.* *#define DEF_SEED*
- {def.value}' is its value, *i.e.* *20* or *30*


hlsCfg
~~~~~~

Assuming the workspace for *ex4* has been created, now create the
configurations/components.

.. code-block:: bash

   $ hlsCfg --create
   Vitis Server started on port '46127'.
   ==============================================================================
   Creating Configuration + Component
   ----------------------------------
   Workspace     :<path_to>/hlsBs-examples/firmware/ex4/products/build/ws/2024.2
   Vitis Version : 2024.2
   Build time    : 20260916112429
   Project.Root  :<path_to>/hlsBs-examples/firmware/ex4
          .File  :<path_to>/hlsBs-examples/firmware/ex4/project/Streams.py
   Components    : *

   Creating Missing -> Existing
     1. Configuration :<path_to>/hlsBs-examples/firmware/ex4/products/build/cfg/2024.2/stream-20-5ns.cfg
        Component     :<path_to>/hlsBs-examples/firmware/ex4/products/build/ws/2024.2/stream-20-5ns

     2. Configuration :<path_to>/hlsBs-examples/firmware/ex4/products/build/cfg/2024.2/stream-20-6ns.cfg
        Component     :<path_to>/hlsBs-examples/firmware/ex4/products/build/ws/2024.2/stream-20-6ns

     3. Configuration :<path_to>/hlsBs-examples/firmware/ex4/products/build/cfg/2024.2/stream-D30-5ns.cfg
        Component     :<path_to>/hlsBs-examples/firmware/ex4/products/build/ws/2024.2/stream-D30-5ns

     4. Configuration :<path_to>/hlsBs-examples/firmware/ex4/products/build/cfg/2024.2/stream-D30-6ns.cfg
        Component     :<path_to>/hlsBs-examples/firmware/ex4/products/build/ws/2024.2/stream-D30-6ns
   ==============================================================================
   Shutting down Vitis server running on port '46127'

New configurations/components can be created just by adding more *Product.Value*'s
to the *values* list. The use of *#defines* has the disadvantage of
modifying the project file. Contrast this with the *ex3*'s *\#include* technique where
files are just added to the */seeds* directory - the project file is not modified.

.. note::

   With some straight-forward Python code plus some user creativity, these *ids* and
   *values* could be

   - read in from an external file
   - define the values in another python file and import that file into the
     project script.

     - *e.g* ``values = MyValues.get ()``


   Providing a method of reading the *ids* and *values* from a file was considered,
   but rejected due to the vagarities of what the file format should be. With some
   experience, perhaps a standard will emerge and it can be provided.


hlsExe
~~~~~~

After making all the *csim.exe*'s with ``hlsRun --csim=m``, run only the
stream-seed20-5ns component using **hlsExe** instead of **hlsRun**. **hlsExe**'s
advantage is parameters can be modified on the command line. Here the default of
5 tests was modified to 10 tests.

.. _command_line_demo-label:

.. code-block:: bash


   $ hlsExe stream-seed10-5ns --ntests=10

   Stream.source = Internal
         .incval =   0
         .defval =  20
          ntests =  10

     0. Success
     1. Success
     2. Success
     3. Success
     4. Success
     5. Success
     6. Success
     7. Success
     8. Success
     9. Success

   INFO [HLS SIM]: The maximum depth reached by any hls::stream() instance in the design is 100

In the output, the test bench has printed

- The source of *incval* was *Internal*
- The *incval* seed was defaulted to 0
- The define seed value, *defval* is 20
- The number of tests was 10

This is an advertisement for the capability of *hlsExe* to modify the parameters. Here,
it is simply changing the number of tests, but it could be any command line parameter
supported by *csim.exe*.

ex5
---

This example combines ex3's *#include* and ex4's *#define* techniques.
The modifications of the project file are

Add to the List of Contributors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Provide both the include file and #define value contributors:

.. code-block:: python

   contributors = Product.Contributors (Product.CtbBuilds ('build',         build),
                                        Product.CtbFpgas  ('fpga',          fpgas),
                                        Product.CtbValues ('def',          values),
                                        Product.CtbFiles  ('seed',   stream_seeds))

Modify the Configuration Template
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   cfg_template = Product.CfgTemplate ('cfg',
                                       '{build.id}-{seed.name}-{def.id}-{fpga.id}')

The configuration file/component creation, *etc* follows exactly as in the previous
examples.

.. _ex6-label:

ex6
---

This example shows how to use **hlsBs**, **hlsExe** in particular, to modify the
run-time command line parameters of an existing *csim.exe* executable.  This is
valuable for multiple reasons:

- Testing corner cases with different input parameters.
- Debugging a specific problem child data set or parameter setting.
- A formalized testing program which tests the same *csim.exe* against
  many sets of test vectors.

It aims to overcome Vitis/HLS very rigid method of setting the input parameters
only by modifying the configuration file specification. This bypasses unnecessarily
repeating many time-consuming steps, when all that is needed is to run *csim.exe*
with a different set of parameters.

Techniques
~~~~~~~~~~

There are 3 techniques to modify the input command line parameters at run-time.

.. list-table:: Command Line Parameters - Entry Options
   :header-rows: 1

   * - Technique
     - Use Case
     - Pros
     - Cons
   * - Command line
     - | Ad-hoc interactive exploration
       | Scripting a set of commands
     - Easy to do
     - | Unless captured in a script
       |  - Easily forgotten
       |  - No formal record
   * - In a file
     - | Capture a set of test
       | parameters in an apprpriately
       | named file
     - | Can capture a coherent set
       | of parameters
       |  - e.g. A set of input and
       |         output data files
       | Permanency, the file persists
       | File name adds description
     - More formal/overhead
   * - | Configuration Defined
       | Environment Variable
     - | Makes
       |  - GUI  marginally more
       |   flexible.
       |  - Command line much more
       |  - flexible,
     - Easy and familar
     - | Unset environment variable
       | result in mysterious behavior

There is a lot of verbiage, much stating the obvious. In practice, usage is
intuitive. Look at the example command lines before despairing.


Precedence
^^^^^^^^^^

These can be used separately or in any combination. If the same parameter is specified
by more than one method or more than time, the precedence order from highest to lowest
is:

- Explicit specification on the command line or from an explicitly named parameter file
- Parameter file specified by the environment varible **HLSBS_PROJECT_INI**

  - This method is not available when running within the GUI

- Value from the project/configuration file, either an explict value or an
  environment variable's translated value.

This is basically from the most informal to the most formal, last specification wins.

Project File Modification
~~~~~~~~~~~~~~~~~~~~~~~~~

*ex6* is a simple extension of *ex0*, redefining the ``csim_argv`` string as
an environment variable, whose translation is deferred until runtime.

To specify an environment variable or environment variables in strings to be
deferred until runtime for translation, in the project file:

.. code-block:: python

   csim_argv  = ( '--ntests=' + Product.EnvString.preserve ('NTESTS') +
                 ' --source=ProjectFile')
   cosim_argv = csim_argv

   # or

   # The environment variables must be expressed as ${NTESTS}, not $NTESTS
   csim.argv  = Product.EnvString.preserveAll('--ntests=${NTESTS} --source=ProjectFile')
   cosim_argv = csim_argv

.. note::

   Due to Vitis/HLS mishandling of environment variables, directly using *${NTESTS}*
   does not work. The *preserve* and *preserveAll* methods are a workarond to this
   limitation.

The test bench C++ code needs a helper method to do the translation to enable
the same functionality within the GUI as at the command line.

.. code-block:: C++

   #include "hlsHelpers/ExpandEnvs.hh"

   // Within the command line parameters parsing, one needs to translate
   // these modified environment variables
   expanded_string = hlsHelpers::expand_envs (<string>)

Note that *expand_envs* will expand **all** environment variables in *string*.


Environment Variable
~~~~~~~~~~~~~~~~~~~~

This uses the translated value of the *NTESTS* environment variable.

.. code-block:: bash

   # Presumably set previously, possibly in a setup script, set NTESTS
   $ export NTESTS=3

   .
   .
   $ hlsExe streams

   Stream.source = Internal
         .incval =   0
         .defval =   0
          ntests =   3

     0. Success
     1. Success
     2. Success

   INFO [HLS SIM]: The maximum depth reached by any hls::stream() instance in the design is 100

..

See :ref:`Implementation Details <implementation_details-label>` for
a more complete explanation.

.. warning::

   If running *csim.exe* within the GUI, be  aware that the translated value of
   any environment variable is the value it had when the GUI was launched.

   It is very easy to forget this and think its value as it currently is in the
   shell it was launched from. It certainly could have changed since when the GUI was
   launched.

   Changing the value of the environment variable does not change the value in the GUI.
   LINUX provides no means to modify the values of environment variables in a
   spawned process, such as the GUI. Only a custom Vitis provided interface in
   the GUI could modify a value.

   **Bottom Line**: Be wary of using all but the most stable environment variables in
   the configuration file specification when using the GUI. They can be used, but
   know the limitations of the GUI.  Using **hlsRun**, **hlsExe** or
   **hlsGdb** to run *csim.exe* will behave as expected since no spawned process is
   involved.


Command Line Specification
~~~~~~~~~~~~~~~~~~~~~~~~~~

This has already been demonstrated in :ref:`ex4 <command_line_demo-label>`, but
for completeness.

.. code-block::

   $ hlsExe streams --ntests=6

   Stream.source = Internal
         .incval =   0
         .defval =   0
          ntests =   6

     0. Success
     1. Success
     2. Success
     3. Success
     4. Success
     5. Success

   INFO [HLS SIM]: The maximum depth reached by any hls::stream() instance in the design is 100

Parameters from the configuration file, which includes the ``--ntests=${NTESTS}``,
by Vitis conventions, are always presented on the command line and must be the first
parameters. Therefore, the explicit specification of ``--ntests=6``, being the last
specification, overrides the value of the environment variable NTESTS.


Parameter Files
~~~~~~~~~~~~~~~

A parameter file is simply a means of capturing command line parameters in a file.
It is a direct mimic of a Python's *argparse* feature. Functionally, the result is as
if the file has been replaced by its contents.

In this example a file, *Ntests8.txt* has been created. It has the single line

.. code-block:: text

   --ntests=8

One can use this in two ways

- Directly

  .. code-block:: bash

     $ hlsExe streams @ex6/prms/NTests8.txt

- The value of the environment variable **HLSBS_PROJECT_INI**

  .. code-block:: bash

     # Perhaps set in a setup script
     $ export HLSBS_PROJECT_INI=ex6/NTests8.txt
     .
     .
     # ---------------------------------------------
     # With HLSBS_PROJECT_INI being defined is as if
     # $ hlsExe streams @HLSBS_PROJECT_INI
     # So saves typing at the expense of clarity
     # ---------------------------------------------
     $ hlsExe streams

  ..

 When using **HLSBS_PROJECT_INI**, the command line parameters from the parameter file
 are the first set of parameters..  Since functionally the *file* is
 replaced by its contents, this affects precedence.

  - **HLSBS_PROJECT_INI**

    - Since it's parameters appear first, they will be overriden by any
      subsequent specification of the same parameter.

  - Explicit

    - Since the file can appear anywhere on the command line, the winner
      is whichever is last. This can be either from the parameter file or
      an explict specification, *i.e.* ``ntests=9``, which every is last.


Parameter File Format
^^^^^^^^^^^^^^^^^^^^^
The file format is very simple, perhaps too simple. These are adopted to maintain
full compatibily with *argparse*.

- No blank lines
- No trailing space
- No include mechanism

The first two are annoyances, but as a workaround to the lack of an include
mechanism. An include mechanism would allow multiple files to be bound into
a single coherent set.

- Muliple separate parameter files can be specified by

  - Capturing in an environment variable

    .. code-block:: bash

       $ export MyPrms="@FILE1 @FILE2 @FILE3"
       .
       $ hlsExe streams $MyPrms

- A colon separate list

    .. code-block:: bash

       $ hlsExe streams @FILE1:FILE2:FILE3

  - Using an environment or shell variable with a descriptive name set to the
    the colon separated list adds meaning, particularly when looking
    back at the shell's history.

    .. code-block:: bash

       $ ProblemChild=@ProblemData:ProblemParameters
       .
       .
       $ hlsExe ${ProblemChild}

    This is almost equivalent to the *MyPrms* above, it is just different syntax.

C++ Helper
^^^^^^^^^^

Unlike Python's *argparse*, which natively recognizes parameter files, *getopt* does
not. A helper method is provided to be used in the testbed's C++ code.

.. code-block:: c++

   #include "hlsHelpers::expand_args.hh"
   .
   .

   // Expand any and all parameter files
   hlsHelpers::ExpandArgs cl (argc, argv);

   // Use the expanded argc and argv exactly as the originals
   Parameters  prms (cl.m_argc, cl.m_argv)


.. _implementation_details-label:

Environment Variables - Implementation Details
----------------------------------------------

The *preserve* method, converts the string into a form that defers its translation
until runtime. If not converted, it would be translated by ``hlsCfg --create``. In
addition to the *convert* method there is

-  Product.EnvString.preserveAll

   - This preserves any and all instances of environment variables specified as
     *${<ENV>}*.
   - *e.g. *csim_argv=${TEST_ROOT}/input.data ${TEST_ROOT}/output.data*

Unfortunately, even if one did pass an environment variable as is into the
configuration file, HLS, in its infinite wisdom will

- Sometimes translate it immediately
- Sometimes preserve it, but then have one of csim, cosim or synthesis reject it

  - It depends on the escaping of special shell characters. It's a mess.

To get around this, the Python methods converts the syntax

- from ${ENV}
- to   %ENV%

  - Some will recognize as the Windows convention
  - Had to pick something.

If the value of 'csim_argv' were was always processed by **hlsBs** commands
the translation to its actual environment value could be done transparently
in those commands.  However, a stated goal of **hlsBs** is compatibility with
the GUI/IDE. Unfortunately this means the translation must occur within (usually)
the test benches C++ code, by a simple method provided by **hlsBs** to expand
all modified forms of the environments variables and get their values.

Final Word
==========

**hlsBs** will happily accept multiple builds, fpgas, includes and
defines combined in any mix. This can produce 10s if not many 10s of components.
The limitation is likely on the user to not be overwhelmed.

**hlsBs** has attempted to provide the tools to create, categorize and track
multiple components, but the burden is still on the user to create a development
roadmap.  For example, it may be that, instead of a single workspace,
multiple workspaces are used in a single package to help separate different
development paths, many of which are exploratory and will not be kept.

Think about your workflow.  If features to assist can be added to **hlsBs** make
them known. For as much as **hlsBs** was an attempt to simplify the mechanics of
building HLS components, it was also an attempt to help in the user implement a
sensible workflow.
