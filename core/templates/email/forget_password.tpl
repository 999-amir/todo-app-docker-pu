{% extends 'mail_templated/base.tpl' %}

{% block subject %}
forget-password
{% endblock %}

{% block html %}
<h1>click blow to change your password</h1>
<a href="http://127.0.0.1:8000/accounts/api/v1/user/forget-password/confirm/{{ token }}">submit</a>
{% endblock %}