[Mozinstall](https://github.com/mozilla/mozbase/tree/master/mozinstall)
is a python package for installing Mozilla applications on various platforms.

For example, depending on the platform, Firefox can be distributed as a 
zip, tar.bz2, exe or dmg file or cloned from a repository. Mozinstall takes the 
hassle out of extracting and/or running these files and for convenience returns
the full path to the application's binary in the install directory. In the case 
that mozinstall is invoked from the command line, the binary path will be 
printed to stdout.

# Usage

For command line options run mozinstall --help

Mozinstall's main function is the install method

    import mozinstall
    mozinstall.install('path_to_install_file', dest='path_to_install_folder')

The dest parameter defaults to the directory in which the install file is located.
The install method accepts a third parameter called apps which tells mozinstall which 
binary to search for. By default it will search for 'firefox', 'thunderbird' and 'fennec'
so unless you are installing a different application, this parameter is unnecessary.

# Dependencies

Mozinstall depends on the [mozinfo](https://github.com/mozilla/mozbase/tree/master/mozinfo) 
package which is also found in the mozbase repository.
