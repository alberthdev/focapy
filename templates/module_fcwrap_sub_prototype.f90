{% macro write_fcwrap_sub_prototype(args_dict, module_name, subroutine, args_hinting) -%}
{#- Subroutine prototype #}
{%- for arg in args_dict %}
    {%- set arg_dict = args_dict[arg] -%}
    {%- if "dimension(:)" in arg_dict["attributes"] -%}
        {{ arg + "_cptr_focapy" }}
        {%- if (module_name in args_hinting) and (subroutine in args_hinting[module_name]) and (arg in args_hinting[module_name][subroutine]) -%}
            {%- if args_hinting[module_name][subroutine][arg]["type"] == "in" and not(args_hinting[module_name][subroutine][arg]["cue"]) -%}
                {{ ", " + arg + "_focapy_arr_len" }}
            {%- endif -%}
        {%- endif -%}
    {%- else -%}
        {{ arg }}
    {%- endif -%}
    {%- if not loop.last -%}
    {{ ", " }}
    {%- endif -%}
{%- endfor -%}
) bind(c){{ "\n" -}}
{%- endmacro %}
