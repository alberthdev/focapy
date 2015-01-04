{% macro write_c_func_prototypes(functions, module_name, args_hinting) -%}
/* Function prototypes */
{% for function_name in functions.keys() %}
    {{- functions[function_name]["returns"][0] }} {{ function_name }}(
    {%- if functions[function_name]["arguments"]|length == 0 -%}
        {{- "void" -}}
    {%- else -%}
        {%- for element in functions[function_name]["arguments"] -%}
            {%- if element[0] -%}
                {{- element[0] }} *{{ element[2] }}{{ element[1] -}}
                {%- set arg_name = element[3][1] -%}
                {%- if ((module_name in args_hinting) and (function_name in args_hinting[module_name]) and (arg_name in args_hinting[module_name][function_name])) -%}
                    {%- if (args_hinting[module_name][function_name][arg_name]["type"] == "in") and not(args_hinting[module_name][function_name][arg_name]["cue"]) -%}
                        {{ ", int *" + element[1] + "_focapy_arr_len" }}
                    {%- endif -%}
                {%- endif -%}
                {%- if not loop.last -%}
                    {{- ", " -}}
                {% endif -%}
            {%- else -%}
                void *{{- element[3][1] + '/* STUB: element ' + element[3][1] + ', type ' + element[3][0] + ' */' -}}
            {%- endif -%}
        {%- endfor -%}
    {%- endif -%}
    {{- ");\n" -}}
{%- endfor -%}
{%- endmacro %}
