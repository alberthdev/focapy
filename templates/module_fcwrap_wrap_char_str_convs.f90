{% macro write_fcwrap_wrap_char_str_convs(args_dict) -%}
{#- Handle string conversions -#}
{%- for arg in args_dict %}
    {%- set arg_dict = args_dict[arg] -%}
    
    {%- if (arg_dict["type"].lower().startswith("character(")) and (arg_dict["type"].lower() not in [ "character(1)", "character(len=1)" ]) -%}
        {{- "\n" -}}
        {{- "            " -}}
        {#- This variable is the final variable that gets passed -#}
        {#- to the subroutine.                                   -#}
        call C_F_POINTER(C_LOC({{ arg }}), {{ arg }}_focapy_tmp)
        {{- "\n" -}}
        {{- "            " -}}
        {{ arg }}_focapy_len = INDEX({{ arg }}_focapy_tmp, C_NULL_CHAR) - 1
        {{- "\n" -}}
        {{- "            " -}}
        allocate(character(len={{ arg }}_focapy_len) :: {{ arg }}_focapy)
        {{- "\n" -}}
        {{- "            " -}}
        {{ arg }}_focapy = {{ arg }}_focapy_tmp(1:{{ arg }}_focapy_len)
        {{- "\n" -}}
    {%- endif -%}
{%- endfor -%}
{%- endmacro %}
