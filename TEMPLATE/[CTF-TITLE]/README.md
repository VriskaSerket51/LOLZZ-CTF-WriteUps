# {{title}}

WriteUps for [{{title}}](Link)

Team Name: `:LOLZZ:`, nth place

{% for type, subs in probs -%}
## {{type}}
{% for k,v in subs -%}
- [{{k}}]({{v}}/README.md)
{% endfor %}
{% endfor %}