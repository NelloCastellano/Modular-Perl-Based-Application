# Modular-Perl-Based-Application

When you want to modularize a PERL application, the “traditional” approach is to have the main script referring (and including) all the modules required for the application to run.

The problem with this approach is that – for every module you will be adding or removing – you would need to modify the application with all the possible mistakes that can arise by doing so.

The approach I propose is to have a main script that read modules as a “plugin” where you will be adding/removing “plugins” without the need to ever touch any other portion of the application.

Using proper coding guidelines, using this approach makes possible to develop big sized applications in PERL in an easy and efficient way.

We have the main controlling file. This is the main application file. This is the file located in the cgi-bin directory called main.cgi (it can have any name of your choice)

This application does the following:

- it scans a directory (in our case we called it “plugins”) which is going to be a sub-directory of the folder where you will be placing this script. This directory will contain plugin files which will have to bear the extension “.pm” (Perl Module);
- once the plugins are loaded, the main module executes the init subroutine located in each plugin. This is used to load the “hooks” that will be then used to execute the various functions.
- upon completion of the initialization procedure, the application tests the existence in memory of the hook to execute “something”

One plugin that always have to be in the system is the “main.pm” which has to contain the function “&main” that is used as the default execution point OR used in case a hook is not found in the system.

Please note that like in any perl module, the last line of the plugin must contain “return 1;” or it will go in error.

As you notice, in the plugins, the first function is always named


init_{plugin name}


and the name has to be exactly like the file name (minus the extension).

All the functions of the plugin should begin with the name of the plugin.

