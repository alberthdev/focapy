    // FCWRAP
    printf(" * Attempting to load fcwrap module...\n");
    fcwrap = dlopen (fcwrap_lib_path, RTLD_NOW);
    if (!fcwrap)
    {
        fatal ("Cannot load %s: %s", fcwrap_lib_path, dlerror ());
    }
    printf("  ** Successfully loaded %s!\n", fcwrap_lib_path);
    
    fortify_c_array_int_ = dlsym(fcwrap, "%PREFIX%fortify_c_array_int_");
    err_str = dlerror();
    if (err_str) {
        fatal("Cannot find fortify_c_array_int_ in %s: %s", fcwrap_lib_path, err_str);
    }
    
    fortify_c_array_float_ = dlsym(fcwrap, "%PREFIX%fortify_c_array_float_");
    err_str = dlerror();
    if (err_str) {
        fatal("Cannot find fortify_c_array_float_ in %s: %s", fcwrap_lib_path, err_str);
    }
    
    fortify_c_array_double_ = dlsym(fcwrap, "%PREFIX%fortify_c_array_double_");
    err_str = dlerror();
    if (err_str) {
        fatal("Cannot find fortify_c_array_double_ in %s: %s", fcwrap_lib_path, err_str);
    }
    
    printf("  ** Successfully loaded all functions for fcwrap!\n");
