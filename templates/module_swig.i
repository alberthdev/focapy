{% from 'module_c_element_vars.h' import write_c_element_vars -%}
{% from 'module_c_structs.h' import write_c_structs -%}
{% from 'module_c_sub_prototypes.h' import write_c_sub_prototypes -%}
{% from 'module_c_func_prototypes.h' import write_c_func_prototypes -%}
%module {{ module_name }}
%include "cpointer.i"
%include "carrays.i"
%include "cstring.i"

/* cpointer.i stuff */
%pointer_functions(int, intp);
%pointer_functions(float, floatp);
%pointer_functions(double, doublep);

/* carrays.i stuff */
%array_functions(int, inta);
%array_functions(float, floata);
%array_functions(double, doublea);

%{
#define SWIG_FILE_WITH_INIT
#include "{% if module_header %}{{ module_header }}{% else %}{{ module_name }}.h{% endif %}"
%}
{% if assumed_shape_vars and assumed_shape_vars|length > 0 -%}
{%-     for assumed_shape_var in assumed_shape_vars %}
%inline %{
  {{ assumed_shape_var }} **mk_{{ assumed_shape_var }}pp({{ assumed_shape_var }} *f) {
    {{ assumed_shape_var }} **{{ assumed_shape_var }}pp = ({{ assumed_shape_var }} **) malloc(sizeof({{ assumed_shape_var }} *));
    *{{ assumed_shape_var }}pp = f;
    return {{ assumed_shape_var }}pp;
  }
%}
{%     endfor -%}
{%- endif -%}

{{ write_c_element_vars(elements) }}
{{ write_c_structs(derived_types, False) }}
{{ write_c_sub_prototypes(subroutines, module_name, args_hinting) }}
{{ write_c_func_prototypes(functions, module_name, args_hinting) }}
