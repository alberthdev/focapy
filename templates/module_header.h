{% from 'module_c_element_vars.h' import write_c_element_vars -%}
{% from 'module_c_structs.h' import write_c_structs -%}
{% from 'module_c_sub_prototypes.h' import write_c_sub_prototypes -%}
{% from 'module_c_func_prototypes.h' import write_c_func_prototypes -%}
#include <stdint.h>

{{ write_c_element_vars(elements) }}
{{ write_c_structs(derived_types) }}
{{ write_c_sub_prototypes(subroutines, module_name, args_hinting) }}
{{ write_c_func_prototypes(functions, module_name, args_hinting) }}
