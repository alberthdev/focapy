{% macro write_fcwrap_arg_prototypes(args_dict) -%}
{#- Subroutine prototype #}
{%- for arg in args_dict %}
    {%- set arg_dict = args_dict[arg] -%}
    {%- if "dimension(:)" in arg_dict["attributes"] -%}
        {{ arg + "_cptr_focapy" }}
    {%- else -%}
        {{ arg }}
    {%- endif -%}
    {%- if not loop.last -%}
    {{ ", " }}
    {%- endif -%}
{%- endfor -%}
) bind(c){{ "\n" -}}
{%- endmacro %}
