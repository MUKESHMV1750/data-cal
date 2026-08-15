import re

with open('templates/dashboard/reports.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace style="width:{{ var }}%;background:...;" with data-width="{{ var }}" style="background:...;"
# Also handles style="width:{{ var }}%;" without background
content = re.sub(
    r'style=\"width:\{\{(.*?)\}\}%;(?:background:(.*?);)?\"',
    lambda m: f'data-width=\"{{{{{m.group(1)}}}}}\" style=\"background:{m.group(2)};\"' if m.group(2) else f'data-width=\"{{{{{m.group(1)}}}}}\"',
    content
)

# Append the script before {% endblock %}
script = '''
<script>
  document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll(".report-bar-fill").forEach(function(el) {
      var width = el.getAttribute("data-width");
      if (width) {
        // use a tiny timeout to allow transition to play if we want, or just set it
        setTimeout(() => { el.style.width = width + '%'; }, 100);
      }
    });
  });
</script>
{% endblock %}'''

if '<script>' not in content:
    content = content.replace('{% endblock %}', script)

with open('templates/dashboard/reports.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed red errors!')
