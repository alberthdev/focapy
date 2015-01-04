{% macro write_fcwrap_wrap_ashapearr_ptr_convs(args_dict, module_name, subroutine, args_hinting) -%}
{#- Handle assumed shaped array variable transitioning (INTENT "in" only) -#}
{%- for arg in args_dict %}
    {%- set arg_dict = args_dict[arg] -%}
    
    {%- if "dimension(:)" in arg_dict["attributes"] -%}
        {#- Check if intent(out) is present in attributes, OR if there's an -#}
        {#- entry in args_hinting dictation type out.                       -#}
        {#- {%- if ("intent(out)" in arg_dict["attributes"]) or ((subroutine in args_hinting[module_name]) and (arg in args_hinting[module_name][subroutine]) and (args_hinting[module_name][subroutine][arg]["type"] == "out")) -%} -#}
        {#- {{- "" -}} -#}
        {#- {%- else -%} -#}
        {%- if not (("intent(out)" in arg_dict["attributes"]) or ((subroutine in args_hinting[module_name]) and (arg in args_hinting[module_name][subroutine]) and (args_hinting[module_name][subroutine][arg]["type"] == "out"))) -%}
            {{- "\n" -}}
            {{- "            " -}}
            {{- "call C_F_POINTER (" + arg + "_cptr_focapy, " + arg + ", [" -}}
            {%- if ((subroutine in args_hinting[module_name]) and (arg in args_hinting[module_name][subroutine]) and (args_hinting[module_name][subroutine][arg]["type"] == "in") and not(args_hinting[module_name][subroutine][arg]["cue"])) -%}
                {{- arg + "_focapy_arr_len" -}}
            {%- else -%}
                {{- args_hinting[module_name][subroutine][arg]["cue"] -}}
            {%- endif -%}
            {{- "])" -}}
            {{- "\n" -}}
            {#- {{ arg_dict["type"] + ", allocatable, dimension (:), target, save" }} :: {{ arg }} -#}
        {%- endif -%}
    {%- endif -%}
{%- endfor -%}
{%- endmacro -%}
