{% extends 'mail_templated/base.tpl' %}

{% block subject %}
activate and verify
{% endblock %}

{% block html %}
<h1>click blow to activate and verify your account</h1>
<a href="{{ host_server }}accounts/api/v1/user/activation/confirm/{{ token }}">submit</a>
{% endblock %}