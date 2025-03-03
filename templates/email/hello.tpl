{% extends "mail_templated/base.tpl" %}

{% block subject %}
Activate User
{% endblock %}

{% block body %}

{% endblock %}

{% block html %}
{{token}}
{% endblock %}