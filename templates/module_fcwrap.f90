{% from 'module_fcwrap_sub_prototype.f90' import write_fcwrap_sub_prototype -%}
{% from 'module_fcwrap_var_prototypes.f90' import write_fcwrap_var_prototypes -%}
{% from 'module_fcwrap_wrap_ashapearr_var_prototypes.f90' import write_fcwrap_wrap_ashapearr_var_prototypes -%}
{% from 'module_fcwrap_wrap_char_var_prototypes.f90' import write_fcwrap_wrap_char_var_prototypes -%}
{% from 'module_fcwrap_wrap_ashapearr_ptr_convs.f90' import write_fcwrap_wrap_ashapearr_ptr_convs -%}
{% from 'module_fcwrap_wrap_char_str_convs.f90' import write_fcwrap_wrap_char_str_convs -%}
{% from 'module_fcwrap_wrap_ashapearr_conv_outptr.f90' import write_fcwrap_wrap_ashapearr_conv_outptr -%}
module fcwrap
    use, intrinsic :: iso_c_binding
    use kinds
    use {{ module_name }}
    implicit none
    
    {%- for subroutine_func in (wrap_subroutines + wrap_functions) %}
    public :: {{ subroutine_func }}
    {%- endfor -%}
    {{ "\n" }}
    contains
        {%- for subroutine in wrap_subroutines %}
        subroutine {{ subroutine }}(
            {#- VARIABLE DECLARATIONS #}
            {#- Subroutine prototype #}
            {{- write_fcwrap_sub_prototype(subroutines[subroutine]["arguments"], module_name, subroutine, args_hinting) -}}
            
            {#- Handle argument list -#}
            {{- write_fcwrap_var_prototypes(subroutines[subroutine]["arguments"]) -}}
            
            {#- Handle assumed shaped array transition variable declaration -#}
            {{- write_fcwrap_wrap_ashapearr_var_prototypes(subroutines[subroutine]["arguments"], module_name, subroutine, args_hinting, fortran_lookup_table) -}}
            
            {#- Handle character string transition variable declaration -#}
            {{- write_fcwrap_wrap_char_var_prototypes(subroutines[subroutine]["arguments"]) -}}
            
            {#- OK, declaration stuff done. Let's get into the fun stuff! -#}
            {#- INPUT PRE-PROCESSING -#}
            
            {#- Handle assumed shaped array variable transitioning (INTENT "in" only) -#}
            {{- write_fcwrap_wrap_ashapearr_ptr_convs(subroutines[subroutine]["arguments"], module_name, subroutine, args_hinting) -}}
            
            {#- Handle string conversions -#}
            {{- write_fcwrap_wrap_char_str_convs(subroutines[subroutine]["arguments"]) -}}
            
            {#- Make the call! -#}
            {{- "\n" -}}
            {{- "            " -}}
            {{- "call " + subroutine + "_focapy_orig(" -}}
            
            {%- for arg in subroutines[subroutine]["arguments"] %}
                {%- set arg_dict = subroutines[subroutine]["arguments"][arg] -%}
                
                {%- if (arg_dict["type"].lower().startswith("character(")) and (arg_dict["type"].lower() not in [ "character(1)", "character(len=1)" ]) -%}
                    {{- arg -}}_focapy
                {%- else -%}
                    {{- arg -}}
                {%- endif -%}
                {%- if not loop.last -%}
                    {{- ", " -}}
                {%- endif -%}
            {%- endfor -%}
            {{- ")\n" -}}
            
            {#- Handle assumed shaped array variable transitioning (INTENT "out" only) -#}
            {{- write_fcwrap_wrap_ashapearr_conv_outptr(subroutines[subroutine]["arguments"], module_name, subroutine, args_hinting) -}}
            
            {{ "        " }}end subroutine {{ subroutine }}{{ "\n" }}
        {%- endfor -%}
        
        {{ "\n" }}
        
        {%- for function in wrap_functions %}
        {{ functions[function]["returns"] }} function {{ function }}(
            {#- VARIABLE DECLARATIONS #}
            {#- function prototype #}
            {{- write_fcwrap_sub_prototype(functions[function]["arguments"], module_name, function, args_hinting) -}}
            
            {#- Handle argument list -#}
            {{- write_fcwrap_var_prototypes(functions[function]["arguments"]) -}}
            
            {#- Handle assumed shaped array transition variable declaration -#}
            {{- write_fcwrap_wrap_ashapearr_var_prototypes(functions[function]["arguments"], module_name, function, args_hinting, fortran_lookup_table) -}}
            
            {#- Handle character string transition variable declaration -#}
            {{- write_fcwrap_wrap_char_var_prototypes(functions[function]["arguments"]) -}}
            
            {#- OK, declaration stuff done. Let's get into the fun stuff! -#}
            {#- INPUT PRE-PROCESSING -#}
            
            {#- Handle assumed shaped array variable transitioning (INTENT "in" only) -#}
            {{- write_fcwrap_wrap_ashapearr_ptr_convs(functions[function]["arguments"], module_name, function, args_hinting) -}}
            
            {#- Handle string conversions -#}
            {{- write_fcwrap_wrap_char_str_convs(functions[function]["arguments"]) -}}
            
            {#- Make the call! -#}
            {{- "\n" -}}
            {{- "            " -}}
            {{- function + " = " + function + "_focapy_orig(" -}}
            
            {%- for arg in functions[function]["arguments"] %}
                {%- set arg_dict = functions[function]["arguments"][arg] -%}
                
                {%- if (arg_dict["type"].lower().startswith("character(")) and (arg_dict["type"].lower() not in [ "character(1)", "character(len=1)" ]) -%}
                    {{- arg -}}_focapy
                {%- else -%}
                    {{- arg -}}
                {%- endif -%}
                {%- if not loop.last -%}
                    {{- ", " -}}
                {%- endif -%}
            {%- endfor -%}
            {{- ")\n" -}}
            
            {#- Handle assumed shaped array variable transitioning (INTENT "out" only) -#}
            {{- write_fcwrap_wrap_ashapearr_conv_outptr(functions[function]["arguments"], module_name, function, args_hinting) -}}
            
            {{ "        " }}end function {{ function }}{{ "\n" }}
        {%- endfor -%}
        
end module fcwrap
