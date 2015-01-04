{% macro write_c_element_vars(elements) -%}
/* Top-level element variable declarations */
{% for element_name in elements.keys() %}
    {%- if elements[element_name][0] -%}
        {{- "extern " + elements[element_name][0] }} *{{ elements[element_name][2] }}{{ elements[element_name][1] }};
    {%- else -%}
        {{- '/* STUB: element "' + elements[element_name][3][1]  + '", type "' + elements[element_name][3][0] + '" */' -}}
    {% endif -%}
    {{- "\n" -}}
{% endfor -%}
{% endmacro %}
