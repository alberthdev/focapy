{% macro write_fcwrap_wrap_char_var_prototypes(args_dict) -%}
{#- Handle character string transition variable declaration -#}
{%- for arg in args_dict %}
    {%- set arg_dict = args_dict[arg] -%}
    
    {%- if (arg_dict["type"].lower().startswith("character(")) and (arg_dict["type"].lower() not in [ "character(1)", "character(len=1)" ]) -%}
        {{- "\n" -}}
        {{ "            " }}
        {#- This variable is the final variable that gets passed -#}
        {#- to the subroutine.                                   -#}
        character(len=:),allocatable   :: {{ arg }}_focapy
        {{- "\n" -}}
        {{ "            " -}}
        {#- This variable stores the temporary Fortran pointer,  -#}
        {#- converted from the C_CHAR ptr input via C_F_POINTER. -#}
        character(len=1000000),pointer :: {{ arg }}_focapy_tmp
        {{- "\n" -}}
        {{ "            " -}}
        {#- This variable stores the length of the C string,     -#}
        {#- which is used when doing the final conversion from   -#}
        {#- C string to Fortran string.                          -#}
        integer                        :: {{ arg }}_focapy_len
        {{- "\n" -}}
    {%- endif -%}
{%- endfor -%}
{%- endmacro %}
