{% extends "mail_templated/base.tpl" %}

{% block subject %}
Activate User
{% endblock %}

{% block body %}

{% endblock %}

{% block html %}
127.0.0.1:8000/accounts/api/v1/confirm-user/{{token}}
{% endblock %}