{% extends 'mail_templated/base.tpl' %}

{% block subject %}
activate and verify
{% endblock %}

{% block html %}
<h1>click blow to activate and verify your account</h1>
<a href="http://127.0.0.1:8000/accounts/api/v1/user/activation/confirm/{{ token }}">submit</a>
{% endblock %}