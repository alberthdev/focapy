    // READ_DUMMY
    printf(" * Attempting to load %MODNAME% module...\n");
    %MODNAME% = dlopen (mod_lib_path, RTLD_NOW);
    if (!%MODNAME%)
    {
        fatal ("Cannot load %s: %s", mod_lib_path, dlerror ());
    }
    printf("  ** Successfully loaded %s!\n", mod_lib_path);
