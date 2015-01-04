{% macro write_fcwrap_wrap_ashapearr_conv_outptr(args_dict, module_name, subroutine, args_hinting) -%}
{#- Handle assumed shaped array variable transitioning (INTENT "out" only) -#}
{%- for arg in args_dict %}
    {%- set arg_dict = args_dict[arg] -%}
    
    {%- if "dimension(:)" in arg_dict["attributes"] -%}
        {#- Check if intent(out) is present in attributes, OR if there's an -#}
        {#- entry in args_hinting dictation type out.                       -#}
        {%- if ("intent(out)" in arg_dict["attributes"]) or ((subroutine in args_hinting[module_name]) and (arg in args_hinting[module_name][subroutine]) and (args_hinting[module_name][subroutine][arg]["type"] == "out")) -%}
            {{- "\n" -}}
            {{- "            " -}}
            {{- arg + "_cptr_focapy = c_loc(" + arg + ")" -}}
            {{- "\n" -}}
        {%- endif -%}
    {%- endif -%}
{%- endfor -%}
{%- endmacro -%}
