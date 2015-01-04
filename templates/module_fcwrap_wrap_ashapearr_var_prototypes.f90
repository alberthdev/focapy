{% macro write_fcwrap_wrap_ashapearr_var_prototypes(args_dict, module_name, subroutine, args_hinting, fortran_lookup_table) -%}
{# Handle assumed shaped array transition variable declaration #}
{%- for arg in args_dict %}
    {%- set arg_dict = args_dict[arg] -%}
    
    {%- if "dimension(:)" in arg_dict["attributes"] -%}
        {{- "\n" -}}
        {{ "            " }}
        {#- This is messy... check if intent(out) is present in attributes, -#}
        {#- OR if there's an entry in args_hinting. Then check to see if    -#}
        {#- this particular argument has a matching entry in                -#}
        {#- fortran_lookup_table or not.                                    -#}
        {%- if ("intent(out)" in arg_dict["attributes"]) or ((subroutine in args_hinting[module_name]) and (arg in args_hinting[module_name][subroutine]) and (args_hinting[module_name][subroutine][arg]["type"] == "out")) -%}
            {%- if (arg_dict["type"].lower() in fortran_lookup_table) -%}
                {{ fortran_lookup_table[arg_dict["type"].lower()].lower() + ", allocatable, dimension (:), target, save" }} :: {{ arg }}
            {%- else -%}
                {{ arg_dict["type"] + ", allocatable, dimension (:), target, save" }} :: {{ arg }} ! [write_fcwrap_wrap_ashapearr_var_prototypes] WARNING: Could not find equivalent C type for '{{ arg_dict["type"].lower() }}'! (Context: subroutine '{{ subroutine }}', argument '{{ arg }}')
                {{- wprint("[write_fcwrap_wrap_ashapearr_var_prototypes] WARNING: Could not find equivalent C type for '" + arg_dict["type"].lower() + "'! (Context: subroutine '" + subroutine + "', argument '" + arg + "')") -}}
            {%- endif -%}
        {%- else -%}
            {{ arg_dict["type"] + ", allocatable, dimension (:), target, save" }} :: {{ arg }}
        {%- endif -%}
        {{- "\n" -}}
    {%- endif -%}
{%- endfor -%}
{%- endmacro %}
