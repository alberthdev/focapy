    %FUNCNAME%_ = dlsym(read_dummy, "%PREFIX%%FUNCNAME%_");
    err_str = dlerror();
    if (err_str) {
        fatal("Cannot find %FUNCNAME%_ in %s: %s", mod_lib_path, err_str);
    }
