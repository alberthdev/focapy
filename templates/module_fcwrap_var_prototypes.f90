{% macro write_fcwrap_var_prototypes(args_dict) -%}
{# Handle argument list - variable prototypes #}
{%- for arg in args_dict %}
    {%- set arg_dict = args_dict[arg] -%}
    {{ "            " }}
    {%- if "dimension(:)" in arg_dict["attributes"] -%}
        {{ "type(C_PTR)" }}
    {%- elif arg_dict["type"].startswith("character(len=") -%}
        character(len=1,kind=c_char)
    {%- else -%}
        {{ arg_dict["type"] }}
    {%- endif -%}
    {%- if "dimension(:)" in arg_dict["attributes"] -%}
        {%- for attr in arg_dict["attributes"] -%}
            {%- if (attr.strip() != "dimension(:)") and (attr.strip() != "allocatable") -%}
                {{ ", " + attr }}
            {%- endif -%}
        {%- endfor %} ::
    {%- else -%}
        {{ ", " + ", ".join(arg_dict["attributes"]) }} ::
    {%- endif -%}
    {%- if "dimension(:)" in arg_dict["attributes"] -%}
        {{ " " + arg + "_cptr_focapy" }}
    {%- else -%}
        {{ " " + arg }}
    {%- endif -%}
    {{ "\n" }}
{%- endfor -%}
{%- endmacro %}
