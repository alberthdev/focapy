{% macro write_c_structs(derived_types, pack = True) -%}
/* Derived type structures */
{% if pack -%}
    #pragma pack(2)
    {{- "\n\n" -}}
{%- endif -%}

{%- for derived_type_name in derived_types.keys() -%}
    typedef struct {{ derived_type_name }}_ {
        {{- "\n" -}}
        {%- for element in derived_types[derived_type_name] -%}
            {% if element[0] %}
                {{- "    " + element[0] }} {{ element[2] }}{{ element[1] }};
                {{- "\n" -}}
            {%- else -%}
                {{- '/* STUB: element "' + element[3][1]  + '", type "' + element[3][0] + '" */' -}}
            {% endif -%}
        {%- endfor -%}
    } {{ derived_type_name }}, *p_{{ derived_type_name }};
    {{- "\n\n" -}}
{% endfor %}
{%- if pack -%}
    #pragma pack()
{%- endif -%}
{{- "\n" -}}
{% endmacro %}
