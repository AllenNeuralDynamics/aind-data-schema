Diagrams
========

.. jinja:: first_ctx

    {% for k, v in diagrams.items() %}

    {{k}}
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    .. image:: {{v}}
    {% endfor %}
