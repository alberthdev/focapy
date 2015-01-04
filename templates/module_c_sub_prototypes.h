{% macro write_c_sub_prototypes(subroutines, module_name, args_hinting) -%}
/* Subroutine prototypes */
{{- "\n" -}}
{%- for subroutine_name in subroutines.keys() %}
        {{- "void " + subroutine_name -}}(
    {%- if subroutines[subroutine_name]|length == 0 -%}
        {{- "void" -}}
    {%- else -%}
        {%- for element in subroutines[subroutine_name] -%}
            {%- if element[0] -%}
                {{ element[0] }} *{{ element[2] }}{{ element[1] -}}
                {%- set arg_name = element[3][1] -%}
                {%- if ((module_name in args_hinting) and (subroutine_name in args_hinting[module_name]) and (arg_name in args_hinting[module_name][subroutine_name])) -%}
                    {%- if (args_hinting[module_name][subroutine_name][arg_name]["type"] == "in") and not(args_hinting[module_name][subroutine_name][arg_name]["cue"]) -%}
                        {{- wprint("Hi2") -}}
                        {{ ", int *" + element[1] + "_focapy_arr_len" }}
                    {%- endif -%}
                {%- endif -%}
                {%- if not loop.last -%}
                    {{ ", " }}
                {%- endif -%}
            {%- else -%}
                void *{{ element[3][1] }} /* STUB: element {{ element[3][1] }}, type {{ element[3][0] }} */
            {%- endif -%}
        {%- endfor -%}
    {%- endif -%}
    {{- ");\n" -}}
    {%- endfor -%}
{% endmacro %}
